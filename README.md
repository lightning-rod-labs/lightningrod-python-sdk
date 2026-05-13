

# Lightning Rod Python SDK [Beta](https://pypi.org/project/lightningrod-ai/0.1.27/)

The Lightning Rod SDK provides a simple Python API for generating custom forecasting datasets to train your LLMs. Transform news articles, documents, and other real-world data into high-quality training samples automatically.

Based on our research: [Future-as-Label: Scalable Supervision from Real-World Outcomes](https://arxiv.org/abs/2601.06336)

Documentation: [docs.lightningrod.ai](https://docs.lightningrod.ai/)

## 👋 Quick Start

### 1. Install the SDK

Install for as a Python library:

```bash
pip install lightningrod-ai
```

Or install the Claude Code plugin for agentic use:

```bash
/plugin marketplace add lightning-rod-labs/lightningrod-python-sdk
/plugin install lightningrod-python-sdk
```

The plugin adds the lightningrod-assistant agent plus skills for forecasting datasets, content-learning datasets, tabular data, BigQuery seeds, custom files, and transform verification.

### 2. Get your API key

Sign up at [dashboard.lightningrod.ai](https://dashboard.lightningrod.ai/sign-up?redirect=/api) to get your API key and **$50 of free credits**.

```python
lr = LightningRod(api_key="your-api-key")
```

Or export your API key in the shell before starting Claude Code session for agentic use:

```bash
export LIGHTNINGROD_API_KEY="your-api-key
```

### 3. Generate your first dataset

Generate **1000+ forecasting questions easily** - from raw sources to labeled dataset, automatically. ⚡

```python
pipeline = QuestionPipeline(...)
dataset = lr.transforms.run(pipeline)
```

**We use this to generate the [Future-as-Label training dataset](https://huggingface.co/datasets/LightningRodLabs/future-as-label-paper-training-dataset) for our research paper.**

### 4. Train & eval a model on your dataset

Training a custom model is as easy as plugging in the generated dataset in the previous step:

```python
train_dataset, test_dataset = prepare_for_training(dataset)
train_config = GRPOTrainingConfig(base_model_id="openai/gpt-oss-120b")
training_job = lr.training.run()
eval_job = lr.evals.run_from_training_job(train_config, training_job, test_dataset)
```

### 5. Inference

You can perform inference on your fine-tuned models or use our frontier forecasting models like [Foresight-v3](notebooks/evaluation/01_foresight_model.ipynb).

```python
lr.predict(training_job.model_id, "Will the Fed cut rates by 25hp in the next 3 months?")
```

Check the [API docs](https://docs.lightningrod.ai/python-sdk/fine-tuning-beta/inference) for use with OpenAI compatible API.

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
| Foresight-v3 Model      | `notebooks/evaluation/01_foresight_model.ipynb`         | [Open in Colab](https://colab.research.google.com/github/lightning-rod-labs/lightningrod-python-sdk/blob/main/notebooks/evaluation/01_foresight_model.ipynb)         |
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