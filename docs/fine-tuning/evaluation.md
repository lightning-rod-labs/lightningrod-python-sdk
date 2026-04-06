---
icon: clipboard-check
---

# Evaluation

Run evals on your trained model against a test dataset. Access via `lr.evals` on your `LightningRod` client.

## EvalModel

Specify each model to evaluate in an eval job:

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

Create an eval job without waiting:

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

Create an eval job and poll until completion. In notebooks, shows a live progress display:

```python
eval_job = lr.evals.run(
    models=[
        EvalModel(model_id=training_job.config.base_model_id, label="Base"),
        EvalModel(model_id=training_job.model_id, label="Fine-tuned"),
        EvalModel(model_id="openai/gpt-5.4", label="GPT-5.4"),
    ],
    dataset=test_dataset,
)
```

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
from lightningrod.training import print_eval

eval_job = lr.evals.run(
    models=[EvalModel(model_id=job.model_id)],
    dataset=test_dataset,
)
print_eval(eval_job)
```

## Evaluating Intermediate Checkpoints

Access model IDs for intermediate training checkpoints via `TrainingJob.model_id_by_step`, then evaluate them individually or compare across steps:

```python
# After training completes
job = lr.training.run(config, dataset=train_dataset)

# Evaluate a specific checkpoint (e.g. step 10)
checkpoint_model_id = job.model_id_by_step["10"]

eval_job = lr.evals.run(
    models=[
        EvalModel(model_id=checkpoint_model_id, label="step-500"),
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

eval_job = lr.evals.run(
    models=[
        EvalModel(model_id=job.model_id, label="fine-tuned"),
        EvalModel(model_id="openai/gpt-4.1", label="baseline"),
    ],
    dataset=test_dataset,
)
print_eval(eval_job)
```

See [notebooks/getting_started/05_fine_tuning.ipynb](../../notebooks/getting_started/05_fine_tuning.ipynb) for the full workflow.
