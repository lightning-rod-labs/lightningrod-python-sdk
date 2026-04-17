---
icon: folder-open
---

# Filesets

A **FileSet** is a collection of documents with optional metadata that you can use as a data source for question generation or labeling. Use filesets when you have PDFs, text files, or other documents (e.g. quarterly reports, 10-Ks, internal memos) that you want to chunk, query, or use for context and labeling.

## Creating a FileSet

Create a fileset with `lr.filesets.create()`. Optionally define a metadata schema so you can filter and organize documents by fields like `ticker`, `quarter`, or `document_type`.

```python
from lightningrod import (
    FileSetMetadataSchemaInput,
    MetadataFieldDefinitionInput,
    MetadataFieldType,
)

schema = FileSetMetadataSchemaInput(fields=[
    MetadataFieldDefinitionInput(
        name="ticker",
        field_type=MetadataFieldType.STRING,
        required=True,
        description="Company ticker symbol",
    ),
    MetadataFieldDefinitionInput(
        name="quarter",
        field_type=MetadataFieldType.STRING,
        required=True,
        description="Fiscal quarter (e.g. Q1 2024)",
    ),
])

fileset = lr.filesets.create(
    name="Quarterly Reports",
    description="Company quarterly investor reports.",
    metadata_schema=schema,
)
```

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `name` | str | Yes | FileSet name |
| `description` | str | No | Optional description |
| `metadata_schema` | FileSetMetadataSchemaInput | No | Schema for file metadata fields |
| `rag_enabled` | bool | No (default `True`) | Enable RAG indexing for this FileSet; set to `False` for document-only workflows |

**MetadataFieldDefinitionInput** fields: `name`, `field_type` (`MetadataFieldType.STRING` or `MetadataFieldType.NUMBER`), `required`, `description`, `extraction_hint`.

## Uploading Files

The SDK provides high-level methods that handle all upload complexity:

### upload_files() — Upload a list of files

```python
from datetime import datetime

# Simple upload without metadata
result = lr.filesets.upload_files(fileset.id, ["doc1.pdf", "doc2.pdf"])

# Upload with metadata
result = lr.filesets.upload_files(
    fileset.id,
    ["report_q1.pdf", "report_q2.pdf"],
    metadata={
        "report_q1.pdf": {"ticker": "AAPL", "quarter": "Q1 2024", "file_date": datetime(2024, 3, 31)},
        "report_q2.pdf": {"ticker": "AAPL", "quarter": "Q2 2024", "file_date": datetime(2024, 6, 30)},
    }
)

print(f"Uploaded {result.succeeded} files, {result.failed} failed")
```

### upload_directory() — Upload all files from a directory

```python
# Upload all PDFs from a directory
result = lr.filesets.upload_directory(
    fileset.id,
    "/path/to/reports",
    pattern="*.pdf"
)

# Upload with metadata derived from filenames
def get_metadata(path):
    # e.g., "AAPL_Q1_2024.pdf" -> {"ticker": "AAPL", "quarter": "Q1 2024"}
    parts = path.stem.split("_")
    return {"ticker": parts[0], "quarter": f"{parts[1]} {parts[2]}"}

result = lr.filesets.upload_directory(
    fileset.id,
    "/path/to/reports",
    pattern="*.pdf",
    metadata_fn=get_metadata
)
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `file_set_id` | str | — | FileSet ID |
| `file_paths` / `directory` | list or str | — | Files to upload |
| `metadata` / `metadata_fn` | dict or callable | None | File metadata |
| `pattern` | str | "*" | Glob pattern (for upload_directory) |
| `max_workers` | int | 10 | Parallel upload threads |
| `use_transfer_manager` | bool | `True` | Use GCS Transfer Manager when available for large uploads |
| `show_progress` | bool | `False` | Display upload progress; requires `google-cloud-storage` |

The vector index is built automatically when the FileSet is first used in a pipeline.

## Using FileSets in Pipelines

Use the FileSet with:

- **FileSetSeedGenerator** — chunks documents into seeds (see [Seed Generators](seed-generators.md))
- **QdrantContextGenerator** — retrieves context from the FileSet during question generation (see [Labeling and Context](labeling-and-context.md))
- **QdrantRAGLabeler** — resolves questions by searching the FileSet for answers (see [Labeling and Context](labeling-and-context.md))

For document-level transforms:
- **FileSetDocumentContextGenerator** — adds full document text as context
- **FileSetDocumentLabeler** — extracts labels from full documents

See the [Custom Filesets examples](https://colab.research.google.com/github/lightning-rod-labs/lightningrod-python-sdk/blob/main/notebooks/custom_filesets/01_create_fileset.ipynb) for a full workflow.
