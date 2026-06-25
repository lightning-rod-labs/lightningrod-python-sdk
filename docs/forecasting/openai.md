# OpenAI API

```python
from openai import OpenAI

client = OpenAI(
    api_key="your-api-key",
    base_url="https://api.lightningrod.ai/v1/openai",
)

response = client.chat.completions.create(
    model="foresight-v4",
    messages=[
        {"role": "user", "content": "Will the Fed cut rates by 25bp in March 2026?"},
    ],
    reasoning_effort="low", # Recommended default for lower costs
    extra_body={"research": True, "answer_type": "auto"}, # Optional extension params
)

message = response.choices[0].message
print(message.content)
```

## Response

A few useful response fields:
- `response.choices[0].message.content` — model response, including `<answer></answer>` tags when `answer_type` is set.
- `response.choices[0].message.thinking` — reasoning tokens
- `response.choices[0].message.annotations` — citations, when research runs.
- `response.usage` — cost metadata.

See the [REST API reference](https://docs.lightningrod.ai/rest-api#post-openai-chat-completions) for more details.

## Answer formats

When `answer_type` is set, `message.content` includes machine-readable tags.


| `answer_type`       | Raw response shape                                           |
| ------------------- | ------------------------------------------------------------ |
| `"binary"`          | `<answer>0.62</answer>`                                      |
| `"continuous"`      | `<answer>{"mean": 42.5, "standard_deviation": 5.2}</answer>` |
| `"multiple_choice"` | `<answer>{"A": 0.55, "B": 0.45}</answer>`                    |
| `"free_response"`   | `<answer>...</answer>`                                       |
| `"auto"`            | Server-selected structured answer                            |


## Research

Pass `research` in `extra_body` to gather live web context before forecasting. Set it to `true` to query all default sources, or pass a `sources` array to limit which providers run:

```python
response = client.chat.completions.create(
    model="foresight-v4",
    messages=[
        {"role": "user", "content": "Will the Fed cut rates by 25bp in March 2026?"},
    ],
    extra_body={
        "research": {"sources": ["perplexity", "google_news"]},
        "answer_type": "binary",
    },
)
```

See our [API reference](https://docs.lightningrod.ai/api-reference) for an up-to-date list of supported sources.