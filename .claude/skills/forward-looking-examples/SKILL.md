---
name: forward-looking-examples
description: Production examples for forward-looking (GRPO) training -- golf, Trump policy, military strikes, Foresight/GDELT, FileSet RAG. Use when building a forecasting dataset with NewsSeedGenerator, GdeltSeedGenerator, or FileSetSeedGenerator + ForwardLookingQuestionGenerator.
---

# Forward-Looking Training Examples (GRPO)

---

## Common Structure

```
Seeds → ForwardLookingQuestionGenerator → Labels → Context (optional) → Train (GRPO)
```

```python
from datetime import datetime
from lightningrod import (
    LightningRod, TrainingConfig, BinaryAnswerType,
    NewsSeedGenerator, ForwardLookingQuestionGenerator,
    NewsContextGenerator, WebSearchLabeler, QuestionPipeline,
    filter_and_split,
)
lr = LightningRod(api_key=api_key)
```

**Default training config** (Foresight uses `num_rollouts=4` — large general datasets need fewer):

```python
batch_size = 32
config = TrainingConfig(
    base_model_id="openai/gpt-oss-120b",
    training_steps=len(train_data) // batch_size,
    lora_rank=32,
    batch_size=batch_size,
    num_rollouts=8,
    max_response_length=16384,
    learning_rate=4e-5,
)
```

---

## Example 1: Golf Forecasting

**Goal:** Predict professional golf outcomes — tournament winners, cuts, matchups, milestones.

Binary questions, news seeds, 14-day interval matching tournament cadence.

> **Source**: `lightningrod-python-sdk/notebooks/fine_tuning/01_golf_forecasting.ipynb` (demo, max_questions=100), `llm_forecasting/notebooks/golf/golf.ipynb` (production, 10000)

```python
instructions = """
Generate binary forecasting questions about professional golf across all major tours and events.
Cover tournament outcomes, cuts, matchups, majors, team events, season races, world rankings,
and player milestones. Specific, verifiable, spanning the full probability spectrum.
"""

good_examples = [
    "Will Scottie Scheffler win the 2025 Masters?",
    "Will Tiger Woods make the cut at the 2025 Masters?",
    "Will any LIV player win a major championship in 2025?",
    "Will Europe win the 2025 Ryder Cup?",
    "Will Nelly Korda win the 2025 US Women's Open?",
]

bad_examples = [
    "Will someone win the tournament? (obvious)",
    "Will golf be exciting? (subjective)",
    "Will there be birdies? (trivial)",
]

pipeline = QuestionPipeline(
    seed_generator=NewsSeedGenerator(
        start_date=datetime(2024, 6, 1),       # base model knowledge cutoff
        end_date=datetime(2026, 1, 1),
        interval_duration_days=14,              # biweekly — tournament cadence
        search_query=[
            "PGA Tour", "LIV Golf", "LPGA", "golf major championship",
            "Ryder Cup Presidents Cup", "golf world rankings",
            "professional golf", "women's golf", "European Tour golf",
        ],
        articles_per_search=10,
    ),
    question_generator=ForwardLookingQuestionGenerator(
        instructions=instructions,
        examples=good_examples,
        bad_examples=bad_examples,
        answer_type=BinaryAnswerType(),
        questions_per_seed=5,
    ),
    context_generators=[
        NewsContextGenerator(articles_per_query=3, num_search_queries=3, num_articles=5)
    ],
    labeler=WebSearchLabeler(answer_type=BinaryAnswerType()),
)

# 10,000 is a good default — some get filtered, and you want a few thousand for training.
# Use max_questions=100 to test the pipeline first.
dataset = lr.transforms.run(pipeline, max_questions=10000, name="Golf forecasting")
```

```python
train_dataset, test_dataset = filter_and_split(
    dataset, test_size=0.2, split_strategy="temporal",
    days_to_resolution_range=(1, None),
)
```


| Train | Model        | Brier  | vs gpt-5         |
| ----- | ------------ | ------ | ---------------- |
| 3,178 | gpt-oss-120b | 0.2074 | 17% better (BSS) |


---

## Example 2: Trump Policy Forecasting

