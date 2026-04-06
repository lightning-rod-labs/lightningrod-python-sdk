---
name: content-learning-examples
description: Production examples for content learning (SFT) training -- survival field guide (TopicTree + WebSearch), medical textbooks (FileSet + QuestionAndLabel). Use when teaching domain knowledge via Q&A pairs and SFT.
---

# Content Learning Examples (SFT)

---

## Two Starting Points

**From documents**: Documents → chunk → `QuestionAndLabelGenerator` (extracts Q and A) → SFT. Use `QuestionAndLabelGenerator`, not `WebSearchLabeler` — the answers are in the documents.

**From a topic/domain (no documents)**: Domain → `TopicTreeSeedGenerator` → questions → `WebSearchLabeler` (finds answers from the web) → SFT.

---

## Example 1: Survival Field Guide (Topic Tree + Web Q&A)

**Goal:** Train a model to give step-by-step survival instructions for grid-down emergencies.

`TopicTreeSeedGenerator` decomposes broad domains into specific leaf seeds for coverage, then `WebSearchLabeler` finds authoritative answers from the web.

> **Source**: `lightningrod-python-sdk/notebooks/fine_tuning/03_survival_llm.ipynb`

### Pipeline

```python
from lightningrod import (
    LightningRod, QuestionPipeline,
    QuestionGenerator, FreeResponseAnswerType, WebSearchLabeler,
)
# TopicTreeSeedGenerator is coming soon — not yet available in the SDK.
# When released, import it from lightningrod and use as shown below.
from lightningrod import TopicTreeSeedGenerator  # available soon

lr = LightningRod(api_key=api_key)

answer_type = FreeResponseAnswerType(
    labeler_instruction=(
        "You are a survival expert giving emergency field instructions. "
        "Direct, numbered steps. No introductions or disclaimers. "
        "Specific measurements and techniques."
    ),
    answer_format_instruction=(
        "Direct, step-by-step answer. Start with step 1, no introduction."
    ),
)

pipeline = QuestionPipeline(
    # TopicTreeSeedGenerator decomposes each root topic into degree^depth leaf seeds.
    # 16 roots × 5^2 = 400 specific seeds like
    # "Field medicine → improvising supplies → makeshift tourniquets"
    seed_generator=TopicTreeSeedGenerator(
        topic=[
            "Field medicine and trauma care in austere environments",
            "Water purification and safe water sourcing without electricity",
            "Food preservation, canning, and long-term storage without refrigeration",
            "Ham radio and emergency communications setup and operation",
            "Land navigation using map, compass, and natural indicators",
            "Growing food: gardening, permaculture, and seed saving",
            "Herbal medicine and natural remedies from wild plants",
            "Construction, structural repair, and improvised building",
            "Welding, metalworking, and tool fabrication",
            "Vehicle repair and mechanical troubleshooting without a shop",
            "Fire starting, fire management, and fuel sourcing",
            "Emergency shelter building from natural and salvaged materials",
            "Hunting, trapping, fishing, and wild game processing",
            "Knot tying, rope work, and cordage making",
            "Weather reading and natural forecasting without instruments",
            "Perimeter security, self-defense, and community safety planning",
        ],
        tree_depth=2,       # levels of recursive expansion
        tree_degree=5,      # subtopics per node
        model_name="google/gemini-3-flash-preview",
        model_system_prompt=(
            "You are an expert in survival and self-reliance. "
            "Generate specific, practical subtopics useful in a grid-down emergency."
        ),
    ),
    question_generator=QuestionGenerator(
        answer_type=answer_type,
        questions_per_seed=10,          # high — topic seeds are conceptual, not dense text
        instructions=(
            "Generate practical survival questions for grid-down emergencies. "
            "Specific, scenario-based, ask HOW to do something with limited tools. "
            "Each must cover a DISTINCT technique."
        ),
        examples=[
            "How do I purify water using only sand, gravel, and charcoal?",
            "How do I perform a needle decompression for tension pneumothorax in the field?",
            "How do I build a Dakota fire hole to minimize smoke and maximize heat?",
        ],
        bad_examples=[
            "What is survival? (too vague)",
            "Tell me about water purification. (not actionable)",
            "How does a ham radio work? (theoretical, not how-to)",
        ],
    ),
    labeler=WebSearchLabeler(answer_type=answer_type, confidence_threshold=0.8),
)

dataset = lr.transforms.run(pipeline, name="SurvivalLLM")
```

### SFT Training

