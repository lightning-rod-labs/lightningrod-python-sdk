---
name: seeds-sourcing
description: Seed sourcing patterns for Lightningrod. Use when choosing between news, GDELT, FileSet, or preprocessing for seed generation.
---

# Seeds Sourcing

## Built-in seed generators

**News (NewsSeedGenerator):** News articles from a date range and search query. Best for forecasting, current events, time-sensitive topics.

```python
NewsSeedGenerator(
    start_date=datetime(2025, 1, 1),
    end_date=datetime(2025, 2, 1),
    search_query="technology"  # or list: ["tech", "AI"]
)
```

**GDELT (GdeltSeedGenerator):** GDELT event data. Best for event-based forecasting, geopolitical topics.

**FileSet (FileSetSeedGenerator, FileSetQuerySeedGenerator):** Documents uploaded to Lightningrod. Use when user has PDFs, text files, CSVs. Create via lr.filesets, then reference by ID.

**Preprocessing (files_to_samples):** Local files chunked into samples, then lr.datasets.create_from_samples(). Use for user's own documents without FileSet.

## When to use which

| Source | Use when |
|--------|----------|
| News | Forecasting from current events, news-driven questions |
| GDELT | Event-centric, geopolitical forecasting |
| FileSet | User has documents to upload; want to query/filter |
| files_to_samples | User has local files; simple chunk-and-upload |

## Iteration constraints

For demo/iteration: short date ranges (7 days not 90), narrow search queries, few files. Scale up only when user confirms.
