---
icon: wand-magic-sparkles
---

# Inference

Use your trained model for predictions. Two options: the convenience method `lr.predict()` or the OpenAI-compatible API directly.

## lr.predict()

Single prediction with a trained model:

```python
response = lr.predict(job.model_id, "Will the Fed cut rates by 25bp in March 2026?")
print(response)
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `model_id` | str | — | Your trained model ID |
| `prompt` | str | — | The question or prompt text |
| `system_prompt` | str | `"Answer as a probability between 0 and 1 between <answer></answer> tags."` | System message |
| `**kwargs` | — | — | Passed to `openai.chat.completions.create` |

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
        {"role": "system", "content": "Answer as a probability between 0 and 1 between <answer></answer> tags."},
        {"role": "user", "content": "Will the Fed cut rates by 25bp in March 2026?"},
    ],
)
print(response.choices[0].message.content)
```

## Model availability

Trained model checkpoints are available for **7 days** after training completes. For long-term hosting, contact support@lightningrod.ai.
