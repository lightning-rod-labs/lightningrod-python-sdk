---
name: transform-pipeline-verification
description: Pattern for running and verifying transform pipeline output at any stage (seeds-only or full). Use when writing seeds.py or dataset.py to run the pipeline, inspect output quality iteratively with explore.py, and only report back once verified.
---

# Transform Pipeline Verification

Each pipeline stage (`seeds.py`, `dataset.py`) should be independently runnable. After a run, use `explore.py` to iteratively verify output quality before reporting back to the orchestrator.

## Phase 1: Run the pipeline

Only plug in the minimum components you are responsible for to `QuestionPipeline`, populate any (or multiple) of: seed_generator, question_generator, labeler, context_generators, renderer, rollout_generator.

```python
pipeline = QuestionPipeline(...)

if __name__ == "__main__":
    lr_client = get_client()
    cost_estimate = lr_client.transforms.estimate_cost(pipeline, max_questions=<limit>)
    dataset = lr_client.transforms.run(pipeline, max_questions=<limit>, name="<project>_seeds")
```

For full pipeline: same pattern with question_generator and labeler configured.

After `transforms.run()`, stdout shows the dataset ID. Pipeline scripts print an explore hint, e.g. `Explore: python explore.py <dataset_id> --summary`.

## Phase 2: Explore output iteratively

Use `explore.py` to probe the dataset and verify for quality and make sure the output roughly matches your expectations.

```bash
python explore.py <dataset_id> [--summary] [--samples N] [--valid N] [--invalid N] [--labels N] [--truncate N]
```

| Flag | Use when |
|------|----------|
| `--summary` (default) | First check — validity %, label distribution |
| `--samples N` | Spot-check N random rows (seed_text or question+label) |
| `--valid N` | Inspect N valid samples |
| `--invalid N` | Debug failures — see `invalid_reason` for N invalid samples |
| `--labels N` | Quality check — question + label + reasoning side-by-side |
| `--truncate N` | Override max chars for long text fields (default: 120) |

Run from the project directory. Iterate until confident: e.g. `--summary` shows 30% invalid → `--invalid 10` to see why → adjust pipeline config → rerun.

## Completing the step

1. Run the pipeline
2. Run `explore.py <id> --summary` and confirm validity
3. Iteratively probe with `--samples`, `--invalid`, `--labels` as needed
4. Only then write to `state.json` and report back to the orchestrator

## Why

- Cheap seeds-only runs catch SQL/ingestion errors before the full pipeline
- `explore.py` owns download and caching — no extra code in pipeline scripts
- Iterative inspection surfaces label quality issues, filter reasons, and bad seeds that a one-time print would miss
