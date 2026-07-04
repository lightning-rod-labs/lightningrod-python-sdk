---
name: verify-forecasting-docs
description: Verify the forecasting docs (quickstart.md, sdk.md, openai.md) by executing every Python code snippet and checking that the surrounding prose accurately describes the actual behavior. Use when docs have changed, when the SDK has changed, or when a new API feature is added.
---

# Verify Forecasting Docs

Two-phase verification of `docs/forecasting/`: run every code snippet against the live API, then check that the prose around each snippet matches observed behavior.

## Setup

Ask the user for an API key if one hasn't been provided. The project `.env` may point to staging — bypass it so snippets run against production:

```bash
LIGHTNINGROD_BASE_URL="https://api.lightningrod.ai/v1" python ...
```

Activate the venv before running any Python:

```bash
source venv/bin/activate
```

## Phase 1: Execute every code snippet

Read each doc file in turn. For every fenced Python block, run it verbatim (substituting the real API key for `"your-api-key"`). Capture stdout and any exception.

Cover all files under `docs/forecasting/**` in the order they are listed in `SUMMARY.md`.

For each snippet record:
- **file** and approximate line range
- **exit status** (pass / error / exception type + message)
- **stdout** (first 300 chars is enough)

## Phase 2: Semantic validation

For each snippet that passed, check the prose immediately before and after it against what you actually observed. Flag any mismatch as a finding.

Common things to check:

| Prose claim | How to verify |
|---|---|
| "field X is populated when answer_type=Y" | Confirm the field is non-None in the output |
| "answer_type='auto' raises ValueError in predict()" | Run it and confirm the error message matches |
| Parameter descriptions in tables (type, default, description) | Cross-check against `client.py` and `prediction.py` source |
| Response field table in sdk.md | Confirm each field is present on the returned `PredictionResult` |
| Cost/token counts mentioned | Confirm `usage` fields are present and non-zero |
| Source objects have `url` and `title` | Confirm with a research call |
| `answer_type='auto'` note says it raises `ValueError` | Run it and confirm |

Flag findings as:
- ⚠️ **wrong** — prose makes a claim that contradicts observed behavior
- ⚠️ **stale** — prose describes something that no longer exists (removed field, renamed param)
- 📝 **missing** — behavior exists but isn't documented

## Report format

```
## Doc Verification: forecasting docs

**Verdict:** PASS | FAIL

### Snippet results
| # | File | Description | Result |
|---|------|-------------|--------|
| 1 | quickstart.md | OpenAI client minimal | ✅ pass |
| 2 | sdk.md | lr.predict() minimal | ✅ pass |
...

### Semantic findings
- ⚠️ <finding>
- 📝 <finding>
(empty = all prose checked out)
```

FAIL if any snippet raises an unexpected exception, or if any ⚠️ finding is found. 📝 findings don't fail but should be noted.
