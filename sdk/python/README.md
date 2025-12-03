# Lightning Rod Python SDK

AI-powered forecasting dataset generation platform.

## Introduction

Lightning Rod helps you generate high-quality datasets by automating the process of seed collection, question generation, and answer labeling. Whether you're building forecasting models or running SFT over unstructed filesets, Lightning Rod transforms raw information into structured, ML-ready datasets.

## Core Concepts

Lightning Rod works with a simple but powerful data model:

### Sample

A **Sample** is the fundamental unit of data in Lightning Rod. Each sample contains:

- `sample_id`: Unique identifier for the sample
- `seed`: Optional starting point (raw data)
- `question`: Optional forecasting question
- `label`: Optional ground truth answer
- `meta`: Dictionary for additional metadata

### Seed

A **Seed** is your starting point - raw data that will be transformed into questions. For example:

- `seed_text`: The raw text content (e.g., news articles, reports, tweets)

### Question

A **Question** is a forecasting question generated from seeds:

- `question_text`: The forecasting question (e.g., "Will Arsenal finish above Tottenham in the 2025-26 season?")

### Label

A **Label** represents the ground truth answer to a question:

- `label`: The answer (e.g., "Yes", "No", or a numeric value)
- `label_confidence`: Confidence score (0.0 to 1.0)
- `resolution_date`: When the question can be resolved

### Dataset

A **Dataset** is a collection of samples stored efficiently as Parquet files. Datasets can be:

- Downloaded for local analysis
- Used as input to pipelines
- Exported for model training

## Installation

```bash
pip install lightningrod-ai
```

## Quick Start

### Authentication

First, get your API key from [lightningrod.ai](https://lightningrod.ai) and initialize the client:

```python
from lightningrod import LightningRodClient

client = LightningRodClient(api_key="your-api-key-here")
```

### Question Generation Pipeline

Create a complete question generation pipeline that takes seeds, generates questions, and labels them:

```python
from datetime import datetime, timedelta
from lightningrod import LightningRodClient
from lightningrod.pipelines import QuestionGenerationPipeline
from lightningrod.transforms import (
    NewsSeedGenerator,
    AIQuestionGenerator,
    FilterCriteria,
    WebSearchLabeler
)

client = LightningRodClient(api_key="your-api-key-here")

pipeline = QuestionGenerationPipeline(
    seed_generator=NewsSeedGenerator(
        start_date=datetime.now() - timedelta(days=90),
        end_date=datetime.now(),
        search_query="Premier League Soccer"
    ),
    question_generator=AIQuestionGenerator(
        instructions="Write forward-looking, self-contained questions with explicit dates/entities.",
        examples=[
            "Who will win Manchester City vs Liverpool on Dec 18, 2025?",
            "Will Arsenal finish above Tottenham in the 2025-26 season?"
        ],
        bad_examples=["Who won the match?"],
        filter=FilterCriteria(
            rubric="The question should be about Premier League soccer",
            min_score=0.5
        ),
    ),
    labeler=WebSearchLabeler(
        confidence_threshold=0.5
    )
)

dataset = client.run(pipeline, dataset=None)
```

This pipeline will:

1. **Collect Seeds**: Search for recent news about Premier League Soccer
2. **Generate Questions**: Use AI to create forecasting questions from the news
3. **Label Questions**: Automatically find answers using web search
4. **Return Dataset**: Get a dataset with all samples ready for download

## Support

- Documentation: [lightningrod.ai/sdk](https://lightningrod.ai/sdk)
- Email: support@lightningrod.ai
- GitHub: [github.com/lightning-rod-labs/lightningrod-python](https://github.com/lightning-rod-labs/lightningrod-python)

## License

MIT License - see LICENSE file for details


## Development

To Release a new version of the package increment the version number then run:

```
pip install build twine

rm -rf dist/*

python -m build
python -m twine upload dist/*
```