---
icon: circle-question
---

# Question Generators

Question generators turn seeds into questions. They run after seed generation and before labeling. Choose based on whether you need forward-looking questions, synthetic labels, or template-based generation.

## QuestionGenerator

General-purpose question generation from seeds.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `instructions` | str | No | — | Instructions for question generation |
| `examples` | list[str] | No | — | Example questions to guide generation |
| `bad_examples` | list[str] | No | — | Examples of questions to avoid |
| `filter_` | FilterCriteria or list | No | — | Optional filter criteria after generation |
| `questions_per_seed` | int | No | 1 | Questions to generate per seed |
| `include_default_filter` | bool | No | False | Include default filter for generated questions |
| `answer_type` | AnswerType | No | — | Expected answer type (Binary, Continuous, etc.) |

## ForwardLookingQuestionGenerator

Specialized for forward-looking forecasting questions. Same parameters as `QuestionGenerator`. Use when you want questions with explicit resolution dates and criteria.

```python
ForwardLookingQuestionGenerator(
    instructions="Generate binary forecasting questions about Trump's actions and decisions.",
    examples=[
        "Will Trump impose 25% tariffs on all goods from Canada by February 1, 2025?",
        "Will Pete Hegseth be confirmed as Secretary of Defense by February 15, 2025?",
    ],
    answer_type=BinaryAnswerType(),
)
```

## QuestionAndLabelGenerator

Generates both questions and labels in one step. Use when you don't need web search for labeling (e.g. synthetic labels from the model). No separate `labeler` is needed when using this generator.

Same parameters as `QuestionGenerator`. Omit `labeler` in your pipeline:

```python
pipeline = QuestionPipeline(
    seed_generator=NewsSeedGenerator(...),
    question_generator=QuestionAndLabelGenerator(
        instructions="Generate binary forecasting questions with synthetic labels.",
        answer_type=BinaryAnswerType(),
    ),
    labeler=None,
)
```

## TemplateQuestionGenerator

Generates questions from a template string. Use when you have structured data and a fixed question format.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `question_template` | str | Yes | — | Template with placeholders. Supports `{seed_text}`, `{seed}`, `{meta.label}` |

```python
TemplateQuestionGenerator(
    question_template="Will {meta.label} be acquired by {meta.date_close}?",
)
```

Placeholders: `{seed_text}`, `{seed}`, and any key in `meta` (e.g. `{meta.label}`).

## When to Use Each

| Generator | Use case |
|-----------|----------|
| `ForwardLookingQuestionGenerator` | Forecasting questions with resolution dates and criteria; most common for prediction tasks |
| `QuestionGenerator` | General questions from seeds |
| `QuestionAndLabelGenerator` | Questions + synthetic labels in one step; no web search labeling |
| `TemplateQuestionGenerator` | Structured questions from templates with `{seed_text}`, `{meta.label}`, etc. |
