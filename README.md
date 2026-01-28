<div align="center">
<!-- Note: only an absolute image URL works on PyPi: https://pypi.org/project/lightningrod-ai -->
  <img src="https://github.com/lightning-rod-labs/lightningrod-python-sdk/blob/main/banner.png?raw=true" alt="Lightning Rod Labs" />
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

## ✨ Examples

We have some example notebooks to help you get started! If you have trouble using the SDK, please submit an issue on Github.

| Example Name | Path | Google Colab Link |
|--------------|------|-------------------|
| Quick Start | `notebooks/01_quick_start.ipynb` | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/lightning-rod-labs/lightningrod-python-sdk/blob/main/notebooks/01_quick_start.ipynb) |
| News Datasource | `notebooks/02_news_datasource.ipynb` | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/lightning-rod-labs/lightningrod-python-sdk/blob/main/notebooks/02_news_datasource.ipynb) |
| Custom Documents | `notebooks/03_custom_documents_datasource.ipynb` | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/lightning-rod-labs/lightningrod-python-sdk/blob/main/notebooks/03_custom_documents_datasource.ipynb) |
| Binary Answer Type | `notebooks/04_binary_answer_type.ipynb` | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/lightning-rod-labs/lightningrod-python-sdk/blob/main/notebooks/04_binary_answer_type.ipynb) |
| Continuous Answer Type | `notebooks/05_continuous_answer_type.ipynb` | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/lightning-rod-labs/lightningrod-python-sdk/blob/main/notebooks/05_continuous_answer_type.ipynb) |
| Multiple Choice Answer Type | `notebooks/06_multiple_choice_answer_type.ipynb` | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/lightning-rod-labs/lightningrod-python-sdk/blob/main/notebooks/06_multiple_choice_answer_type.ipynb) |
| Free Response Answer Type | `notebooks/07_free_response_answer_type.ipynb` | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/lightning-rod-labs/lightningrod-python-sdk/blob/main/notebooks/07_free_response_answer_type.ipynb) |


For complete API reference documentation, see [API.md](API.md). This includes overview of the core system concepts, methods and types.

## License

MIT License - see LICENSE file for details
