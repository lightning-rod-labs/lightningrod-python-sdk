---
name: examples-guide
description: Decision tree for choosing a training pattern (forward-looking GRPO, content learning SFT, tabular data). Use when starting a new project, choosing between RL and SFT, or selecting an answer type.
---

# Lightning Rod Examples Guide

Three common patterns for building datasets and training models. These are starting points — adapt to fit the use case.

---

## Pattern 1: Forward-Looking Training (RL)

Train a model to reason within a domain and/or learn to predict outcomes. Forward-looking questions with known outcomes let GRPO discover cause-and-effect, probability calibration, and signal identification. Even if the end goal isn't prediction, reasoning about the future is a powerful way to learn domain reasoning.

**Training**: GRPO | **Answer types**: Binary, continuous, multiple choice | **Labels**: WebSearchLabeler, FileSetRAGLabeler, or pre-computed

**When to use**: Teaching domain reasoning. Questions have a future resolution date; the answer isn't known at question time. The model learns to reason about causality and uncertainty, not just memorize facts.

**Why RL**: The model explores reasoning strategies and gets rewarded for calibration. It discovers causal reasoning training data doesn't explicitly teach. SFT memorizes; GRPO generalizes.

**Default model**: `openai/gpt-oss-120b` | **Benchmark**: `openai/gpt-5`

**Common steps**:

1. Gather seeds (news, GDELT, FileSets, custom data)
2. Generate forward-looking questions
3. Resolve labels (web search, RAG, or pre-computed)
4. Add context (optional)
5. Lint the generated dataset, split temporally, train with GRPO

**Watch for**:

- Lint the full dataset before splitting — catches duplicates, missing fields, and label issues that filtering misses. Linting runs server-side on the whole dataset
- Always split temporally — shuffling leaks future info
- No sample's close date past the first test prediction date
- Spot-check questions for sense and unambiguous resolution criteria
- Filter to resolved questions (`days_to_resolution_range=(1, None)`)

**Examples**: See `forward-looking-examples` skill

---

## Pattern 2: Content Learning (SFT)

Teach a model domain knowledge — facts, procedures, expertise — via Q&A pairs and SFT.

Two starting points depending on what you have:

- **From documents**: `QuestionAndLabelGenerator` extracts Q and A from text. No labeler needed.
- **From a topic/domain (no documents)**: `TopicTreeSeedGenerator` decomposes topics into specific leaf seeds → generate questions → `WebSearchLabeler` finds answers from the web.

**Training**: SFT | **Answer types**: Free response, multiple choice

**When to use**: Model should internalize domain knowledge, not predict the future.

**Why SFT**: Answers are known. No reasoning to discover — SFT directly optimizes for the right answer.

**Default model**: `openai/gpt-oss-120b` for production, `Qwen/Qwen3-8B-Instruct` for smaller models

**Watch for**:

- From documents: use `QuestionAndLabelGenerator`, not `WebSearchLabeler` — answers are in the documents
- From topics: `WebSearchLabeler` is correct — the web is the knowledge source
- Quality filter always. `FilterCriteria`, score cutoffs, or agreement checks
- Lint the dataset before splitting — catches duplicates and malformed samples that quality filters miss
- No reward signal for free-response yet → GRPO doesn't apply

**Examples**: See `content-learning-examples` skill

---

## Pattern 3: Tabular Data Processing

Map structured data to `Sample()` fields, fill in what's missing, optionally enrich with context.

**Training**: Often GRPO (same as Pattern 1 once prepared), but SFT is also common when the data is non-forecasting (e.g., call data, survey responses) | **Answer types**: Binary, continuous

**When to use**: Structured data — CSV, BigQuery, API results, financial data. Some fields exist, some need generating.

**Key challenge**: The mapping. Common scenarios:

- Have outcomes, need questions → compute labels, use `TemplateQuestionGenerator`. Think about horizons: if starting from end dates, subtract the horizon to get `prediction_date` (used for context enrichment and temporal splits).
- Have questions + labels, need context → map both, add `NewsContextGenerator`
- Have questions, need labels → map questions, add `WebSearchLabeler`

