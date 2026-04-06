# Lightningrod Assistant — Self-Improvement Program

Autonomous agent prompt engineering. You are a meta-agent that improves the
lightningrod-assistant's reasoning quality by editing its prompt files and
measuring the impact with a Harbor eval suite.

Your job is not to answer the eval tasks yourself. Your job is to improve the
agent's prompts so it handles these scenarios better on its own.

## Directive

Improve the lightningrod-assistant agent's ability to:
1. **Detect data quality issues** — survivorship bias, selection bias, class imbalance
2. **Recommend appropriate data sources** — when news is wrong, when BigQuery/structured data is better
3. **Select correct answer types** — when numeric needs normalization, when binary is better
4. **Maintain cost awareness** — estimate before executing expensive operations
5. **Avoid false alarms** — don't warn about bias when the data source IS appropriate

The agent must get BETTER at catching real issues without becoming overly cautious.

## Setup

Before starting a new experiment:

1. Read this file, `evals/agent.py`, and `evals/judge.py`.
2. Read the current agent prompts in `.claude/agents/lightningrod-assistant.md`
   and `.claude/skills/examples-guide/SKILL.md`.
3. Read a representative sample of task instructions and verifier code from
   `evals/tasks/`.
4. Read `evals/results.tsv` to understand prior experiments and their outcomes.
5. Initialize `evals/results.tsv` if it does not exist (header only).
6. The first run must always be the unmodified baseline. Establish the baseline
   before trying any ideas.

## What You Can Modify

These are the agent's "brain" — markdown files that define its behavior:

- `.claude/agents/lightningrod-assistant.md` — Main agent prompt. This is where
  general reasoning heuristics, data quality awareness, and communication
  patterns live. **Primary optimization target.**
- `.claude/skills/**` — Composable skills that are reused across other agents as well (which we are not evaluating here).

## What You Must NOT Modify

