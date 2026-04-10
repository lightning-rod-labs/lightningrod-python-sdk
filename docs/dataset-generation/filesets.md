---
icon: folder-open
---

# Filesets

A **FileSet** is a collection of documents with optional metadata that you can use as a data source for question generation or labeling. Use filesets when you have PDFs, text files, or other documents (e.g. quarterly reports, 10-Ks, internal memos) that you want to chunk, query, or use for context and labeling.

## Creating a FileSet

Create a fileset with `lr.filesets.create()`. Optionally define a metadata schema so you can filter and organize documents by fields like `ticker`, `quarter`, or `document_type`.

```python
from lightningrod._generated.models import (
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

Upload files with `lr.filesets.files.upload()`. Each file can have metadata and a `file_date` for temporal filtering.

```python
lr.filesets.files.upload(
    file_set_id=fileset.id,
    file_path="/path/to/document.pdf",
    metadata={"ticker": "AAPL", "quarter": "Q1 2024"},
    file_date=datetime(2024, 3, 31),
)
```

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `file_set_id` | str | Yes | FileSet ID |
| `file_path` | str | Yes | Path to the file |
| `metadata` | dict | No | Metadata dict (must match schema if defined) |
| `file_date` | datetime | No | Document date for temporal filtering |
| `auto_extract_metadata` | bool | No (default `False`) | Automatically extract metadata fields from the document content using the FileSet's schema |

Files start in `PENDING` status and move to `ACTIVE` after processing (typically 1–2 minutes). Poll `lr.filesets.files.list()` until all files are `ACTIVE` before using the FileSet for generation.

## Adding an Existing File

If you have already uploaded a file via `lr.files.upload()` and want to add it to a FileSet without re-uploading, use `lr.filesets.files.add()`:

```python
lr.filesets.files.add(
    file_set_id=fileset.id,
    file_id="existing-file-id",
    metadata={"ticker": "AAPL", "quarter": "Q1 2024"},
    file_date=datetime(2024, 3, 31),
)
```

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `file_set_id` | str | Yes | FileSet ID |
| `file_id` | str | Yes | ID of a previously uploaded file |
| `metadata` | dict | No | Metadata dict (must match schema if defined) |
| `file_date` | datetime | No | Document date for temporal filtering |
| `auto_extract_metadata` | bool | No (default `False`) | Automatically extract metadata fields from the document content |

## Listing Files

```python
response = lr.filesets.files.list(file_set_id=fileset.id)
for f in response.files:
    print(f"{f.original_file_name}: {f.status} — {f.metadata}")
```

## Using FileSets in Pipelines

Once files are `ACTIVE`, use the FileSet with:

- **FileSetSeedGenerator** — chunks documents into seeds (see [Seed Generators](seed-generators.md))
- **FileSetQuerySeedGenerator** — runs RAG-style queries to produce seeds from retrieved chunks (see [Seed Generators](seed-generators.md))
- **FileSetContextGenerator** — retrieves context from the FileSet during question generation (see [Labeling and Context](labeling-and-context.md))
- **FileSetRAGLabeler** — resolves questions by searching the FileSet for answers (see [Labeling and Context](labeling-and-context.md))

See the [Custom Filesets examples](https://colab.research.google.com/github/lightning-rod-labs/lightningrod-python-sdk/blob/main/notebooks/custom_filesets/01_create_fileset.ipynb) for a full workflow.
