# Lightning Rod Python SDK API Reference

## Overview

The Lightning Rod SDK lets you generate forecasting datasets from real-world data. The typical workflow:

1. **Collect seeds** (raw data like news articles or documents)
2. **Generate questions** from seeds using AI
3. **Label questions** with ground truth answers
4. **Export datasets** for model training

## Core Concepts

**Sample** - The fundamental unit of data containing:
- `seed`: Raw starting data (news articles, documents, etc.)
- `question`: Forecasting question generated from seed
- `label`: Ground truth answer with confidence score
- `prompt`: Formatted prompt ready for model input
- `context`: Additional context (news, RAG results)
- `meta`: Custom metadata

**Dataset** - Collection of samples stored as Parquet files. Can be downloaded, used as pipeline input, or exported for training.

## Main Client

### LightningRod

Main entry point for the SDK.

```python
from lightningrod import LightningRod

client = LightningRod(api_key="your-api-key")
```

**Client attributes:**
- `client.transforms` - Run transform pipelines
- `client.datasets` - Access dataset samples
- `client.files` - Upload files
- `client.filesets` - Manage file collections

## Transforms

Transform pipelines generate datasets from raw data. The main method is `transforms.run()` which submits a job, waits for completion, and returns a dataset.

### Running Transforms

**`transforms.run(config, dataset_id=None, max_questions=None)`** - Submit and wait for completion

**`transforms.submit(config, dataset_id=None, max_questions=None)`** - Submit without waiting

**`transforms.jobs.get(job_id)`** - Check job status

### Transform Configurations

**QuestionPipeline** - Complete pipeline combining seed generation, question generation, and labeling.

**Seed Generators:**
- `NewsSeedGenerator` - Google News search results
- `GdeltSeedGenerator` - GDELT global news database
- `FileSetSeedGenerator` - Chunk documents from a file set
- `FileSetQuerySeedGenerator` - RAG queries against a file set

**Question Generators:**
- `QuestionGenerator` - Generate questions from seeds
- `ForwardLookingQuestionGenerator` - Specialized for forward-looking questions
- `QuestionAndLabelGenerator` - Generate questions and labels together

**Labelers:**
- `WebSearchLabeler` - Label questions via web search

**Other Components:**
- `NewsContextGenerator` - Add relevant news context to questions
- `QuestionRenderer` - Format questions into prompts
- `RolloutGenerator` - Generate model completions
- `FilterCriteria` - LLM-based content filtering

All configurations support optional parameters for customization. See examples in the `examples/` directory for detailed usage.

## Datasets

**`Dataset`** - Represents a dataset with `id` and `num_rows`.

**`dataset.to_samples()`** - Download all samples (handles pagination automatically)

**`client.datasets.list(dataset_id)`** - Alternative way to list samples

## Files

**`client.files.upload(file_path)`** - Upload a file, returns file ID and metadata.

## File Sets

File sets are collections of files used as data sources.

**`client.filesets.create(name, description=None)`** - Create a file set

**`client.filesets.get(file_set_id)`** - Get file set details

**`client.filesets.list()`** - List all file sets

**`client.filesets.files.upload(file_set_id, file_path, metadata=None)`** - Upload file to set

**`client.filesets.files.add(file_set_id, file_id, metadata=None)`** - Add existing file to set

**`client.filesets.files.list(file_set_id)`** - List files in set

## Types

**TransformJob** - Job status, IDs, timestamps, error messages

**TransformJobStatus** - Enum: `RUNNING`, `COMPLETED`, `FAILED`

**FileSet** - File set metadata: id, name, description, file counts, timestamps

**FileSetFile** - File entry with file_id and optional metadata
