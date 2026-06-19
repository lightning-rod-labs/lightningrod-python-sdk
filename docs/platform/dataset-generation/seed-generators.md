---
icon: seedling
---

# Seed Generators

Seed generators produce the raw data (seeds) that feeds into question generation - news articles, GDELT results, or chunks from your documents. They are the first stage of the pipeline; choose based on where your source data lives.

## NewsSeedGenerator

Fetches news articles from Google News search.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `start_date` | datetime | Yes | — | Start date for seed search |
| `end_date` | datetime | Yes | — | End date for seed search |
| `search_query` | str or list[str] | Yes | — | Search query. Multiple queries run separate searches |
| `interval_duration_days` | int | No | 7 | Duration of each interval in days |
| `articles_per_search` | int | No | 10 | Articles per search (max 100) |
| `filter_criteria` | FilterCriteria or list | No | — | Optional LLM-based filtering before scraping |
| `source_domain` | str or list[str] | No | — | Optional URL source (e.g. `https://reuters.com/business`) |

```python
NewsSeedGenerator(
    start_date=datetime(2025, 1, 1),
    end_date=datetime(2025, 3, 1),
    search_query=["Trump", "Fed rates"],
    articles_per_search=20,
)
```

## GdeltSeedGenerator

Fetches articles from the GDELT global news database via BigQuery.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `start_date` | datetime | Yes | — | Start date for seed search |
| `end_date` | datetime | Yes | — | End date for seed search |
| `interval_duration_days` | int | No | 7 | Duration of each interval in days |
| `articles_per_interval` | int | No | 1000 | Articles to fetch per interval from BigQuery |

```python
GdeltSeedGenerator(
    start_date=datetime(2025, 1, 1),
    end_date=datetime(2025, 2, 1),
    articles_per_interval=500,
)
```

## BigQuerySeedGenerator

Runs a BigQuery SQL query and converts results into seeds. Use when your source data lives in BigQuery.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `query` | str | Yes | — | BigQuery SQL to execute |
| `seed_text_column` | str | No | `"text"` | Column mapped to seed text |
| `date_column` | str | No | — | Column mapped to seed creation date |
| `max_rows` | int | No | 10000 | Total rows to fetch across all batches |

```python
from lightningrod import BigQuerySeedGenerator

seed_generator = BigQuerySeedGenerator(
    query="""
        SELECT CONCAT('Title: ', title, '\\n\\nContent: ', content) AS text,
               timestamp AS created_at
        FROM `some_public_dataset.table`
        WHERE created_at >= '2025-01-01'
        ORDER BY created_at DESC
    """,
    seed_text_column="text",
    date_column="created_at",
    max_rows=1000,
)
```

## FileSetSeedGenerator

Chunks documents from an uploaded file set. Use when you have PDFs, text files, or other documents.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `file_set_id` | str | Yes | — | FileSet ID to read from |
| `chunk_size` | int | No | 4000 | Characters per chunk |
| `chunk_overlap` | int | No | 200 | Overlapping characters between chunks |
| `metadata_filters` | list[str] | No | — | Metadata filters (e.g. `["ticker='AAL'"]`). Files matching ANY filter are included |

```python
FileSetSeedGenerator(
    file_set_id="your-file-set-id",
    chunk_size=4000,
    chunk_overlap=200,
)
```

## FileSetQuerySeedGenerator

Runs RAG-style queries against a file set. Produces seeds from retrieved chunks instead of full chunks.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `file_set_id` | str | Yes | — | FileSet ID to query |
| `prompts` | list[str] | Yes | — | Queries to run against the file set |
| `metadata_filters` | list[str] | No | — | Optional metadata filters |

```python
FileSetQuerySeedGenerator(
    file_set_id="your-file-set-id",
    prompts=[
        "What are the key risks mentioned in the 10-K?",
        "What growth metrics does the company report?",
    ],
)
```

## CsvSeedGenerator

Generates seeds from a CSV file uploaded via `lr.files.upload()`. Each row becomes a seed. Use when your source data is a spreadsheet or flat CSV.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `file_id` | `str \| list[str]` | Yes | — | OrgFile ID(s) from `lr.files.upload()` response |
| `seed_text_column` | `str \| None` | No | None | Column name for seed text; if None, serializes entire row as JSON |
| `label_column` | `str \| None` | No | None | Column with pre-existing labels (populates `Sample.label`) |
| `date_column` | `str \| None` | No | None | Column name for seed creation date |

```python
from lightningrod import CsvSeedGenerator

# Upload your CSV first
upload = lr.files.upload("data/my_data.csv")

seed_generator = CsvSeedGenerator(
    file_id=upload.id,
    seed_text_column="text",
    date_column="date",
)
```

## TopicTreeSeedGenerator

Generates diverse seeds by recursively decomposing broad topics into specific subtopics. An LLM breaks each root topic into `tree_degree` subtopics, then repeats `tree_depth` levels deep. The leaf paths become seeds for downstream transforms. Produces `tree_degree^tree_depth` seeds per root topic.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `topic` | `str \| list[str]` | Yes | — | Root topic(s) to recursively decompose |
| `tree_depth` | int | No | 2 | Levels of recursive expansion |
| `tree_degree` | int | No | 5 | Subtopics generated per node |
| `model_name` | str | No | `google/gemini-3-flash-preview` | LLM for subtopic generation |
| `model_system_prompt` | `str \| None` | No | None | Optional system prompt for the LLM |

```python
from lightningrod import TopicTreeSeedGenerator

# Produces 4^2 = 16 specific seeds branching from "AI Regulation"
seed_generator = TopicTreeSeedGenerator(
    topic="AI Regulation",
    tree_depth=2,
    tree_degree=4,
)
# e.g. "AI Regulation → Healthcare → FDA approval of diagnostic algorithms"

# Multiple root topics
seed_generator = TopicTreeSeedGenerator(
    topic=["AI Regulation", "Climate Policy", "Monetary Policy"],
    tree_depth=2,
    tree_degree=5,
)
# Produces 3 × 5^2 = 75 seeds
```

## Using with QuestionPipeline

Pass any seed generator to `QuestionPipeline.seed_generator`:

```python
pipeline = QuestionPipeline(
    seed_generator=NewsSeedGenerator(...),
    question_generator=ForwardLookingQuestionGenerator(...),
    labeler=WebSearchLabeler(...),
)
```

## Custom Input Seeds

To use your own samples instead of a seed generator, create a dataset with `lr.datasets.create_from_samples()` and pass it as `input_dataset` to `lr.transforms.run()`. The pipeline will skip seed generation and use your samples as input.
