# Tabular Data Processing Examples

---

## The Mapping

Map structured data to `Sample()` fields, fill in what's missing:

- **Have outcomes, need questions**: Compute labels, use `TemplateQuestionGenerator`
- **Have questions + labels, need context**: Map both, add `NewsContextGenerator`
- **Have questions, need labels**: Map questions, add `WebSearchLabeler`

Key `Sample()` fields:
- `question_text` — template from row values
- `label` — from outcome column or a labeler
- `prediction_date` — when the model "sees" the question (BEFORE outcome)
- `date_close` / `resolution_date` — when outcome is known
- `resolution_criteria` — how to determine Yes/No

---

## Example: Supply Chain Shock Detection

Predict monthly shocks (index spike > 1 SD) across 113 time-series. Labels from data, questions from templates, news context for real-world signal.

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

Seed text includes current values. Label and meta fields carry what `TemplateQuestionGenerator` needs.

```python
from lightningrod import create_sample

samples = []
for _, row in questions_df.iterrows():
    month_str = pd.to_datetime(row["ym"]).strftime("%B %Y")

    # Current values only — NOT next_mom_change (the label)
    seed_text = (
        f"As of {month_str}, the supply chain disruption index for {row['index_name']} "
        f"has a current value of {row['index']:.2f} and changed {row['mom_change']:+.2f} "
        f"from the previous month."
    )

    samples.append(create_sample(
        seed_text=seed_text,
        label=row["shock"],
        seed_creation_date=row["prediction_date"],
        meta={"index_name": row["index_name"], "mom_sd": f"{row['mom_sd']:.2f}"},
    ))

dataset = lr.datasets.create_from_samples(samples)
```

### Step 3: Template Questions

`TemplateQuestionGenerator` builds question text from `{seed_text}` and `{meta.*}` placeholders:

```python
from lightningrod import TemplateQuestionGenerator, QuestionPipeline

pipeline = QuestionPipeline(
    question_generator=TemplateQuestionGenerator(
        question_template=(
            "{seed_text} Will there be a supply chain shock for {meta.index_name} "
            "next month? A shock is defined as a month-over-month increase exceeding "
            "1 standard deviation ({meta.mom_sd}) of historical monthly changes."
        ),
    ),
)
```

### Step 4: Add News Context (Optional)

```python
from lightningrod import BinaryAnswerType, NewsContextGenerator, QuestionRenderer

template = """You are a supply chain analyst forecasting disruption shocks.
    QUESTION: {question_text}
    TODAY'S DATE: {question_date}
    RESOLUTION CRITERIA: {resolution_criteria}
    CONTEXT: {context}
    ANSWER FORMAT: {answer_instructions}"""

pipeline = QuestionPipeline(
    context_generators=[NewsContextGenerator(
        num_search_queries=3, articles_per_query=5, num_articles=10,
        time_delta_days=30, enable_relevance_ranking=True,
    )],
    renderer=QuestionRenderer(answer_type=BinaryAnswerType(), template=template),
)

rendered = lr.transforms.run(pipeline, input_dataset=dataset.id, max_questions=6000)
```

### Step 5: Split and Train

```python
test_date_cutoff = "2025-10-01"
train_set = [s for s in full_dataset if s["prediction_date"] < test_date_cutoff]
test_set = [s for s in full_dataset if s["prediction_date"] >= test_date_cutoff]
# Train: 4,972, Test: 452

# Default config: openai/gpt-oss-120b, lora_rank=32, batch_size=32, learning_rate=4e-5
# reward_function_type="binary_log_score" — better for 14.5% imbalance
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

**Use `TemplateQuestionGenerator`.** LLM generation adds cost when questions follow a fixed pattern. Put computed values in `meta`, reference with `{meta.*}`.

**Split on time.** Train on past, test on future. For multi-entity data (per-country, per-stock), ensure no entity's test samples overlap temporally with its training samples. For cross-sectional data without timestamps, split on whatever grouping prevents the model from memorizing entity-specific patterns.

**Validate first.** Check 10-20 samples: label correct? prediction_date < resolution_date? Enough context to reason?

**`binary_log_score` for imbalanced data.** Penalizes confident wrong predictions harder. Model can't just predict the majority class.
