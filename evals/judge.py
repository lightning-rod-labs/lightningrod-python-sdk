"""
LLM-as-judge scoring infrastructure for Harbor test cases.

Each test case defines a rubric (list of weighted criteria). The judge
evaluates the agent's response against the rubric and returns per-criterion
scores that are combined into a single reward.
"""

import json
import os
import sys
from dataclasses import dataclass
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
    client = Anthropic()

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
        # Agent failed to produce output — score 0
        result = JudgeResult(
            scores=[0.0] * len(criteria),
            reasoning=f"Agent produced no valid output: {response_text[:200]}",
            total=0.0,
        )
    else:
        result = judge(scenario, response_text, criteria)

    # Write Harbor reward files
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

    print(f"Score: {result.total:.4f}")
    for c, s in zip(criteria, result.scores):
        print(f"  [{s:.1f}] (w={c.weight}) {c.description[:80]}")
    print(f"Reasoning: {result.reasoning}")
