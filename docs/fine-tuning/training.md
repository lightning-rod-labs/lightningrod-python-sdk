---
icon: gears
---

# Training

Create and manage LoRA fine-tuning jobs on Lightning Rod datasets. Access via `lr.training` on your `LightningRod` client.

## TrainingConfig

Configure base model, training steps, and optional LoRA parameters:

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `base_model` | str | — | HuggingFace model ID for LoRA base (e.g. `"Qwen/Qwen3-8B"`) |
| `training_steps` | int | — | Number of training loop iterations |
| `batch_size` | int \| None | None | Rows per batch; used to slice train_rows each step |
| `lora_rank` | int \| None | None | LoRA adapter rank |
| `learning_rate` | float \| None | None | Step size for weight updates; higher values learn faster but may overshoot |
| `adam_beta1` | float \| None | None | Exponential decay rate for first-moment estimates (moving average of gradients) |
| `adam_beta2` | float \| None | None | Exponential decay rate for second-moment estimates (moving average of squared gradients) |
| `num_rollouts` | int \| None | None | Samples per prompt for GRPO |
| `max_response_length` | int \| None | None | Max tokens for sampling |
| `start_idx` | int \| None | None | Row index to skip at start; train_rows = train_rows[start_idx:] |

## Methods

### estimate_cost

Estimate training cost before running:

```python
from lightningrod.training import TrainingConfig

config = TrainingConfig(
    base_model="Qwen/Qwen3-4B-Instruct-2507",
    training_steps=50,
)

cost_estimate = lr.training.estimate_cost(config, dataset=train_dataset)
print(f"Estimated cost: ${cost_estimate.total_cost_dollars:.2f}")
print(f"Effective steps: {cost_estimate.effective_steps}")
print(f"Train tokens: {cost_estimate.train_tokens}")
```

Returns `EstimateTrainingCostResponse` with `total_cost_dollars`, `prefill_tokens`, `sample_tokens`, `train_tokens`, `effective_steps`, `notes`, and optional `warning_message`.

### create

Create a training job without waiting:

```python
job = lr.training.create(config, dataset=train_dataset, name="My fine-tune")
print(job.id, job.status)
```

### run

Create a job and poll until completion. In notebooks, shows a live progress display. Outside notebooks, raises on failure:

```python
job = lr.training.run(
    config,
    dataset=train_dataset,
    name="Forecasting fine-tune",
    poll_interval=15.0,
)
print(f"Model ID: {job.model_id}")
```

### get

Fetch a single job by ID:

```python
job = lr.training.get(job_id)
```

### list

List training jobs with pagination and optional status filter:

```python
response = lr.training.list(page=1, limit=10, status="completed")
for job in response.jobs:
    print(job.id, job.model_id)
```

## Example

See [notebooks/getting_started/05_fine_tuning.ipynb](../../notebooks/getting_started/05_fine_tuning.ipynb) for the full workflow.
