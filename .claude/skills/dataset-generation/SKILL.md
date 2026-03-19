---
name: dataset-generation
description: Dataset generation pipeline patterns for Lightningrod. Use when configuring QuestionPipeline, choosing answer types, question generators, labelers, and running transforms.
---

# Dataset Generation

## Answer types

- **`BinaryAnswerType`** — Yes/no questions ("Will X happen?")
- **`ContinuousAnswerType`** — Numeric answers ("What will the price be?")
- **`MultipleChoiceAnswerType`** — Fixed set of choices
- **`FreeResponseAnswerType`** — Open-ended text answers

For guidance on which answer type to recommend and how each affects fine-tuning performance, see the `prediction-framing` skill.

## Question generators

- **`ForwardLookingQuestionGenerator`** — Forecasting questions from news/events. Takes `instructions`, `answer_type`, optional `examples`/`bad_examples`, `questions_per_seed`, `filter_` (`FilterCriteria`)
- **`QuestionGenerator`** — General question generation from any seed content
- **`TemplateQuestionGenerator`** — Template-based generation with variable substitution
- **`QuestionAndLabelGenerator`** — Generates questions AND labels in one step. Use when ground truth is embedded in the seed (e.g. BigQuery rows with known outcomes). No separate labeler needed.

## Labelers

- **`WebSearchLabeler(answer_type)`** — Labels questions via web search. Use for forecasting where answers can be looked up
- **`FileSetRAGLabeler`** — Labels via RAG against a FileSet

## Context generators (optional)

- **`NewsContextGenerator(articles_per_query, num_search_queries, num_articles)`** — Adds recent news context to each question
- **`FileSetContextGenerator`** — Adds RAG context from a FileSet

## QuestionPipeline structure

```python
from lightningrod import (
    QuestionPipeline, ForwardLookingQuestionGenerator,
    WebSearchLabeler, BinaryAnswerType, NewsContextGenerator,
)

answer_type = BinaryAnswerType()
pipeline = QuestionPipeline(
    seed_generator=seed_generator,
    question_generator=ForwardLookingQuestionGenerator(
        instructions="Generate forward-looking yes/no questions about X.",
        answer_type=answer_type,
    ),
    labeler=WebSearchLabeler(answer_type=answer_type),
    context_generators=[NewsContextGenerator(articles_per_query=3)],  # optional
)
```

## Cost estimation

Always estimate before scaling up:

```python
cost = lr.transforms.estimate_cost(pipeline, max_questions=1000)
print(cost)
```

## Run vs submit

```python
# Blocking — good for notebooks and small runs
MAX_QUESTIONS = 10  # Increase for full run (e.g. 1000)
dataset = lr.transforms.run(pipeline, max_questions=MAX_QUESTIONS, name="my-dataset")

# Non-blocking — for long runs
job = lr.transforms.submit(pipeline, max_questions=1000, name="my-dataset")
```

## Output

```python
rows = dataset.flattened(answer_type)  # list of dicts, ready for DataFrame
import pandas as pd
pd.DataFrame(rows)
```

Next step: pass `dataset` to `prepare_for_training` to filter, deduplicate, and split.