```python
import tinker

SYSTEM_PROMPT = (
    "You are SurvivalLLM. Direct, step-by-step survival instructions. "
    "No introductions or disclaimers. Start with the first action."
)

sft_data = []
for s in dataset.download():
    if not s.is_valid: continue
    q, a = s.question.question_text, s.label.label
    if not q or not a or a == "undetermined": continue
    sft_data.append({"messages": [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": q},
        {"role": "assistant", "content": a},
    ]})

# Small model appropriate for on-device usage (survival in emergency)
BASE_MODEL = "Qwen/Qwen3-8B-Instruct"
service = tinker.ServiceClient()
trainer = service.create_lora_training_client(base_model_id=BASE_MODEL, train_unembed=False)
adam = tinker.AdamParams(learning_rate=2e-4)

for epoch in range(3):
    result = trainer.forward_backward(datums, loss_fn="cross_entropy").result()
    trainer.optim_step(adam).result()
    # loss: 1.49 → 1.46 → 1.40
```

---

## Example 2: Medical Textbooks (Document Q&A)

**Goal:** Train a model to answer clinical nutrition questions using knowledge from medical textbooks.

`QuestionAndLabelGenerator` extracts Q&A pairs directly from document chunks — no labeler needed since the answers are in the text.

> **Source**: `llm_forecasting/notebooks/client_work/takeoff41/dataset_generation.ipynb`

### Step 1: Upload Documents to FileSet

```python
from lightningrod import (
    LightningRod, FileSetMetadataSchemaInput,
    MetadataFieldDefinitionInput, MetadataFieldType,
)

lr = LightningRod(api_key=api_key)

schema = FileSetMetadataSchemaInput(fields=[
    MetadataFieldDefinitionInput(
        name="book_title", field_type=MetadataFieldType.STRING, required=True,
        description="Title of the textbook"
    ),
])

fileset = lr.filesets.create(
    name="Medical Nutrition Textbooks",
    description="Clinical nutrition textbooks for SFT training data",
    metadata_schema=schema,
)

# Upload each PDF with metadata
for pdf_path, title in textbooks:
    lr.filesets.files.upload(
        file_set_id=fileset.id,
        file_path=pdf_path,
        metadata={"book_title": title},
    )

# Wait for file processing (PENDING → PROCESSING → ACTIVE)
# Poll lr.filesets.files.list(fileset.id) until all files are ACTIVE
```

### Step 2: Run Q&A Generation Pipeline

```python
from lightningrod import (
    QuestionPipeline, FileSetSeedGenerator,
    QuestionAndLabelGenerator, FreeResponseAnswerType,
)

pipeline = QuestionPipeline(
    seed_generator=FileSetSeedGenerator(
        file_set_id=fileset.id,
        chunk_size=4000,        # larger chunks = more context per Q&A
        chunk_overlap=200,
    ),
    question_generator=QuestionAndLabelGenerator(
        answer_type=FreeResponseAnswerType(),
        questions_per_seed=3,   # 3 Q&A pairs per chunk — dense medical text
        instructions=(
            "Generate questions testing understanding of clinical nutrition concepts, "
            "medical procedures, and evidence-based practices. Specific, proper terminology. "
            "Answers should cite specific values/ranges when mentioned."
        ),
    ),
)

dataset = lr.transforms.run(pipeline, max_questions=12000, name="Medical nutrition Q&A")
```

### Step 3: Filter and Format for SFT

```python
sft_data = []
for s in dataset.download():
    if not s.is_valid: continue
    q, a = s.question.question_text, s.label.label
    if not q or not a or a == "undetermined": continue
    sft_data.append({"messages": [
        {"role": "system", "content": "You are a clinical nutrition expert."},
        {"role": "user", "content": q},
        {"role": "assistant", "content": a},
    ]})
```

### Results

| Book                        | Q&A Pairs  |
| --------------------------- | ---------- |
| ASPEN Parenteral Nutrition  | 1,504      |
| ASPEN Fluids & Electrolytes | 1,127      |
| ASPEN Pediatric Nutrition   | 3,787      |
| Handbook                    | 1,347      |
| NBNSC Book                  | 908        |
| Pediatric Nutrition         | 1,666      |
| **Total**                   | **10,339** |


---

## Things to Watch For

- From documents: use `QuestionAndLabelGenerator`, not `WebSearchLabeler` — answers are in the documents
- From topics: `WebSearchLabeler` is correct — the web provides answers for topic-generated questions
- **Quality filter always.** `FilterCriteria(min_score=0.7)`, score cutoffs, or agreement checks
- **System prompt matters.** Shapes persona and gets baked into training data
- **Match `questions_per_seed` to density:** topic tree nodes → 10, doc chunks (4000) → 3, doc chunks (2000) → 2, short text → 1
