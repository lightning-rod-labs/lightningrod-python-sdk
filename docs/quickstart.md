---
icon: bolt
description: Lightning Rod's Foresight models return calibrated probability forecasts through an OpenAI-compatible API — and a platform to fine-tune your own forecasting models.
---

## Introduction

Lightning Rod's **Foresight** models return calibrated probability forecasts for any forward-looking question through an OpenAI-compatible API.

```python
from openai import OpenAI

client = OpenAI(
    api_key="your-api-key",
    base_url="https://api.lightningrod.ai/api/public/v1/openai",
)

response = client.chat.completions.create(
    model="foresight-v4",
    messages=[
        {"role": "user", "content": "Will the Fed cut rates by 25bp in March 2026?"},
    ],
    extra_body={"research": True},
)
print(response.choices[0].message.content)
```

That `0.62` is a **calibrated probability**—a 62% chance, not a confidence score. `0.5` means genuinely uncertain. See [Guides](forecasting/guides.md) for how to write questions and read the numbers.

[**Get an API key →**](https://dashboard.lightningrod.ai/sign-up?redirect=/api)

## Start forecasting

* [Forecasting Reference](forecasting/reference.md) — models, usage paths, `answer_type`, `research`, and `reasoning_effort`
* [Guides](forecasting/guides.md) — writing good questions and interpreting probabilities

## Enterprise

The hosted [Foresight](forecasting/reference.md) models answer forward-looking questions out of the box. When you need a model tailored to your domain, proprietary data, or internal workflows, Lightning Rod's enterprise platform helps your team build one.

We work with teams to:

- **Generate** labeled forecasting datasets from your own sources—news, documents, and custom data—through a configurable pipeline, with no manual question writing or labeling.
- **Fine-tune** specialized models on those datasets.
- **Evaluate** performance against held-out test sets.
- **Serve** the resulting models through the same `lr.predict()` and OpenAI-compatible API as Foresight.

[**Book a call →**](https://calendly.com/d/ctq4-7gd-nyq/lightning-rod-demo) to talk through your use case.

See the [Platform Overview](platform/overview.md) to get started.

## Research

Lightning Rod is based on our research: [Future-as-Label: Scalable Supervision from Real-World Outcomes](https://arxiv.org/abs/2601.06336). We use this approach to generate the [Future-as-Label training dataset](https://huggingface.co/datasets/LightningRodLabs/future-as-label-paper-training-dataset) for our paper.
