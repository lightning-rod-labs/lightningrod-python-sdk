<div align="center">
<!-- Note: only an absolute image URL works on PyPi: https://pypi.org/project/lightningrod-ai -->
  <img src="https://github.com/lightning-rod-labs/lightningrod-python-sdk/blob/main/banner.png?raw=true" alt="Lightning Rod Labs" />
</div>

# Lightning Rod Python SDK [![Beta](https://img.shields.io/badge/beta-0.1.27-orange)](https://pypi.org/project/lightningrod-ai/0.1.27/)

Lightning Rod's **Foresight** models return calibrated probability forecasts for any forward-looking question, through an OpenAI-compatible API. Ask a question, get a probability — no training and no dataset required. The SDK also includes a platform to generate forecasting datasets and fine-tune your own models.

Based on our research: [Future-as-Label: Scalable Supervision from Real-World Outcomes](https://arxiv.org/abs/2601.06336)

Documentation: [docs.lightningrod.ai](https://docs.lightningrod.ai/)

## 👋 Quick Start

### 1. Install the SDK

Install as a Python library:

```bash
pip install lightningrod-ai openai
```

`lr.predict()` uses the `openai` package under the hood, so install both.

### 2. Get your API key

Sign up at [dashboard.lightningrod.ai](https://dashboard.lightningrod.ai/sign-up?redirect=/api) to get your API key.

```python
import lightningrod as lr

client = lr.LightningRod(api_key="your-api-key")
```

### 3. Get your first forecast ⚡

```python
result = client.predict(
    "foresight-v4",
    "Will the Fed cut rates by 25bp in March 2026?",
    answer_type="binary",
)
print(result.binary.probability)  # e.g. 0.62
```

Add `research=True` to let the model gather live web evidence first, or `reasoning_effort="high"` for harder questions. `foresight-v4` is also served behind an [OpenAI-compatible API](https://docs.lightningrod.ai/forecasting/quickstart) for use with any OpenAI client or framework.

## 🏗️ Platform: build your own forecasting model

Need a model tuned to your domain? The platform turns raw sources into labeled datasets and fine-tunes models on them.

Install the Claude Code plugin for agentic use:

```bash
/plugin marketplace add lightning-rod-labs/lightningrod-python-sdk
/plugin install lightningrod-python-sdk
```

The plugin adds the lightningrod-assistant agent plus skills for forecasting datasets, content-learning datasets, tabular data, BigQuery seeds, custom files, and transform verification. Export your API key before starting a Claude Code session:

```bash
export LIGHTNINGROD_API_KEY="your-api-key"
```

### 1. Generate a dataset

Generate **1000+ forecasting questions easily** — from raw sources to labeled dataset, automatically.

```python
pipeline = QuestionPipeline(...)
dataset = client.transforms.run(pipeline)
```

**We use this to generate the [Future-as-Label training dataset](https://huggingface.co/datasets/LightningRodLabs/future-as-label-paper-training-dataset) for our research paper.**

### 2. Train & eval a model on your dataset

Training a custom model is as easy as plugging in the generated dataset from the previous step:

```python
train_dataset, test_dataset = prepare_for_training(dataset)
train_config = GRPOTrainingConfig(base_model_id="openai/gpt-oss-120b")
training_job = client.training.run()
eval_job = client.evals.run_from_training_job(train_config, training_job, test_dataset)
```

### 3. Forecast with your model

Your fine-tuned model is served through the same `predict()` API:

```python
client.predict(training_job.model_id, "Will the Fed cut rates by 25bp in the next 3 months?")
```

Check the [API docs](https://docs.lightningrod.ai/forecasting/quickstart) for use with the OpenAI-compatible API.

## ✨ Examples

We have example notebooks to help you get started. If you have trouble using the SDK, please submit an issue on GitHub.

### Quick Start


| Example Name | Path                            | Google Colab Link                                                                                                                            |
| ------------ | ------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------- |
| Quick Start  | `notebooks/00_quickstart.ipynb` | [Open in Colab](https://colab.research.google.com/github/lightning-rod-labs/lightningrod-python-sdk/blob/main/notebooks/00_quickstart.ipynb) |


### Getting Started


| Example Name        | Path                                                             | Google Colab Link                                                                                                                                                             |
| ------------------- | ---------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| News Datasource     | `notebooks/getting_started/01_news_datasource.ipynb`             | [Open in Colab](https://colab.research.google.com/github/lightning-rod-labs/lightningrod-python-sdk/blob/main/notebooks/getting_started/01_news_datasource.ipynb)             |
| Custom Documents    | `notebooks/getting_started/02_custom_documents_datasource.ipynb` | [Open in Colab](https://colab.research.google.com/github/lightning-rod-labs/lightningrod-python-sdk/blob/main/notebooks/getting_started/02_custom_documents_datasource.ipynb) |
| BigQuery Datasource | `notebooks/getting_started/03_bigquery_datasource.ipynb`         | [Open in Colab](https://colab.research.google.com/github/lightning-rod-labs/lightningrod-python-sdk/blob/main/notebooks/getting_started/03_bigquery_datasource.ipynb)         |
| Answer Types        | `notebooks/getting_started/04_answer_types.ipynb`                | [Open in Colab](https://colab.research.google.com/github/lightning-rod-labs/lightningrod-python-sdk/blob/main/notebooks/getting_started/04_answer_types.ipynb)                |
| GRPO Training       | `notebooks/getting_started/05_grpo_training.ipynb`               | [Open in Colab](https://colab.research.google.com/github/lightning-rod-labs/lightningrod-python-sdk/blob/main/notebooks/getting_started/05_grpo_training.ipynb)               |
| SFT Training        | `notebooks/getting_started/06_sft_training.ipynb`                | [Open in Colab](https://colab.research.google.com/github/lightning-rod-labs/lightningrod-python-sdk/blob/main/notebooks/getting_started/06_sft_training.ipynb)                |
| Embedding Dedup     | `notebooks/getting_started/08_embedding_deduplication.ipynb`     | [Open in Colab](https://colab.research.google.com/github/lightning-rod-labs/lightningrod-python-sdk/blob/main/notebooks/getting_started/08_embedding_deduplication.ipynb)     |


### Custom Filesets


| Example Name                   | Path                                                     | Google Colab Link                                                                                                                                                     |
| ------------------------------ | -------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Create Fileset                 | `notebooks/custom_filesets/01_create_fileset.ipynb`      | [Open in Colab](https://colab.research.google.com/github/lightning-rod-labs/lightningrod-python-sdk/blob/main/notebooks/custom_filesets/01_create_fileset.ipynb)      |
| Basic QA Generation            | `notebooks/custom_filesets/02_basic_qa_generation.ipynb` | [Open in Colab](https://colab.research.google.com/github/lightning-rod-labs/lightningrod-python-sdk/blob/main/notebooks/custom_filesets/02_basic_qa_generation.ipynb) |
| Advanced Features              | `notebooks/custom_filesets/03_advanced_features.ipynb`   | [Open in Colab](https://colab.research.google.com/github/lightning-rod-labs/lightningrod-python-sdk/blob/main/notebooks/custom_filesets/03_advanced_features.ipynb)   |
| Beige Book (Document Labeling) | `notebooks/custom_filesets/04_beige_book_e2e.ipynb`      | [Open in Colab](https://colab.research.google.com/github/lightning-rod-labs/lightningrod-python-sdk/blob/main/notebooks/custom_filesets/04_beige_book_e2e.ipynb)      |


### Answer Types


| Example Name    | Path                                        | Google Colab Link                                                                                                                                        |
| --------------- | ------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Binary          | `notebooks/answer_types/binary.ipynb`       | [Open in Colab](https://colab.research.google.com/github/lightning-rod-labs/lightningrod-python-sdk/blob/main/notebooks/answer_types/binary.ipynb)       |
| Continuous      | `notebooks/answer_types/continuous.ipynb`   | [Open in Colab](https://colab.research.google.com/github/lightning-rod-labs/lightningrod-python-sdk/blob/main/notebooks/answer_types/continuous.ipynb)   |
| Multiple Choice | `notebooks/answer_types/multi-choice.ipynb` | [Open in Colab](https://colab.research.google.com/github/lightning-rod-labs/lightningrod-python-sdk/blob/main/notebooks/answer_types/multi-choice.ipynb) |


### Evaluation


| Example Name            | Path                                                    | Google Colab Link                                                                                                                                                    |
| ----------------------- | ------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Foresight-v4 Model      | `notebooks/evaluation/01_foresight_model.ipynb`         | [Open in Colab](https://colab.research.google.com/github/lightning-rod-labs/lightningrod-python-sdk/blob/main/notebooks/evaluation/01_foresight_model.ipynb)         |
| Model Consensus         | `notebooks/evaluation/02_model_consensus.ipynb`         | [Open in Colab](https://colab.research.google.com/github/lightning-rod-labs/lightningrod-python-sdk/blob/main/notebooks/evaluation/02_model_consensus.ipynb)         |
| Polymarket Backtesting  | `notebooks/evaluation/03_polymarket_backtesting.ipynb`  | [Open in Colab](https://colab.research.google.com/github/lightning-rod-labs/lightningrod-python-sdk/blob/main/notebooks/evaluation/03_polymarket_backtesting.ipynb)  |
| Document Classification | `notebooks/evaluation/04_document_classification.ipynb` | [Open in Colab](https://colab.research.google.com/github/lightning-rod-labs/lightningrod-python-sdk/blob/main/notebooks/evaluation/04_document_classification.ipynb) |


### Fine Tuning


| Example Name                 | Path                                               | Google Colab Link                                                                                                                                               |
| ---------------------------- | -------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Golf Forecasting             | `notebooks/fine_tuning/01_golf_forecasting.ipynb`  | [Open in Colab](https://colab.research.google.com/github/lightning-rod-labs/lightningrod-python-sdk/blob/main/notebooks/fine_tuning/01_golf_forecasting.ipynb)  |
| Trump Forecasting            | `notebooks/fine_tuning/02_trump_forecasting.ipynb` | [Open in Colab](https://colab.research.google.com/github/lightning-rod-labs/lightningrod-python-sdk/blob/main/notebooks/fine_tuning/02_trump_forecasting.ipynb) |
| Survival LLM                 | `notebooks/fine_tuning/03_survival_llm.ipynb`      | [Open in Colab](https://colab.research.google.com/github/lightning-rod-labs/lightningrod-python-sdk/blob/main/notebooks/fine_tuning/03_survival_llm.ipynb)      |
| Military Strikes Forecasting | `notebooks/fine_tuning/04_military_strikes.ipynb`  | [Open in Colab](https://colab.research.google.com/github/lightning-rod-labs/lightningrod-python-sdk/blob/main/notebooks/fine_tuning/04_military_strikes.ipynb)  |


For full documentation, see [docs.lightningrod.ai](https://docs.lightningrod.ai/). For the SDK API reference in this repo, see [API.md](API.md).