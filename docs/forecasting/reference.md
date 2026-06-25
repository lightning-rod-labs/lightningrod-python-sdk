---
icon: chart-line
description: Foresight forecasting API reference.
---

**Foresight** returns calibrated forecasts through an OpenAI-compatible API.

- Use the OpenAI client for chat/completions compatibility.
- Use `lr.predict()` for a parsed SDK result.

## OpenAI API

```python
from openai import OpenAI

client = OpenAI(
    api_key="your-api-key",
    base_url="https://api.lightningrod.ai/v1/openai",
)

response = client.chat.completions.create(
    model="foresight-v4",
    messages=[
        {"role": "user", "content": "Will the Fed cut rates by 25bp in March 2026?"},
    ],
    reasoning_effort="low",
    extra_body={"research": True, "answer_type": "binary"},
)

message = response.choices[0].message
print(message.content)
```

### Response

- `response.choices[0].message.content` — model response, including `<answer></answer>` tags when `answer_type` is set.
- `response.choices[0].message.thinking` — reasoning, when returned.
- `response.choices[0].message.annotations` — citations, when research runs.
- `response.usage` — usage metadata.

For a dictionary:

```python
data = response.model_dump()
usage = data["usage"]
annotations = data["choices"][0]["message"].get("annotations", [])
```

See the [REST API reference](https://docs.lightningrod.ai/rest-api#post-openai-chat-completions).

## Predict API

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

### Response

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

## Models

| Model | Model ID | Description |
|-------|----------|-------------|
| Foresight v4 | `foresight-v4` | Current forecasting model. |
| Foresight v3 | `foresight-v3` | Previous forecasting model. |
| Military Strikes | `military-strikes` | Trained for Numinous forecasters, generally available. |

## Answer Types

When `answer_type` is set, the response includes machine-readable tags. `predict()` parses them into typed fields.

| `answer_type`       | Raw response shape                                                                           | `PredictionResult` field                                                 |
| ------------------- | -------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------ |
| `"binary"`          | `<answer>0.62</answer>`                                                                      | `result.binary.probability`                                              |
| `"continuous"`      | `<answer>{"mean": 42.5, "standard_deviation": 5.2}</answer>`                                 | `result.continuous.mean`, `result.continuous.standard_deviation`         |
| `"multiple_choice"` | `<options>{"A": "...", "B": "..."}</options>` plus `<answer>{"A": 0.55, "B": 0.45}</answer>` | `result.multiple_choice.options`, `result.multiple_choice.probabilities` |
| `"free_response"`   | `<answer>...</answer>`                                                                       | `result.free_response.text`                                              |
| `"auto"`            | Server-selected structured answer                                                            | Parsed into the best matching typed field                                |

## Enterprise

Need forecasting models tailored to your domain? Use the [Platform](../platform/overview.md) to generate datasets, fine-tune models, and evaluate performance.

[Book a call](https://calendly.com/d/ctq4-7gd-nyq/lightning-rod-demo) to talk through your use case.

## Next steps

* [Guides](guides.md) — writing good forecasting prompts
* [Platform Overview](../platform/overview.md) — generate datasets and fine-tune your own forecasting models
