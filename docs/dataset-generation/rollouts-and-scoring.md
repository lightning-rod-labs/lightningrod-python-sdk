---
icon: chart-line
---

# Rollouts & Scoring

Rollouts send rendered prompts to one or more LLMs and score their outputs against ground truth. Use them to benchmark models, compare forecasts, or analyze model consensus on forecasting questions.

## Pipeline Flow

When you add `rollout_generator` and `scorer` to a `QuestionPipeline`, the pipeline runs two extra stages after rendering:

1. **Rollout** — Each rendered prompt is sent to every configured model; each model returns a completion (and optionally structured output).
2. **Scoring** — Each model's output is scored against the sample's label using a reward function that matches the answer type.

Samples end up with a `rollouts` list: one entry per model, each with `model_name`, `content`, `parsed_output`, and `reward`.

## QuestionRenderer

Formats questions into prompts for model input. The rendered prompt becomes `sample.prompt`, which `RolloutGenerator` sends to each model. Optional; a default renderer is used if omitted.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `template` | str | No | — | Custom template. Placeholders: `{question_text}`, `{context}`, `{answer_instructions}` |
| `answer_type` | AnswerType | No | — | Used to render answer instructions |

```python
QuestionRenderer(
    answer_type=BinaryAnswerType(),
)
```

## RolloutGenerator

Sends prompts to multiple models. Requires a list of `ModelConfig` objects.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `models` | list[ModelConfig] | Yes | — | Models to run (e.g. via `open_router_model()`) |
| `prompt_template` | str \| None | No | — | Template with `{column}` placeholders. If None, uses `sample.prompt` |
| `input_columns` | list[str] | No | — | Columns from meta to substitute into template |
| `output_schema` | Any | No | — | Pydantic model for structured output |

## RolloutScorer

Scores each rollout against the sample's label. The reward function depends on the answer type (Brier score for binary, log score for continuous, etc.).

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `answer_type` | AnswerType | Yes | — | Must match the pipeline's answer type |
| `multiple_choice_options` | dict \| None | No | — | For multiple choice: option key → display value |
| `is_mutually_exclusive` | bool | No | True | Whether options are mutually exclusive |

## Analysis Utilities

After downloading samples with rollouts, use these utilities to analyze model performance and consensus.

### compute_metrics_summary

Per-model accuracy and calibration metrics.

```python
from lightningrod.utils import compute_metrics_summary

summary = compute_metrics_summary(samples)
# Returns: {model_name: {"mean_reward", "parse_rate", "n_total", "accuracy", ...}}
```

For multiple choice, pass the options mapping:

```python
summary = compute_metrics_summary(samples, multiple_choice_options=OPTIONS)
```

### compute_consensus

For binary/continuous probability forecasts: where do models agree or disagree?

```python
from lightningrod.utils import compute_consensus

consensus = compute_consensus(samples)
# Returns list of dicts with: question_text, predictions (model → prob), label, spread, all_agree
```

Each entry has:
- `predictions` — model name → predicted probability
- `spread` — max minus min probability across models (higher = more disagreement)
- `all_agree` — whether all models predict the same side of 0.5

### compute_multi_choice_consensus / compute_consensus_summary

For multiple-choice tasks, use `compute_multi_choice_consensus` or `compute_consensus_summary` with the options mapping. See [document_classification.ipynb](https://colab.research.google.com/github/lightning-rod-labs/lightningrod-python-sdk/blob/main/notebooks/e2e/document_classification.ipynb).

## When to Use Rollouts

| Use case | Setup |
|----------|------|
| Benchmark multiple models on the same questions | Add `RolloutGenerator` + `RolloutScorer` to pipeline |
| Compare model consensus (agreement/disagreement) | Run pipeline, then `compute_consensus(samples)` |
| Per-model accuracy and calibration | Run pipeline, then `compute_metrics_summary(samples)` |
| Training data only (no model comparison) | Omit `rollout_generator` and `scorer` |

## Example: Rollouts in a QuestionPipeline

RolloutGenerator and RolloutScorer plug into `QuestionPipeline` as optional stages after rendering. The pipeline runs seeds → questions → labeling → rendering, then sends each rendered prompt to every configured model and scores the outputs.

```python
from lightningrod import (
    QuestionPipeline,
    RolloutGenerator,
    RolloutScorer,
    BinaryAnswerType,
    open_router_model,
)

models = [
    open_router_model("openai/gpt-4.1-mini"),
    open_router_model("anthropic/claude-sonnet-4"),
    open_router_model("google/gemini-2.5-flash"),
]

answer_type = BinaryAnswerType()
rollout_generator = RolloutGenerator(models=models)
scorer = RolloutScorer(answer_type=answer_type)

pipeline = QuestionPipeline(
    seed_generator=...,
    question_generator=...,
    labeler=...,
    renderer=...,
    rollout_generator=rollout_generator,
    scorer=scorer,
)

dataset = lr.transforms.run(pipeline, max_questions=20)
samples = dataset.download()
```

For a full end-to-end example including seed generation, question generation, and consensus analysis, see [model_consensus.ipynb](https://colab.research.google.com/github/lightning-rod-labs/lightningrod-python-sdk/blob/main/notebooks/e2e/model_consensus.ipynb).

## Related

- [Answer Types](answer-types.md) — Binary, Continuous, MultipleChoice affect scoring
- [Examples](examples.md) — [model_consensus.ipynb](https://colab.research.google.com/github/lightning-rod-labs/lightningrod-python-sdk/blob/main/notebooks/e2e/model_consensus.ipynb), [polymarket_backtesting.ipynb](https://colab.research.google.com/github/lightning-rod-labs/lightningrod-python-sdk/blob/main/notebooks/e2e/polymarket_backtesting.ipynb), [document_classification.ipynb](https://colab.research.google.com/github/lightning-rod-labs/lightningrod-python-sdk/blob/main/notebooks/e2e/document_classification.ipynb)
