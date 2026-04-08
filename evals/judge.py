"""
LLM-as-judge scoring infrastructure for Harbor test cases.

Each test case defines a rubric (list of weighted criteria). The judge
evaluates the agent's response against the rubric and returns per-criterion
scores that are combined into a single reward.

Supports two modes:
- Response-based: judge the final agent output text (run_judge_from_file)
- Trace-based: judge the full ATIF conversation trajectory (run_judge_from_trace)
"""

import json
from dataclasses import dataclass
import os
from pathlib import Path

from anthropic import Anthropic


@dataclass
class Criterion:
    """A single scoring criterion with a weight and description."""
    description: str
    weight: float


@dataclass
class JudgeResult:
    """Result from the LLM judge."""
    scores: list[float]         # Per-criterion scores (0.0-1.0)
    reasoning: str              # Judge's reasoning
    total: float                # Weighted total score


JUDGE_SYSTEM_PROMPT = """\
You are an expert evaluator assessing an AI agent's response quality.

You will be given:
1. A scenario description (what the user asked)
2. The agent's response
3. A list of scoring criteria

For each criterion, assign a score from 0.0 to 1.0:
- 1.0: Fully satisfied — the agent clearly and explicitly addresses this
- 0.7: Partially satisfied — the agent touches on this but incompletely
- 0.3: Weakly addressed — only a vague or indirect reference
- 0.0: Not addressed at all

Important:
- Score based on substance, not surface keywords. The agent must demonstrate
  genuine understanding, not just mention a term.
- If the agent raises the issue as a clarifying question ("I notice X might
  be a problem — should we address it?"), that counts as addressing it.
- The agent does NOT need to use specific technical terminology. Explaining
  the concept in plain language is sufficient.

Return your evaluation as JSON:
{
  "scores": [<score for criterion 1>, <score for criterion 2>, ...],
  "reasoning": "<brief explanation of your scoring>"
}

Return ONLY the JSON object, no other text."""


def judge(
    scenario: str,
    response_text: str,
    criteria: list[Criterion],
    model: str = "claude-sonnet-4-20250514",
) -> JudgeResult:
    """Score an agent response against a rubric using an LLM judge."""
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable is not set.")
    client = Anthropic(api_key=api_key)

    criteria_text = "\n".join(
        f"{i+1}. (weight={c.weight}) {c.description}"
        for i, c in enumerate(criteria)
    )

    user_prompt = f"""\
## Scenario
{scenario}

## Agent Response
---
{response_text}
---

## Scoring Criteria
{criteria_text}

Score each criterion 0.0-1.0 and return JSON."""

    message = client.messages.create(
        model=model,
        max_tokens=1024,
        system=JUDGE_SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_prompt}],
    )

    raw = message.content[0].text.strip()
    # Handle potential markdown code block wrapping
    if raw.startswith("```"):
        raw = raw.split("\n", 1)[1].rsplit("```", 1)[0].strip()

    result = json.loads(raw)
    scores = result["scores"]
    reasoning = result.get("reasoning", "")

    total = sum(s * c.weight for s, c in zip(scores, criteria))
    return JudgeResult(scores=scores, reasoning=reasoning, total=round(total, 4))


def run_judge_from_file(
    response_path: str,
    scenario: str,
    criteria: list[Criterion],
) -> None:
    """Run the judge and write Harbor reward files.

    Reads agent response from response_path, scores it, and writes
    reward.txt and reward.json to /logs/verifier/.
    """
    response_text = Path(response_path).read_text()

    if not response_text.strip() or response_text.startswith("[AGENT ERROR]"):
        result = JudgeResult(
            scores=[0.0] * len(criteria),
            reasoning=f"Agent produced no valid output: {response_text[:200]}",
            total=0.0,
        )
    else:
        result = judge(scenario, response_text, criteria)

    _write_reward(result, criteria)
    _print_result(result, criteria)


# ---------------------------------------------------------------------------
# Trace-based judging
# ---------------------------------------------------------------------------

JUDGE_TRACE_SYSTEM_PROMPT = """\
You are an expert evaluator assessing an AI agent's behavior during a
multi-step conversation.

You will be given:
1. A scenario description (what the user asked)
2. The full conversation trace showing the agent's messages, tool calls,
   tool results, and reasoning
3. A list of scoring criteria

Evaluate not just the final answer but HOW the agent got there:
- Which tools did it choose and why?
- What did its intermediate messages say?
- Did it handle errors or unexpected results appropriately?
- Was the workflow efficient and well-structured?

For each criterion, assign a score from 0.0 to 1.0:
- 1.0: Fully satisfied — the agent clearly demonstrates this in its behavior
- 0.7: Partially satisfied — the agent shows some evidence but incompletely
- 0.3: Weakly addressed — only a vague or indirect indication
- 0.0: Not addressed at all

Important:
- Score based on substance, not surface keywords. The agent must demonstrate
  genuine understanding, not just mention a term.
- If the agent raises the issue as a clarifying question ("I notice X might
  be a problem — should we address it?"), that counts as addressing it.
- The agent does NOT need to use specific technical terminology. Explaining
  the concept in plain language is sufficient.
- Look at the FULL trace — intermediate steps matter as much as the final output.

Return your evaluation as JSON:
{
  "scores": [<score for criterion 1>, <score for criterion 2>, ...],
  "reasoning": "<brief explanation of your scoring>"
}

Return ONLY the JSON object, no other text."""

TOOL_RESULT_TRUNCATE_CHARS = 2000


