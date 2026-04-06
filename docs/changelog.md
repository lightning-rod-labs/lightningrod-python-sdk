---
icon: clock-rotate-left
---

# Changelog

## v0.1.19 — April 2026

### New: `ContinuousValueOnlyAnswerType`

A new answer type for questions that expect a single scalar point estimate (e.g. `42.5`) rather than a full `{mean, stddev}` distribution. Scored via `CONTINUOUS_VALUE_ONLY_LOG_SCORE`. Use `ContinuousAnswerType` when uncertainty-aware predictions are needed; use `ContinuousValueOnlyAnswerType` when you want a single number.

See [Answer Types](dataset-generation/answer-types.md#continuousvalueonlyanswertype).

### New: `CsvSeedGenerator`

Generate seeds from a CSV file uploaded via `lr.files.upload()`. Each row becomes a seed. Configure which column maps to seed text, labels, and dates.

See [Seed Generators](dataset-generation/seed-generators.md#csvseedgenerator).

### New: `TopicTreeSeedGenerator`

Generate diverse seeds by recursively decomposing broad topics into specific subtopics. An LLM breaks each root topic into `tree_degree` subtopics, repeated `tree_depth` levels deep. Produces `tree_degree^tree_depth` seeds per root topic — useful for synthetic data generation without a news or document source.

See [Seed Generators](dataset-generation/seed-generators.md#topictreeseedgenerator).

### New: `FileSetDocumentContextGenerator`

A new context generator that resolves a **single document** by temporal ordering, downloads its full text, and appends it as context. Supports optional LLM processing before injection and a character limit. Use this instead of `FileSetContextGenerator` when you want the complete text of one specific document rather than RAG chunks from multiple documents.

See [Labeling and Context](dataset-generation/labeling-and-context.md#filesetdocumentcontextgenerator).

### New: `FileSetDocumentLabeler`

A new labeler that resolves a **single document** by temporal ordering and uses an LLM to extract a structured label from its full text. Use this instead of `FileSetRAGLabeler` when labeling from the complete content of one document (e.g. Federal Reserve Beige Book reports).

See [Labeling and Context](dataset-generation/labeling-and-context.md#filesetdocumentlabeler).

### Updated: `TemporalConstraint` — new values

`TemporalConstraint` now has five values (previously two). The additions enable single-document resolution:

- `NEXT_DOCUMENT` — first document after the seed timestamp
- `PREVIOUS_DOCUMENT` — most recent document before the seed timestamp
- `EQUAL` — document with an exact matching date

These are primarily used with `FileSetDocumentContextGenerator` and `FileSetDocumentLabeler`.

See [Labeling and Context](dataset-generation/labeling-and-context.md#temporalconstraint).

### Updated: Multi-model evals and intermediate checkpoint access

The evals API has been updated to accept a `list[EvalModel]` instead of a single `model_id`, enabling multiple models to be evaluated in a single job. The new `EvalModel` class accepts a `model_id` and an optional `label` for display.

Training jobs now expose `model_id_by_step` — a dict mapping training step numbers to intermediate checkpoint model IDs, enabling evaluation of checkpoints before the final model.

**Before:**
```python
lr.evals.run(model_id=job.model_id, dataset=test_dataset, benchmark_model_id="openai/gpt-4.1")
```

**After:**
```python
from lightningrod import EvalModel

lr.evals.run(
    models=[
        EvalModel(model_id=job.model_id, label="fine-tuned"),
        EvalModel(model_id="openai/gpt-4.1", label="baseline"),
    ],
    dataset=test_dataset,
)
```

See [Evaluation](fine-tuning/evaluation.md).

### New: Example builder utilities

Three helper functions for building formatted question example strings to pass as `examples` / `bad_examples` in question generators:

- `binary_example(question, comment=None)`
- `continuous_example(question, comment=None)`
- `multiple_choice_example(question, options, label=None, comment=None)`

```python
from lightningrod import binary_example, continuous_example, multiple_choice_example
```

See [Answer Types — Example Builder Utilities](dataset-generation/answer-types.md#example-builder-utilities).
