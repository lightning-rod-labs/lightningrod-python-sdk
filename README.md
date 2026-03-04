

# Lightning Rod Python SDK [Beta](https://pypi.org/project/lightningrod-ai/0.1.16/)

The Lightning Rod SDK provides a simple Python API for generating custom forecasting datasets to train your LLMs. Transform news articles, documents, and other real-world data into high-quality training samples automatically.

Based on our research: [Future-as-Label: Scalable Supervision from Real-World Outcomes](https://arxiv.org/abs/2601.06336)

## 👋 Quick Start

### 1. Install the SDK

```bash
pip install lightningrod-ai
```

### 2. Get your API key

Sign up at [dashboard.lightningrod.ai](https://dashboard.lightningrod.ai/?redirect=/api) to get your API key and **$50 of free credits**.

### 3. Generate your first dataset

Generate **1000+ forecasting questions in minutes** - from raw sources to labeled dataset, automatically. ⚡

```python
from lightningrod import LightningRod, BinaryAnswerType, QuestionPipeline, NewsSeedGenerator, ForwardLookingQuestionGenerator, WebSearchLabeler

lr = LightningRod(api_key="your-api-key")

binary_answer = BinaryAnswerType()

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
dataset.flattened(binary_answer)  # Ready-to-use data for your training pipelines
```

**We use this to generate the [Future-as-Label training dataset](https://huggingface.co/datasets/LightningRodLabs/future-as-label-paper-training-dataset) for our research paper.**

## 🆕 New: Foresight-v3 Forecasting Model

We've released **foresight-v3**, our latest forecasting model. Use it via the OpenAI-compatible API for probability estimates on forecasting questions:

```python
from openai import OpenAI

client = OpenAI(
    api_key="your-api-key",
    base_url="https://api.lightningrod.ai/api/public/v1"
)

response = client.chat.completions.create(
    model="LightningRodLabs/foresight-v3",
    messages=[{"role": "user", "content": "Will the Fed cut rates by 25bp in March 2025?"}]
)
print(response.choices[0].message.content)
```

See the [API docs](https://dashboard.lightningrod.ai/public/docs#tag/openai-compatible/post/openai/chat/completions) for full details, or try the [Foresight-v3 notebook](notebooks/08_foresight_model.ipynb).

## ✨ Examples

We have some example notebooks to help you get started! If you have trouble using the SDK, please submit an issue on Github.

### Tutorials


| Example Name                | Path                                             | Google Colab Link                                                                                                                                             |
| --------------------------- | ------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Quick Start                 | `notebooks/01_quick_start.ipynb`                 | [Open in Colab](https://colab.research.google.com/github/lightning-rod-labs/lightningrod-python-sdk/blob/main/notebooks/01_quick_start.ipynb)                 |
| News Datasource             | `notebooks/02_news_datasource.ipynb`             | [Open in Colab](https://colab.research.google.com/github/lightning-rod-labs/lightningrod-python-sdk/blob/main/notebooks/02_news_datasource.ipynb)             |
| Custom Documents            | `notebooks/03_custom_documents_datasource.ipynb` | [Open in Colab](https://colab.research.google.com/github/lightning-rod-labs/lightningrod-python-sdk/blob/main/notebooks/03_custom_documents_datasource.ipynb) |
| Binary Answer Type          | `notebooks/04_binary_answer_type.ipynb`          | [Open in Colab](https://colab.research.google.com/github/lightning-rod-labs/lightningrod-python-sdk/blob/main/notebooks/04_binary_answer_type.ipynb)          |
| Continuous Answer Type      | `notebooks/05_continuous_answer_type.ipynb`      | [Open in Colab](https://colab.research.google.com/github/lightning-rod-labs/lightningrod-python-sdk/blob/main/notebooks/05_continuous_answer_type.ipynb)      |
| Multiple Choice Answer Type | `notebooks/06_multiple_choice_answer_type.ipynb` | [Open in Colab](https://colab.research.google.com/github/lightning-rod-labs/lightningrod-python-sdk/blob/main/notebooks/06_multiple_choice_answer_type.ipynb) |
| Free Response Answer Type   | `notebooks/07_free_response_answer_type.ipynb`   | [Open in Colab](https://colab.research.google.com/github/lightning-rod-labs/lightningrod-python-sdk/blob/main/notebooks/07_free_response_answer_type.ipynb)   |
| Foresight-v3 Model          | `notebooks/08_foresight_model.ipynb`             | [Open in Colab](https://colab.research.google.com/github/lightning-rod-labs/lightningrod-python-sdk/blob/main/notebooks/08_foresight_model.ipynb)             |
| Training on Generated Datasets                | `notebooks/09_training_api.ipynb`                | [Open in Colab](https://colab.research.google.com/github/lightning-rod-labs/lightningrod-python-sdk/blob/main/notebooks/09_training_api.ipynb)                |


### End-to-end


| Example Name            | Path                                          | Google Colab Link                                                                                                                                          |
| ----------------------- | --------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Golf Forecasting        | `notebooks/e2e/golf_forecasting.ipynb`        | [Open in Colab](https://colab.research.google.com/github/lightning-rod-labs/lightningrod-python-sdk/blob/main/notebooks/e2e/golf_forecasting.ipynb)        |
| Trump Forecasting       | `notebooks/e2e/trump_forecasting.ipynb`       | [Open in Colab](https://colab.research.google.com/github/lightning-rod-labs/lightningrod-python-sdk/blob/main/notebooks/e2e/trump_forecasting.ipynb)       |
| Document Classification | `notebooks/e2e/document_classification.ipynb` | [Open in Colab](https://colab.research.google.com/github/lightning-rod-labs/lightningrod-python-sdk/blob/main/notebooks/e2e/document_classification.ipynb) |
| Polymarket Backtesting  | `notebooks/e2e/polymarket_backtesting.ipynb`  | [Open in Colab](https://colab.research.google.com/github/lightning-rod-labs/lightningrod-python-sdk/blob/main/notebooks/e2e/polymarket_backtesting.ipynb)  |
| Model Consensus         | `notebooks/e2e/model_consensus.ipynb`         | [Open in Colab](https://colab.research.google.com/github/lightning-rod-labs/lightningrod-python-sdk/blob/main/notebooks/e2e/model_consensus.ipynb)         |


For complete API reference documentation, see [API.md](API.md). This includes overview of the core system concepts, methods and types.