def _render_trace(atif: dict) -> str:
    """Render ATIF trajectory steps as readable text for the judge."""
    parts = []

    for step in atif.get("steps", []):
        source = step.get("source", "unknown")
        message = step.get("message", "")

        if source == "user":
            parts.append(f"### User\n{message}")
            continue

        # Agent step — may include text, tool calls, observations, reasoning
        section = []

        # Reasoning (thinking)
        reasoning = step.get("reasoning_content")
        if reasoning:
            # Truncate long reasoning
            if len(reasoning) > 3000:
                reasoning = reasoning[:3000] + "\n... (truncated)"
            section.append(f"**Thinking:** {reasoning}")

        # Main message text (skip pure "Tool: X" markers)
        if message and not message.startswith("Tool: "):
            section.append(message)

        # Tool calls
        tool_calls = step.get("tool_calls", [])
        for tc in tool_calls:
            fn = tc.get("function_name", "unknown")
            args = tc.get("arguments", {})
            # Show a compact representation of args
            args_str = json.dumps(args, indent=None)
            if len(args_str) > 500:
                args_str = args_str[:500] + "..."
            section.append(f"**Tool call:** {fn}({args_str})")

        # Tool results (observations)
        obs = step.get("observation", {})
        for result in obs.get("results", []):
            content = result.get("content", "")
            if len(content) > TOOL_RESULT_TRUNCATE_CHARS:
                content = content[:TOOL_RESULT_TRUNCATE_CHARS] + "\n... (truncated)"
            section.append(f"**Tool result:**\n{content}")

        if section:
            parts.append(f"### Agent\n" + "\n".join(section))

    # Metadata summary
    tools_used = atif.get("agent", {}).get("tools_used", [])
    metrics = atif.get("final_metrics") or {}
    num_turns = (metrics.get("extra") or {}).get("num_turns", "?")
    parts.append(
        f"### Metadata\n"
        f"- Tools used: {', '.join(tools_used) if tools_used else 'none'}\n"
        f"- Number of turns: {num_turns}\n"
        f"- Total steps: {metrics.get('total_steps', '?')}"
    )

    return "\n\n".join(parts)


def judge_trace(
    scenario: str,
    atif: dict,
    criteria: list[Criterion],
    model: str = "claude-sonnet-4-20250514",
) -> JudgeResult:
    """Score an agent's conversation trace against a rubric using an LLM judge."""
    client = Anthropic()

    trace_text = _render_trace(atif)
    criteria_text = "\n".join(
        f"{i+1}. (weight={c.weight}) {c.description}"
        for i, c in enumerate(criteria)
    )

    user_prompt = f"""\
## Scenario
{scenario}

## Conversation Trace
---
{trace_text}
---

## Scoring Criteria
{criteria_text}

Score each criterion 0.0-1.0 and return JSON."""

    message = client.messages.create(
        model=model,
        max_tokens=1024,
        system=JUDGE_TRACE_SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_prompt}],
    )

    raw = message.content[0].text.strip()
    if raw.startswith("```"):
        raw = raw.split("\n", 1)[1].rsplit("```", 1)[0].strip()

    result = json.loads(raw)
    scores = result["scores"]
    reasoning = result.get("reasoning", "")

    total = sum(s * c.weight for s, c in zip(scores, criteria))
    return JudgeResult(scores=scores, reasoning=reasoning, total=round(total, 4))


def run_judge_from_trace(
    trace_path: str,
    scenario: str,
    criteria: list[Criterion],
) -> None:
    """Run the judge on an ATIF trajectory and write Harbor reward files.

    Reads trajectory.json, scores the full conversation trace, and writes
    reward.txt and reward.json to /logs/verifier/.
    """
    trace_text = Path(trace_path).read_text()

    try:
        atif = json.loads(trace_text)
    except (json.JSONDecodeError, ValueError):
        result = JudgeResult(
            scores=[0.0] * len(criteria),
            reasoning=f"Failed to parse trajectory: {trace_text[:200]}",
            total=0.0,
        )
        _write_reward(result, criteria)
        _print_result(result, criteria)
        return

    if atif.get("error") or not atif.get("steps"):
        result = JudgeResult(
            scores=[0.0] * len(criteria),
            reasoning=f"Agent produced no valid trajectory: {atif.get('error', 'empty steps')}",
            total=0.0,
        )
    else:
        result = judge_trace(scenario, atif, criteria)

    _write_reward(result, criteria)
    _print_result(result, criteria)


# ---------------------------------------------------------------------------
# Shared helpers
# ---------------------------------------------------------------------------

def _write_reward(result: JudgeResult, criteria: list[Criterion]) -> None:
    """Write Harbor reward files."""
    verifier_dir = Path("/logs/verifier")
    verifier_dir.mkdir(parents=True, exist_ok=True)

    (verifier_dir / "reward.txt").write_text(str(result.total))
    (verifier_dir / "reward.json").write_text(json.dumps({
        "total": result.total,
        "scores": result.scores,
        "criteria": [
            {"description": c.description, "weight": c.weight, "score": s}
            for c, s in zip(criteria, result.scores)
        ],
        "reasoning": result.reasoning,
    }, indent=2))


def _print_result(result: JudgeResult, criteria: list[Criterion]) -> None:
    """Print human-readable score summary."""
    print(f"Score: {result.total:.4f}")
    for c, s in zip(criteria, result.scores):
        print(f"  [{s:.1f}] (w={c.weight}) {c.description[:80]}")
    print(f"Reasoning: {result.reasoning}")
