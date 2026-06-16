---
icon: tags
---

# Labeling and Context

Labeling resolves questions with ground truth; context enriches samples with relevant information, which leads to better results in training. This page covers the labeler, document context generators, and filter criteria you plug into `QuestionPipeline`.

## WebSearchLabeler

Resolves questions with ground truth via web search. Use when you need real-world answers.

| Parameter              | Type       | Required | Default | Description                               |
| ---------------------- | ---------- | -------- | ------- | ----------------------------------------- |
| `answer_type`          | AnswerType | No       | —       | Expected answer type (guides the labeler) |
| `confidence_threshold` | float      | No       | 0.9     | Minimum confidence to include a question  |
| `resolve_redirects`    | bool       | No       | False   | Resolve redirect URLs to destinations     |

```python
WebSearchLabeler(
    answer_type=BinaryAnswerType(),
    confidence_threshold=0.9,
)
```

Omit `labeler` when using `QuestionAndLabelGenerator`, which produces labels synthetically.

## QdrantContextGenerator

Retrieves context from documents in a FileSet via **vector search**. Builds a Qdrant index on first use (chunking + embedding with `BAAI/bge-small-en-v1.5`), then retrieves the top-k most semantically relevant chunks per question. Use when your seeds come from a FileSet and you want to enrich questions with passages that may be scattered across many documents. Add to `context_generators` in `QuestionPipeline`.

