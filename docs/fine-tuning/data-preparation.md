---
icon: filter
---

# Data Preparation

`filter_and_split` is the main entry point for preparing Lightning Rod datasets for model training. It filters invalid samples, deduplicates, splits into train/test, and returns `SampleDataset` objects ready for `lr.training.run(...)` (with a `GRPOTrainingConfig` or `SFTTrainingConfig`) or `lr.evals.run(config, job, dataset=...)` / `lr.evals.create(...)`.

## What It Does

1. **Filter** — Drops invalid samples, optionally by resolution horizon and context presence
2. **Deduplicate** — Removes duplicates by (question_text, resolution_date) or custom key
3. **Split** — Splits into train/test by temporal order or random shuffle

## Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `dataset` | SampleDataset | — | Dataset to prepare (required) |
| `test_size` | float | 0.2 | Fraction of samples for test set (0.0–1.0) |
| `split_strategy` | str | `"temporal"` | `"temporal"` (chronological) or `"random"` |
| `test_start` | str \| None | None | ISO date for temporal split cutoff; alternative to `test_size` for exact date control |
| `drop_missing_context` | bool | False | Exclude samples with no rendered context |
| `days_to_resolution_range` | (min, max) \| None | None | Filter by resolution horizon. E.g. `(90, None)` keeps ≥ 90 days; `(14, 60)` keeps 14–60 days |
| `random_state` | int | 196 | Seed for reproducible random splits |
| `filter_leaky_train` | bool | True | Remove train samples whose `date_close` or `resolution_date` falls within the test period |
| `deduplicate_key_fn` | Callable \| None | None | Custom dedup key; default is `(question_text, resolution_date)` |
| `verbose` | bool | False | Print filter/dedup/split stats |

## Guidelines

- **Prefer `"temporal"` split for forecasting** — It reflects real-world deployment where the model never sees future questions during training.
- **Use `test_start` vs `test_size`** — Use `test_start` when you want the test set to cover a specific time window (e.g. a recent month); use `test_size` when you just want a fixed proportion.
- **Use `days_to_resolution_range` to control difficulty** — Short horizons (e.g. `(7, 30)`) are easier; longer horizons (e.g. `(90, None)`) test genuine uncertainty.
- **Set `drop_missing_context=True` only if your dataset was generated with `context_generators`** (e.g. `NewsContextGenerator`) in `QuestionPipeline`. Context is absent by default, so enabling this on a dataset without context will drop all samples. See [Labeling and Context](../dataset-generation/labeling-and-context.md).
- **Keep `filter_leaky_train=True`** (default) unless you intentionally want to test without temporal leak protection.
- **Use `verbose=True` on first runs** to understand how many samples are dropped at each stage and why.

## Example

```python
from lightningrod.training import filter_and_split

train_dataset, test_dataset = filter_and_split(
    dataset,
    test_size=0.2,
    days_to_resolution_range=(90, None),
    verbose=True,
)
```

## Output

Returns `(train_dataset, test_dataset)` — two `SampleDataset` objects ready for `lr.training.run(training_config, dataset=train_dataset)` (GRPO or SFT config) and evaluation on `test_dataset` via `lr.evals.run(training_config, job, test_dataset)` or `lr.evals.create(...)`.
