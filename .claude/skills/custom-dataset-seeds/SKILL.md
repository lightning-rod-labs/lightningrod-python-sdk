---
name: custom-dataset-seeds
description: Seed generation from user-provided files and custom datasets. Use when converting local files, CSVs, PDFs, or user uploads into Lightningrod seeds.
---

# Custom Dataset Seeds

## Converting files to samples

```python
from lightningrod import preprocessing

# Glob pattern — supports .txt, .md, .pdf, .csv
samples = preprocessing.files_to_samples(
    "data/*.pdf",
    chunk_size=1000,
    chunk_overlap=100,
)

# Single file
samples = preprocessing.file_to_samples("report.pdf")

# CSV with explicit columns
samples = preprocessing.files_to_samples(
    "data.csv",
    csv_text_column="body",
    csv_label_column="outcome",  # optional — embeds label in sample
)

# Raw string chunks
samples = preprocessing.chunks_to_samples(chunks, metadata={"source": "internal"})
```

## Creating an input dataset

```python
input_dataset = lr.datasets.create_from_samples(samples, batch_size=1000)

# Pass to lr.transforms.run():
dataset = lr.transforms.run(pipeline, input_dataset=input_dataset, max_questions=10)
```

## FileSets — when to use

Prefer `preprocessing.files_to_samples()` for small, one-shot collections that only need to become seeds. Reach for a **FileSet** when any of these apply:

- The corpus is large (hundreds+ of files) or needs parallel upload
- You need metadata filtering on seeds (e.g. only one ticker)
- You need context or labels pulled **from the same document collection** (RAG or chronological lookups)
- You need temporal ordering across documents (forecasting, report-to-report resolution)

### Create the FileSet

```python
from lightningrod import (
    FileSetMetadataSchemaInput, MetadataFieldDefinitionInput, MetadataFieldType,
)

# Metadata schema is optional — include it only if you plan to filter on these fields later
schema = FileSetMetadataSchemaInput(fields=[
    MetadataFieldDefinitionInput(
        name="ticker", field_type=MetadataFieldType.STRING, required=True,
        description="Company ticker",
    ),
])

fs = lr.filesets.create(
    name="quarterly-reports",
    description="Investor reports",
    metadata_schema=schema,  # omit for unstructured collections
)
```

### Upload files

```python
from datetime import datetime

# Per-file metadata is a dict keyed by filename. file_date powers temporal ordering.
result = lr.filesets.upload_files(
    fs.id,
    file_paths=["report_q1.pdf", "report_q2.pdf"],
    metadata={
        "report_q1.pdf": {"ticker": "APEX", "file_date": datetime(2024, 3, 31)},
        "report_q2.pdf": {"ticker": "APEX", "file_date": datetime(2024, 6, 30)},
    },
)
print(result.succeeded, result.failed, result.errors)

# Scale path — uses parallel GCS transfer. Requires the [transfer] extra:
#   pip install "lightningrod-ai[transfer]"
result = lr.filesets.upload_directory(
    fs.id, "./docs", pattern="*.pdf", max_workers=100, show_progress=True,
)
```

## FileSet transforms — pick one of three patterns

After upload, choose the transform pattern that matches how the documents relate to your questions.

### 1. Seeds only — `FileSetSeedGenerator`

Use when documents provide the **material questions are about**, but labels come from elsewhere (web search, news events, a later-resolved outcome).

```python
from lightningrod import FileSetSeedGenerator

seed_gen = FileSetSeedGenerator(
    file_set_id=fs.id,
    chunk_size=2000,
    chunk_overlap=200,
    metadata_filters=["ticker='APEX'"],  # SQL-style, optional
)
```

### 2. Non-RAG whole-document — `FileSetDocumentContextGenerator` / `FileSetDocumentLabeler`

**No embeddings, no vector search.** Picks a **single document** by chronological relationship to the seed and passes its full text to the LLM. Right when:

- Each document fits in context (Beige Book, 10-Q, periodic status reports)
- Resolution is naturally "the next report answers the previous one's questions"
- You want whole-document reasoning, not cherry-picked chunks
- You need the *exact* adjacent document (`NEXT_DOCUMENT` / `PREVIOUS_DOCUMENT`) — Qdrant can't express this

