---
icon: python
description: Structured predictions with lr.predict()
---

# Using our SDK

```python
import lightningrod as lr

client = lr.LightningRod(api_key="your-api-key")

result = client.predict(
    "Will the Fed cut rates by 25bp in March 2026?",
    model="foresight-v4",
    answer_type="binary",
    research=True,
    reasoning_effort="low",
)

print(result.binary.probability)
print(result.content)
```

## Response

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

| `answer_type`       | `PredictionResult` field                                                 |
| ------------------- | ------------------------------------------------------------------------ |
| `"binary"`          | `result.binary.probability`                                              |
| `"continuous"`      | `result.continuous.mean`, `result.continuous.standard_deviation`         |
| `"multiple_choice"` | `result.multiple_choice.options`, `result.multiple_choice.probabilities` |
| `"free_response"`   | `result.free_response.text`                                              |
| `"auto"`            | Parsed into the best matching typed field                                |

## Research

Pass `research=True` to query all default sources, or pass a list to restrict providers:

```python
result = client.predict(
    "Will the Fed cut rates by 25bp in March 2026?",
    model="foresight-v4",
    answer_type="binary",
    research=["perplexity", "google_news"],
)

for source in result.sources:
    print(source.title, source.url)
print(result.usage.research_cost_usd)
```

See our [API reference](https://docs.lightningrod.ai/api-reference) for an up-to-date list of supported sources.