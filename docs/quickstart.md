---
icon: bolt
description: Forecast with Foresight or build domain-specific models on the Lightning Rod platform.
---

Lightning Rod's **Foresight** models return calibrated probability forecasts for any forward-looking question through an OpenAI-compatible API.

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
    extra_body={"research": True, "answer_type": "binary"},
)
print(response.choices[0].message.content)
```

See [Guides](forecasting/guides.md) for how to write good forecasting prompts.

[**Get an API key →**](https://dashboard.lightningrod.ai/sign-up?redirect=/api)

## Start forecasting

* [Forecasting Reference](forecasting/reference.md) — models, response shape, and answer types
* [Guides](forecasting/guides.md) — writing good forecasting prompts

## Enterprise

Use the Lightning Rod platform when you need a forecasting model tailored to your domain or data.

We work with teams to:

- **Generate** labeled forecasting datasets from your own sources—news, documents, and custom data—through a configurable pipeline, with no manual question writing or labeling.
- **Fine-tune** specialized models on those datasets.
- **Evaluate** performance against held-out test sets.
- **Serve** the resulting models through `lr.predict()` or the OpenAI-compatible API.

[**Book a call →**](https://calendly.com/d/ctq4-7gd-nyq/lightning-rod-demo) to talk through your use case.

See the [Platform Overview](platform/overview.md).

## Research

Lightning Rod is based on our research: [Future-as-Label: Scalable Supervision from Real-World Outcomes](https://arxiv.org/abs/2601.06336). We use this approach to generate the [Future-as-Label training dataset](https://huggingface.co/datasets/LightningRodLabs/future-as-label-paper-training-dataset) for our paper.
