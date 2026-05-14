---
name: experiment-tracking
description: Standardised training-experiment tracking. One notebook per experiment under `./userland/<project>/experiments/`, plus a single `experiments.md` index table at the project root. Use whenever a training run's tracked config differs from the previous run.
---

# Experiment tracking

Every meaningful training run is its own experiment: a self-contained notebook plus one row in a project-level index. This makes runs comparable, makes regressions visible, and lets the user (or you, in a later session) understand at a glance what has been tried and what worked.

## Directory layout

```
./userland/<project>/
├── experiments/
│   ├── exp_001_baseline.ipynb
│   ├── exp_002_more_steps.ipynb
│   ├── exp_003_conf_threshold.ipynb
│   └── ...
└── experiments.md            # the index (single source of truth for results)
```

- Experiment IDs are zero-padded, monotonically increasing, **never reused** (even for failed runs — they still get an ID and a row).
- Slugs are short and descriptive: `exp_004_lora_rank_64`, not `exp_004_run`.
- The first experiment in a project is always `exp_001_baseline` — it captures the out-of-the-box config from the relevant example skill, with no modifications.

## When to create a new experiment notebook

Create a new `exp_NNN_<slug>.ipynb` **whenever the next training run's tracked config differs from the last experiment's config.** Tracked config knobs:

- `base_model_id`
- `training_steps`, `lora_rank`, `batch_size`, `num_rollouts`, `max_response_length`, `learning_rate`
- `epochs` (SFT)
- Dataset version / `max_questions` if the training dataset was regenerated
- Pipeline-level changes that produced the training dataset: question generator instructions, labeler confidence threshold, answer type, seed generator, examples / bad_examples

Skip creating a new experiment if you are re-running the **exact same** config (e.g. recovering from a transient failure) — append a note to the existing experiment's notebook instead.

Initial small-scale verification runs (`max_questions=50` test) are **not** experiments — they belong in the main pipeline notebook. The first experiment starts when you have a dataset you intend to train on.

## Experiment notebook structure

Each `exp_NNN_<slug>.ipynb` is a self-contained record. It must run end-to-end from a clean kernel using artifacts in the project (dataset ID, training config). Required cells, in order:

1. **Header (markdown)** — fixed format, fill every field:

   ```markdown
   # exp_003 — Raise labeler confidence threshold

   - **Date started:** 2026-05-14
   - **Hypothesis:** Raising WebSearchLabeler confidence from 0.6 → 0.8 removes the noisiest labels and improves Brier vs frontier.
   - **Parent experiment:** exp_002
   - **Change vs parent:** `labeler.confidence_threshold` 0.6 → 0.8. All other config unchanged.
   - **Dataset:** `<dataset_id>` (n_train=..., n_test=...)
   - **Frontier baseline:** `openai/gpt-5.5`
   - **Status:** running
   ```

   Update **Status** to `done` / `failed` once eval completes, and add a **Result** line (see step 5).

2. **Config cell** — the full `GRPOTrainingConfig` / `SFTTrainingConfig` literal. Inline, not imported. Future-you reading this notebook should see every knob without cross-referencing another file.

3. **Cost estimate cell** — `lr.training.estimate_cost(config, dataset=train_dataset)`. Print the result.

4. **Train cell** — `lr.training.run(config, dataset=train_dataset, name=f"<project>-exp_003")`. The job name must include the experiment ID so it is identifiable in the dashboard.

5. **Eval cell** — `lr.evals.run_from_training_job(config, job, test_dataset, extra_models=[EvalModel(model_id="openai/gpt-5.5", label="GPT-5.5")])`. The frontier model is always included (see lightningrod-assistant "Frontier benchmark"). Print the eval summary.

6. **Result cell (markdown)** — fill in once eval returns. Always report **both Brier and ECE**, and **both deltas** (vs frontier and vs base model). Lower is better for both metrics, so positive Δ = we beat the comparison model.

   ```markdown
   ## Result

   |                       | Brier  | ECE    |
   |-----------------------|--------|--------|
   | Fine-tuned            | 0.1821 | 0.0612 |
   | Base (gpt-oss-120b)   | 0.1980 | 0.0834 |
   | Frontier (GPT-5.5)    | 0.2003 | 0.0701 |
   | **Δ vs base**         | +0.0159 Brier / +0.0222 ECE |
   | **Δ vs frontier**     | +0.0182 Brier / +0.0089 ECE |

   - **Verdict:** Beat both base and frontier on Brier and ECE; threshold change worked as hypothesised.
   - **Next:** Try 0.8 → 0.9 in exp_004, or revert and explore a different axis.
   ```

