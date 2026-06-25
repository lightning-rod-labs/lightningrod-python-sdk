---
icon: building
description: Generate labeled forecasting datasets from your sources and fine-tune custom models.
---

# Platform (Enterprise)

The Lightning Rod platform turns your data into forecasting datasets and custom models.

## When you need it

| You want… | Use |
|-----------|-----|
| A forecast from a hosted model | **[Forecasting](../forecasting/reference.md)** |
| A model specialized to your domain and data | **Platform** |

## The workflow

1. **[Dataset Generation](dataset-generation/overview.md)** — Turn news, documents, and custom sources into labeled forecasting samples.
2. **[Fine-tuning](fine-tuning/overview.md)** — Train a model on your dataset, evaluate it against a held-out test set, and serve it.
3. **Forecast** — Use the trained model with [`lr.predict()`](../forecasting/reference.md) or the OpenAI-compatible API.

## Get started

* [Dataset Generation Overview](dataset-generation/overview.md) — pipelines, seed generators, and question types
* [Fine-tuning Overview](fine-tuning/overview.md) — data preparation, training, evaluation, and inference
* [Examples](../examples.md) — notebooks from seeds to fine-tuned models
