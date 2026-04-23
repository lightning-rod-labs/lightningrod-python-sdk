<div align="center">
<!-- Note: only an absolute image URL works on PyPi: https://pypi.org/project/lightningrod-ai -->
  <img src="https://github.com/lightning-rod-labs/lightningrod-python-sdk/blob/main/banner.png?raw=true" alt="Lightning Rod Labs" />
</div>

# Lightning Rod Python SDK [![Beta](https://img.shields.io/badge/beta-0.1.24-orange)](https://pypi.org/project/lightningrod-ai/0.1.24/)

The Lightning Rod SDK provides a simple Python API for generating custom forecasting datasets to train your LLMs. Transform news articles, documents, and other real-world data into high-quality training samples automatically.

Based on our research: [Future-as-Label: Scalable Supervision from Real-World Outcomes](https://arxiv.org/abs/2601.06336)

Documentation: [docs.lightningrod.ai](https://docs.lightningrod.ai/)

## 👋 Quick Start

### 1. Install the SDK

```bash
pip install lightningrod-ai
```

### 2. Get your API key

Sign up at [dashboard.lightningrod.ai](https://dashboard.lightningrod.ai/sign-up?redirect=/api) to get your API key and **$50 of free credits**.

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
dataset.flattened()  # Ready-to-use data for your training pipelines
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

See the [API docs](https://docs.lightningrod.ai/rest-api#post-openai-chat-completions) for full details, or try the [Foresight-v3 notebook](notebooks/evaluation/01_foresight_model.ipynb).

## ✨ Examples

We have example notebooks to help you get started. If you have trouble using the SDK, please submit an issue on GitHub.

### Quick Start

| Example Name | Path | Google Colab Link |
| ------------ | ---- | ----------------- |
| Quick Start | `notebooks/00_quickstart.ipynb` | [Open in Colab](https://colab.research.google.com/github/lightning-rod-labs/lightningrod-python-sdk/blob/main/notebooks/00_quickstart.ipynb) |

### Getting Started

| Example Name | Path | Google Colab Link |
| ------------ | ---- | ----------------- |
| News Datasource | `notebooks/getting_started/01_news_datasource.ipynb` | [Open in Colab](https://colab.research.google.com/github/lightning-rod-labs/lightningrod-python-sdk/blob/main/notebooks/getting_started/01_news_datasource.ipynb) |
| Custom Documents | `notebooks/getting_started/02_custom_documents_datasource.ipynb` | [Open in Colab](https://colab.research.google.com/github/lightning-rod-labs/lightningrod-python-sdk/blob/main/notebooks/getting_started/02_custom_documents_datasource.ipynb) |
| BigQuery Datasource | `notebooks/getting_started/03_bigquery_datasource.ipynb` | [Open in Colab](https://colab.research.google.com/github/lightning-rod-labs/lightningrod-python-sdk/blob/main/notebooks/getting_started/03_bigquery_datasource.ipynb) |
| Answer Types | `notebooks/getting_started/04_answer_types.ipynb` | [Open in Colab](https://colab.research.google.com/github/lightning-rod-labs/lightningrod-python-sdk/blob/main/notebooks/getting_started/04_answer_types.ipynb) |
| GRPO Training | `notebooks/getting_started/05_grpo_training.ipynb` | [Open in Colab](https://colab.research.google.com/github/lightning-rod-labs/lightningrod-python-sdk/blob/main/notebooks/getting_started/05_grpo_training.ipynb) |
| SFT Training | `notebooks/getting_started/06_sft_training.ipynb` | [Open in Colab](https://colab.research.google.com/github/lightning-rod-labs/lightningrod-python-sdk/blob/main/notebooks/getting_started/06_sft_training.ipynb) |

### Custom Filesets

| Example Name | Path | Google Colab Link |
| ------------ | ---- | ----------------- |
| Create Fileset | `notebooks/custom_filesets/01_create_fileset.ipynb` | [Open in Colab](https://colab.research.google.com/github/lightning-rod-labs/lightningrod-python-sdk/blob/main/notebooks/custom_filesets/01_create_fileset.ipynb) |
| Basic QA Generation | `notebooks/custom_filesets/02_basic_qa_generation.ipynb` | [Open in Colab](https://colab.research.google.com/github/lightning-rod-labs/lightningrod-python-sdk/blob/main/notebooks/custom_filesets/02_basic_qa_generation.ipynb) |
| Advanced Features | `notebooks/custom_filesets/03_advanced_features.ipynb` | [Open in Colab](https://colab.research.google.com/github/lightning-rod-labs/lightningrod-python-sdk/blob/main/notebooks/custom_filesets/03_advanced_features.ipynb) |
| Beige Book (Document Labeling) | `notebooks/custom_filesets/04_beige_book_e2e.ipynb` | [Open in Colab](https://colab.research.google.com/github/lightning-rod-labs/lightningrod-python-sdk/blob/main/notebooks/custom_filesets/04_beige_book_e2e.ipynb) |

### Answer Types

| Example Name | Path | Google Colab Link |
| ------------ | ---- | ----------------- |
| Binary | `notebooks/answer_types/binary.ipynb` | [Open in Colab](https://colab.research.google.com/github/lightning-rod-labs/lightningrod-python-sdk/blob/main/notebooks/answer_types/binary.ipynb) |
| Continuous | `notebooks/answer_types/continuous.ipynb` | [Open in Colab](https://colab.research.google.com/github/lightning-rod-labs/lightningrod-python-sdk/blob/main/notebooks/answer_types/continuous.ipynb) |
| Multiple Choice | `notebooks/answer_types/multi-choice.ipynb` | [Open in Colab](https://colab.research.google.com/github/lightning-rod-labs/lightningrod-python-sdk/blob/main/notebooks/answer_types/multi-choice.ipynb) |

### Evaluation

| Example Name | Path | Google Colab Link |
| ------------ | ---- | ----------------- |
| Foresight-v3 Model | `notebooks/evaluation/01_foresight_model.ipynb` | [Open in Colab](https://colab.research.google.com/github/lightning-rod-labs/lightningrod-python-sdk/blob/main/notebooks/evaluation/01_foresight_model.ipynb) |
| Model Consensus | `notebooks/evaluation/02_model_consensus.ipynb` | [Open in Colab](https://colab.research.google.com/github/lightning-rod-labs/lightningrod-python-sdk/blob/main/notebooks/evaluation/02_model_consensus.ipynb) |
| Polymarket Backtesting | `notebooks/evaluation/03_polymarket_backtesting.ipynb` | [Open in Colab](https://colab.research.google.com/github/lightning-rod-labs/lightningrod-python-sdk/blob/main/notebooks/evaluation/03_polymarket_backtesting.ipynb) |
| Document Classification | `notebooks/evaluation/04_document_classification.ipynb` | [Open in Colab](https://colab.research.google.com/github/lightning-rod-labs/lightningrod-python-sdk/blob/main/notebooks/evaluation/04_document_classification.ipynb) |

### Fine Tuning

| Example Name | Path | Google Colab Link |
| ------------ | ---- | ----------------- |
| Golf Forecasting | `notebooks/fine_tuning/01_golf_forecasting.ipynb` | [Open in Colab](https://colab.research.google.com/github/lightning-rod-labs/lightningrod-python-sdk/blob/main/notebooks/fine_tuning/01_golf_forecasting.ipynb) |
| Trump Forecasting | `notebooks/fine_tuning/02_trump_forecasting.ipynb` | [Open in Colab](https://colab.research.google.com/github/lightning-rod-labs/lightningrod-python-sdk/blob/main/notebooks/fine_tuning/02_trump_forecasting.ipynb) |
| Survival LLM | `notebooks/fine_tuning/03_survival_llm.ipynb` | [Open in Colab](https://colab.research.google.com/github/lightning-rod-labs/lightningrod-python-sdk/blob/main/notebooks/fine_tuning/03_survival_llm.ipynb) |
| Military Strikes Forecasting | `notebooks/fine_tuning/04_military_strikes.ipynb` | [Open in Colab](https://colab.research.google.com/github/lightning-rod-labs/lightningrod-python-sdk/blob/main/notebooks/fine_tuning/04_military_strikes.ipynb) |

For full documentation, see [docs.lightningrod.ai](https://docs.lightningrod.ai/). For the SDK API reference in this repo, see [API.md](API.md).
