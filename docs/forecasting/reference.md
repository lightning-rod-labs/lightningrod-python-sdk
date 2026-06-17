---
icon: chart-line
description: Calibrated probability forecasts from Lightning Rod's Foresight models via an OpenAI-compatible API. Models, usage paths, request fields, answer types, and the response shape.
---

![LLMs tuned on our data have outperformed frontier models](../.gitbook/assets/forecasting.png)

# Forecasting Reference

Lightning Rod's **Foresight** models return calibrated probability forecasts for any forward-looking question, through an OpenAI-compatible API. No training and no dataset required—get an API key, ask a question, receive a probability.

Forecasting is available through the same model-serving API in two ways:

- Use the **OpenAI-compatible chat/completions endpoint** when you want full control over messages, OpenAI client/framework compatibility, streaming, or raw response handling.
- Use the **`LightningRod.predict()` helper** when you want a single-call SDK wrapper that accepts Lightning Rod-specific options as keyword arguments and returns a parsed `PredictionResult`.

Both paths call the same underlying API. The main difference is where request fields go and how much response parsing the SDK does for you.

## Setup

```bash
pip install lightningrod-ai openai
```

`lr.predict()` uses the `openai` package under the hood, so install both. Sign up at [dashboard.lightningrod.ai](https://dashboard.lightningrod.ai/sign-up?redirect=/api) to get your API key.

## Making predictions

### Predict helper

`predict()` is the SDK convenience wrapper for a single prompt. It returns a structured `PredictionResult`—the parsed answer, the reasoning chain, any sources, and cost.

```python
import lightningrod as lr

client = lr.LightningRod(api_key="your-api-key")

# Note: requires installation of openai client (pip install openai)
result = client.predict(
    "foresight-v4",
    "Will the Fed cut rates by 25bp in March 2026?",
    answer_type="binary",
    research=["perplexity", "news"],
    reasoning_effort="high",
    system_prompt="Give calibrated forecasts and cite sources when research is used.",
    temperature=0.2,
)

print(result.binary.probability)  # e.g. 0.62
print(result.content)             # full prose response with <answer> tags
print(result.thinking)            # reasoning chain
print(result.usage.cost_usd)      # cost of the call
```

The helper builds the chat/completions request for you:

- `prompt` becomes a single user message.
- `system_prompt`, when provided, becomes a system message before the user message.
- `answer_type`, `research`, and `reasoning_effort` are placed into the request body for you.
- Additional keyword arguments are forwarded to `openai.chat.completions.create`.
- The response is parsed into `PredictionResult`, including typed answer fields when possible.

Use this path when you have one prompt and want parsed answer, sources, reasoning, and cost fields without manually unpacking the OpenAI response.

### OpenAI Chat/Completions

`foresight-v4` is served behind an OpenAI-compatible endpoint, so any OpenAI client or framework (LangChain, LiteLLM, Vercel AI SDK) works—point it at the Lightning Rod base URL. Pass Lightning Rod-specific fields via `extra_body`.

```python
from openai import OpenAI

client = OpenAI(
    api_key="your-api-key",
    base_url="https://api.lightningrod.ai/api/public/v1/openai",
)

response = client.chat.completions.create(
    model="LightningRodLabs/foresight-v4",
    messages=[
        {
            "role": "system",
            "content": "Give calibrated forecasts and cite sources when research is used.",
        },
        {"role": "user", "content": "Will the Fed cut rates by 25bp in March 2026?"},
    ],
    temperature=0.2,
    extra_body={
        "answer_type": "binary",
        "research": {"sources": ["perplexity", "news"]},
        "reasoning_effort": "high",
    },
)

message = response.choices[0].message
print(message.content)
```

OpenAI-standard fields such as `messages`, `temperature`, `max_tokens`, and `top_p` are sent as normal chat/completions fields. Lightning Rod-specific fields go in `extra_body`.

Use this path when you need multi-turn conversations, an existing OpenAI-compatible framework such as LangChain or LiteLLM, streaming, or direct access to the raw response object.

## Models

Hosted Foresight models use short IDs in `predict()` and full provider IDs through the OpenAI-compatible endpoint:

| Model | `predict()` ID | OpenAI-compatible ID | Description |
|-------|----------------|----------------------|-------------|
| Foresight v4 | `foresight-v4` | `LightningRodLabs/foresight-v4` | **Latest** hosted forecasting model. Calibrated probabilities for forward-looking questions. Recommended for new projects. |
| Foresight v3 | `foresight-v3` | `LightningRodLabs/foresight-v3` | Previous generation, still available for compatibility and benchmark comparisons. |

Foresight models are always available—no training or hosting setup required. Fine-tuned models you train on the [Platform](../platform/overview.md) are served through the same interface; pass the trained `model_id` to either `client.predict(...)` or `client.chat.completions.create(...)`. See [Inference](../platform/fine-tuning/inference.md) for their model IDs and availability.

Each call reports its cost on the response (`result.usage.cost_usd`), broken down into inference and—when applicable—research and classification costs. See [dashboard.lightningrod.ai](https://dashboard.lightningrod.ai) for current rates.

## Request Fields

| Field                                | OpenAI chat/completions                                               | Predict helper                        | Description                                                                 |
| ------------------------------------ | --------------------------------------------------------------------- | ------------------------------------- | --------------------------------------------------------------------------- |
| `model` / `model_id`                 | `model="LightningRodLabs/foresight-v4"`                               | first argument, e.g. `"foresight-v4"` | Model to query. Use the ID form for your usage path.                        |
| `messages` / `prompt`                | `messages=[...]`                                                      | second argument, `prompt`             | Raw API accepts full chat history. `predict()` accepts one prompt string.   |
| `system_prompt`                      | Add a `{"role": "system"}` message                                    | `system_prompt="..."`                 | Optional system instruction.                                                |
| `answer_type`                        | `extra_body={"answer_type": "binary"}`                                | `answer_type="binary"`                | Requests a structured answer format.                                        |
| `research`                           | `extra_body={"research": True}` or `{"research": {"sources": [...]}}` | `research=True` or `research=[...]`   | Opts into web research before forecasting.                                  |
| `reasoning_effort`                   | `extra_body={"reasoning_effort": "high"}`                             | `reasoning_effort="high"`             | Controls how much reasoning the model spends before answering.              |
| `temperature`, `max_tokens`, `top_p` | top-level request fields                                              | keyword arguments                     | Forwarded to the chat/completions request.                                  |
| `extra_body`                         | direct request field                                                  | advanced keyword argument             | Use for lower-level API fields not exposed as first-class helper arguments. |

When using `predict()`, first-class keyword arguments win over the same keys inside `extra_body`.

## Lightning Rod Parameters

| Parameter          | Values                                                                       | Description                                                                                                                                                            |
| ------------------ | ---------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `answer_type`      | `"binary"`, `"multiple_choice"`, `"continuous"`, `"free_response"`, `"auto"` | Adds output-format guidance and appends a structured answer between `<answer></answer>` tags. `"auto"` classifies the question server-side first. Omit for prose only. |
| `research`         | `True`, or selected sources                                                  | Opt-in web research before forecasting. `True` queries all sources; pass selected sources to limit research. Each source is billed as a separate research event.       |
| `reasoning_effort` | `"low"`, `"medium"`, `"high"`                                                | How much reasoning the model spends before answering. `predict()` defaults to `"medium"`. Higher effort helps on harder questions.                                     |
| `system_prompt`    | string                                                                       | Optional system message. In raw chat/completions requests, add this to `messages`; in `predict()`, use the first-class keyword argument.                               |

Research source IDs are `perplexity`, `news`, and `google_search`.

With a raw OpenAI client, selected research sources use the object form:

```python
extra_body={"research": {"sources": ["perplexity", "news"]}}
```

With `predict()`, pass the list directly:

```python
result = client.predict(
    "foresight-v4",
    "Will the Fed cut rates by 25bp in March 2026?",
    research=["perplexity", "news"],
)
```

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

## Prediction result

`LightningRod.predict()` returns a structured `PredictionResult`:

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

> **Note:** `predict()` previously returned the raw content string. It now returns a `PredictionResult`; the raw string is available as `result.content`.

## Raw OpenAI Response

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

## Enterprise

Need forecasting models tailored to your domain, proprietary data, or internal workflows? Lightning Rod's enterprise platform helps teams generate forecasting datasets, fine-tune specialized models, evaluate performance, and serve those models through the same API.

[Book a call](https://calendly.com/d/ctq4-7gd-nyq/lightning-rod-demo) to talk through your use case.

## Next steps

* [Guides](guides.md) — writing good questions and interpreting probabilities
* [Recipes](recipes.md) — Polymarket backtesting, model consensus, and more
* [Platform Overview](../platform/overview.md) — generate datasets and fine-tune your own forecasting models
