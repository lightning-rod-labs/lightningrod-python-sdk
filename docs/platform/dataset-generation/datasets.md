---
icon: database
---

# Sample Datasets

Datasets are collections of samples. They are the central data artifact: pipelines produce them as output, and you can pass one as input to run a pipeline, training, or evaluation. The SDK exposes them as `SampleDataset` (named to avoid collision with the `datasets` package).

## Creating a Dataset from Samples

Use `create_from_samples` when you have custom samples (e.g. from your own data) and want to run them through a pipeline or use them for training.

```python
from lightningrod import LightningRod, create_sample

lr = LightningRod(api_key="your-api-key")

samples = [
    create_sample(
        seed_text="Company X announced a new product launch.",
        label="1",
        meta={"label": "Acquired", "date_close": "2025-06-01"},
    ),
    create_sample(
        seed_text="Company Y reported Q4 earnings.",
        label="0",
    ),
]

dataset = lr.datasets.create_from_samples(samples, batch_size=1000)
```

`create_sample(seed_text, label=None, seed_date=None, meta=None)` builds a `Sample` with minimal boilerplate.

## Fetching a Dataset

```python
dataset = lr.datasets.get(dataset_id)
```

## Accessing Samples

```python
samples = dataset.samples()
```

Downloads samples on first call and caches them. Handles pagination automatically.

## Flattening for Analysis

```python
rows = dataset.flattened()
```

Returns a list of flat dicts with `question_text`, `label`, `prompt`, `context`, etc. Suitable for `pd.DataFrame(rows)` or direct iteration.

## Other Methods

- **`valid_count()`** — Counts samples where `is_valid` is `True`. Requires samples to be downloaded first (call `dataset.samples()` before using).
- **`preview_prompts(include_assistant=False, n=3)`** — Previews formatted prompt messages using the dataset's `prompt_template`.
- **`subset(sample_ids)`** — Returns a new `SampleDataset` filtered to the given sample IDs.

## Attributes

- **`prompt_template`** — Optional string for formatting prompts. When set, used by `preview_prompts()` and passed to training/eval API calls.

## Using a Dataset

A `SampleDataset` can be passed into three parts of the system:

### Transform pipeline input

Pass a dataset to skip seed generation and use your own seed samples instead:

```python
input_dataset = lr.datasets.create_from_samples(samples)
dataset = lr.transforms.run(
    pipeline_config,
    input_dataset=input_dataset,
    max_seeds=500,
)
```

See [Dataset Generation Overview](overview.md) for pipeline details.

### Training input

Pass a dataset to train a model:

```python
job = lr.training.run(training_config, dataset=train_dataset)
```

`training_config` is a `GRPOTrainingConfig` or `SFTTrainingConfig` (see [Training](../fine-tuning/training.md)). See [Data Preparation](../fine-tuning/data-preparation.md) for filtering and splitting.

### Eval input

Pass a dataset to evaluate a model:

```python
eval_job = lr.evals.run_from_training_job(training_config, job, test_dataset)
```

See [Evaluation](../fine-tuning/evaluation.md) for eval options.

## Linting

Validate dataset quality before training with the dataset linter. Access via `lr.datasets.linter`.

### list_rules

List all available lint rules:

```python
rules = lr.datasets.linter.list_rules()
```

### run

Run the linter on a dataset. Polls until completion and shows live progress in notebooks:

```python
result = lr.datasets.linter.run(dataset.id)
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `dataset_id` | `str` | — | Dataset ID to lint |
| `rules` | `list[str] \| None` | `None` | Specific rule IDs to run (all rules if `None`) |
| `random_sample_size` | `int \| None` | `None` | Lint a random subset of samples instead of the full dataset |
| `poll_interval` | `float` | `15` | Seconds between status polls |

### get_run

Fetch a previous linter run by ID:

```python
run = lr.datasets.linter.get_run(run_id)
```

### list_runs

List linter runs for a dataset:

```python
runs = lr.datasets.linter.list_runs(dataset.id, limit=20)
```

### Display helpers

Pretty-print linter results with the top-level display functions:

```python
from lightningrod import display_lint_overview, display_lint_detailed

display_lint_overview(result)     # summary table
display_lint_detailed(result)     # full issue breakdown with sample IDs
```

### Extracting affected samples

Get the sample IDs flagged by the linter to filter or inspect them:

```python
from lightningrod import get_lint_affected_sample_ids

bad_ids = get_lint_affected_sample_ids(result)
clean_dataset = dataset.subset([s.id for s in dataset.samples() if s.id not in set(bad_ids)])
```

`get_lint_affected_sample_ids` accepts an optional `severities` parameter (defaults to `WARNING` and `ERROR`).
