<div align="center">
  <img src="banner.png" alt="Lightning Rod Labs" />
</div>

# Lightning Rod Python SDK

Generate training data from real world sources. Instantly.

The Lightning Rod SDK provides a simple Python API for generating custom forecasting datasets to train your LLMs. Transform news articles, documents, and other real-world data into high-quality training samples automatically.

## Quick Start

### 1. Install the SDK

```bash
pip install lightningrod-ai
```

### 2. Get your API key

Sign up at [lightningrod.ai](https://lightningrod.ai) to get your API key.

### 3. Generate your first dataset

```python
from datetime import datetime, timedelta
from lightningrod import (
    LightningRod,
    NewsSeedGenerator,
    AIQuestionGenerator,
    FilterCriteria,
    WebSearchLabeler,
    QuestionGenerationPipeline
)

lr = LightningRod(api_key="your-api-key-here")

pipeline = QuestionGenerationPipeline(
    seed_generator=NewsSeedGenerator(
        start_date=datetime.now() - timedelta(days=90),
        end_date=datetime.now(),
        search_query="Premier League Soccer"
    ),
    question_generator=AIQuestionGenerator(
        instructions="Write forward-looking, self-contained questions with explicit dates/entities",
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

dataset = lr.transforms.run(pipeline)
```

This pipeline will:

1. **Collect Seeds**: Search for recent news about Premier League Soccer
2. **Generate Questions**: Use AI to create forecasting questions from the news
3. **Label Questions**: Automatically find answers using web search
4. **Return Dataset**: Get a dataset with all samples ready for download

## Examples

Comprehensive example notebooks demonstrate different use cases and features:

### Getting Started
- **[Quick Start](examples/01_quick_start.ipynb)** — Simplest example to get you running quickly

### Data Sources
- **[Google News](examples/02_google_news_datasource.ipynb)** — Use Google News search as a data source
- **[GDELT](examples/03_gdelt_datasource.ipynb)** — Use GDELT global news database for large-scale datasets
- **[Custom Documents](examples/04_custom_documents_datasource.ipynb)** — Generate questions from your own documents and files

### Question Types
- **[Binary](examples/05_binary_answer_type.ipynb)** — Yes/No questions for event prediction
- **[Continuous](examples/06_continuous_answer_type.ipynb)** — Numeric questions for quantitative predictions
- **[Multiple Choice](examples/07_multiple_choice_answer_type.ipynb)** — Questions with predefined answer options
- **[Free Response](examples/08_free_response_answer_type.ipynb)** — Open-ended questions with detailed text answers

## Documentation

For complete API reference documentation, see [API.md](API.md). This includes overview of the core system concepts, methods and types.

## License

MIT License - see LICENSE file for details
