# Lightningrod Assistant — Self-Improvement Program

## Objective

Improve the lightningrod-assistant agent's ability to:
1. **Detect data quality issues** — survivorship bias, selection bias, class imbalance
2. **Recommend appropriate data sources** — when news is wrong, when BigQuery/structured data is better
3. **Select correct answer types** — when numeric needs normalization, when binary is better
4. **Maintain cost awareness** — estimate before executing expensive operations
5. **Avoid false alarms** — don't warn about bias when the data source IS appropriate

The agent must get BETTER at catching real issues without becoming overly cautious.

## What You Can Modify

These are the agent's "brain" — markdown files that define its behavior:

- `.claude/agents/lightningrod-assistant.md` — Main agent prompt. This is where general reasoning heuristics, data quality awareness, and communication patterns live. **Primary optimization target.**
- `.claude/skills/examples-guide/SKILL.md` — Decision tree for choosing training patterns (forward-looking GRPO, content learning SFT, tabular). Contains answer type guidance and "watch for" sections. Good place for bias-detection heuristics.
- `.claude/agents/workflow-orchestrator.md` — Multi-agent orchestrator. Controls data source routing. Relevant for cases where the wrong specialist gets invoked.
- `.claude/agents/news-seeds-specialist.md` — News/GDELT seed sourcing. Could include guidance about when news is NOT the right source.
- `.claude/agents/dataset-generator.md` — Pipeline configuration and answer type selection. Contains autonomous decision logic for answer types.

## What You CANNOT Modify

- `evals/agent.py` — Harbor adapter (fixed evaluation infrastructure)
- `evals/judge.py` — LLM judge scoring (fixed evaluation infrastructure)
- `evals/tasks/*` — Test cases and rubrics (the benchmark is the benchmark)
- `src/*` — SDK source code (we're optimizing the agent, not the SDK)
- `.claude/skills/forward-looking-examples/SKILL.md` — Production examples (reference material, not editable guidance)
- `.claude/skills/content-learning-examples/SKILL.md` — Production examples
- `.claude/skills/tabular-examples/SKILL.md` — Production examples

## Strategy

The agent currently defaults to news seeds for most forecasting tasks and does not proactively identify data bias issues. Focus improvements on:

### High Priority
1. **Bias detection heuristics** — Add guidance to the main agent prompt that helps it recognize when a proposed data source has systematic bias (survivorship, selection, representation). This should be concise — a few sentences of reasoning guidance, not a lecture.
2. **Data source selection logic** — When the user's data is actually structured/available in BigQuery or APIs, the agent should recognize this and recommend the structured source over news.
3. **Answer type pushback** — Strengthen the agent's tendency to reframe raw numeric predictions as binary thresholds or normalized values. The examples-guide skill already has some of this, but the agent doesn't always follow through.

### Medium Priority
4. **Cost awareness** — The agent should always estimate cost before scaling operations. This is partially implemented but not consistently enforced.

### Critical Constraint
5. **No false alarms** — The agent must NOT become overly cautious. Golf forecasting from news is VALID. Policy forecasting from news is VALID. If changes cause the positive tests to regress, revert. A good heuristic: only warn about bias when the data source systematically excludes one outcome class.

## Optimization Approach

1. **Start with the lowest-scoring task** — Read its reward.json to understand which criteria scored poorly
2. **Make a targeted, minimal edit** — One concept per change. Don't rewrite entire files
3. **Test the change** — Re-run the full suite. Check that:
   - The target task improved
   - No other tasks regressed (especially positive tests)
   - The total score is higher
4. **Keep or revert** — If total score improved, keep. If it didn't, revert and try a different approach
5. **Iterate** — Repeat until improvements plateau

## Quality Guardrails

- **Prompt length**: Keep each agent prompt under 300 lines. Bloated prompts degrade overall performance
- **Specificity over generality**: "News articles about funding events have survivorship bias" is better than "be careful about data bias"
- **Action-oriented**: Guidance should tell the agent what to DO, not just what to worry about
- **Business language**: The agent communicates in domain terms, not SDK jargon. Keep new guidance in the same voice
- **Simpler is better**: At equal performance, prefer the shorter/simpler prompt. Cut guidance that doesn't improve scores

## Running the Benchmark

```bash
# Single task
harbor run -p evals/tasks/bias-survivorship-news --agent-import-path evals.agent:LightningrodAssistantAgent

# Full suite (5 trials each for statistical reliability)
harbor run -p evals/tasks/ --agent-import-path evals.agent:LightningrodAssistantAgent -n 5

# Check results
cat /logs/verifier/reward.json
```
