---
name: seeds-sourcing
description: Seed sourcing patterns for Lightningrod. Use when choosing between news, GDELT, or FileSet seed generators.
---

# Seeds Sourcing

## Built-in seed generators

**News (`NewsSeedGenerator`):** News articles from a date range and search query. Best for forecasting, current events, time-sensitive topics.

```python
from lightningrod import NewsSeedGenerator
from datetime import datetime

seed_generator = NewsSeedGenerator(
    start_date=datetime(2025, 1, 1),
    end_date=datetime(2025, 2, 1),
    search_query="technology",  # or list: ["tech", "AI"]
    interval_duration_days=7,
    articles_per_search=5,
)
```

**GDELT (`GdeltSeedGenerator`):** GDELT global event database. Best for event-based forecasting and geopolitical topics.

```python
from lightningrod import GdeltSeedGenerator

seed_generator = GdeltSeedGenerator(
    start_date=datetime(2025, 1, 1),
    end_date=datetime(2025, 2, 1),
    interval_duration_days=7,
    articles_per_interval=10,
)
```

**FileSet (`FileSetSeedGenerator`, `FileSetQuerySeedGenerator`):** Documents uploaded to Lightningrod. Use when the user has PDFs, text files, or CSVs already in a FileSet.

```python
from lightningrod import FileSetSeedGenerator

seed_generator = FileSetSeedGenerator(file_set_id="fs_abc123")
```

## When to use which

| Source | Use when |
|--------|----------|
| News | Forecasting from current events, news-driven questions |
| GDELT | Event-centric, geopolitical forecasting |
| FileSet | User has documents in Lightningrod; want to query/chunk them |

## Iteration constraints

For demo/iteration: short date ranges (7 days not 90), narrow search queries, few files. Scale up only when user confirms output looks right.
