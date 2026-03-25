# Lightning Rod Examples Guide

Three common patterns for building datasets and training models. These are starting points — adapt to fit the use case.

---

## Pattern 1: Forward-Looking Training (RL)

Teach a model to reason about the future. Generate questions with known outcomes, let GRPO discover effective reasoning — cause-and-effect, probability calibration, signal identification.

**Training**: GRPO | **Answer types**: Binary, continuous, multiple choice | **Labels**: WebSearchLabeler, FileSetRAGLabeler, or pre-computed

**When to use**: Predicting outcomes. Questions have a future resolution date; the answer isn't known at question time.

**Why RL**: The model explores reasoning strategies and gets rewarded for calibration. It discovers causal reasoning training data doesn't explicitly teach. SFT memorizes; GRPO generalizes.

**Default model**: `openai/gpt-oss-120b` | **Benchmark**: `openai/gpt-5`

**Common steps**:
1. Gather seeds (news, GDELT, FileSets, custom data)
2. Generate forward-looking questions
3. Resolve labels (web search, RAG, or pre-computed)
4. Add context (optional)
5. Split temporally, train with GRPO

**Watch for**:
- Always split temporally — shuffling leaks future info
- No sample's close date past the first test prediction date
- Spot-check questions for sense and unambiguous resolution criteria
- Filter to resolved questions (`days_to_resolution_range=(1, None)`)

**Examples**: [forward-looking-examples.md](forward-looking-examples.md)

---

## Pattern 2: Content Learning (SFT)

Teach a model domain knowledge — facts, procedures, expertise — via Q&A pairs and SFT.

**2A — Document Q&A**: Have documents → `QuestionAndLabelGenerator` extracts Q and A from text. No labeler needed.

**2B — Topic-Driven Knowledge**: Have a domain, no documents → generate a topic tree for coverage → create questions → `WebSearchLabeler` finds answers from the web.

> **TopicTreeSeedGenerator**: Exists server-side ([PR #1096](https://github.com/lightning-rod-labs/llm_forecasting/pull/1096)). Takes `topic` (string or list), `tree_depth` (default 2), `tree_degree` (default 5), decomposes via LLM into `degree^depth` leaf seeds. Available as `topic_tree` seed type in the pipeline API. **Not yet in the Python SDK** — check `lightningrod.__init__` for it; fall back to [Pluto](https://github.com/pluto-data/pluto) (`pip install pluto-data`) if unavailable.

**Training**: SFT | **Answer types**: Free response, multiple choice

**When to use**: Model should internalize domain knowledge, not predict the future.

**Why SFT**: Answers are known. No reasoning to discover — SFT directly optimizes for the right answer.

**Default model**: `openai/gpt-oss-120b` for production, `Qwen/Qwen3-8B-Instruct` for smaller models

**Watch for**:
- 2A: Use `QuestionAndLabelGenerator`, not `WebSearchLabeler` — answers are in the documents
- 2B: `WebSearchLabeler` is correct — the web is the knowledge source
- Quality filter always. `FilterCriteria`, score cutoffs, or agreement checks
- No reward signal for free-response yet → GRPO doesn't apply

**Examples**: [content-learning-examples.md](content-learning-examples.md)

---

## Pattern 3: Tabular Data Processing

Map structured data to `Sample()` fields, fill in what's missing, optionally enrich with context.

**Training**: Usually GRPO (same as Pattern 1 once prepared) | **Answer types**: Binary, continuous

**When to use**: Structured data — CSV, BigQuery, API results, financial data. Some fields exist, some need generating.

**Key challenge**: The mapping. Common scenarios:
- Have outcomes, need questions → compute labels, use `TemplateQuestionGenerator`
- Have questions + labels, need context → map both, add `NewsContextGenerator`
- Have questions, need labels → map questions, add `WebSearchLabeler`

**Default model**: `openai/gpt-oss-120b` | **Benchmark**: `openai/gpt-5`

**Watch for**:
- Don't leak labels into question text
- `prediction_date` must be BEFORE the outcome
- **Think about splits carefully.** What's the right temporal key? For per-entity data, does entity overlap between train/test cause leakage? Ask: "what would be available at prediction time in production?"
- Validate 10-20 samples manually before scaling

**Examples**: [tabular-examples.md](tabular-examples.md)

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
├── From documents → Pattern 2A
├── From a topic/domain → Pattern 2B
└── From conversations → Pattern 2 (Transcript SFT)

Evaluate models → RolloutGenerator + RolloutScorer
```