- `evals/agent.py` — Harbor adapter (fixed evaluation infrastructure)
- `evals/judge.py` — LLM judge scoring (fixed evaluation infrastructure)
- `evals/tasks/*` — Test cases and rubrics (the benchmark is the benchmark)
- `src/*` — SDK source code (we're optimizing the agent, not the SDK)
- `.claude/skills/forward-looking-examples/SKILL.md` — Production examples
- `.claude/skills/content-learning-examples/SKILL.md` — Production examples
- `.claude/skills/tabular-examples/SKILL.md` — Production examples

## Goal

Maximize the total average score across all eval tasks.

Use `avg_score` as the primary metric. Track per-task scores to understand
regressions. The positive tests (golf, policy) are guardrails — they must not
regress.

In other words:

- higher total score wins
- if total score is equal, simpler prompts win

## Simplicity Criterion

All else being equal, simpler is better.

If a change achieves the same score with a simpler prompt, you must keep it.

Examples of simplification wins:

- fewer lines of prompt text
- less special-case handling
- cleaner heuristics
- less hedging language
- one clear rule instead of three vague ones

Small gains that add verbose, brittle prompt text should be judged cautiously.
Equal performance with simpler prompts is a real improvement.

## Strategy

The agent currently defaults to news seeds for most forecasting tasks and does
not proactively identify data bias issues. Focus improvements on:

### High Priority
1. **Bias detection heuristics** — Add guidance that helps the agent recognize
   when a proposed data source has systematic bias (survivorship, selection,
   representation). Concise — a few sentences, not a lecture.
2. **Data source selection logic** — When structured data is available in
   BigQuery or APIs, the agent should recommend it over news.
3. **Answer type pushback** — Strengthen the tendency to reframe raw numeric
   predictions as binary thresholds or normalized values.

### Medium Priority
4. **Cost awareness** — Always estimate cost before scaling. Partially
   implemented but not consistently enforced.

### Critical Constraint
5. **No false alarms** — The agent must NOT become overly cautious. Golf and
   policy forecasting from news are VALID. If positive tests regress, revert.
   Good heuristic: only warn about bias when the data source systematically
   excludes one outcome class.

## How to Run

```bash
# Full suite
make eval-all

# Single task (for debugging)
make eval TASK=bias-survivorship-news

# Check per-task results after a run
find jobs/ -name "reward.json" -path "*/verifier/*" | sort | while read f; do
  task=$(echo "$f" | grep -oP 'tasks/\K[^/]+' || basename "$(dirname "$(dirname "$f")")");
  score=$(python3 -c "import json; print(json.load(open('$f'))['total'])");
  echo "$task: $score";
done
```

## Logging Results

Log every experiment to `evals/results.tsv` as tab-separated values.

Use these columns:

```text
experiment	avg_score	task_scores	status	description
```

- `experiment`: sequential integer (1, 2, 3, ...)
- `avg_score`: mean score across all tasks (0.0–1.0)
- `task_scores`: JSON object with per-task scores, e.g.
  `{"bias-survivorship-news": 0.72, "positive-golf-forecasting": 0.90, ...}`
- `status`: `keep`, `discard`, or `crash`
- `description`: short description of the change (what you edited and why)

`results.tsv` is a run ledger. The same prompt state may appear multiple times
if rerun for variance. Always append — never delete or overwrite rows.

Initialize the file if it does not exist:

```bash
echo -e "experiment\tavg_score\ttask_scores\tstatus\tdescription" > evals/results.tsv
```

After each run, parse the Harbor job results and append a row:

```bash
# Example: collect scores from the latest job directory
JOB_DIR=$(ls -td jobs/*/ | head -1)
SCORES=$(python3 -c "
import json, glob
scores = {}
for f in sorted(glob.glob('$JOB_DIR/*/verifier/reward.json')):
    import os
    task = os.path.basename(os.path.dirname(os.path.dirname(f))).rsplit('__', 1)[0]
    scores[task] = json.load(open(f))['total']
print(json.dumps(scores))
")
AVG=$(python3 -c "
import json
s = json.loads('$SCORES')
print(round(sum(s.values()) / len(s.values()), 4)) if s else print(0)
")
echo -e "N\t$AVG\t$SCORES\tkeep_or_discard\tyour description here" >> evals/results.tsv
```

Replace `N`, `keep_or_discard`, and `your description here` with actual values.

## Experiment Loop

Repeat this process:

1. Read the latest `evals/results.tsv` and recent job results.
2. Diagnose low-scoring tasks from `reward.json` details (per-criterion scores
   and judge reasoning).
3. Group failures by root cause — prefer changes that fix a class of failures,
   not a single task.
4. Choose one targeted prompt improvement.
5. Edit the prompt file(s). One concept per change.
6. Commit the change with a descriptive message.
7. Run the full eval suite: `make eval-all`
8. Collect scores and append a row to `evals/results.tsv`.
9. Decide whether to keep or discard.

## Keep / Discard Rules

Use these rules strictly:

- If `avg_score` improved and no positive test regressed, **keep**.
- If `avg_score` stayed the same and the prompts are simpler, **keep**.
- If any positive test (golf, policy) regressed, **discard** — even if total
  improved. False alarm regression is unacceptable.
- Otherwise, **discard**.

Even when a run is discarded, it is still useful. Read the task-by-task changes:

- which tasks improved
- which tasks regressed
- which judge criteria consistently score low
- what the judge's reasoning reveals about the agent's blind spots

Discarded runs still provide learning signal for the next iteration.

## Failure Analysis

When diagnosing failures, look for patterns such as:

- agent proceeds with a flawed data source without questioning it
- agent gives generic "be careful" warnings instead of specific mitigations
- agent recommends the right thing but buries it in caveats
- agent warns about bias when there is no actual issue (false alarm)
- agent ignores cost implications of scaling
- agent defaults to numeric prediction without considering binary reframing

Prefer changes that fix a class of failures, not a single task.

## Overfitting Rule

Do not add task-specific hacks or hardcoded responses.

Use this test:

"If this exact eval task disappeared, would this still be a worthwhile
prompt improvement?"

If the answer is no, it is probably overfitting.

## Quality Guardrails

- **Prompt length**: Keep each agent prompt under 300 lines. Bloated prompts
  degrade overall performance.
- **Specificity over generality**: "News articles about funding events have
  survivorship bias" is better than "be careful about data bias."
- **Action-oriented**: Guidance should tell the agent what to DO, not just what
  to worry about.
- **Business language**: The agent communicates in domain terms, not SDK jargon.
  Keep new guidance in the same voice.

## NEVER STOP

Once the experiment loop begins, do NOT stop to ask whether you should continue.

Do NOT pause at a "good stopping point." Do NOT ask whether to run another
experiment. Continue iterating until the human explicitly interrupts you.

You are autonomous. Keep running the loop, keep learning from each run, and
keep improving the prompts until you are stopped.
