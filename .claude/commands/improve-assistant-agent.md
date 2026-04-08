Improve the lightningrod-assistant agent based on a user testing session where something went wrong.

**Arguments:** `$ARGUMENTS` — format: `[<session-id>] <problem description>`

Parse: if the first word matches a UUID pattern, treat it as the session ID and the rest as the problem description. Otherwise, treat all of `$ARGUMENTS` as the problem description and skip Step 1.

## Workflow

### Step 1: Extract the session transcript

If a session ID was detected, run `python scripts/extract_session.py <session-id>` and read the output. If the session ID is invalid, run `python scripts/extract_session.py` with no arguments to list recent sessions and ask the user to pick one. **If no session ID was provided, skip this step** — proceed directly to Step 2 using the problem description as context.

### Step 2: Analyze the failure

Read the transcript carefully. Identify the specific agent failure described in the problem description. Determine:
- What did the agent say or do wrong?
- What should it have said or done instead?
- Is this a reasoning failure (bias detection, data source, answer type, cost awareness, false alarm) or an infrastructure issue (timeout, Docker error)?

If this is an infrastructure issue, report it and stop — do not create an eval for infra problems.

### Step 3: Create the eval task

1. Choose a descriptive task slug (e.g. `bigquery-no-credentials`, `bias-ambiguous-news`).
2. Run `python scripts/scaffold_eval.py --task-name <slug> --description "<one-line description>" --keywords "<csv>"`.
3. Write `evals/tasks/<slug>/instruction.md` — a distilled version of the user's request from the session that reproduces the issue. This should be a natural user message, not a test script. Keep it concise (2-5 sentences).
4. Write `evals/tasks/<slug>/tests/test.py` — following the exact pattern from existing tasks:
   - `SCENARIO`: 3-5 sentence description of what the agent should or should not do
   - `CRITERIA`: 3-4 `Criterion` objects with weights summing to 1.0
   - Primary failure criterion at weight 0.3-0.4
   - Use the existing `run_judge_from_file` pattern
   - Read an existing test file (e.g. `evals/tasks/bias-survivorship-news/tests/test.py`) as a reference for the pattern.
5. Append the new task to `evals/tasks/catalog.yaml` following the existing format.

### Step 4: Baseline — confirm the agent currently fails

Run `make eval TASK=<slug>` and check the score. If the score is already > 0.7, the eval is too easy — tighten the criteria or make the instruction more challenging, then re-run.

### Step 5: Fix the agent

Read the current agent prompt (`.claude/agents/lightningrod-assistant.md`) and relevant skill files (`.claude/skills/`). Diagnose what change would fix this failure.

Follow these principles from `evals/program.md`:
- **Generalize.** Prefer changes that fix a class of failures, not just this one task.
- **Overfitting rule.** Ask: "If this exact eval task disappeared, would this still be a worthwhile prompt improvement?" If no, rethink.
- **Simplicity.** Keep the agent prompt under 300 lines. Look for opportunities to generalize existing guidance rather than adding new blocks.
- **Action-oriented.** Tell the agent what to DO, not just what to worry about.
- **Business language.** Keep guidance in domain terms, not SDK jargon.

Edit the relevant prompt/skill file(s).

### Step 6: Verify the fix

Run `make eval TASK=<slug>` again. The score should improve significantly (target > 0.7).

If the fix didn't work, iterate: read the judge's reasoning from the job output, adjust the prompt change, and re-run. Do not give up after one attempt.

### Step 7: Regression check

Run `make eval-all` to verify no existing tests regress.

Apply the keep/discard rules:
- If avg_score improved and no positive test (golf, policy) regressed → **keep**
- If avg_score stayed the same and prompts are simpler → **keep**
- If any positive test regressed → **discard** and revert the prompt changes
- Otherwise → **discard**

### Step 8: Log and report

Append a row to `evals/results.tsv` with the experiment number, scores, status, and description.

Report the outcome to the user:
- What eval task was created
- What prompt/skill changes were made
- Baseline score → final score on the new task
- Full suite avg_score and any regressions
- Whether the changes were kept or discarded

## Guardrails

- Do NOT modify `evals/agent.py`, `evals/judge.py`, or `src/*`
- Do NOT create task-specific hacks in the agent prompt
- Do NOT modify existing eval tasks — only create new ones
- If the session reveals multiple independent issues, focus on the one described in the problem description. Mention the others in your report so they can be addressed separately.
