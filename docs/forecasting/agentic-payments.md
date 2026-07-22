---
icon: robot
description: Get an API key and credits with no human, no signup, no dashboard — pay per top-up with MPP.
---

# Agentic Payments (MPP)

Agents can obtain an API key and credits without a human — no signup, no dashboard. Pay a fixed **$5.00** credit top-up over [MPP](https://datatracker.ietf.org/doc/draft-ietf-httpauth-payment/) (`Machine Payments Protocol`) and get an API key back, then use it against the standard [OpenAI-compatible API](openai.md).

The top-up endpoint offers **two payment rails** — pay whichever your wallet supports:

- `method="tempo"` — on-chain USDC on [Tempo](https://tempo.xyz) (chain id `4217`)
- `method="stripe"` — Stripe card / Link Shared Payment Token

## Fastest path (Tempo wallet)

If you have a Tempo wallet (`tempo wallet login`):

```bash
tempo request -X POST https://api.lightningrod.ai/v1/mpp/topup
```

This pays the $5.00 USDC-on-Tempo challenge and returns credits + an API key automatically. Any other MPP-aware client (`mppx`, `link-cli`) works the same way — point it at the same URL.

## Manual flow (raw HTTP, any MPP client)

### 1. Request a challenge (no payment)

```bash
curl -s -X POST https://api.lightningrod.ai/v1/mpp/topup
```

Returns `402` with **two** `WWW-Authenticate: Payment` header instances — pay whichever rail you can:

```
WWW-Authenticate: Payment id="...", realm="api.lightningrod.ai", method="stripe", intent="charge", request="<base64url>", expires="2026-01-01T00:00:00Z", description="Lightning Rod Labs credit top-up ($5.00)"
WWW-Authenticate: Payment id="...", realm="api.lightningrod.ai", method="tempo", intent="charge", request="<base64url>", expires="2026-01-01T00:00:00Z", description="Lightning Rod Labs credit top-up ($5.00)"
```

`request` is base64url-encoded JSON per the MPP spec (`draft-ietf-httpauth-payment`); decode it for the exact recipient/amount, or read the machine-readable offers (amount, currency, decimals) in `x-payment-info` at [`https://api.lightningrod.ai/openapi.json`](https://api.lightningrod.ai/openapi.json).

### 2. Pay and retry with the credential

Your wallet/CLI builds and signs the credential for you. Retry with `Authorization: Payment <credential>`:

```bash
curl -s -X POST https://api.lightningrod.ai/v1/mpp/topup \
  -H 'Authorization: Payment <credential-from-step-2>'
```

Returns `200`:

```json
{"organization_id": "org_mpp_...", "credited_cents": 500, "api_key": "sk_...", "api_key_id": "key_..."}
```

`api_key` is minted once — **save it.**

### 3. Use the key, and refill when credits run out

Use it as `Authorization: Bearer sk_...` on `POST /v1/openai/chat/completions`:

```bash
curl -s https://api.lightningrod.ai/v1/openai/chat/completions \
  -H 'Authorization: Bearer sk_...' \
  -H 'Content-Type: application/json' \
  -d '{"model": "foresight-v4", "messages": [{"role": "user", "content": "Will the Fed cut interest rates in 2026?"}]}'
```

When credits run out, that endpoint returns `402`. Call `/mpp/topup` again with the same key in `X-API-Key` to refill **without minting a new org**:

```bash
tempo request -X POST https://api.lightningrod.ai/v1/mpp/topup \
  -H 'X-API-Key: sk_...'
```

## See also

- [OpenAI API](openai.md) — everything you can do once you have a key
- [API reference: Agentic Payments](https://docs.lightningrod.ai/api-reference/agentic-payments) — the `/mpp/topup` schema
