---
name: prediction-framing
description: How prediction question format and answer type choices affect fine-tuning performance. Use when recommending answer types, deciding whether to normalize numeric outputs, or diagnosing poor training results caused by answer type mismatch.
---

# Prediction Framing

How you frame a prediction question determines the quality of the training signal. Users often gravitate toward numeric or multiple choice because it feels more expressive — but that usually hurts training. Always recommend based on what will train best, not just what fits the question surface.

## Answer type decision guide

### Binary — default for forecasting
"Will X happen before date Y?" — yes/no.

**Use this unless there's a specific reason not to.** Binary gives:
- Cleanest training signal — unambiguous 0/1 label
- Highest labeling reliability via web search
- Best calibration properties for GRPO/RL fine-tuning
- Highest data yield (more labelable questions per seed)

When a user's goal seems numeric ("predict the star count"), try reframing as binary first: *"Will the repo exceed 1000 stars within 7 days?"* — this almost always trains better.

### Multiple choice — when outcomes are naturally discrete
"Which range will X fall into? A) <100 B) 100–500 C) 500–2000 D) 2000+"

Use when the outcome space has meaningful natural categories. But:
- **Equal-frequency buckets** (e.g. quartiles from historical data), not equal-width — avoids class imbalance, gives the model an even training signal
- Cap at 4 choices; more options increases labeling noise and model confusion
- If binary can express the same decision, prefer binary

### Numeric — only when relative magnitude matters; always normalize
"Predict the exact star count 7 days post-launch."

High-variance training signal. Only use when the magnitude itself is the thing being learned. Always normalize:

| Distribution shape | Normalization | Example |
|-------------------|---------------|---------|
| Power-law / long tail | Log-transform: `log(1 + x)` | Star counts, view counts, revenue, prices |
| Relative comparison | Percentile rank within peer group | Rank vs. similar repos launched same week |
| Naturally bounded range | Min-max scaling to [0, 1] | Percentage, ratio, score out of 100 |

Raw integers are almost always a mistake — the model has no way to know if 1000 vs. 1001 is meaningful.

### Free response — rarely suitable for fine-tuning
Open-ended text answers. Hard to label consistently; high variance in training signal. Reserve for evaluation/benchmarking, not training data generation.

## Worked example: "predict GitHub star growth from an HN launch"

This is a common pattern that illustrates all the pitfalls:

**❌ Total stars** — wrong quantity entirely. Conflates "repo was already popular before the post" with "grew because of HN". Never use absolute follower/star counts as a prediction target.

**⚠️ Stars gained in 7 days (raw numeric)** — right quantity, wrong format. Power-law distributed: a few posts drive thousands of stars, most drive tens. Raw regression is badly calibrated and hard to label reliably.

**✓ log(1 + stars_gained_7d) (normalized numeric)** — better. Tames the long tail. But you still have a regression problem and labeling noise. Use only if you specifically need the magnitude.

**✓✓ Binary** — simplest good option. Pick a meaningful threshold (e.g. median star growth for HN posts, ~100 stars in 7 days) and frame as: *"Will this HN post drive 100+ GitHub stars within 7 days?"* Clean 0/1 signal, easy to label, trains well.

**✓✓ Percentile-bucketed multiple choice** — best option for nuance without regression. Rank each post's star growth against other HN posts in the same time window, split into equal-frequency quartiles (bottom 25% / 25–50% / 50–75% / top 25%). Fully handles the power-law, avoids regression, gives clean classification signal.

The general pattern: **always predict growth over a defined window relative to the event, never absolute totals. Then prefer binary or equal-frequency multiple choice over raw numeric.**

## Diagnosing answer type problems after training

If eval scores are poor, check whether the answer type was a contributing factor:

| Symptom | Likely framing issue | Fix |
|---------|---------------------|-----|
| Model predicts same answer for everything | Class imbalance in multiple choice | Switch to equal-frequency buckets or binary |
| Numeric predictions are wildly off scale | No normalization applied | Apply log-transform or percentile normalization |
| Low labeling confidence in dataset stats | Answer type too hard for web search to resolve | Simplify to binary or reframe the question |
| Model barely beats baseline despite good data volume | Noisy labels from numeric/free-response | Reframe as binary threshold question |
