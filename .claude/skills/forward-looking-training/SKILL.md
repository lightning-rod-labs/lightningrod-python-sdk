---
name: forward-looking-training
description: Build forecasting datasets and fine-tune models with Lightning Rod GRPO. Use when the user wants to predict future outcomes, train a forecasting model, generate binary/continuous forecasting questions, seed from news or GDELT or timestamped documents, reason about causality or probability calibration, or when they mention GRPO, reinforcement learning, ForwardLookingQuestionGenerator, or "unresolved at question time". Covers the canonical pipeline (Seeds -> ForwardLookingQuestionGenerator -> Labels -> Context -> GRPO), seed generator choice, WebSearchLabeler vs FileSetRAGLabeler, temporal splits, and leakage traps.
---

# Forward-Looking Training (GRPO)

Teach a model to reason about the future by generating questions whose answers are unknown at question time and resolved later. GRPO rewards calibration, so the model discovers causal reasoning rather than memorizing.

Full worked examples live in `agent-docs/forward-looking-examples.md` and the notebooks under `notebooks/fine_tuning/` — open them for anything beyond the decisions below.

## When this pattern fits

- The question has a **future resolution date**; no one knows the answer when the question is written.
- Answer type is binary, continuous, or multiple choice (free response has no reward signal).
- Goal is domain reasoning / prediction, not pure fact recall. If answers are known today, use the content-learning-sft skill instead. If you're starting from a CSV or BigQuery table, use the tabular-data-pipeline skill.

## Canonical pipeline

```
Seeds -> ForwardLookingQuestionGenerator -> Labeler -> (NewsContextGenerator) -> GRPOTrainingConfig
```

```python
from datetime import datetime
from lightningrod import (
    LightningRod, QuestionPipeline, BinaryAnswerType,
    NewsSeedGenerator, ForwardLookingQuestionGenerator,
    NewsContextGenerator, WebSearchLabeler,
    GRPOTrainingConfig,
)
from lightningrod.training import prepare_for_training, FilterParams, SplitParams

lr = LightningRod(api_key=api_key)

pipeline = QuestionPipeline(
    seed_generator=NewsSeedGenerator(
        start_date=datetime(2024, 6, 1),          # >= base model knowledge cutoff
        end_date=datetime(2026, 1, 1),
        interval_duration_days=14,                 # match domain cadence
        search_query=["..."],
        articles_per_search=10,
    ),
    question_generator=ForwardLookingQuestionGenerator(
        instructions="...",
        examples=[...],
        bad_examples=[...],
        answer_type=BinaryAnswerType(),
        questions_per_seed=5,                      # see heuristic below
    ),
    context_generators=[NewsContextGenerator(num_articles=5)],
    labeler=WebSearchLabeler(answer_type=BinaryAnswerType()),
)

dataset = lr.transforms.run(pipeline, max_questions=10000, name="...")
```

## Key decisions

### Seed generator

| Source | Use |
| --- | --- |
| `NewsSeedGenerator` | Domain-specific news (golf, tariffs, military strikes). Pass `search_query` list. |
| `GdeltSeedGenerator` | Broad general forecasting across all domains. Higher `articles_per_interval` (~25). |
| `FileSetSeedGenerator` | Corpus of timestamped documents (Fed reports, filings, memos). Requires date metadata per file. |

### Labeler

- `WebSearchLabeler(answer_type=...)` — resolves from the web. Default confidence threshold is fine; raise to `0.9` for production-quality general datasets.
- `FileSetRAGLabeler(..., temporal_constraint=TemporalConstraint.AFTER)` — when seeds come from a FileSet and later documents resolve earlier ones. The `AFTER` constraint is mandatory or the model "sees" the answer at question time. Use a lower confidence threshold (~0.7) because answers live in known documents.

### `questions_per_seed`

- Narrow fast-moving domain (one article covers many angles): **20** (Trump policy)
- General domain, one angle per article: **5** (golf, military strikes, GDELT)

### `interval_duration_days`

Match the cadence of the domain: weekly for fast-moving politics, biweekly for sports tournaments, weekly for military news.

### Default GRPO config

```python
batch_size = 32
config = GRPOTrainingConfig(
    base_model_id="openai/gpt-oss-120b",
    training_steps=len(train_dataset.flattened()) // batch_size,
    lora_rank=32,
    batch_size=batch_size,
    num_rollouts=8,                 # drop to 4 on very large general datasets
    max_response_length=16384,
    learning_rate=4e-5,
)
job = lr.training.run(config, dataset=train_dataset, name="...")
```

Benchmark against GPT-5:

```python
from lightningrod import EvalModel
eval_job = lr.evals.run(
    config, job, test_dataset,
    extra_models=[EvalModel(model_id="openai/gpt-5", label="GPT-5")],
)
```

## Split — temporal or bust

```python
train_dataset, test_dataset = prepare_for_training(
    dataset,
    filter=FilterParams(days_to_resolution_range=(1, None)),   # resolved only
    split=SplitParams(strategy="temporal", test_size=0.2),
)
```

`days_to_resolution_range` by domain: politics `(1, 60)`, sports `(1, None)`, geopolitics `(1, 90)`, general `(1, None)`.

## Watch for

- **Temporal split is non-negotiable.** Shuffling leaks future info into training.
- No training sample's close date can fall past the first test prediction date. `prepare_for_training` with `strategy="temporal"` enforces this.
- Spot-check 10-20 generated questions for sense, unambiguous resolution criteria, and no label leakage in the question text.
- `start_date` should be on or after the base model's knowledge cutoff — otherwise the model recalls instead of predicting.
- Begin with `max_questions=100` to validate the pipeline before scaling to thousands.

## References

- Full worked pipelines: `agent-docs/forward-looking-examples.md` (golf, Trump policy, military strikes, Foresight/GDELT, Fed Beige Book RAG).
- Runnable notebooks: `notebooks/fine_tuning/01_golf_forecasting.ipynb`, `02_trump_forecasting.ipynb`, `04_military_strikes.ipynb`.
- Pattern overview: `agent-docs/examples-guide.md` (Pattern 1).