**Goal:** Predict Trump administration policy actions, decisions, and political outcomes within a 2-month horizon.

Weekly intervals, high questions_per_seed (20) for a narrow domain.

> **Source**: `lightningrod-python-sdk/notebooks/fine_tuning/02_trump_forecasting.ipynb` (demo, max_questions=500), `llm_forecasting/notebooks/e2e/wwtd_2025.ipynb` (production)

```python
instructions = """
Generate binary forecasting questions about Trump's actions, decisions, positions, and statements.
Diverse, covering the full range from very likely to very unlikely.
Horizon: outcomes known within 2 months. Binary, exact dates, self-contained, verifiable, newsworthy.
"""

good_examples = [
    "Will Trump impose 25% tariffs on all goods from Canada by February 1, 2025?",
    "Will Trump issue pardons to January 6 defendants within his first week in office?",
    "Will Pete Hegseth be confirmed as Secretary of Defense by February 15, 2025?",
    "Will Trump sign an executive order to keep TikTok operational in the US by January 31, 2025?",
    "Will Kash Patel be confirmed as FBI Director by March 1, 2025?",
]

bad_examples = [
    "Will Trump do something controversial? (too vague)",
    "Will Trump be in the news? (obvious)",
    "Will tariffs be imposed? (needs specifics)",
]

pipeline = QuestionPipeline(
    seed_generator=NewsSeedGenerator(
        start_date=datetime(2025, 1, 1),
        end_date=datetime(2026, 1, 1),
        interval_duration_days=7,               # weekly — fast-moving domain
        search_query=[
            "Donald Trump domestic policy agenda",
            "Donald Trump trade and tariff actions",
            "Donald Trump foreign policy decisions",
            "Donald Trump interviews and press appearances",
            "Donald Trump lawsuits and court rulings",
        ],
        articles_per_search=10,
    ),
    question_generator=ForwardLookingQuestionGenerator(
        instructions=instructions,
        examples=good_examples,
        bad_examples=bad_examples,
        answer_type=BinaryAnswerType(),
        questions_per_seed=20,                  # narrow domain, many angles per article
    ),
    context_generators=[
        NewsContextGenerator(articles_per_query=3, num_search_queries=1, num_articles=5)
    ],
    labeler=WebSearchLabeler(answer_type=BinaryAnswerType()),
)
```

```python
train_dataset, test_dataset = filter_and_split(
    dataset, test_size=0.2, split_strategy="temporal",
    days_to_resolution_range=(1, 60),           # 2-month horizon
)
```


| Train | Model        | Brier  | vs gpt-5      |
| ----- | ------------ | ------ | ------------- |
| 2,108 | gpt-oss-120b | 0.1939 | Beat (0.2003) |


---

## Example 3: Military Strikes (Large Scale)

**Goal:** Predict military strike events — airstrikes, missile strikes, drone strikes, naval operations — across global conflicts.

Large-scale generation (10k questions). Detailed instructions requiring specific actor/target naming — vague military questions are useless.

> **Source**: `lightningrod-python-sdk/notebooks/fine_tuning/04_military_strikes.ipynb`

```python
instructions = """
Generate binary forecasting questions about military strikes and attack operations.

Cover all strike types: airstrikes, missile strikes, drone strikes, naval strikes.
Cover state and non-state actors using natural news language.

Questions must name the specific actor, specific target, have a specific date/milestone,
be verifiable from open-source news, and span the full probability spectrum.
"""

good_examples = [
    "Will the IDF conduct airstrikes on Hezbollah weapons depots in the Bekaa Valley before November 2024?",
    "Will Iran launch a direct ballistic missile strike on Israeli territory before May 2024?",
    "Will Ukraine conduct drone strikes on Russian oil refineries before April 2024?",
    "Will the US Navy conduct Tomahawk strikes on Houthi radar sites before February 2024?",
    "Will NATO aircraft conduct strikes inside Russian territory before January 2025?",
]

bad_examples = [
    "Will there be an attack somewhere? (no actor, target, or location)",
    "Will violence increase in the Middle East? (vague)",
    "Will conflict continue in Ukraine? (trivially obvious)",
    "Will missiles be fired? (no actor, no target, no date)",
]

pipeline = QuestionPipeline(
    seed_generator=NewsSeedGenerator(
        start_date=datetime(2024, 6, 1),
        end_date=datetime(2026, 3, 1),
        interval_duration_days=7,
        search_query=[
            "military airstrike", "military strike",
            "missile strike", "drone strike", "naval strike",
        ],
        articles_per_search=10,
    ),
    question_generator=ForwardLookingQuestionGenerator(
        instructions=instructions,
        examples=good_examples,
        bad_examples=bad_examples,
        answer_type=BinaryAnswerType(),
        questions_per_seed=5,
    ),
    context_generators=[
        NewsContextGenerator(articles_per_query=3, num_search_queries=3, num_articles=5)
    ],
    labeler=WebSearchLabeler(answer_type=BinaryAnswerType()),
)

dataset = lr.transforms.run(pipeline, max_questions=10000, name="Military strikes forecasting")
```

