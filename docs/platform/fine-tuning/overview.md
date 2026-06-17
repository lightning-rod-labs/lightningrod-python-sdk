---
icon: graduation-cap
description: Fine-tune LLMs on your Lightning Rod datasets with LoRA, then evaluate and serve them.
---

# Fine-tuning Overview

Fine-tune LLMs on your Lightning Rod datasets. The training API supports LoRA fine-tuning with configurable base models, training steps, batch size, and rank.

## Workflow

1. **Generate Dataset** — Use the dataset generation pipeline to create labeled forecasting samples
2. **Prepare Data** — Run `filter_and_split()` to filter, deduplicate, and split into train/test datasets
3. **Configure Training** — Set base model, training steps, and optional LoRA parameters
4. **Train** — Submit a training job and monitor progress
5. **Evaluation** — Run evals against your test dataset
6. **Inference** — Use the trained model via `lr.predict()` or the OpenAI-compatible API

## Key Capabilities

- LoRA fine-tuning with configurable rank and batch size
- Configurable base models (e.g. Qwen, Llama)
- Cost estimation before running
- Live progress monitoring in notebooks
- OpenAI-compatible inference with your trained model
- Built-in evals against test datasets

## Next Steps

- [Data Preparation](data-preparation.md) — Use `filter_and_split()` to get training-ready datasets
- [Training](training.md) — Configure and run training jobs
- [Evaluation](evaluation.md) — Evaluate your trained model
- [Inference](inference.md) — Use your trained model for predictions
