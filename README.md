<img width="2540" height="1520" alt="04-product-ui" src="https://github.com/user-attachments/assets/66056c7a-6c6e-4040-a1a0-9852f709a0c5" />


# Lightning Rod Python SDK

**Foresight** returns a calibrated probability for any question about the future through an OpenAI-compatible API.

**Trusted for high-stakes predictions** by Numinous, Shore Capital Partners, Awardable, ERIS Marketplace, and others. Foresight processes **billions of tokens** and serves **100k+ inference requests every day**.

[Documentation](https://docs.lightningrod.ai/) · [Get an API key](https://dashboard.lightningrod.ai/sign-up?redirect=/api) · [Research paper](https://arxiv.org/abs/2601.06336)

## ⚡ Better AI Predictions

Foresight is served behind an OpenAI-compatible endpoint, so any OpenAI client works — just point `base_url` at Lightning Rod.

```python
from openai import OpenAI

client = OpenAI(
    api_key="your-api-key",
    base_url="https://api.lightningrod.ai/v1/openai",
)

completion = client.chat.completions.create(
    model="foresight-v4",
    messages=[
        {"role": "user", "content": "Will the Fed cut rates at its next meeting?"},
    ],
    extra_body={"research": True}, # Auto research the most relevant prediction context
)

print(completion.choices[0].message.content)
```

See the [forecasting guides](https://docs.lightningrod.ai/forecasting/guides) for how to write good forecasting prompts.

### Prefer an SDK helper?

`lr.predict()` wraps the same API and parses the structured answer for you:

```bash
pip install lightningrod-ai
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

Need a model tuned to your domain? Our platform turns raw sources into labeled datasets and fine-tuned models. Read the [Future-as-Label paper](https://arxiv.org/abs/2601.06336) or view public models and datasets on [Hugging Face](https://huggingface.co/LightningRodLabs).

[**📅 Book a call with us**](https://calendly.com/d/ctq4-7gd-nyq/lightning-rod-demo)

## 📚 Learn more

- [Documentation](https://docs.lightningrod.ai/) — quickstart, guides, recipes, and the REST API reference
- [Example notebooks](notebooks/) — forecasting, dataset generation, training, and evaluation (runnable in Colab)
- [SDK API reference](API.md) — every class and method in this repo
