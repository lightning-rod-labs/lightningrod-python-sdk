---
icon: plug
description: Use Foresight through any OpenAI-compatible client.
---

# OpenAI API

## Minimal example

```python
from openai import OpenAI

client = OpenAI(
    api_key="your-api-key",
    base_url="https://api.lightningrod.ai/v1/openai",
)

response = client.chat.completions.create(
    model="foresight-v4",
    messages=[
        {"role": "user", "content": "Will the Fed cut interest rates in 2026?"},
    ],
)

message = response.choices[0].message
print(message.content)
```

A few useful response fields:
- `response.choices[0].message.content` — model response, including `<answer></answer>` tags when `answer_type` is set.
- `response.choices[0].message.thinking` — reasoning tokens
- `response.choices[0].message.annotations` — citations, when research runs.
- `response.usage` — cost metadata.

See the [REST API reference](https://docs.lightningrod.ai/api-reference) for more details.

## Answer formats

When `answer_type` is set, `message.content` includes machine-readable tags.

```python
response = client.chat.completions.create(
    model="foresight-v4",
    messages=[
        {"role": "user", "content": "Will the Fed cut interest rates in 2026?"},
    ],
    extra_body={"answer_type": "auto"},
)

print(response.choices[0].message.content) # ... <answer>0.62</answer>
```

| `answer_type`       | Raw response shape                                           |
| ------------------- | ------------------------------------------------------------ |
| `"binary"`          | `<answer>0.62</answer>`                                      |
| `"continuous"`      | `<answer>{"mean": 42.5, "standard_deviation": 5.2}</answer>` |
| `"multiple_choice"` | `<answer>{"A": 0.55, "B": 0.45}</answer>`                    |
| `"free_response"`   | `<answer>...</answer>`                                       |
| `"auto"`            | Server-selected structured answer raw response shape                            |


See our [API reference](https://docs.lightningrod.ai/api-reference) for more response examples.

## Research

Pass `research` in `extra_body` to gather live web context before forecasting. Set it to `true` to query all default sources, or pass a `sources` array to limit which providers run:

```python
response = client.chat.completions.create(
    model="foresight-v4",
    messages=[
        {"role": "user", "content": "Will the Fed cut interest rates in 2026?"},
    ],
    extra_body={
        "research": {"sources": ["perplexity", "google_news"]},
        "answer_type": "binary",
    },
)
```

See our [API reference](https://docs.lightningrod.ai/api-reference) for an up-to-date list of supported sources.

## Historical forecasts

Pass `prediction_date` in `extra_body` to make a historical, as-of forecast. The
ISO-8601 value becomes both the model's temporal anchor (the date it treats as
today) and the cutoff for research results:

```python
response = client.chat.completions.create(
    model="foresight-v4",
    messages=[
        {"role": "user", "content": "Will the Fed cut interest rates in 2025?"},
    ],
    extra_body={
        "prediction_date": "2024-06-01T00:00:00Z",
        "research": {"sources": ["google_news"]},
    },
)
```

When a prediction date is set, automatic research retains only providers that
can honor the cutoff; currently that is Google News. Explicitly requesting
Perplexity with `prediction_date` returns a client error. This field is supported
only by chat completions, not the text-completions endpoint.

## Reasoning effort

```python
response = client.chat.completions.create(
    model="foresight-v4",
    messages=[
        {"role": "user", "content": "Will the Fed cut interest rates in 2026?"},
    ],
    reasoning_effort="low",
)

print(response.choices[0].message.content)
print(response.usage.total_tokens)
```

Recommendation: use `low` reasoning effort if cost and latency outweigh marginal improvements in accuracy.

See [Recipes](recipes.md) for more forecasting guidelines.