```python
train_dataset, test_dataset = filter_and_split(
    dataset, test_size=0.2, split_strategy="temporal",
    days_to_resolution_range=(1, 90),
)

batch_size = 32
config = TrainingConfig(
    base_model_id="openai/gpt-oss-120b",
    training_steps=len(train_dataset.flattened()) // batch_size,
    lora_rank=32, batch_size=batch_size, num_rollouts=8,
    max_response_length=16384, learning_rate=4e-5,
)
job = lr.training.run(config, dataset=train_dataset, name="military-strikes-v1")

eval_job = lr.evals.run(
    model_id=job.model_id, dataset=test_dataset,
    benchmark_model_id="openai/gpt-5",
)
```

---

## Example 4: Foresight v3 — General Forecasting (GDELT)

**Goal:** Build a general-purpose forecasting model across all domains — politics, economics, science, geopolitics.

Seeds from GDELT (broad global news). High confidence threshold (0.9) for production quality. Custom answer format.

> **Source**: `llm_forecasting/notebooks/foresight-gpt-oss/data-generation-binary.ipynb`, `tinker-train-with-template.ipynb`

```python
from lightningrod import GdeltSeedGenerator, QuestionRenderer

instructions = """
Generate forward-looking binary forecasting questions with exactly one yes/no answer.
Must be unresolved when asked, resolve within 3 months, materially important, fully self-contained,
and resolvable via public web search. Do NOT include numeric, multiple-choice, trivial, vague,
or > 3-month questions.
"""

good_examples = [
    "Will the U.S. Federal Reserve cut interest rates at its FOMC meeting ending May 6, 2026?",
    "Will the S&P 500 index close above 5,000 on April 30, 2026?",
    "Will the Liberal Party win a majority in the Canadian federal election on April 28, 2026?",
    "Will NASA's Artemis II crewed lunar flyby mission launch before June 30, 2026?",
    "Will Brent crude oil futures close above $80 per barrel on June 30, 2026?",
]

bad_examples = [
    "What will the inflation rate be in March 2026? # numeric, not binary",
    "Will inflation rise? # no time frame, no metric",
    "Which party will win the election? # multiple-choice",
    "Will the economy improve next year? # vague, exceeds 3 months",
]

answer_type = BinaryAnswerType(
    answer_format_instruction=(
        "Think carefully about your answer and output your final prediction "
        "(a float between 0.0 and 1.0) between <answer></answer> tags."
    ),
)

pipeline = QuestionPipeline(
    seed_generator=GdeltSeedGenerator(
        start_date=datetime(2024, 7, 3),
        end_date=datetime(2025, 11, 30),
        interval_duration_days=7,
        # Higher than NewsSeedGenerator — GDELT covers broad global topics,
        # so more articles per interval still yields diverse seeds.
        articles_per_interval=25,
    ),
    question_generator=ForwardLookingQuestionGenerator(
        instructions=instructions,
        examples=good_examples,
        bad_examples=bad_examples,
        questions_per_seed=5,
        answer_type=answer_type,
    ),
    context_generators=[NewsContextGenerator(num_articles=10)],
    labeler=WebSearchLabeler(answer_type=answer_type, confidence_threshold=0.9),
    renderer=QuestionRenderer(answer_type=answer_type),
)

dataset = lr.transforms.run(pipeline, max_questions=9000)
```

