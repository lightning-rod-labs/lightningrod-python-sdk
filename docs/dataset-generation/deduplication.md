---
icon: clone
---

# Deduplication

Deduplication removes near-duplicate questions from your pipeline. It runs after question generation and before labeling, comparing samples across configurable fields using exact or fuzzy matching.

## KeyDeduplication

Configures which fields to compare and how strictly to match. When two samples match on **all** configured keys, the duplicate is removed.

| Parameter | Type                  | Required | Default                                          | Description                      |
| --------- | --------------------- | -------- | ------------------------------------------------ | -------------------------------- |
| `keys`    | `list[KeyMatchConfig]` | No       | `question_text` (0.9 similarity) + `date_close` (exact) | Per-key match configuration |

When `keys` is omitted, the server defaults to fuzzy matching on `question_text` (90% similarity threshold) and exact matching on `date_close`.

### KeyMatchConfig

Defines how a single field is compared between samples.

| Parameter              | Type           | Required | Default | Description                                                                                                 |
| ---------------------- | -------------- | -------- | ------- | ----------------------------------------------------------------------------------------------------------- |
| `field`                | str            | Yes      | —       | Field to match on (see available fields below)                                                              |
| `similarity_threshold` | float or None  | No       | —       | Fuzzy matching threshold (0.0–1.0, where 1.0 is identical). Omit or set to `None` for exact matching only.  |

**Available fields:** `question_text`, `seed_text`, `seed_url`, `date_close`, `event_date`, `prediction_date`, `resolution_criteria`, `resolution_date`, `label`

## Usage

Enable deduplication with default settings (fuzzy match on `question_text` + exact match on `date_close`):

```python
from lightningrod._generated.models import KeyDeduplication

pipeline = lr.QuestionPipeline(
    seed_generator=...,
    question_generator=...,
    labeler=...,
    deduplication=KeyDeduplication(),
)
```

Customize which fields are compared and their thresholds:

```python
from lightningrod._generated.models import KeyDeduplication, KeyMatchConfig

pipeline = lr.QuestionPipeline(
    seed_generator=...,
    question_generator=...,
    labeler=...,
    deduplication=KeyDeduplication(
        keys=[
            KeyMatchConfig(field="question_text", similarity_threshold=0.85), # fuzzy match
            KeyMatchConfig(field="date_close"),       # exact match
            KeyMatchConfig(field="seed_url"),          # exact match
        ]
    ),
)
```

To disable deduplication explicitly:

```python
pipeline = lr.QuestionPipeline(
    ...,
    deduplication=None,
)
```

> **Note:** `KeyDeduplication` and `KeyMatchConfig` are not yet available in the top-level `lightningrod` package. Import from `lightningrod._generated.models`.
