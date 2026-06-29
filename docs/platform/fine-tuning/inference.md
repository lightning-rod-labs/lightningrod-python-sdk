---
icon: wand-magic-sparkles
description: Run predictions with your fine-tuned model via lr.predict() or the OpenAI-compatible API.
---

# Inference

Use your trained `model_id` with `lr.predict()` or the OpenAI-compatible API.

## LightningRod.predict()

```python
client = lr.LightningRod(api_key="your-api-key")

result = client.predict(
    "Will the Fed cut interest rates in 2026?",
    model=job.model_id,
    answer_type="binary",
)
print(result.binary.probability)
```

`predict()` returns a structured `PredictionResult`. See the [Forecasting Reference](../../forecasting/reference.md) for response fields and answer types.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `prompt` | str | — | The question or prompt text |
| `model` | str | — | Trained model ID |
| `answer_type` | str \| None | `None` | Structured answer format (`"binary"`, `"continuous"`, …) |
| `research` | bool \| list \| None | `None` | Opt-in web research before forecasting |
| `system_prompt` | str \| None | `None` | Optional system message |
| `**kwargs` | — | — | Forwarded to `openai.chat.completions.create` |

Requires `openai`.

## OpenAI-compatible API

Use the OpenAI client with Lightning Rod's base URL:

```python
from openai import OpenAI

client = OpenAI(
    api_key=api_key,
    base_url="https://api.lightningrod.ai/v1/openai",
)

response = client.chat.completions.create(
    model=job.model_id,
    messages=[
        {"role": "user", "content": "Will the Fed cut interest rates in 2026?"},
    ],
    extra_body={"answer_type": "binary"},
)
print(response.choices[0].message.content)
```

## Model availability

Trained model checkpoints are available for **7 days** after training completes. For long-term hosting, contact [support@lightningrod.ai](mailto:support@lightningrod.ai).
