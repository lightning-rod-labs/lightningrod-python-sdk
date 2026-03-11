---
icon: tags
---

# Labeling and Context

Labeling resolves questions with ground truth; context enriches samples with relevant information, which leads to better results in training. This page covers the labeler, context generators, and filter criteria you plug into `QuestionPipeline`.

## WebSearchLabeler

Resolves questions with ground truth via web search. Use when you need real-world answers.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `answer_type` | AnswerType | No | — | Expected answer type (guides the labeler) |
| `confidence_threshold` | float | No | 0.9 | Minimum confidence to include a question |
| `resolve_redirects` | bool | No | False | Resolve redirect URLs to destinations |

```python
WebSearchLabeler(
    answer_type=BinaryAnswerType(),
    confidence_threshold=0.9,
)
```

Omit `labeler` when using `QuestionAndLabelGenerator`, which produces labels synthetically.

## NewsContextGenerator

Enriches samples with relevant news articles. Add to `context_generators` in `QuestionPipeline`.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `num_search_queries` | int | No | 5 | Search queries per question |
| `articles_per_query` | int | No | 3 | Articles per search query |
| `num_articles` | int | No | 10 | Max articles in final output |
| `relevance_threshold` | int | No | 2 | Min relevance (1–6) to include |
| `min_articles` | int | No | 6 | Minimum articles to ensure |
| `time_delta_days` | int | No | 30 | Days to look back for news |
| `enable_relevance_ranking` | bool | No | True | Use LLM-based relevance ranking |

```python
pipeline = QuestionPipeline(
    seed_generator=...,
    question_generator=...,
    labeler=...,
    context_generators=[NewsContextGenerator(num_articles=15)],
)
```

## FileSetContextGenerator

Retrieves context from documents in a FileSet. Use when your seeds come from a FileSet and you want to enrich questions with related documents (e.g. earlier quarterly reports from the same company). Add to `context_generators` in `QuestionPipeline`.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `file_set_id` | str | Yes | — | FileSet ID to query |
| `metadata_filter_keys` | list[str] | No | — | Keys from seed's file metadata for dynamic filtering (e.g. `["ticker"]`) |
| `metadata_filter` | str | No | — | Static AIP-160 metadata filter (combined with dynamic via AND) |
| `temporal_constraint` | TemporalConstraint | No | — | `BEFORE` for docs on or before seed date (no lookahead); `AFTER` for future docs |
| `date_metadata_key` | str | No | `"file_date"` | Metadata key storing unix timestamp for temporal filtering |

```python
from lightningrod import FileSetContextGenerator, FileSetSeedGenerator, TemporalConstraint

pipeline = QuestionPipeline(
    seed_generator=FileSetSeedGenerator(file_set_id="..."),
    question_generator=...,
    labeler=...,
    context_generators=[
        FileSetContextGenerator(
            file_set_id="...",
            metadata_filter_keys=["ticker"],
            temporal_constraint=TemporalConstraint.BEFORE,
        ),
    ],
)
```

## FileSetRAGLabeler

Resolves questions by searching a FileSet for answers. Use when your seeds come from a FileSet and the answer may appear in later documents (e.g. forward-looking questions resolved by future quarterly reports).

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `file_set_id` | str | Yes | — | FileSet ID to query |
| `answer_type` | AnswerType | No | — | Expected answer type (guides the labeler) |
| `metadata_filter_keys` | list[str] | No | — | Keys from seed's file metadata for dynamic filtering |
| `metadata_filter` | str | No | — | Static AIP-160 metadata filter |
| `temporal_constraint` | TemporalConstraint | No | — | `AFTER` for resolution docs (future); `BEFORE` for historical only |
| `confidence_threshold` | float | No | 0.9 | Minimum confidence to include a question |
| `date_metadata_key` | str | No | `"file_date"` | Metadata key for temporal filtering |

```python
from lightningrod import BinaryAnswerType, FileSetRAGLabeler, FileSetSeedGenerator, TemporalConstraint

pipeline = QuestionPipeline(
    seed_generator=FileSetSeedGenerator(file_set_id="..."),
    question_generator=...,
    labeler=FileSetRAGLabeler(
        file_set_id="...",
        metadata_filter_keys=["ticker"],
        temporal_constraint=TemporalConstraint.AFTER,
        confidence_threshold=0.7,
        answer_type=BinaryAnswerType(),
    ),
)
```

## TemporalConstraint

Enum used by `FileSetContextGenerator` and `FileSetRAGLabeler` to filter documents by date relative to the seed:

| Value | Description |
|-------|-------------|
| `BEFORE` | Documents on or before the seed date (no lookahead) |
| `AFTER` | Documents after the seed date (future docs) |

Use `BEFORE` for context (historical documents only). Use `AFTER` for labeling (resolve forward-looking questions from later reports).

## FilterCriteria

LLM-based content scoring and filtering. An LLM scores each item against your rubric; items below `min_score` are excluded.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `rubric` | str | Yes | — | Scoring rubric/prompt |
| `min_score` | float | No | 0.5 | Minimum score threshold |
| `model_name` | str | No | `google/gemini-3-flash-preview` | Model for scoring |

**Use case 1 — filter seeds (news snippets):** Pass `filter_criteria` to `NewsSeedGenerator`. Snippets scored below `min_score` are dropped before scraping.

**Use case 2 — filter generated questions:** Pass `filter_` to question generators. Questions scored below `min_score` are dropped after generation.

```python
from lightningrod import (
    NewsSeedGenerator,
    ForwardLookingQuestionGenerator,
    FilterCriteria,
    BinaryAnswerType,
)

# Use case 1: filter seeds — drop news snippets that score below min_score
seed_generator = NewsSeedGenerator(
    start_date=...,
    end_date=...,
    search_query="technology announcements",
    filter_criteria=FilterCriteria(
        rubric="Score 1-5: Is this article relevant to technology product launches?",
        min_score=0.6,
    ),
)

# Use case 2: filter questions — drop generated questions that score below min_score
question_generator = ForwardLookingQuestionGenerator(
    instructions="Generate binary forecasting questions...",
    answer_type=BinaryAnswerType(),
    filter_=FilterCriteria(
        rubric="Score 1-5: Is this question forward-looking and clearly resolvable?",
        min_score=0.7,
    ),
)
```

## Composing in QuestionPipeline

```python
pipeline = QuestionPipeline(
    seed_generator=NewsSeedGenerator(
        ...,
        filter_criteria=FilterCriteria(rubric="...", min_score=0.6),
    ),
    question_generator=ForwardLookingQuestionGenerator(
        ...,
        filter_=FilterCriteria(rubric="...", min_score=0.7),
    ),
    labeler=WebSearchLabeler(answer_type=BinaryAnswerType()),
    context_generators=[NewsContextGenerator(num_articles=10)],
)
```
