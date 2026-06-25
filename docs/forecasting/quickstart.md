---
icon: bolt
description: Forecasting API quickstart.
---

Lightning Rod's **Foresight** models return calibrated probability forecasts for any forward-looking question through an OpenAI-compatible API.


## Your first prediction

To get started, [get an API key](https://dashboard.lightningrod.ai/sign-up?redirect=/api) in our dashboard and configure the `api_key` and `base_url` of any [OpenAI API client](https://developers.openai.com/api/docs/libraries) or query [our REST API](https://docs.lightningrod.ai/api-reference) directly.

Minimal example code using Python:

```python
from openai import OpenAI

client = OpenAI(
    api_key="your-api-key",
    base_url="https://api.lightningrod.ai/v1/openai",
)

response = client.chat.completions.create(
    model="foresight-v4",
    messages=[
        {"role": "user", "content": "Will Elon Musk still be the richest person by 2030?"},
    ],
)
print(response.choices[0].message.content)
```

## Available Models

| Model | Model ID | Description |
|-------|----------|-------------|
| Foresight v4 | `foresight-v4` | Latest forecasting model. |
| Foresight v3 | `foresight-v3` | Previous forecasting model. |

## Structured Prediction

The unstructured result is useful when the response message consumer is a human or an LLM, but for programmatic use you'll probably want a structured prediction response.

We offer a custom `answer_type` extension parameter to achieve exactly that. We recommend using our [SDK](./sdk.md) to automatically parse the responses, but if you want to use a standard OpenAI client please refer to [our answer format guide](./openai.md).

## Prediction Context

By default, none of the models have access to external sources - they are limited by the context they were trained on.

To achieve accurate and useful prediction results, you should always provide relevant context alongside your question. There are currently two ways of doing that:
1. provide your own custom-aggregated context (this is the "secret sauce" that can give you an edge)
2. use our built-in "research mode" to automatically gather relevant context from trusted sources like Perplexity or Google News

See how you can configure research mode using [OpenAI clients](openai.md) or our [Python SDK](sdk.md).

## Custom Models

Need forecasting models tailored to your domain? Use the [enterprise platform](../platform/overview.md) to generate datasets, fine-tune models, and evaluate performance.

[Book a call](https://calendly.com/d/ctq4-7gd-nyq/lightning-rod-demo) to talk through your use case.

## Next steps

* [OpenAI](openai.md) - how to effectively use our OpenAI API
* [SDK](sdk.md) - Python wrapper on top of the OpenAI API for ease of use
* [Recipes](recipes.md) — writing good forecasting prompts
* [Enterprise Platform](../platform/overview.md) — generate datasets and fine-tune your own forecasting models
