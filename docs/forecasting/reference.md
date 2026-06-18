---
icon: chart-line
description: Calibrated probability forecasts from Lightning Rod's Foresight models via an OpenAI-compatible API. Models, usage paths, request fields, answer types, and the response shape.
---

![LLMs tuned on our data have outperformed frontier models](../.gitbook/assets/forecasting.png)

Lightning Rod's **Foresight** models return calibrated probability forecasts for any forward-looking question, through an OpenAI-compatible API. No training and no dataset required—get an API key, ask a question, receive a probability distribution in the response.

> **Reading the result.** A `binary` answer like `0.62` is a *calibrated probability*—a 62% chance, not a confidence score or a yes/no. `0.5` means genuinely uncertain, and the model is right "on average": across many forecasts marked ~0.7, roughly 70% should resolve true. Judge Foresight over a *set* of questions, not a single call. See [Guides](guides.md) for how to write questions and interpret probabilities.

Forecasting is available through the same model-serving API in two ways:

- Use the **LightningRod `predict()` helper** for a single call that takes Lightning Rod options as keyword arguments and returns a parsed `PredictionResult` with the probability already extracted. Easiest place to start.
- Use the **OpenAI-compatible chat/completions endpoint** when you want full control over messages, OpenAI client/framework compatibility, streaming, or raw response handling.

Both paths call the same underlying API. The main difference is where request fields go and how much response parsing the SDK does for you.

## Predict API

The fastest way to get a forecast: one call that returns a parsed `PredictionResult` with the probability already pulled out of the response—no tag parsing on your end. This is the recommended starting point.

```python
# pip install lightningrod-ai openai
import lightningrod as lr

client = lr.LightningRod(api_key="your-api-key")

result = client.predict(
    "Will the Fed cut rates by 25bp in March 2026?",  # prompt: the question, sent as a single user message (first positional arg)
    answer_type="binary",                             # structured answer format: "binary" | "multiple_choice" | "continuous" | "free_response" | "auto". Omit for prose only
    research=["perplexity", "news"],                  # web research: True for all sources, a list to select sources, or omit/False to disable
)

print(result.binary.probability)  # e.g. 0.62  — a calibrated 62% probability
print(result.sources)             # URL citations gathered during research
```

`predict()` also takes `model`, `system_prompt`, `reasoning_effort`, and any standard chat/completions field (`temperature`, `max_tokens`, …) as keyword arguments:

```python
result = client.predict(
    "Will the Fed cut rates by 25bp in March 2026?",  # prompt: the question, sent as a single user message (first positional arg)
    model="LightningRodLabs/foresight-v4",            # model to query; short or full provider ID. Optional—defaults to the latest Foresight model
    system_prompt="Give calibrated forecasts and cite sources when research is used.",  # optional, prepended as a system message
    answer_type="binary",                             # structured answer format: "binary" | "multiple_choice" | "continuous" | "free_response" | "auto". Omit for prose only
    research=["perplexity", "news"],                  # web research: True for all sources, a list to select sources, or omit/False to disable
    reasoning_effort="high",                          # reasoning budget: "low" | "medium" | "high". Defaults to "medium"
    temperature=0.2,                                  # standard chat/completions fields (temperature, max_tokens, top_p, ...) are forwarded as **kwargs
    max_tokens=2048,                                  # forwarded to openai.chat.completions.create
)

print(result.binary.probability)  # e.g. 0.62
print(result.content)             # full prose response with <answer> tags
print(result.thinking)            # reasoning chain
print(result.usage.cost_usd)      # cost of the call
```

### Response

| Field             | Type                    | Description                                                     |
| ----------------- | ----------------------- | --------------------------------------------------------------- |
| `content`         | `str`                   | Full raw response, including prose and any `<answer>` tags.     |
| `thinking`        | `str \| None`           | Reasoning chain, when returned by the model.                    |
| `sources`         | `list[Source]`          | URL citations from research. Each source has `url` and `title`. |
| `usage`           | `Usage`                 | Token counts and cost fields.                                   |
| `model`           | `str`                   | Model that served the request.                                  |
| `id`              | `str`                   | Response ID.                                                    |
| `binary`          | `BinaryPrediction \| None`       | Populated when `answer_type="binary"`.            |
| `continuous`      | `ContinuousPrediction \| None`   | Populated when `answer_type="continuous"`.        |
| `multiple_choice` | `MultiChoicePrediction \| None`  | Populated when `answer_type="multiple_choice"`.   |
| `free_response`   | `FreeResponsePrediction \| None` | Populated when `answer_type="free_response"`.     |

`Usage` includes `prompt_tokens`, `completion_tokens`, `total_tokens`, and cost fields: `cost_usd`, `inference_cost_usd`, `research_cost_usd`, and `classification_cost_usd` when applicable.

## OpenAI API

All our models are served using an OpenAI-compatible endpoint, so any OpenAI client works out of the box—just point it at the Lightning Rod base URL.

```python
# pip install openai
from openai import OpenAI

client = OpenAI(
    api_key="your-api-key",
    base_url="https://api.lightningrod.ai/api/public/v1/openai",
)

response = client.chat.completions.create(
    model="LightningRodLabs/foresight-v4",            # model to query; accepts short or full provider ID (full form shown here)
    messages=[                                        # full chat history; the system instruction is just a system-role message
        {"role": "system", "content": "Give calibrated forecasts and cite sources when research is used.",},
        {"role": "user", "content": "Will the Fed cut rates by 25bp in March 2026?"},
    ],
    temperature=0.2,                                  # standard OpenAI fields (temperature, max_tokens, top_p, ...) are top-level request fields
    max_tokens=2048,
    extra_body={                                      # Lightning Rod-specific fields go inside extra_body
        "answer_type": "binary",                      # structured answer format: "binary" | "multiple_choice" | "continuous" | "free_response" | "auto". Omit for prose only
        "research": {"sources": ["perplexity", "news"]},  # web research: True for all sources, or {"sources": [...]} to select sources
        "reasoning_effort": "high",                   # reasoning budget: "low" | "medium" | "high"
    },
)

message = response.choices[0].message
print(message.content)
```

