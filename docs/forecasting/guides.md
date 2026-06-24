---
icon: compass
description: How to write good forecasting questions and improve forecasts.
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

## Improving accuracy

gather and provide current context

- **Turn on `research`** for questions that depend on recent events—it lets the model gather live evidence and attach sources you can inspect via `result.sources`.
- **Backtest against your context/strategy.**
