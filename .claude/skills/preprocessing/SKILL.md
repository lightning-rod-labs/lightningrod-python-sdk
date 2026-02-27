---
name: preprocessing
description: Preprocessing patterns for converting files to Lightningrod samples. Use when working with files_to_samples, chunking, or metadata.
---

# Preprocessing

## Converting files to samples

```python
from lightningrod import preprocessing

samples = preprocessing.files_to_samples(
    "path/to/file.pdf",  # or pattern: "data/*.txt"
    chunk_size=1000,
    chunk_overlap=100,
)
```

Single file: `preprocessing.file_to_samples(path)`. Chunks only: `preprocessing.chunks_to_samples(chunks, metadata=...)`.

## Creating input dataset

```python
input_dataset = lr.datasets.create_from_samples(samples, batch_size=1000)
```

Then use input_dataset.id as input_dataset_id when submitting a transform with FileSetSeedGenerator or similar.

## Chunking

Default chunk_size=1000, chunk_overlap=100. Uses langchain-text-splitters. Adjust for document type: smaller chunks for dense text, larger for narrative.

## Metadata

Pass metadata dict to chunks_to_samples for filtering or context. Metadata flows through to samples.