OpenAI-standard fields such as `messages`, `temperature`, `max_tokens`, and `top_p` are sent as normal chat/completions fields. Lightning Rod-specific fields go in `extra_body`.

Use this path when you need multi-turn conversations, an existing OpenAI-compatible framework such as LangChain or LiteLLM, streaming, or direct access to the raw response object.

### Response

When calling the OpenAI-compatible endpoint directly, the same data is on the chat/completion response:

- `response.choices[0].message.content` — full response; structured answer embedded between `<answer></answer>` tags when `answer_type` is set.
- `response.choices[0].message.thinking` — reasoning chain, when returned by the model.
- `response.choices[0].message.annotations` — `url_citation` entries, present only when research ran.
- `response.usage` — token counts plus Lightning Rod cost fields such as `cost_usd`, `inference_cost_usd`, `research_cost_usd`, and `classification_cost_usd`.

For a plain dictionary with all provider-specific fields, use:

```python
data = response.model_dump()
usage = data["usage"]
annotations = data["choices"][0]["message"].get("annotations", [])
```

See the [REST API reference](https://docs.lightningrod.ai/rest-api#post-openai-chat-completions) for full endpoint details.

## Models

Both `predict()` and the OpenAI-compatible endpoint accept the same model IDs—either the short form or the full provider form. `predict()` defaults to the latest model (`LightningRodLabs/foresight-v4`) when `model` is omitted.

| Model | Model ID | Description |
|-------|----------|-------------|
| Foresight v4 | `LightningRodLabs/foresight-v4` | **New** version of our frontier forecasting model. |
| Foresight v3 | `LightningRodLabs/foresight-v3` |  |

Foresight models are always available—no training or hosting setup required. Fine-tuned models you train on the [Platform](../platform/overview.md) are served through the same interface; pass the trained `model_id` to either `client.predict(...)` or `client.chat.completions.create(...)`. See [Inference](../platform/fine-tuning/inference.md) for their model IDs and availability.

Each call reports its cost on the response (`result.usage.cost_usd`), broken down into inference and—when applicable—research and classification costs. See [dashboard.lightningrod.ai](https://dashboard.lightningrod.ai) for current rates.

## Parameters

These are custom Lightning Rod extensions to the standard OpenAI API compatible parameters. They can be used both in the OpenAI compatible endpoints (under `extra_body`) and our predict helper.

| Parameter          | Values                                                                       | Description                                                                                                                                                            |
| ------------------ | ---------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `answer_type`      | `"binary"`, `"multiple_choice"`, `"continuous"`, `"free_response"`, `"auto"` | Adds output-format guidance and appends a structured answer between `<answer></answer>` tags. `"auto"` classifies the question server-side first. Omit for prose only. |
| `research`         | `True`, or selected source keys (`"perplexity"`, `"news"`, `"google_search"`) | Opt-in web research before forecasting. Each source key maps to a distinct research provider the model can pull live evidence from: `"perplexity"` (Perplexity web search), `"news"` (recent news articles), and `"google_search"` (Google results). `True` queries all of them; pass a subset to control cost and which evidence the model sees. Each source runs as its own query and is billed as a separate research event. |
| `reasoning_effort` | `"low"`, `"medium"`, `"high"`                                                | How much reasoning the model spends before answering. `predict()` defaults to `"medium"`. Higher effort helps on harder questions.                                     |
| `system_prompt`    | string                                                                       | Optional system message. In raw chat/completions requests, add this to `messages`; in `predict()`, use the first-class keyword argument.                               |


## Answer Types

When `answer_type` is set, the full response still includes prose in `content`, followed by machine-readable tags. `predict()` parses those tags and populates the matching typed field on `PredictionResult`.

| `answer_type`       | Raw response shape                                                                           | `PredictionResult` field                                                 |
| ------------------- | -------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------ |
| `"binary"`          | `<answer>0.62</answer>`                                                                      | `result.binary.probability`                                              |
| `"continuous"`      | `<answer>{"mean": 42.5, "standard_deviation": 5.2}</answer>`                                 | `result.continuous.mean`, `result.continuous.standard_deviation`         |
| `"multiple_choice"` | `<options>{"A": "...", "B": "..."}</options>` plus `<answer>{"A": 0.55, "B": 0.45}</answer>` | `result.multiple_choice.options`, `result.multiple_choice.probabilities` |
| `"free_response"`   | `<answer>...</answer>`                                                                       | `result.free_response.text`                                              |
| `"auto"`            | Server-selected structured answer                                                            | Best-effort parsed into one of the typed fields                          |

At most one typed answer field is populated. If no `answer_type` is requested, all typed answer fields are `None` and the full prose response is available as `result.content`.

## Enterprise

Need forecasting models tailored to your domain, proprietary data, or internal workflows? Lightning Rod's enterprise platform helps teams generate forecasting datasets, fine-tune specialized models, evaluate performance, and serve those models through the same API.

[Book a call](https://calendly.com/d/ctq4-7gd-nyq/lightning-rod-demo) to talk through your use case.

## Next steps

* [Guides](guides.md) — writing good questions and interpreting probabilities
* [Recipes](recipes.md) — Polymarket backtesting, model consensus, and more
* [Platform Overview](../platform/overview.md) — generate datasets and fine-tune your own forecasting models
