---
icon: building
description: The Lightning Rod platform for enterprises — generate labeled forecasting datasets from your own sources and fine-tune custom models.
---

# Platform (Enterprise)

The Lightning Rod platform turns your own data into a forecasting model specialized to your domain. Use it when an off-the-shelf [Foresight](../forecasting/reference.md) forecast isn't specialized enough—you have proprietary sources, a niche domain, or accuracy targets that warrant a custom model.

## When you need it

| You want… | Use |
|-----------|-----|
| A probability for a question, right now | **[Forecasting](../forecasting/reference.md)** — `foresight-v4`, self-serve |
| A model specialized to your domain and data | **Platform** (this section) |

## The workflow

1. **[Dataset Generation](dataset-generation/overview.md)** — Turn news, documents, and custom sources into labeled forecasting samples through a configurable pipeline. No manual question writing or labeling.
2. **[Fine-tuning](fine-tuning/overview.md)** — Train a model on your dataset, evaluate it against a held-out test set, and serve it.
3. **Forecast** — Your fine-tuned model is served through the same [`lr.predict()`](../forecasting/reference.md) and OpenAI-compatible API as Foresight.

## Get started

* [Dataset Generation Overview](dataset-generation/overview.md) — pipelines, seed generators, and question types
* [Fine-tuning Overview](fine-tuning/overview.md) — data preparation, training, evaluation, and inference
* [Examples](../examples.md) — end-to-end notebooks from seeds to fine-tuned models
