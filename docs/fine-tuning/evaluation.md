---
icon: clipboard-check
---

# Evaluation

Run evals on your trained model against a test dataset. Access via `lr.evals` on your `LightningRod` client.

## EvalModel

Specify each model to evaluate when using [`create`](#create) or [`run`](#run) (you supply the full list). For [`run_from_training_job`](#run_from_training_job), the SDK adds the base and fine-tuned models for you; use `EvalModel` only for [`extra_models`](#run_from_training_job).

| Parameter | Type | Required | Default | Description |
|-----------|------|---------|---------|-------------|
| `model_id` | str | Yes | — | Model ID to evaluate (trained model or any supported model) |
| `label` | `str \| None` | No | None | Human-readable label shown in results display |

```python
from lightningrod import EvalModel

EvalModel(model_id=job.model_id, label="my-fine-tune")
```

## Methods

### create

Create an eval job without waiting. You pass the **complete** list of models to compare:

```python
from lightningrod import EvalModel

eval_job = lr.evals.create(
    models=[EvalModel(model_id=job.model_id, label="my-fine-tune")],
    dataset=test_dataset,
)
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `models` | `list[EvalModel]` | — | Models to evaluate |
| `dataset` | SampleDataset | — | Test dataset |

### run

Create an eval job and poll until completion. In notebooks, shows a live progress display. You pass the **full** `models` list (same idea as [`create`](#create), but waited).

```python
from lightningrod import EvalModel

eval_job = lr.evals.run(
    test_dataset,
    [
        EvalModel(model_id=config.base_model_id, label="Base"),
        EvalModel(model_id=training_job.model_id, label="Fine-tuned"),
    ],
)
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `dataset` | SampleDataset | — | Test dataset (e.g. test split). |
| `models` | `list[EvalModel]` | — | Models to evaluate (complete list). |

### run_from_training_job

Same waiting behavior as [`run`](#run), but builds the model list from your training config and completed job.

The benchmark **always** includes two models, in order:

1. **Base** — `config.base_model_id` (label `"Base"`).
2. **Fine-tuned** — `job.model_id` after training completes (label `"Fine-tuned"`).

You do not pass these explicitly. Use **`extra_models`** only for additional models (e.g. OpenAI baselines).

**SFT:** `run_from_training_job` raises `NotImplementedError` if `config` is `SFTTrainingConfig`, because SFT-specific eval metrics are not implemented yet. Use **GRPO** with `run_from_training_job`, or use [`run`](#run) / [`create`](#create) with your own `EvalModel` list.

```python
from lightningrod import EvalModel

eval_job = lr.evals.run_from_training_job(
    config,
    training_job,
    test_dataset,
    extra_models=[
        EvalModel(model_id="openai/gpt-5.4", label="GPT-5.4"),
    ],
)
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `config` | `GRPOTrainingConfig \| SFTTrainingConfig` | — | Same training config you used with `lr.training.run` (SFT raises until supported). |
| `job` | `TrainingJob` | — | Completed job from `lr.training.run`; must have `model_id` set. |
| `dataset` | SampleDataset | — | Test dataset (e.g. test split). |
| `extra_models` | `list[EvalModel] \| None` | `None` | Optional extra models appended after Base and Fine-tuned. |

### get

Fetch a single eval job by ID:

```python
eval_job = lr.evals.get(eval_id)
```

### list

List eval jobs with pagination:

```python
response = lr.evals.list(page=1, limit=10)
for job in response.jobs:
    print(job.id, job.status)
```

## print\_eval

Pretty-print eval results:

```python
from lightningrod import training

eval_job = lr.evals.run_from_training_job(config, training_job, test_dataset)
training.print_eval(eval_job)
```

## Evaluating Intermediate Checkpoints

`run_from_training_job` always evaluates the **final** `job.model_id` as the fine-tuned slot. To compare checkpoints or choose a different model list, use **`run`** / **`create`** and pass every `EvalModel` yourself:

```python
from lightningrod import EvalModel
from lightningrod.training import print_eval

# After training completes (config is GRPO or SFT)
job = lr.training.run(config, dataset=train_dataset)

checkpoint_model_id = job.model_id_by_step["10"]

eval_job = lr.evals.create(
    models=[
        EvalModel(model_id=checkpoint_model_id, label="step-10"),
        EvalModel(model_id=job.model_id, label="final"),
    ],
    dataset=test_dataset,
)
print_eval(eval_job)
```

## Example

```python
from lightningrod import EvalModel
from lightningrod.training import print_eval

eval_job = lr.evals.create(
    models=[
        EvalModel(model_id=job.model_id, label="fine-tuned"),
        EvalModel(model_id="openai/gpt-4.1", label="baseline"),
    ],
    dataset=test_dataset,
)
print_eval(eval_job)
```

See [notebooks/getting_started/05_grpo_training.ipynb](../../notebooks/getting_started/05_grpo_training.ipynb) for the full GRPO workflow including `evals.run_from_training_job`.