7. **Index update cell (last cell)** — appends/updates the row in `../experiments.md` (see below). Keep this as the final cell so it only runs once the result is real.

## experiments.md (the index)

One markdown table at `./userland/<project>/experiments.md`. Newest row on top. Single source of truth — read it before designing the next experiment.

```markdown
# Experiments — <project name>

Base model: `openai/gpt-oss-120b` · Frontier benchmark: `openai/gpt-5.5` · Metrics: Brier, ECE (lower is better; Δ shown as fine-tuned − comparison, signed so positive = we win)

| ID  | Date       | Hypothesis                   | Δ Brier (base / frontier) | Δ ECE (base / frontier) | Status | Notebook                                            |
|-----|------------|------------------------------|---------------------------|-------------------------|--------|-----------------------------------------------------|
| 003 | 2026-05-14 | Raise conf threshold 0.6→0.8 | +0.016 / +0.018           | +0.022 / +0.009         | done   | [exp_003](experiments/exp_003_conf_threshold.ipynb) |
| 002 | 2026-05-12 | 2x training steps            | -0.001 / -0.004           | +0.003 / -0.002         | done   | [exp_002](experiments/exp_002_more_steps.ipynb)     |
| 001 | 2026-05-10 | Baseline (golf defaults)     | +0.010 / +0.012           | +0.015 / +0.005         | done   | [exp_001](experiments/exp_001_baseline.ipynb)       |
```

Column rules:

- **ID** — `NNN` zero-padded. Matches the notebook filename.
- **Date** — `YYYY-MM-DD` of the day the experiment started.
- **Hypothesis** — one line, the same first sentence as the notebook header's Hypothesis field. Compress if needed.
- **Δ Brier (base / frontier)** — two signed deltas separated by ` / `: fine-tuned vs base model, then fine-tuned vs frontier. Sign convention: positive = fine-tuned wins (since lower Brier is better, this is `base − fine_tuned` / `frontier − fine_tuned`).
- **Δ ECE (base / frontier)** — same format and sign convention as Δ Brier.
- Use `—` for any delta column while the experiment is still `running`.
- **Status** — `running`, `done`, `failed`. Update at completion.
- **Notebook** — relative markdown link to the `.ipynb`.

When the assistant starts a new experiment, it writes a row with `Status: running` and `Δ vs frontier: —`, then updates that row in place once eval completes. Never reorder rows except to keep newest on top when inserting.

## Workflow inside the assistant

1. Before any training run, read `./userland/<project>/experiments.md`. Find the previous experiment's tracked config (from its notebook's config cell).
2. Diff the planned config against it. If anything tracked changed, create the next `exp_NNN_<slug>.ipynb` from the template above. If nothing changed, do not create a new experiment.
3. Create/update the row in `experiments.md` with `running` and `—` before kicking off `lr.training.run`.
4. After eval, update both the notebook's Result cell and the matching row in `experiments.md`.
5. When the user asks "what have we tried?" or "what's next?", read `experiments.md` first, not the notebooks.

## Hard rules

- **One experiment = one notebook.** Never reuse an experiment notebook for a different config.
- **IDs are append-only.** Failed experiments keep their ID and get `Status: failed` with a short note in the Result cell. Do not renumber.
- **Always include the frontier model in eval.** This is the column that makes the index comparable — never omit it.
- **The index is markdown only.** Do not introduce a separate JSON/YAML store; the table is the source of truth.
- **Always report Brier and ECE, and always against both base and frontier.** Four numbers per experiment (Δ Brier vs base, Δ Brier vs frontier, Δ ECE vs base, Δ ECE vs frontier). Brier captures accuracy; ECE captures calibration — both matter for forecasting and one can move without the other. If the eval job did not return one of these metrics, fix the eval call rather than dropping the column.
- **Sign convention is fixed.** Δ = `comparison − fine_tuned`, so positive always means the fine-tuned model wins. Keep this consistent across every row and project.
