---
name: tabular-data-pipeline
description: Turn structured/tabular data into Lightning Rod training samples and fine-tune on them. Use when the user has a CSV, BigQuery table, pandas DataFrame, API result, or any row-per-record dataset and wants to generate questions, compute labels, enrich with context, or train a model. Triggers on "I have outcomes and want to generate questions", "I have questions and need labels", time-series forecasting from rows, per-row prediction, structured data mapping, TemplateQuestionGenerator, create_sample, computed labels. Covers the three mapping scenarios, leakage rules, and entity-aware splits.
---

# Tabular Data Pipelines

Map structured rows to `Sample()` fields, fill in what's missing, optionally enrich with context. This is the least structured of the three paradigms — every dataset is different, so always spot-check and check intent with the user.

Full worked example (supply chain disruption forecasting) lives in `agent-docs/tabular-examples.md`.

## When this pattern fits

- Source is structured: CSV, BigQuery, pandas DataFrame, API response, financial data.
- Some `Sample()` fields are already in the data (outcomes, dates, entities); others need to be generated (questions, context, sometimes labels).
- The user may want either forecasting (GRPO, same as forward-looking-training once samples are prepared) or non-forecasting SFT (survey responses, call transcripts, ad persuasion).

## Gut checks before coding

- Does this mapping actually make sense for the user's goal? Ask if it's ambiguous.
- Will the resulting samples be high quality? Plan to spot-check 10-20 before scaling.
- Any leakage? Labels hidden in question text, future info in context, train/test entity overlap.

## The three mapping scenarios

| What you have | What you need | How |
| --- | --- | --- |
| Outcomes | Questions | Compute labels in pandas, then `TemplateQuestionGenerator` |
| Questions + labels | Context | Map both to samples, then a second pipeline pass with `NewsContextGenerator` |
| Questions | Labels | Map questions to samples, add `WebSearchLabeler` |

## Canonical flow (outcomes -> questions)

### 1. Compute labels in pandas

Keep the outcome column separate from features. Do not let the outcome leak into feature text.

```python
import pandas as pd
combined["next_mom_change"] = combined.groupby("entity")["value"].diff().shift(-1)
combined["shock"] = (combined["next_mom_change"] > combined["mom_sd"]).map(
    {True: "yes", False: "no"}
)
```

### 2. Map rows to samples

```python
from lightningrod import LightningRod
from lightningrod.utils.sample import create_sample

lr = LightningRod(api_key=api_key)

samples = []
for _, row in df.iterrows():
    # seed_text carries CURRENT-time values only. Never the outcome / future value.
    seed_text = (
        f"As of {row['month_str']}, {row['entity']} has value {row['value']:.2f}, "
        f"changed {row['mom_change']:+.2f} from last month. Historical SD = {row['mom_sd']:.2f}."
    )
    samples.append(create_sample(
        seed_text=seed_text,
        label=row["shock"],
        seed_date=row["prediction_date"],       # when the model "sees" the question
        meta={"entity": row["entity"]},
    ))

dataset = lr.datasets.create_from_samples(samples)
```

Key `Sample()` fields:

- `seed_text` — features the model sees. Current values only.
- `label` — from the outcome column (or fill later via a labeler).
- `seed_date` / `prediction_date` — when the question is asked. Must be BEFORE the outcome.
- `date_close` / `resolution_date` — when the outcome becomes known.
- `resolution_criteria` — how Yes/No is determined.
- `meta` — anything else the template or analysis needs (entity names, thresholds).

### 3. Template the question

```python
from lightningrod import QuestionPipeline, TemplateQuestionGenerator

pipeline = QuestionPipeline(
    question_generator=TemplateQuestionGenerator(
        question_template=(
            "{seed_text} Will there be a shock next month? "
            "A shock is a month-over-month increase exceeding 1 standard deviation."
        ),
    ),
)
```

**Prefer `TemplateQuestionGenerator` over LLM generation when rows follow a fixed pattern** — it's free and deterministic. Put all computed values into `seed_text` and reference with `{seed_text}` in the template.

### 4. (Optional) Add news context

Second pass on the already-uploaded dataset:

```python
from lightningrod import BinaryAnswerType, NewsContextGenerator, QuestionRenderer

context_pipeline = QuestionPipeline(
    context_generators=[NewsContextGenerator(
        num_search_queries=3, articles_per_query=5, num_articles=10,
        time_delta_days=30, enable_relevance_ranking=True,
    )],
    renderer=QuestionRenderer(answer_type=BinaryAnswerType(), template=render_template),
)
rendered = lr.transforms.run(context_pipeline, input_dataset=dataset.id, max_questions=6000)
```

### 5. Split with leakage in mind

- **Forecasting data (has time):** split on time — train on past, test on future.
- **Multi-entity data (countries, stocks, products):** also ensure no entity's test samples overlap temporally with its own training samples.
- **Non-forecasting tabular (survey responses, ad persuasion):** temporal split may not apply. Ensure no content leakage — e.g., if multiple questions reference the same ad, keep all of that ad's questions in the same split.

```python
test_date_cutoff = "2025-10-01"
train_set = [s for s in full_dataset if s.prediction_date < test_date_cutoff]
test_set  = [s for s in full_dataset if s.prediction_date >= test_date_cutoff]
```

## Training

Same configs as the other paradigms — `GRPOTrainingConfig` for forecasting tabular data, `SFTTrainingConfig` for non-forecasting. For imbalanced binary labels (rare positives), switch the reward:

```python
from lightningrod import BinaryAnswerType
from lightningrod._generated.models.reward_function_type import RewardFunctionType

answer_type = BinaryAnswerType(reward_function_type=RewardFunctionType.BINARY_LOG_SCORE)
```

`BINARY_LOG_SCORE` penalizes confident-wrong predictions harder than Brier, so the model can't just predict the majority class.

## Watch for

- **Do not leak labels.** `seed_text` gets current values. It never contains `next_mom_change`, future outcomes, or the label itself.
- **`prediction_date` strictly before `resolution_date`.** For monthly data: prediction_date in the current month, resolution_date in the next.
- **Template over LLM** when rows follow a pattern — cheaper and deterministic.
- **Validate first.** Print 10-20 samples: label correct? dates ordered? enough context to reason?
- **Pick the split axis that matters.** Time for forecasting, entity/content grouping for cross-sectional data.

## References

- Full worked example (supply chain shocks, 113 time-series, multi-entity split): `agent-docs/tabular-examples.md`.
- Pattern overview: `agent-docs/examples-guide.md` (Pattern 3).
- For the forecasting-training side, the forward-looking-training skill covers the GRPO config and temporal split logic.
