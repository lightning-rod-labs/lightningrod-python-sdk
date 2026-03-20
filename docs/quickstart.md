---
icon: book-open
---

# Quickstart

Get from zero to a labeled forecasting dataset in a few minutes.

## 1. Install the SDK

```bash
pip install lightningrod-ai
```

## 2. Get your API key

Sign up at [dashboard.lightningrod.ai](https://dashboard.lightningrod.ai/sign-up?redirect=/api) to get your API key and **$50 of free credits**.

## 3. Generate your first dataset

```python
import lightningrod as lr

client = lr.LightningRod(api_key="your-api-key")
binary_answer = lr.BinaryAnswerType()

# Get AI news to train a domain expert
seeds = lr.NewsSeedGenerator(
    start_date="2025-01-01",
    end_date="2025-04-01",
    search_query=["frontier AI model", "AI agents", "open source LLM", "AI research"],
)

# Define the scope and style of the questions
questioner = lr.ForwardLookingQuestionGenerator(
    instructions="Write forward-looking, self-contained questions with explicit dates/entities.",
    examples=["Will OpenAI publicly release GPT-5 by March 15, 2026?"],
    answer_type=binary_answer,
)

# Verify answers against live sources
labeler = lr.WebSearchLabeler(answer_type=binary_answer)

# Run pipeline
pipeline = lr.QuestionPipeline(seed_generator=seeds, question_generator=questioner, labeler=labeler)
dataset = client.transforms.run(pipeline, max_questions=1000)
```

The pipeline fetches news seeds, generates forecasting questions, labels them via web search, and returns a dataset.

## Where to go next

* [Dataset Generation Overview](dataset-generation/overview.md) — Understand pipelines, seed generators, and question types
* [Forecasting Overview](forecasting/overview.md) — Get probability estimates with foresight-v3 forecasting model
* [Fine Tuning Overview](fine-tuning/overview.md) — Fine-tune models on your datasets (early access)
