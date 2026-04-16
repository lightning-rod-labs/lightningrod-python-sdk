---
name: content-learning-sft
description: Build Q&A training data and fine-tune models with Lightning Rod SFT. Use when the user wants to teach a model domain knowledge, create Q&A pairs from textbooks or PDFs or technical documents, generate questions from a topic or domain without documents, train with supervised fine-tuning (SFT), build a domain expert, or when they mention QuestionAndLabelGenerator, TopicTreeSeedGenerator, FreeResponseAnswerType, or "internalize facts". Covers both document-sourced Q&A (answers inside documents) and topic-sourced Q&A (answers found via web search), plus SFT config and persona shaping.
---

# Content Learning (SFT)

Teach a model domain knowledge — facts, procedures, expertise — via Q&A pairs and supervised fine-tuning. Answers are known at question time, so there is no reasoning to discover; SFT directly optimizes for the right answer.

Full worked examples live in `agent-docs/content-learning-examples.md`. Open it for anything beyond the decisions below.

## When this pattern fits

- The model should **internalize domain knowledge**, not predict the future. If answers only resolve later, use the forward-looking-training skill instead.
- Answer types: free response (most common) or multiple choice. GRPO doesn't apply — there is no reward signal for free-response.

## Two branches — pick based on what the user has

### Branch A: From documents (answers live in the text)

Use `FileSetSeedGenerator` + `QuestionAndLabelGenerator`. **No labeler** — the generator extracts question and answer together from each chunk.

```python
from lightningrod import (
    LightningRod, QuestionPipeline,
    FileSetSeedGenerator, QuestionAndLabelGenerator, FreeResponseAnswerType,
)

lr = LightningRod(api_key=api_key)

# Upload PDFs to a FileSet first (see agent-docs for upload + metadata schema).

pipeline = QuestionPipeline(
    seed_generator=FileSetSeedGenerator(
        file_set_id=fileset.id,
        chunk_size=4000,
        chunk_overlap=200,
    ),
    question_generator=QuestionAndLabelGenerator(
        answer_type=FreeResponseAnswerType(),
        questions_per_seed=3,                   # density heuristic below
        instructions="...",
    ),
)

dataset = lr.transforms.run(pipeline, max_questions=12000, name="...")
```

**Trap:** do NOT add `WebSearchLabeler` to a document-sourced pipeline. The answers are already in the chunks — web search will drift, contradict the source, or lower quality.

### Branch B: From a topic / domain (no documents)

Decompose the domain into specific leaf seeds with `TopicTreeSeedGenerator`, then `QuestionGenerator` writes questions and `WebSearchLabeler` finds authoritative answers from the web.

```python
from lightningrod import (
    QuestionPipeline, TopicTreeSeedGenerator,
    QuestionGenerator, FreeResponseAnswerType, WebSearchLabeler,
)

answer_type = FreeResponseAnswerType(
    labeler_instruction="You are a <domain> expert. Direct, numbered steps. No disclaimers.",
    answer_format_instruction="Direct, step-by-step answer. Start with step 1, no introduction.",
)

pipeline = QuestionPipeline(
    seed_generator=TopicTreeSeedGenerator(
        topic=["<root topic 1>", "<root topic 2>", ...],  # 8-16 roots
        tree_depth=2,                                      # 2 levels of expansion
        tree_degree=5,                                     # 5 subtopics per node
        model_name="google/gemini-3-flash-preview",
        model_system_prompt="You are an expert in <domain>. Generate specific, practical subtopics.",
    ),
    question_generator=QuestionGenerator(
        answer_type=answer_type,
        questions_per_seed=10,                             # topic seeds are conceptual, high density
        instructions="Specific, scenario-based, actionable. Each question must cover a distinct technique.",
        examples=["How do I ...?", ...],
        bad_examples=["What is ...? (too vague)", ...],
    ),
    labeler=WebSearchLabeler(answer_type=answer_type, confidence_threshold=0.8),
)
```

## Key decisions

### `questions_per_seed` by seed density

| Seed source | `questions_per_seed` |
| --- | --- |
| `TopicTreeSeedGenerator` leaf (conceptual) | 10 |
| 4000-char document chunk (dense) | 3 |
| 2000-char document chunk | 2 |
| Short text / single article | 1 |

### Answer-type persona

`FreeResponseAnswerType(labeler_instruction=..., answer_format_instruction=...)` shapes both **what the labeler writes** and **how the model responds**. Those instructions get baked into the training data — treat them like a system prompt for the eventual model.

### Quality filtering

Always filter. `FilterCriteria(min_score=0.7)`, labeler confidence thresholds (0.7-0.9), and/or agreement checks. Bad Q&A pairs poison SFT faster than they do RL.

## SFT training

```python
from lightningrod import SFTTrainingConfig
from lightningrod.training import prepare_for_training, FilterParams, SplitParams

train_dataset, test_dataset = prepare_for_training(
    dataset,
    filter=FilterParams(),
    split=SplitParams(test_size=0.2),        # temporal split not required — no forecasting
)

config = SFTTrainingConfig(
    base_model_id="Qwen/Qwen3-8B-Instruct",  # or "openai/gpt-oss-120b" for production
    training_steps=50,
    epochs=3,
    learning_rate=2e-4,
)

cost = lr.training.estimate_cost(config, dataset=train_dataset)
job = lr.training.run(config, dataset=train_dataset, name="...-sft-v1")
# job.model_id is your LoRA checkpoint. Serve via lr.predict(...).
```

## Watch for

- **Wrong generator kills quality.** Documents -> `QuestionAndLabelGenerator` (no labeler). Topics -> `QuestionGenerator` + `WebSearchLabeler`. Don't mix.
- **System / labeler instructions are training signal.** Whatever persona, tone, or format you set becomes baked into the model — shape it deliberately.
- Spot-check 10-20 generated Q&A pairs before scaling.
- `max_questions=100` as a smoke test before running the full pipeline.

## References

- Full worked pipelines: `agent-docs/content-learning-examples.md` (survival LLM via topic tree, medical textbook Q&A via documents).
- Runnable notebook: `notebooks/fine_tuning/03_survival_llm.ipynb`.
- Pattern overview: `agent-docs/examples-guide.md` (Pattern 2).