**Default model**: `openai/gpt-oss-120b` | **Benchmark**: `openai/gpt-5`

**Watch for**:

- Don't leak labels into question text
- `prediction_date` must be BEFORE the outcome
- **Split carefully.** For forecasting data, split on time — train on past, test on future. If data has multiple entities (countries, stocks), ensure no entity's test samples overlap temporally with its training samples. For non-forecasting tabular data (e.g., ad persuasion, survey responses), temporal splits may not apply — but ensure no content leakage between train and test (e.g., if multiple questions reference the same ad, keep all of that ad's questions in the same split). Shuffling is fine when there's no temporal structure.
- Validate 10-20 samples manually before scaling
- Lint the dataset before splitting — tabular mappings often produce duplicates from overlapping time windows or missing fields from incomplete row mappings

**Examples**: See `tabular-examples` skill

---

## Context Enrichment (All Patterns)

```python
# Defaults: 5 search queries/question, 3 articles/query, 10 kept after ranking
NewsContextGenerator()

# Lighter context (common in domain notebooks):
NewsContextGenerator(num_search_queries=3, articles_per_query=3, num_articles=5)
```

For FileSets, use `FileSetContextGenerator` with temporal constraints.

---

## Decision Tree

Starting points — use cases may combine patterns.

```
Predict future outcomes
├── From news/GDELT → Pattern 1
├── From documents → Pattern 1 (FileSet RAG)
└── From structured data → Pattern 3

Teach domain knowledge
├── From documents → Pattern 2
└── From a topic/domain → Pattern 2

Evaluate models → RolloutGenerator + RolloutScorer
```

---

## Prediction Framing — Answer Type Guide

How you frame a prediction question determines the quality of the training signal. Users often gravitate toward numeric or multiple choice because it feels more expressive — but that usually hurts training. Always recommend based on what will train best, not just what fits the question surface.

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

### Worked example: "predict GitHub star growth from an HN launch"

**Bad: Total stars** — wrong quantity entirely. Conflates "repo was already popular before the post" with "grew because of HN". Never use absolute follower/star counts as a prediction target.

**Caution: Stars gained in 7 days (raw numeric)** — right quantity, wrong format. Power-law distributed: a few posts drive thousands of stars, most drive tens. Raw regression is badly calibrated and hard to label reliably.

**Better: log(1 + stars_gained_7d) (normalized numeric)** — tames the long tail. But you still have a regression problem and labeling noise. Use only if you specifically need the magnitude.

**Good: Binary** — simplest good option. Pick a meaningful threshold (e.g. median star growth for HN posts, ~100 stars in 7 days) and frame as: *"Will this HN post drive 100+ GitHub stars within 7 days?"* Clean 0/1 signal, easy to label, trains well.

**Best: Percentile-bucketed multiple choice** — best option for nuance without regression. Rank each post's star growth against other HN posts in the same time window, split into equal-frequency quartiles (bottom 25% / 25–50% / 50–75% / top 25%). Fully handles the power-law, avoids regression, gives clean classification signal.

The general pattern: **always predict growth over a defined window relative to the event, never absolute totals. Then prefer binary or equal-frequency multiple choice over raw numeric.**

### Diagnosing answer type problems after training

If eval scores are poor, check whether the answer type was a contributing factor:

| Symptom | Likely framing issue | Fix |
|---------|---------------------|-----|
| Model predicts same answer for everything | Class imbalance in multiple choice | Switch to equal-frequency buckets or binary |
| Numeric predictions are wildly off scale | No normalization applied | Apply log-transform or percentile normalization |
| Low labeling confidence in dataset stats | Answer type too hard for web search to resolve | Simplify to binary or reframe the question |
| Model barely beats baseline despite good data volume | Noisy labels from numeric/free-response | Reframe as binary threshold question |

If the table above doesn't explain poor results, use **reasoning comparison** to see how the base and fine-tuned models actually think. Run eval with `reasoning_comparison_sample_size=20` — this produces side-by-side reasoning traces showing where the fine-tuned model reasons differently (better or worse) than the base model. See `forward-looking-examples` skill for the code pattern.
