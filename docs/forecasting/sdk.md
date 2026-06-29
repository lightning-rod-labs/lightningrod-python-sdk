---
icon: python
description: Structured predictions with lr.predict()
---

# Python SDK

## Minimal example

```python
import lightningrod as lr

client = lr.LightningRod(api_key="your-api-key")

result = client.predict("Will the Fed cut interest rates in 2026?", model="foresight-v4")

print(result.content)
```

Response fields:

| Field             | Type                    | Description                                                     |
| ----------------- | ----------------------- | --------------------------------------------------------------- |
| `content`         | `str`                   | Full response, including any `<answer>` tags.                   |
| `thinking`        | `str \| None`           | Reasoning, when returned.                                      |
| `sources`         | `list[Source]`          | URL citations from research. Each source has `url` and `title`. |
| `usage`           | `Usage`                 | Token counts and cost fields.                                   |
| `model`           | `str`                   | Model that served the request.                                  |
| `id`              | `str`                   | Response ID.                                                    |
| `binary`          | `BinaryPrediction \| None`       | Populated when `answer_type="binary"`.            |
| `continuous`      | `ContinuousPrediction \| None`   | Populated when `answer_type="continuous"`.        |
| `multiple_choice` | `MultiChoicePrediction \| None`  | Populated when `answer_type="multiple_choice"`.   |
| `free_response`   | `FreeResponsePrediction \| None` | Populated when `answer_type="free_response"`.     |

## Answer formats

When `answer_type` is set, `predict()` parses the response tags into typed fields on `PredictionResult`.

```python
import lightningrod as lr

client = lr.LightningRod(api_key="your-api-key")

result = client.predict(
    "Will the Fed cut interest rates in 2026?",
    answer_type="binary",
)

print(result.binary.probability)
print(result.content)
```

| `answer_type`       | `PredictionResult` field                                                 |
| ------------------- | ------------------------------------------------------------------------ |
| `"binary"`          | `result.binary.probability`                                              |
| `"continuous"`      | `result.continuous.mean`, `result.continuous.standard_deviation`         |
| `"multiple_choice"` | `result.multiple_choice.options`, `result.multiple_choice.probabilities` |
| `"free_response"`   | `result.free_response.text`                                              |
| `"auto"`            | One of the above fields, inferred from the server-classified answer type |

`answer_type="auto"` classifies the question server-side and populates the matching
prediction field. `result.usage.classification_cost_usd` is set when classification runs (cost is negligible).

See our [API reference](https://docs.lightningrod.ai/api-reference) for more response examples.

## Research

Pass `research=True` to query all default sources, or pass a list to restrict providers:

```python
result = client.predict(
    "Will the Fed cut interest rates in 2026?",
    research=["perplexity", "google_news"],
)

for source in result.sources:
    print(source.title, source.url)
print(result.usage.research_cost_usd)
```

See our [API reference](https://docs.lightningrod.ai/api-reference) for an up-to-date list of supported sources.

## Reasoning effort

```python
result = client.predict(
    "Will the Fed cut interest rates in 2026?",
    reasoning_effort="low",
)

print(result.content)
print(result.usage.total_tokens)
```

Recommendation: use `low` reasoning effort if cost and latency outweigh marginal improvements in accuracy.

See [Recipes](recipes.md) for more forecasting guidelines.