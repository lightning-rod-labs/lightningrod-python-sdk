---
name: tabular-examples
description: Production example for tabular data processing -- supply chain shock detection with create_sample(), TemplateQuestionGenerator, and QuestionRenderer. Use when mapping structured data (CSV, BigQuery, API results) to Sample() fields.
---

# Tabular Data Processing Examples

This is the least structured pattern — every dataset is different. The supply chain example below is a well-documented walkthrough of one common case (time-series with computed labels), but you'll need to adapt it. Tabular data can be twisted many ways to produce a result, and not all of them make sense. When in doubt, check with the user.

**Gut checks to apply throughout:**
- Does this mapping actually make sense for what the user is trying to do?
- Does the resulting data look high quality? (Spot-check 10-20 samples.)
- Is there any leakage — labels in the question text, future info in the context, train/test overlap?
- Is the end result achieving the user's goal, or just producing output?

---

## The Mapping

Map structured data to `Sample()` fields, fill in what's missing:

- **Have outcomes, need questions**: Compute labels, use `TemplateQuestionGenerator`
- **Have questions, need labels**: Map questions, add `WebSearchLabeler`

Key `Sample()` fields:
- `question_text` — template from row values
- `label` — from outcome column or a labeler
- `prediction_date` — when the model "sees" the question (BEFORE outcome)
- `date_close` / `resolution_date` — when outcome is known
- `resolution_criteria` — how to determine Yes/No

---

## Example: Supply Chain Shock Detection

**Goal:** Predict monthly supply chain disruption shocks (index spike > 1 SD) across 113 time-series, using news context for real-world signal.

One common case: time-series data where outcomes are known and you need to generate questions and context. The steps below generalize to other tabular forecasting problems — swap the domain, adjust the mapping, but the structure is the same.

> **Source**: `llm_forecasting/notebooks/supply-chain-disruptions/01_binary_data_pipeline.ipynb` (branch: `supply-chain-disruptions-analysis`)

### Step 1: Compute Labels

```python
import pandas as pd

combined = combined.sort_values(["index_name", "ym"]).copy()
combined["mom_change"] = combined.groupby("index_name")["index"].diff()
series_sd = combined.groupby("index_name")["mom_change"].std()
combined = combined.join(series_sd.rename("mom_sd"), on="index_name")
combined["next_mom_change"] = combined.groupby("index_name")["mom_change"].shift(-1)

# Shock = next month's increase > 1 SD
combined["shock"] = (combined["next_mom_change"] > combined["mom_sd"]).map(
    {True: "yes", False: "no"}
)

questions_df = combined[combined["ym"] > "2022-01-01"].dropna(
    subset=["mom_change", "next_mom_change"]
).copy()
# 5,424 questions, 14.5% shock rate
```

### Step 2: Map to Samples

Seed text includes current values and all fields needed for the question template. Label and meta fields carry additional data.

```python
from lightningrod import LightningRod, create_sample

lr = LightningRod(api_key=api_key)

samples = []
for _, row in questions_df.iterrows():
    month_str = pd.to_datetime(row["ym"]).strftime("%B %Y")

    # Current values only — NOT next_mom_change (the label).
    # Include all values needed for the question template in seed_text.
    seed_text = (
        f"As of {month_str}, the supply chain disruption index for {row['index_name']} "
        f"has a current value of {row['index']:.2f} and changed {row['mom_change']:+.2f} "
        f"from the previous month. The historical standard deviation of monthly changes "
        f"is {row['mom_sd']:.2f}."
    )

    samples.append(create_sample(
        seed_text=seed_text,
        label=row["shock"],
        seed_date=row["prediction_date"],
        meta={"index_name": row["index_name"], "mom_sd": f"{row['mom_sd']:.2f}"},
    ))

dataset = lr.datasets.create_from_samples(samples)
```

### Step 3: Template Questions

`TemplateQuestionGenerator` builds question text from `{seed_text}` placeholders. Put all values needed for the question into `seed_text`:

```python
from lightningrod import TemplateQuestionGenerator, QuestionPipeline

pipeline = QuestionPipeline(
    question_generator=TemplateQuestionGenerator(
        question_template=(
            "{seed_text} Will there be a supply chain shock next month? "
            "A shock is defined as a month-over-month increase exceeding "
            "1 standard deviation of historical monthly changes."
        ),
    ),
)
```

### Step 4: Render Prompts (Optional)

Second pass on the uploaded dataset — renders prompts:

```python
from lightningrod import BinaryAnswerType, QuestionRenderer

render_template = """You are a supply chain analyst forecasting disruption shocks.
    QUESTION: {question_text}
    TODAY'S DATE: {question_date}
    RESOLUTION CRITERIA: {resolution_criteria}
    ANSWER FORMAT: {answer_instructions}"""

render_pipeline = QuestionPipeline(
    renderer=QuestionRenderer(answer_type=BinaryAnswerType(), template=render_template),
)

rendered = lr.transforms.run(render_pipeline, input_dataset=dataset.id, max_seeds=6000)
```

### Step 5: Split and Train

```python
test_date_cutoff = "2025-10-01"
train_set = [s for s in full_dataset if s["prediction_date"] < test_date_cutoff]
test_set = [s for s in full_dataset if s["prediction_date"] >= test_date_cutoff]
# Train: 4,972, Test: 452

# Default config: openai/gpt-oss-120b, lora_rank=32, batch_size=32, learning_rate=4e-5
# For imbalanced data, set reward_function_type on the answer type:
# BinaryAnswerType(reward_function_type=RewardFunctionType.BINARY_LOG_SCORE)
```

| Metric | Value |
|--------|-------|
| Series | 113 (25 countries + 88 products) |
| Samples | 5,424 |
| Shock rate | 14.5% |
| Train / Test | 4,972 / 452 |

---

## Things to Watch For

**Don't leak labels.** Seed text has current values, not the outcome. `index=0.85, mom_change=+0.12` is fine; `next_mom_change` is not.

**`prediction_date` before `resolution_date`.** For monthly data: prediction_date within current month, date_close is next month.

**Use `TemplateQuestionGenerator`.** LLM generation adds cost when questions follow a fixed pattern. Put all computed values into `seed_text` and reference with `{seed_text}` in the template.

**Split on time.** Train on past, test on future. For multi-entity data (per-country, per-stock), ensure no entity's test samples overlap temporally with its training samples. For cross-sectional data without timestamps, split on whatever grouping prevents the model from memorizing entity-specific patterns.

**Validate first.** Check 10-20 samples: label correct? prediction_date < resolution_date? Enough context to reason?

**Lint before splitting.** Run the dataset linter on the full generated dataset before splitting or training. Linting runs server-side on the whole dataset. Tabular data is especially prone to duplicates from overlapping time windows or missing fields from incomplete row mappings.

**`binary_log_score` for imbalanced data.** Penalizes confident wrong predictions harder. Model can't just predict the majority class.
