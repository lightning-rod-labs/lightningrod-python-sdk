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

Numeric values with uncertainty. Labels are `{mean, standard_deviation}` distributions. Prompts ask for a mean and standard deviation.

```python
ContinuousAnswerType()
```

Use for: "What will the S&P 500 close at?", "How many units will be sold?"

## ContinuousValueOnlyAnswerType

Single scalar point estimates. Labels are a single float (e.g. `42.5`). Use this when the model should output a point estimate rather than a full distribution. Scored via `CONTINUOUS_VALUE_ONLY_LOG_SCORE`.

```python
ContinuousValueOnlyAnswerType()
```

Use for: "What will the U.S. CPI YoY inflation rate be for March 2026?", "How many units of X were sold in Q1?"

Prefer `ContinuousAnswerType` when you want uncertainty-aware predictions (`{mean, stddev}`). Use `ContinuousValueOnlyAnswerType` when you want a single number.

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

dataset = lr.transforms.run(pipeline, max_seeds=100)
rows = dataset.flattened()
```

`dataset.flattened()` returns a list of flat dicts ready for use in training pipelines.

## Example Builders

Use these helpers to produce formatted example strings for the `examples` and `bad_examples` parameters of question generators. Good examples guide the model toward well-formed questions; bad examples teach it what to avoid.

```python
from lightningrod import binary_example, continuous_example, multiple_choice_example
```

### binary\_example

```python
binary_example(question: str, comment: str | None = None) -> str
```

```python
# Good example — no comment
binary_example("Will the Fed cut rates at its May 6, 2026 FOMC meeting?")

# Bad example — explain why it's bad
binary_example(
    "Will inflation rise?",
    comment="No time frame, no specific metric, no resolution date.",
)
```

### continuous\_example

```python
continuous_example(question: str, comment: str | None = None) -> str
```

```python
# Good example
continuous_example(
    "What will be the U.S. CPI year-over-year inflation rate for March 2026 "
    "as reported by the Bureau of Labor Statistics?"
)

# Bad example
continuous_example(
    "How much will the economy grow soon?",
    comment="Vague timing, no country, no metric, no units.",
)
```

### multiple\_choice\_example

```python
multiple_choice_example(
    question: str,
    options: list[str],
    label: int | str | None = None,
    comment: str | None = None,
) -> str
```

`label` and `comment` are mutually exclusive. Pass `label` for good examples (accepts an int index or the option text directly), `comment` for bad examples.

```python
# Good example — label by index
multiple_choice_example(
    "What will the ECB decide at its April 10, 2025 meeting?",
    ["Rate increase", "No change", "Rate cut"],
    label=1,  # "No change"
)

# Bad example
multiple_choice_example(
    "Which of the following will occur by December 31, 2025?",
    ["Japan raises interest rates", "Apple releases a foldable iPhone"],
    comment="Multiple unrelated events; violates single-event criterion.",
)
```
