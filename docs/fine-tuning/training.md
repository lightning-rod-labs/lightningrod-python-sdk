---
icon: gears
---

# Training

Create and manage LoRA fine-tuning jobs on Lightning Rod datasets. Access via `lr.training` on your `LightningRod` client.

Training jobs use one of two configuration types: **GRPO** (reinforcement-style training for forecasting) or **SFT** (supervised fine-tuning on labeled question–answer pairs). Pass the matching SDK config class; the API stores a discriminated config on the job. When you read `job.config` from `get` or `list`, it is a generated `GRPOTrainingConfig` or `SFTTrainingConfig` from the API (not the thin SDK wrapper classes).

## GRPOTrainingConfig

Use for forward-looking / GRPO training. Configure base model, training steps, and optional LoRA parameters:

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `base_model_id` | str | — | HuggingFace model ID for LoRA base (e.g. `"Qwen/Qwen3-8B"`) |
| `training_steps` | int | — | Number of training loop iterations |
| `batch_size` | int \| None | None | Rows per batch; used to slice train_rows each step |
| `lora_rank` | int \| None | None | LoRA adapter rank |
| `learning_rate` | float \| None | None | Step size for weight updates; higher values learn faster but may overshoot |
| `adam_beta1` | float \| None | None | Exponential decay rate for first-moment estimates (moving average of gradients) |
| `adam_beta2` | float \| None | None | Exponential decay rate for second-moment estimates (moving average of squared gradients) |
| `num_rollouts` | int \| None | None | Samples per prompt for GRPO |
| `max_response_length` | int \| None | None | Max tokens for sampling |
| `start_idx` | int \| None | None | Row index to skip at start; train_rows = train_rows[start_idx:] |
| `save_frequency` | int \| None | None | Checkpoint frequency in training steps (server default if omitted) |

## SFTTrainingConfig

Use for supervised fine-tuning. Same core hyperparameters as GRPO where applicable, plus SFT-specific fields. **No** `num_rollouts` or `max_response_length`.

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `base_model_id` | str | — | HuggingFace model ID for LoRA base |
| `training_steps` | int | — | Number of training loop iterations |
| `batch_size` | int \| None | None | Rows per batch |
| `lora_rank` | int \| None | None | LoRA adapter rank |
| `learning_rate` | float \| None | None | Step size for weight updates |
| `adam_beta1` | float \| None | None | Adam β₁ |
| `adam_beta2` | float \| None | None | Adam β₂ |
| `start_idx` | int \| None | None | Row index to skip at start |
| `save_frequency` | int \| None | None | Checkpoint frequency in training steps (server default if omitted) |
| `resume_from` | str \| None | None | Resume from a Tinker checkpoint path |
| `epochs` | int \| None | None | Passes over the training data (server default if omitted) |

## Methods

### estimate_cost

Estimate training cost before running:

```python
from lightningrod.training import GRPOTrainingConfig

config = GRPOTrainingConfig(
    base_model_id="openai/gpt-oss-120b",
    training_steps=50,
)

cost_estimate = lr.training.estimate_cost(config, dataset=train_dataset)
print(f"Estimated cost: ${cost_estimate.total_cost_dollars:.2f}")
print(f"Effective steps: {cost_estimate.effective_steps}")
print(f"Train tokens: {cost_estimate.train_tokens}")
```

For SFT, use `SFTTrainingConfig` the same way.

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

See [notebooks/getting_started/05_grpo_training.ipynb](../../notebooks/getting_started/05_grpo_training.ipynb) for GRPO forecasting workflow and [notebooks/getting_started/06_sft_training.ipynb](../../notebooks/getting_started/06_sft_training.ipynb) for SFT.