```python
from lightningrod import (
    FileSetDocumentContextGenerator, FileSetDocumentLabeler, TemporalConstraint,
    BinaryAnswerType,
)

# TemporalConstraint values: EQUAL, NEXT_DOCUMENT, PREVIOUS_DOCUMENT, BEFORE, AFTER
context = FileSetDocumentContextGenerator(
    file_set_id=fs.id,
    temporal_constraint=TemporalConstraint.EQUAL,       # same doc as seed
    metadata_filter_keys=["ticker"],                     # match seed's ticker
    system_instruction="Extract sections relevant to forecasting.",
    max_document_chars=200_000,                          # optional
)

labeler = FileSetDocumentLabeler(
    file_set_id=fs.id,
    temporal_constraint=TemporalConstraint.NEXT_DOCUMENT,  # resolve from next report
    metadata_filter_keys=["ticker"],
    confidence_threshold=0.7,
    answer_type=BinaryAnswerType(
        labeler_instruction="Resolve Yes/No only when explicitly addressed.",
    ),
)
```

### 3. RAG semantic retrieval — `QdrantContextGenerator` / `QdrantRAGLabeler`

Builds a **vector index** over the FileSet (`BAAI/bge-small-en-v1.5`, `index_chunk_size=1500`). At runtime, embeds the question and retrieves `top_k` chunks across the whole corpus. Right when:

- Corpus is too large to stuff a whole document into context
- You want "find any relevant passage anywhere"
- Facts are scattered across long documents

```python
from lightningrod import QdrantContextGenerator, QdrantRAGLabeler

context = QdrantContextGenerator(
    file_set_id=fs.id,
    top_k=5,
    # Maps Qdrant payload key -> sample metadata key. Restricts retrieval to
    # chunks whose `ticker` payload equals the sample's `ticker`.
    payload_filters={"ticker": "ticker"},
    temporal_direction="before",   # soft timestamp filter: "before" | "after"
)

labeler = QdrantRAGLabeler(
    file_set_id=fs.id,
    payload_filters={"ticker": "ticker"},
    temporal_direction="after",    # forward-looking questions resolved by later docs
    confidence_threshold=0.7,
    answer_type=BinaryAnswerType(),
)
```

### Qdrant vs FileSetDocument — quick reference

| Dimension | `Qdrant*` | `FileSetDocument*` |
|---|---|---|
| Retrieval | Vector search, top_k chunks | Single whole document, picked chronologically |
| Index | Builds embeddings on first use | None |
| Temporal param | `temporal_direction="before"/"after"` | `temporal_constraint=TemporalConstraint.{EQUAL,NEXT_DOCUMENT,PREVIOUS_DOCUMENT,BEFORE,AFTER}` |
| Metadata filter | `payload_filters={"qdrant_key": "sample_key"}` | `metadata_filter_keys=["key1", "key2"]` |
| Best for | Knowledge-base search | Periodic reports that resolve each other |

**Rule of thumb:** FileSetDocument = *periodic reports that resolve each other*. Qdrant = *searching a knowledge base*.

## Fitness assessment

Before building a pipeline, check that the data is suitable:

| Check | How | Minimum bar |
|-------|-----|-------------|
| Volume | `len(samples)` | ≥ 50 samples for a meaningful demo |
| Date coverage | Check `sample.date` fields | Dates present for temporal split; span ≥ 30 days for forecasting |
| Text quality | Spot-check `sample.text` values | Readable prose, not garbled OCR or empty strings |
| Label availability | Check `sample.label` if using `QuestionAndLabelGenerator` | Labels present and non-null |

If the data fails a check, explain the issue clearly and stop — do not build a pipeline on bad inputs.

## Chunking guidance

- Default `chunk_size=1000`, `chunk_overlap=100` works for most documents
- Dense technical text: use smaller chunks (`chunk_size=500`)
- Narrative/long-form text: larger chunks are fine (`chunk_size=1500`)
- CSVs: each row becomes one sample — chunking parameters are ignored

## Reference notebooks

- `notebooks/getting_started/02_custom_documents_datasource.ipynb`
- `notebooks/custom_filesets/`
