---
icon: compass
description: Guidelines on how to effectively forecast using our API.
---

# Recipes

## Writing good questions

Foresight works best when the question has clear resolution criteria: the event or value, the threshold, and the deadline.

- **Name the event and deadline.** *"Will the Federal Reserve lower the target federal funds rate by at least 25 bps by December 31, 2026?"* is clearer than *"Will the Fed cut soon?"*
- **Use measurable thresholds.** *"Will the S&P 500 close above 7,000 on December 31, 2026?"* is clearer than *"Will stocks do well?"*
- **Ask one thing and choose the right answer type.** Use `binary` for yes/no, `continuous` for a number, and `multiple_choice` for a fixed set of outcomes.

## Improving accuracy

- **Gather and provide relevant context.**
- **Turn on `research`** for questions that depend on recent events—it lets the model gather live evidence and attach sources you can inspect via `result.sources`.
- **Use ensemble predictions.** Send the same request multiple times and use the median response.
- **Fine-tune on your domain (enterprise).** If you want to achieve better accuracy and cost on your domain, leveraging your internal data, see [our enteprise platform](../platform/overview.md).

## Optimizing costs

- **Use low reasoning.** This will significantly reduce token usage, while still maintaining accuracy edge over the current frontier models.
- **Curate your context.** Implement custom context aggregation logic, tuned for your forecasting question.