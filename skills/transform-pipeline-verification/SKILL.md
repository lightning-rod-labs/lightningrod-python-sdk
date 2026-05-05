---
name: transform-pipeline-verification
description: Pattern for running and verifying transform pipeline output at any stage (seeds-only or full). Use when building a pipeline in a notebook or script — run transforms, inspect output quality iteratively, then scale or move on.
---

# Transform Pipeline Verification

After `lr.transforms.run()`, inspect the returned dataset before scaling `max_questions` or moving to training.

## Phase 1: Run the pipeline

Configure `QuestionPipeline` with the minimum stages you need: seed_generator, question_generator, labeler, context_generators, renderer, rollout_generator.

```python
pipeline = QuestionPipeline(...)

if __name__ == "__main__":
    lr_client = get_client()
    cost_estimate = lr_client.transforms.estimate_cost(pipeline, max_questions=<limit>)
    dataset = lr_client.transforms.run(pipeline, max_questions=<limit>, name="<project>_seeds")
```

Stdout includes the dataset ID. In a notebook, keep that ID in a variable for the next cell.

## Phase 2: Explore output iteratively

Use the client to download and inspect rows (prefer typed `Sample` objects; use `flattened()` only if you need a quick tabular view in pandas).

```python
lr_client = get_client()
ds = lr_client.datasets.get(dataset_id)
rows = ds.flattened()
```

Then:

- Check validity rate and label distribution (`is_valid`, `label` columns if present).
- Spot-check `question_text`, `label`, `reasoning`, `invalid_reason` on a small random subset.
- For seeds-only runs, inspect `seed_text` and validation flags before adding question/label stages.

Iterate: if validity is low or labels look wrong, adjust pipeline config and rerun before increasing `max_questions`.

## Before scaling up

1. Run with a small `max_questions` (e.g. 10–50).
2. Confirm validity and spot-check quality in code or notebook output.
3. Call `estimate_cost` for the target scale, then run the larger job.

## Before splitting (lint the full dataset)

Run the dataset linter on the generated dataset before splitting or training. Linting runs server-side on the whole dataset — it catches structural issues that pipeline verification and filtering don't check (duplicate samples, missing required fields, label inconsistencies). This is useful even outside training workflows as a dataset health check.

```python
from lightningrod import display_lint_overview, get_lint_affected_sample_ids

lint_result = lr.datasets.linter.run(dataset.id)
display_lint_overview(lint_result)

bad_ids = get_lint_affected_sample_ids(lint_result)
if bad_ids:
    clean_ids = [s.id for s in dataset.samples() if s.id not in set(bad_ids)]
    dataset = dataset.subset(clean_ids)
```

## Why

- Cheap seeds-only runs catch SQL/ingestion errors before the full pipeline.
- Iterative inspection surfaces label quality issues, filter reasons, and bad seeds that a one-time print would miss.
