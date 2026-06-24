---
icon: compass
description: How to write good forecasting questions and how to interpret the calibrated probabilities Foresight returns.
---

# Guides

Practical guidance for getting reliable forecasts out of Foresight.

## Writing good questions

Foresight is most accurate when a question has a single, unambiguous resolution. Aim for questions a neutral observer could grade later without debate.

- **Be self-contained.** Include the entities, dates, and thresholds in the question itself rather than relying on prior context. *"Will OpenAI publicly release GPT-5 by March 15, 2026?"* beats *"Will they ship it soon?"*
- **Pin the resolution date.** Forward-looking questions need a deadline. *"…by end of Q1 2026"* is gradable; *"…eventually"* is not.
- **Make the threshold explicit.** Prefer *"close above 6,000"* to *"go up a lot."* Numbers resolve cleanly.
- **One event per question.** Split compound questions ("rate cut *and* a market rally") into separate forecasts so each gets its own probability.
- **Match the question to the answer type.** Yes/no → `binary`; a numeric magnitude → `continuous`; a fixed set of outcomes → `multiple_choice`. Use `"auto"` if you want the server to classify for you.

## Interpreting probabilities

`binary` answers are calibrated probabilities between 0 and 1—not confidence scores or yes/no labels.

- **0.5 means genuinely uncertain**, not "no answer." Treat it as a coin flip on current evidence.
- **Calibration is the goal:** across many forecasts marked ~0.7, roughly 70% should resolve true. Evaluate the model over a *set* of questions, not a single call.
- **Don't hard-threshold blindly.** Converting to a yes/no at 0.5 throws away the signal in how far from 0.5 the estimate sits. Use the probability directly where you can.
- **For `continuous`,** the `standard_deviation` is the model's stated uncertainty—a wide band means low confidence in the point estimate.
- **For `multiple_choice`,** probabilities across options sum toward 1; compare them to each other rather than to an absolute bar.

## Improving accuracy

- **Turn on `research`** for questions that depend on recent events—it lets the model gather live evidence and attach sources you can inspect via `result.sources`.
- **Use `reasoning_effort="low"`** when you want to reduce reasoning budget; keep the default `"medium"` for harder questions.
- **Backtest before you trust it in production.** The [Polymarket recipe](recipes.md) shows how to score Foresight against resolved real-world markets.
