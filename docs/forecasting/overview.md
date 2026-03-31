---
icon: chart-line
---

![LLMs tuned on our data have outperformed frontier models](../.gitbook/assets/forecasting.png)

# Forecasting

Get probability estimates on binary forecasting questions with Lightning Rod's hosted models. No training required—call the API and receive calibrated forecasts.

## Foresight-v3

**foresight-v3** is Lightning Rod's latest forecasting model. Pass any binary forecasting question and receive a probability estimate between 0 and 1. Use it via the OpenAI-compatible API.

### Setup

Sign up at [dashboard.lightningrod.ai](https://dashboard.lightningrod.ai/sign-up?redirect=/api) to get your API key and **$50 of free credits**.

```bash
pip install openai lightningrod-ai
```

```python
from openai import OpenAI

client = OpenAI(
    api_key="lightningrod-api-key", 
    base_url="https://api.lightningrod.ai/api/public/v1/openai"
)
```

### Get forecasts

Pass any forecasting question to foresight-v3.

```python
questions = [
    "Will the Fed cut rates by 25bp in March 2026?",
    "Will Apple announce a new Vision Pro model in 2026?",
    "Will the S&P 500 close above 6000 by end of 2026?",
]

for q in questions:
    response = client.chat.completions.create(
        model="LightningRodLabs/foresight-v3",
        messages=[
            {"role": "system", "content": "Answer as a probability between 0 and 1."},
            {"role": "user", "content": q}
        ]
    )
    print(f"Q: {q}")
    print(f"A: {response.choices[0].message.content}\n")
```

### API reference

See the [API docs](https://dashboard.lightningrod.ai/public/docs#tag/openai-compatible/post/openai/chat/completions) for full details on parameters (temperature, max_tokens, etc.).

## Try it

Run the [foresight-v3 notebook](https://colab.research.google.com/github/lightning-rod-labs/lightningrod-python-sdk/blob/main/notebooks/evaluation/01_foresight_model.ipynb) in Google Colab for a complete walkthrough.
