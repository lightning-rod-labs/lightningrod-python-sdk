---
name: pipeline-patterns
description: QuestionPipeline structure, cost estimation, minimal-output defaults. Use when configuring transforms.
---

# Pipeline Patterns

## QuestionPipeline structure

```python
pipeline = QuestionPipeline(
    seed_generator=seed_generator,
    question_generator=question_generator,
    labeler=labeler,
)
```

Optional: context_generators, renderer, rollout_generator, scorer.

## Cost estimation

```python
cost = lr.transforms.estimate_cost(pipeline, max_questions=1000)
```

Show user cost before scaling. Use for planning full runs.

## Run vs submit

- `lr.transforms.run(pipeline, max_questions=10)` — blocks until complete, good for notebooks
- `lr.transforms.submit(...)` — returns job ID, poll separately; use for long runs or detach

## Minimal-output defaults

**Always use max_questions=10 (or 5–20) for demo cells.** Add a variable or comment for scaling:

```python
MAX_QUESTIONS = 10  # Increase for full run (e.g. 1000)
dataset = lr.transforms.run(pipeline, max_questions=MAX_QUESTIONS)
```

Optional: max_cost_dollars to cap spend.
