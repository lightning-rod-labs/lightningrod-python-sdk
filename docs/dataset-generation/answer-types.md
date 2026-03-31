---
icon: list-check
---

# Answer Types

Answer types define the format of labels and how questions are rendered: binary (yes/no), continuous (numeric), multiple choice, or free response. Use the same answer type across your question generator, labeler, and renderer so labels and prompts stay consistent.

## BinaryAnswerType

Yes/No probability estimates. Labels are 0 (No) or 1 (Yes). Prompts ask for a probability between 0 and 1.

```python
BinaryAnswerType()
```

Use for: "Will X happen by date Y?", "Did X occur?"

## ContinuousAnswerType

Numeric values. Labels are floats. Prompts ask for a numeric estimate.

```python
ContinuousAnswerType()
```

Use for: "What will the S&P 500 close at?", "How many units will be sold?"

## MultipleChoiceAnswerType

Categorical options. Labels are one of the allowed choices. Prompts list the options.

```python
MultipleChoiceAnswerType()
```

Use for: "Which candidate will win?", "What is the most likely outcome?"

## FreeResponseAnswerType

Open-ended text. Labels are strings. No structured format.

```python
FreeResponseAnswerType()
```

Use for: "Summarize the key risks", "What is the main takeaway?"

## Using Answer Types

Pass the answer type to your question generator, labeler, and renderer:

```python
binary = BinaryAnswerType()

pipeline = QuestionPipeline(
    seed_generator=...,
    question_generator=ForwardLookingQuestionGenerator(
        answer_type=binary,
        ...
    ),
    labeler=WebSearchLabeler(answer_type=binary),
    renderer=QuestionRenderer(answer_type=binary),
)

dataset = lr.transforms.run(pipeline, max_questions=100)
rows = dataset.flattened()
```

`dataset.flattened()` returns a list of flat dicts ready for use in training pipelines.
