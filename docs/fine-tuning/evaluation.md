---
icon: clipboard-check
---

# Evaluation

Run evals on your trained model against a test dataset. Access via `lr.evals` on your `LightningRod` client.

## Methods

### create

Create an eval job without waiting:

```python
eval_job = lr.evals.create(
    model_id=job.model_id,
    dataset=test_dataset,
    benchmark_model_id="openai/gpt-5.2",
    temperature=0.0,
)
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `model_id` | str | — | Your trained model ID |
| `dataset` | SampleDataset | — | Test dataset |
| `benchmark_model_id` | str \| None | None | Optional model to compare against |
| `temperature` | float | 0.0 | Sampling temperature |

### run

Create an eval job and poll until completion. In notebooks, shows a live progress display:

```python
eval_job = lr.evals.run(
    model_id=job.model_id,
    dataset=test_dataset,
    benchmark_model_id="openai/gpt-5.2",
    temperature=0.0,
    poll_interval=15.0,
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

## print_eval

Pretty-print eval results:

```python
from lightningrod.training import print_eval

eval_job = lr.evals.run(model_id=job.model_id, dataset=test_dataset)
print_eval(eval_job)
```

Or with a previously fetched job:

```python
print_eval(lr.evals.get(eval_job.id))
```

## Example

```python
eval_job = lr.evals.run(
    model_id=job.model_id,
    dataset=test_dataset,
    benchmark_model_id="openai/gpt-5.2",
)

from lightningrod.training import print_eval
print_eval(eval_job)
```

See [notebooks/getting_started/05_fine_tuning.ipynb](../../notebooks/getting_started/05_fine_tuning.ipynb) for the full workflow.
