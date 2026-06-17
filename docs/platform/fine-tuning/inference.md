---
icon: wand-magic-sparkles
description: Run predictions with your fine-tuned model via lr.predict() or the OpenAI-compatible API — the same interface as Foresight.
---

# Inference

Your fine-tuned model is served through the same interface as the hosted [Foresight](../../forecasting/reference.md) models. Everything in the [Forecasting](../../forecasting/reference.md) section applies—just pass your trained `model_id` instead of `foresight-v4`.

## LightningRod.predict()

```python
client = lr.LightningRod(api_key="your-api-key")

result = client.predict(
    job.model_id,
    "Will the Fed cut rates by 25bp in March 2026?",
    answer_type="binary",
)
print(result.binary.probability)
```

`predict()` returns a structured `PredictionResult` and accepts the same first-class parameters as Foresight—`answer_type`, `research`, `reasoning_effort`, and `system_prompt`. See the [Forecasting Reference](../../forecasting/reference.md) for the full reference.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `model_id` | str | — | Your trained model ID |
| `prompt` | str | — | The question or prompt text |
| `answer_type` | str \| None | `None` | Structured answer format (`"binary"`, `"continuous"`, …) |
| `research` | bool \| list \| None | `None` | Opt-in web research before forecasting |
| `reasoning_effort` | str | `"medium"` | `"low"`, `"medium"`, or `"high"` |
| `system_prompt` | str \| None | `None` | Optional system message |
| `**kwargs` | — | — | Forwarded to `openai.chat.completions.create` |

Requires `pip install openai` (uses Lightning Rod's API key and base URL automatically).

## OpenAI-compatible API

Use the OpenAI client with Lightning Rod's base URL for full control:

```python
from openai import OpenAI

client = OpenAI(
    api_key=api_key,
    base_url="https://api.lightningrod.ai/api/public/v1/openai",
)

response = client.chat.completions.create(
    model=job.model_id,
    messages=[
        {"role": "user", "content": "Will the Fed cut rates by 25bp in March 2026?"},
    ],
    extra_body={"answer_type": "binary"},
)
print(response.choices[0].message.content)
```

## Model availability

Trained model checkpoints are available for **7 days** after training completes. For long-term hosting, contact [support@lightningrod.ai](mailto:support@lightningrod.ai).
