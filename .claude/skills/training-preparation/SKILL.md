---
name: training-preparation
description: Training data preparation patterns for Lightningrod. Use when running prepare_for_training, configuring FilterParams/DedupParams/SplitParams, or handling validation errors.
---

# Training Preparation

## prepare_for_training

```python
from lightningrod import prepare_for_training, FilterParams, DedupParams, SplitParams

train_ds, test_ds = prepare_for_training(
    dataset,
    filter=FilterParams(
        days_to_resolution_range=(1, 60),  # keep questions resolving within this window
        drop_missing_context=False,
    ),
    dedup=DedupParams(
        key_fn=None,  # default key: (question_text, resolution_date)
    ),
    split=SplitParams(
        strategy="temporal",  # "temporal" or "random"
        test_size=0.2,
        test_start=None,       # explicit cutoff date (optional)
        leakage_keys=None,
        filter_leaky_train=True,
    ),
    verbose=True,
)
```

Returns `(train_SampleDataset, test_SampleDataset)`. In notebooks displays a rich validation table.

## Common FilterParams adjustments

| Problem | Fix |
|---------|-----|
| Too few samples after filter | Widen `days_to_resolution_range`, e.g. `(1, 90)` |
| Questions without context | Set `drop_missing_context=False` or regenerate with context |
| Want only resolved questions | Default behavior — unresolved are filtered automatically |

## Validation errors

`prepare_for_training` raises `ValueError` with actionable tips when the dataset is unhealthy:

- **Too few samples** → re-run transforms with more `max_questions`, or widen filter range
- **High dedup rate** → seeds are too repetitive; use more diverse seed sources or date ranges
- **High invalid rate** → question quality is poor; tighten question generator instructions
- **Temporal leakage** → test questions overlap with train date range; adjust `test_start` or use `strategy="temporal"`

## Iteration loop

```
prepare_for_training fails or produces poor split
  → check error message for specific cause
  → if filter issue: adjust FilterParams and retry
  → if volume issue: go back to dataset-generator, re-run with more max_questions
  → if quality issue: go back to dataset-generator, tighten pipeline instructions
```

## Inspecting the split

```python
import pandas as pd
from lightningrod.training import to_record

pd.DataFrame([to_record(s) for s in train_ds.samples])
```