**Training**: `gpt-oss-120b`, `num_rollouts=4` (sufficient for large general dataset), `training_steps=160`.

---

## Example 5: Timestamped Documents (FileSet RAG)

**Goal:** Train a domain expert from a corpus of timestamped documents, with no pre-existing labeled data.

General pattern for any set of documents that arrive over time — quarterly reports, research papers, regulatory filings, internal memos, etc. Generate questions from earlier documents, resolve them with later ones via `FileSetRAGLabeler` with `TemporalConstraint.AFTER`.

This example uses Fed Beige Book reports, but the pattern applies to any corpus where later documents can confirm or deny outcomes discussed in earlier ones.

> **Source**: `llm_forecasting/notebooks/filesets/beigebook/01_beige_book_pipeline.ipynb` (branch: `beige-book-e2e`)

```python
from lightningrod import FileSetSeedGenerator

# Upload documents to FileSet with date metadata.
# Each document needs a date so the labeler can enforce temporal ordering.
# (see source notebook for download + upload code)

pipeline = QuestionPipeline(
    seed_generator=FileSetSeedGenerator(
        file_set_id=fileset.id, chunk_size=4000, chunk_overlap=200,
    ),
    question_generator=ForwardLookingQuestionGenerator(
        questions_per_seed=5,
        answer_type=BinaryAnswerType(),
        instructions=(
            "Generate questions about specific economic outcomes (decrease, increase, slow, "
            "accelerate). Ask about the outcome directly — 'Will loan nonperformance in Dallas "
            "decrease?' — NOT 'Will the next Beige Book report that...'. "
            "No dates/months/years. Focus on district-specific topics. "
            "Flat/stable/unchanged = No. Not reported = Undetermined."
        ),
        examples=[
            "Will loan nonperformance in the Dallas district decrease?",
            "Will employment growth in the Philadelphia district slow?",
            "Will manufacturing activity in the St. Louis district improve?",
        ],
        bad_examples=[
            "Will the next Beige Book report that X? # report framing",
            "Will the October 2024 Beige Book report X? # specific dates",
            "Will economic activity in Cleveland change? # too vague",
        ],
    ),
)

dataset = lr.transforms.run(pipeline, max_questions=3000)

# Phase 2: Label via FileSetRAGLabeler with TemporalConstraint.AFTER
# This ensures only documents published AFTER the question's seed date are used for labeling,
# so the model can't "see" the answer at question time.
# confidence_threshold=0.7 (lower — answers from known documents)
# labeler_instruction emphasizes: flat/stable = No, not reported = Undetermined,
# never infer No from absence
```

**Training**: `gpt-oss-120b`, `training_steps=66`, `num_rollouts=4`.

---

## Reference

### filter_and_split()

Temporal splitting ensures no training sample has a close date past the start of the test set, preventing data leakage. `days_to_resolution_range` filters to resolved questions within the expected horizon.

```python
train_dataset, test_dataset = filter_and_split(
    dataset, test_size=0.2, split_strategy="temporal",
    days_to_resolution_range=(1, None),  # resolved only
)
```


| Domain      | `days_to_resolution_range` |
| ----------- | -------------------------- |
| Politics    | `(1, 60)`                  |
| Sports      | `(1, None)`                |
| Geopolitics | `(1, 90)`                  |
| General     | `(1, None)`                |


### Training Parameters


| Parameter             | Value                           | Notes                |
| --------------------- | ------------------------------- | -------------------- |
| `base_model_id`       | `openai/gpt-oss-120b`           | Default              |
| `lora_rank`           | 32 or 16                        | Standard             |
| `batch_size`          | 32                              | Standard             |
| `num_rollouts`        | 8                               | More = better signal |
| `max_response_length` | 16384                           | Reasoning chains     |
| `learning_rate`       | 4e-5                            | Standard             |
| `training_steps`      | `len(train_data) // batch_size` | One pass             |


### Cost Estimation

```python
cost = lr.training.estimate_cost(config, dataset=train_dataset)
```
