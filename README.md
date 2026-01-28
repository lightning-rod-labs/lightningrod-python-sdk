<div align="center">
  <img src="banner.png" alt="Lightning Rod Labs" />
</div>

# Lightning Rod Python SDK

The Lightning Rod SDK provides a simple Python API for generating custom forecasting datasets to train your LLMs. Transform news articles, documents, and other real-world data into high-quality training samples automatically.

Based on our research: [Future-as-Label: Scalable Supervision from Real-World Outcomes](https://arxiv.org/abs/2601.06336)

## 👋 Quick Start

### 1. Install the SDK

```bash
pip install lightningrod-ai
```

### 2. Get your API key

Sign up at [dashboard.lightningrod.ai](https://dashboard.lightningrod.ai/?redirect=/api) to get your API key.

### 3. Generate your first dataset

Generate **1000+ forecasting questions in ~10 minutes** - from raw sources to labeled dataset, automatically. ⚡

```python
from lightningrod import LightningRod, AnswerType, QuestionPipeline, NewsSeedGenerator, ForwardLookingQuestionGenerator, WebSearchLabeler

lr = LightningRod(api_key="your-api-key")

binary_answer = AnswerType(answer_type=AnswerTypeEnum.BINARY)

pipeline = QuestionPipeline(
    seed_generator=NewsSeedGenerator(
        start_date=datetime.now() - timedelta(days=90),
        end_date=datetime.now(),
        search_query=["Trump"],
    ),
    question_generator=ForwardLookingQuestionGenerator(
        instructions="Generate binary forecasting questions about Trump's actions and decisions.",
        examples=[
            "Will Trump impose 25% tariffs on all goods from Canada by February 1, 2025?",
            "Will Pete Hegseth be confirmed as Secretary of Defense by February 15, 2025?",
        ]
    ),
    labeler=WebSearchLabeler(answer_type=binary_answer),
)

dataset = lr.transforms.run(pipeline, max_questions=3000)
dataset.flattened() # Ready-to-use data for your training pipelines
```

**We use this to generate our [Future-as-Label training dataset](https://huggingface.co/datasets/LightningRodLabs/future-as-label-paper-training-dataset) for our research paper.**

## 🎥 Examples

We have some example notebooks to help you get started! If you have trouble using the SDK, please submit an issue on Github.

### Getting Started
- **[Quick Start](notebooks/01_quick_start.ipynb)** — Simplest example + docs to get you running quickly

### Data Sources
- **[News Search](notebooks/02_search_news_datasource.ipynb)** — Use Google News search for fresh news
- **[GDELT](notebooks/03_top_news_datasource.ipynb)** — Use top aggregated news from GDELT database
- **[Custom Documents](notebooks/04_custom_documents_datasource.ipynb)** — Generate questions from your own documents and files

### Question Types
- **[Binary](notebooks/05_binary_answer_type.ipynb)** — Yes/No questions for event prediction
- **[Continuous](notebooks/06_continuous_answer_type.ipynb)** — Numeric questions for quantitative predictions
- **[Multiple Choice](notebooks/07_multiple_choice_answer_type.ipynb)** — Questions with predefined answer options
- **[Free Response](notebooks/08_free_response_answer_type.ipynb)** — Open-ended questions with detailed text answers

## 📁 Documentation

**[Quick Start](notebooks/01_quick_start.ipynb)**  example also serves as interactive documentation - we recommend starting there!

For complete API reference documentation, see [API.md](API.md). This includes overview of the core system concepts, methods and types.

## License

MIT License - see LICENSE file for details
