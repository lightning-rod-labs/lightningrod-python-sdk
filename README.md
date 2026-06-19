

# Lightning Rod Python SDK

**Foresight** returns a calibrated probability for any question about the future — through an OpenAI-compatible API. No fine-tuning, no setup. Ranked **#1 for forecasting accuracy on ProphetArena**.

**Trusted for high-stakes predictions** by Numinous, Shore Capital Partners, Awardable (Tradewinds Solutions Marketplace), and ERIS Marketplace. Foresight processes **billions of tokens** and serves **100k+ inference requests every day**.

[Documentation](https://docs.lightningrod.ai/) · [Get an API key](https://dashboard.lightningrod.ai/sign-up?redirect=/api) · [Research paper](https://arxiv.org/abs/2601.06336)

## ⚡ Better predictions in seconds

Foresight is served behind an OpenAI-compatible endpoint, so any OpenAI client works — just point `base_url` at Lightning Rod.

```bash
pip install openai
```

```python
from openai import OpenAI

client = OpenAI(
    base_url="https://api.lightningrod.ai/api/public/v1/openai",
    api_key="your-api-key",
)

completion = client.chat.completions.create(
    model="LightningRodLabs/foresight-v4",
    messages=[
        {"role": "user", "content": "Will the Fed cut rates at its next meeting?"},
    ],
    extra_body={
        "research": True,       # gather live web evidence before forecasting
        "answer_type": "auto",  # append a structured answer in <answer></answer> tags
    },
)

print(completion.choices[0].message.content)
# Foresight weighs the evidence and returns a calibrated probability,
# e.g.: "... <answer>0.34</answer>"
```

That `0.34` is a **calibrated probability** — a 34% chance, not a confidence score or a yes/no. `0.5` means genuinely uncertain, and across many ~0.7 forecasts roughly 70% should come true. See the [forecasting reference](https://docs.lightningrod.ai/forecasting/reference) for answer types, research sources, and the full response shape.

### Prefer an SDK helper?

`lr.predict()` wraps the same API and parses the structured answer for you:

```bash
pip install lightningrod-ai openai
```

```python
import lightningrod as lr

client = lr.LightningRod(api_key="your-api-key")
result = client.predict(
    "Will the Fed cut rates by 25bp in March 2026?",
    answer_type="binary",
    research=True,
)
print(result.binary.probability)  # e.g. 0.62
```

## 🏗️ Train an expert on your domain

Need a model tuned to your domain? Our enterprise platform enables companies to turn raw sources into labeled datasets and fine-tunes models on them — served through the same API.

[**📅 Book a call with us**](https://calendly.com/d/ctq4-7gd-nyq/lightning-rod-demo)

```python
pipeline = QuestionPipeline(...)
dataset = client.transforms.run(pipeline)

train_dataset, test_dataset = prepare_for_training(dataset)
train_config = GRPOTrainingConfig(base_model_id="openai/gpt-oss-120b")
training_job = client.training.run(train_config, train_dataset)

# your fine-tuned model is served through the same predict() / OpenAI API
client.predict("Will the Fed cut rates by 25bp in the next 3 months?", model=training_job.model_id)
```

We used this to generate the [Future-as-Label training dataset](https://huggingface.co/datasets/LightningRodLabs/future-as-label-paper-training-dataset) from our paper, [Future-as-Label: Scalable Supervision from Real-World Outcomes](https://arxiv.org/abs/2601.06336).

## 📚 Learn more

- [Documentation](https://docs.lightningrod.ai/) — quickstart, guides, recipes, and the REST API reference
- [Example notebooks](notebooks/) — forecasting, dataset generation, training, and evaluation (runnable in Colab)
- [SDK API reference](API.md) — every class and method in this repo

