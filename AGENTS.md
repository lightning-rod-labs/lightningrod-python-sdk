# AGENTS.md

## What This Is

Python SDK for Lightning Rod's **Foresight** forecasting models. The SDK wraps
an OpenAI-compatible inference API — `lr.predict()` sends a prompt and parses
back a calibrated probability forecast (optionally with live web research).

## Commands

```bash
make install-dev          # Install with dev deps (editable mode)
make test                 # Run all tests: pytest tests/ -v
python -m pytest tests/test_prediction.py -v   # Single test file
make bump-patch           # Version bump (also: bump-minor, bump-major)
make publish-new-version  # Build + upload to PyPI
```

## Architecture

### Source layout (`src/lightningrod/`)

- **`client.py`** — `LightningRod` is the entire public entry point. `predict()`
  builds a chat-completion request against the OpenAI-compatible endpoint
  (`{base_url}/openai`) via the `openai` package, and parses the response into
  a typed `PredictionResult`.
- **`prediction.py`** — `AnswerType`, `ReasoningEffort`, the per-answer-type
  prediction dataclasses (`BinaryPrediction`, `ContinuousPrediction`,
  `MultiChoicePrediction`, `FreeResponsePrediction`), `Source`, `Usage`,
  `PredictionResult`, and `_parse_prediction()` — the `<answer>` tag parser.
- **`utils/config.py`** — `get_config_value()` resolves API key/base URL from
  env vars, a project-local `.env`, or Colab secrets; `LightningrodAuthError`.
- **`__init__.py`** — re-exports `LightningRod` plus the prediction types.
  This is the entire public API surface.

### Key patterns

- `predict()` is a thin wrapper around the `openai` Python client — no custom
  HTTP/auth layer. Lightning Rod-specific params (`research`, `answer_type`,
  `reasoning_effort`) travel via `extra_body`.
- `notebooks/00_quickstart.ipynb` is the one example notebook, showing both
  the raw OpenAI-compatible client and the `lr.predict()` helper.
- `docs/` contains GitBook documentation source. `docs/forecasting/*` documents
  the inference API/SDK; `docs/platform/overview.md` is an enterprise pitch
  page (dataset generation and fine-tuning are no longer part of the public
  SDK, but the enterprise offering is still described there for potential
  customers).

## Publishing

See `DEVELOPMENT.md` for the release process (`make bump-patch/minor/major`,
`make publish-new-version`).