| Parameter             | Type                | Required | Default                 | Description                                                                                           |
| --------------------- | ------------------- | -------- | ----------------------- | ----------------------------------------------------------------------------------------------------- |
| `file_set_id`         | str                 | Yes\*    | —                       | FileSet ID to load the Qdrant collection from (\*or `collection_name` for direct injection)           |
| `top_k`               | int                 | No       | 5                       | Number of chunks to retrieve                                                                          |
| `temporal_direction`  | str                 | No       | —                       | `"before"` (timestamp ≤ seed date, includes seed's doc) or `"after"` (timestamp > seed date)          |
| `payload_filters`     | dict\[str, str]     | No       | —                       | `{qdrant_payload_key: sample_meta_key}` — values pulled from the sample's metadata at query time      |
| `index_chunk_size`    | int                 | No       | 1500                    | Chunk size used when building the backing Qdrant index                                                |
| `index_chunk_overlap` | int                 | No       | 150                     | Chunk overlap used when building the backing Qdrant index                                             |
| `embedding_model`     | str                 | No       | `"BAAI/bge-small-en-v1.5"` | FastEmbed model name for query embedding                                                           |

```python
from lightningrod import QdrantContextGenerator, FileSetSeedGenerator

pipeline = QuestionPipeline(
    seed_generator=FileSetSeedGenerator(file_set_id="..."),
    question_generator=...,
    labeler=...,
    context_generators=[
        QdrantContextGenerator(
            file_set_id="...",
            payload_filters={"ticker": "ticker"},  # restrict retrieval to same ticker
            temporal_direction="before",           # historical context, no lookahead
            top_k=5,
        ),
    ],
)
```

## FileSetDocumentContextGenerator

Resolves a **single document** from a FileSet by temporal ordering, downloads its full text, and appends it as context. No vector search — picks the one document whose chronological position matches `temporal_constraint`. Optionally processes the document through an LLM before injection. Add to `context_generators` in `QuestionPipeline`.

Use this instead of `QdrantContextGenerator` when you want the complete text of one document rather than RAG-retrieved chunks from multiple documents.

| Parameter | Type | Required | Default | Description |
| ----------------------- | ------------------- | -------- | ------- | ------------------------------------------------------------------- |
| `file_set_id` | str | Yes | — | FileSet ID to resolve documents from |
| `temporal_constraint` | TemporalConstraint | No | — | Temporal filtering direction relative to the seed document's date |
| `metadata_filter_keys` | `list[str]` | No | — | Keys from sample's file metadata for exact-match filtering |
| `system_instruction` | `str \| None` | No | None | System prompt for optional LLM processing of the document |
| `model` | `ModelConfig \| None` | No | None | Model for LLM processing; if None, raw document text is used as context |
| `max_document_chars` | `int \| None` | No | None | Character limit for document text; truncates from the end if exceeded |

```python
from lightningrod import FileSetDocumentContextGenerator, FileSetSeedGenerator, TemporalConstraint

pipeline = QuestionPipeline(
    seed_generator=FileSetSeedGenerator(file_set_id="..."),
    question_generator=...,
    labeler=...,
    context_generators=[
        FileSetDocumentContextGenerator(
            file_set_id="...",
            temporal_constraint=TemporalConstraint.PREVIOUS_DOCUMENT,
            metadata_filter_keys=["district"],
            max_document_chars=50000,
        ),
    ],
)
```

## QdrantRAGLabeler

Resolves questions by **vector-searching** a FileSet for answer evidence and using an LLM to extract a structured label from the retrieved chunks. Use when your seeds come from a FileSet and the answer may appear in chunks scattered across multiple documents (e.g. forward-looking questions resolved by future quarterly reports).

| Parameter              | Type              | Required | Default                    | Description                                                                              |
| ---------------------- | ----------------- | -------- | -------------------------- | ---------------------------------------------------------------------------------------- |
| `file_set_id`          | str               | Yes\*    | —                          | FileSet ID to load the Qdrant collection from (\*or `collection_name`)                   |
| `answer_type`          | AnswerType        | No       | —                          | Expected answer type (guides the labeler)                                                |
| `payload_filters`      | dict\[str, str]   | No       | —                          | `{qdrant_payload_key: sample_meta_key}` mapping                                          |
| `temporal_direction`   | str               | No       | —                          | `"before"` or `"after"` relative to the seed date                                        |
| `confidence_threshold` | float             | No       | 0.9                        | Minimum confidence to include a question                                                 |
| `top_k`                | int               | No       | 5                          | Number of chunks to retrieve                                                             |
| `extraction_model`     | ModelConfig \| None | No     | gemini-2.5-flash           | LLM used for structured label extraction                                                 |
| `index_chunk_size`     | int               | No       | 1500                       | Chunk size used when building the backing Qdrant index                                   |
| `index_chunk_overlap`  | int               | No       | 150                        | Chunk overlap used when building the backing Qdrant index                                |
| `embedding_model`      | str               | No       | `"BAAI/bge-small-en-v1.5"` | FastEmbed model name for query embedding                                                 |

```python
from lightningrod import BinaryAnswerType, QdrantRAGLabeler, FileSetSeedGenerator

pipeline = QuestionPipeline(
    seed_generator=FileSetSeedGenerator(file_set_id="..."),
    question_generator=...,
    labeler=QdrantRAGLabeler(
        file_set_id="...",
        payload_filters={"ticker": "ticker"},
        temporal_direction="after",       # resolve from future docs
        confidence_threshold=0.7,
        answer_type=BinaryAnswerType(),
    ),
)
```

## FileSetDocumentLabeler

Resolves a **single document** from a FileSet by temporal ordering, downloads its full text, and uses an LLM to extract a structured label. No vector search — picks the one document whose chronological position matches `temporal_constraint`. Use this instead of `QdrantRAGLabeler` when you want to label from the full content of a specific document rather than RAG-retrieved chunks.

| Parameter | Type | Required | Default | Description |
| ----------------------- | ------------------- | -------- | ------- | ------------------------------------------------------------------- |
| `file_set_id` | str | Yes | — | FileSet ID to resolve documents from |
| `temporal_constraint` | TemporalConstraint | No | — | Temporal filtering direction relative to the seed document's date |
| `metadata_filter_keys` | `list[str]` | No | — | Keys from sample's file metadata for exact-match filtering (e.g. `["district"]`) |
| `confidence_threshold` | float | No | 0.7 | Minimum confidence threshold for valid labels |
| `answer_type` | AnswerType | No | — | Expected answer type (guides the labeler) |
| `model` | `ModelConfig \| None` | No | None | Model for label extraction; defaults to gemini-2.5-flash |
| `system_instruction` | `str \| None` | No | None | Domain-specific system instruction (e.g. `"You are labeling Federal Reserve Beige Book questions."`) |

```python
from lightningrod import (
    BinaryAnswerType,
    FileSetDocumentLabeler,
    FileSetSeedGenerator,
    TemporalConstraint,
)

pipeline = QuestionPipeline(
    seed_generator=FileSetSeedGenerator(file_set_id="..."),
    question_generator=...,
    labeler=FileSetDocumentLabeler(
        file_set_id="...",
        temporal_constraint=TemporalConstraint.NEXT_DOCUMENT,
        metadata_filter_keys=["district"],
        answer_type=BinaryAnswerType(),
        system_instruction="You are labeling Federal Reserve Beige Book forecasting questions.",
    ),
)
```

## TemporalConstraint

Enum used by `FileSetDocumentContextGenerator` and `FileSetDocumentLabeler` to pick the single document resolved relative to the seed. (The Qdrant transforms use a separate `temporal_direction` string — `"before"` / `"after"` — instead.)

| Value | Description |
| ------------------- | ------------------------------------------------------------------ |
| `BEFORE` | Documents on or before the seed date (no lookahead, multiple docs) |
| `AFTER` | Documents after the seed date (future docs, multiple docs) |
| `NEXT_DOCUMENT` | First document after the seed timestamp (single-doc resolution) |
| `PREVIOUS_DOCUMENT` | Most recent document before the seed timestamp (single-doc context) |
| `EQUAL` | Document with an exact matching date (single-doc) |

Use `BEFORE` for context (historical documents). Use `AFTER` for labeling from multiple future documents. Use `NEXT_DOCUMENT` or `PREVIOUS_DOCUMENT` when you want exactly one document relative to the seed — useful with the document-level transforms (`FileSetDocumentContextGenerator`, `FileSetDocumentLabeler`).

## FilterCriteria

LLM-based content scoring and filtering. An LLM scores each item against your rubric; items below `min_score` are excluded.

| Parameter    | Type  | Required | Default                         | Description             |
| ------------ | ----- | -------- | ------------------------------- | ----------------------- |
| `rubric`     | str   | Yes      | —                               | Scoring rubric/prompt   |
| `min_score`  | float | No       | 0.5                             | Minimum score threshold |
| `model_name` | str   | No       | `google/gemini-3-flash-preview` | Model for scoring       |

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
    search_query="technology announcements",
    filter_criteria=FilterCriteria(rubric="Tech product launch or announcement", min_score=0.6),
)

# Use case 2: filter questions — drop generated questions that score below min_score
question_generator = ForwardLookingQuestionGenerator(
    instructions="Generate binary forecasting questions...",
    filter_=FilterCriteria(rubric="Forward looking and resolvable question", min_score=0.7),
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
)
```
