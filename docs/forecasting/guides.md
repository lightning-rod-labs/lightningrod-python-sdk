---
icon: compass
description: How to write good forecasting questions and improve forecasts.
---

# Guides

## Writing good questions

Foresight works best when the question has clear resolution criteria: the event or value, the threshold, and the deadline.

- **Name the event and deadline.** *"Will the Federal Reserve lower the target federal funds rate by at least 25 bps by December 31, 2026?"* is clearer than *"Will the Fed cut soon?"*
- **Use measurable thresholds.** *"Will the S&P 500 close above 7,000 on December 31, 2026?"* is clearer than *"Will stocks do well?"*
- **Ask one thing and choose the right answer type.** Use `binary` for yes/no, `continuous` for a number, and `multiple_choice` for a fixed set of outcomes.

## Improving accuracy

- **Gather and provide current context.**
- **Turn on `research`** for questions that depend on recent events—it lets the model gather live evidence and attach sources you can inspect via `result.sources`.
- **Use ensemble predictions.** Send the same request multiple times and use the median response.
