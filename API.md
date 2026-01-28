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

lr = LightningRod(api_key="your-api-key")
```

## Transforms

Transform pipelines generate datasets from raw data. The main method is `transforms.run()` which submits a job, waits for completion, and returns a dataset.

### API

**`lr.transforms.run(config, dataset_id=None, max_questions=None)`** - Submit and wait for completion

**`lr.transforms.submit(config, dataset_id=None, max_questions=None)`** - Submit without waiting

**`lr.transforms.jobs.get(job_id)`** - Check job status

### Types

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

**Other Pipeline Components:**
- `NewsContextGenerator` - Add relevant news context to questions
- `QuestionRenderer` - Format questions into prompts
- `RolloutGenerator` - Generate model completions
- `FilterCriteria` - LLM-based content filtering

**Jobs:**
- `TransformJob` - Job status, IDs, timestamps, error messages
- `TransformJobStatus` - Enum: `RUNNING`, `COMPLETED`, `FAILED`

See examples in the `examples/` directory for detailed usage of the pipeline types.

## Datasets

### API

**`dataset.download()`** - Download all samples (handles pagination automatically)

**`dataset.samples()`** - Returns cached samples (auto-downloads if needed)

**`dataset.flattened()`** - Returns cached samples in a flat-object list format (auto-downloads if needed)

**`lr.datasets.list(dataset_id)`** - Alternative way to list samples

### Types

`Dataset` - Represents a dataset with `id` and `num_rows`.