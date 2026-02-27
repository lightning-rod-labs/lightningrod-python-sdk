---
name: dataset-generation
description: Answer types, question generators, labelers for Lightningrod. Use when configuring dataset generation pipelines.
---

# Dataset Generation

## Answer types

- **BinaryAnswerType:** Yes/no questions
- **ContinuousAnswerType:** Numeric (e.g. "What will the price be?")
- **MultipleChoiceAnswerType:** Fixed choices
- **FreeResponseAnswerType:** Open-ended text

## Question generators

- **ForwardLookingQuestionGenerator:** Forecasting questions from seeds (news, events). Instructions + answer_type.
- **TemplateQuestionGenerator:** Template-based generation.
- **QuestionAndLabelGenerator:** Generate questions and labels in one step (no separate labeler).

## Labeler

**WebSearchLabeler:** Finds answers via web search. Pass answer_type. Used for forecasting (future-as-label).

## Typical pipeline (forecasting)

```python
answer_type = BinaryAnswerType()
question_generator = ForwardLookingQuestionGenerator(
    instructions="Generate forward-looking questions about X.",
    answer_type=answer_type,
)
labeler = WebSearchLabeler(answer_type=answer_type)
pipeline = QuestionPipeline(
    seed_generator=seed_generator,
    question_generator=question_generator,
    labeler=labeler,
)
```

## Output

```python
dataset = lr.transforms.run(pipeline, max_questions=10)
rows = dataset.flattened(answer_type)
```

Rows are dicts ready for inspection or export.
