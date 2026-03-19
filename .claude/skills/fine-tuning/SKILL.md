---
name: fine-tuning
description: Fine-tuning and evaluation patterns for Lightningrod. Use when running training jobs, estimating training cost, or evaluating model performance.
---

# Fine-Tuning

## TrainingConfig

```python
from lightningrod import TrainingConfig

config = TrainingConfig(
    base_model="Qwen/Qwen3-4B-Instruct",  # see available models below
    training_steps=50,
)
```

Available base models: 
- `Qwen/Qwen3-4B-Instruct` 
- `Qwen/Qwen3-8B-Instruct`
- `openai/gpt-oss-120b`
- `openai/gpt-oss-20b`

## Always estimate cost first

```python
cost = lr.training.estimate_cost(config, dataset=train_ds)
print(cost)
```

## Run training

```python
job = lr.training.run(config, dataset=train_ds, name="my-model-v1")
# Blocks until complete. job.model_id is available when done.
print(job.model_id)
```

## Run evaluation

```python
eval_job = lr.evals.run(
    model_id=job.model_id,
    dataset=test_ds,
    benchmark_model_id="openai/gpt-4o",  # comparison baseline
)
```

## Iteration loop

If eval scores are poor, identify the root cause before re-running:

| Symptom | Likely cause | Action |
|---------|-------------|--------|
| Score barely above baseline | Not enough training data | Go back to dataset-generator: increase `max_questions`, broaden seed sources |
| Score worse than baseline | Data quality issue | Go back to dataset-generator: tighten question generator instructions, check `prepare_for_training` stats |
| Train/test distribution mismatch | Temporal split too aggressive | Adjust `SplitParams.test_start` or `test_size` |
| Overfitting (train >> test) | Too many steps or too little data | Reduce `training_steps` or get more data |

Always pass specific guidance when flagging back to the dataset-generator (e.g. "need more temporal diversity across 6 months", "too few test samples — only 12 after split").

## Reference notebooks

- `notebooks/getting_started/05_fine_tuning.ipynb`
- `notebooks/fine_tuning/02_trump_forecasting.ipynb` — full end-to-end example
- `notebooks/evaluation/` — evaluation patterns
