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

## FileSet upload (for larger collections)

```python
fs = lr.filesets.create(name="my-docs", description="Internal reports")
lr.filesets.files.upload(fs.id, "report.pdf", file_date="2025-01-15")

# Then use FileSetSeedGenerator(file_set_id=fs.id) in the pipeline
```

## Fitness assessment

Before building a pipeline, check that the data is suitable:

| Check | How | Minimum bar |
|-------|-----|-------------|
| Volume | `len(samples)` | ≥ 50 samples for a meaningful demo |
| Date coverage | Check `sample.date` fields | Dates present for temporal split; span ≥ 30 days for forecasting |
| Text quality | Spot-check `sample.text` values | Readable prose, not garbled OCR or empty strings |
| Label availability | Check `sample.label` if using `QuestionAndLabelGenerator` | Labels present and non-null |

If the data fails a check, surface the issue to the orchestrator before proceeding.

## Chunking guidance

- Default `chunk_size=1000`, `chunk_overlap=100` works for most documents
- Dense technical text: use smaller chunks (`chunk_size=500`)
- Narrative/long-form text: larger chunks are fine (`chunk_size=1500`)
- CSVs: each row becomes one sample — chunking parameters are ignored

## Reference notebooks

- `notebooks/getting_started/02_custom_documents_datasource.ipynb`
- `notebooks/custom_filesets/`
