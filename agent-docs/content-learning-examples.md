# Content Learning Examples (SFT)

---

## Two Sub-Patterns

**2A — Document Q&A**: Documents → chunk → `QuestionAndLabelGenerator` (extracts Q and A) → SFT.

**2B — Topic-Driven Knowledge**: Domain → `TopicTreeSeedGenerator` → questions → `WebSearchLabeler` (finds answers) → SFT.

---

## Example 1: Survival Field Guide (2B — Topic Tree + Web Q&A)

Train a model to give step-by-step survival instructions. `TopicTreeSeedGenerator` decomposes broad domains into specific leaf seeds for coverage, then `WebSearchLabeler` finds authoritative answers from the web.

> **Source**: `lightningrod-python-sdk/notebooks/fine_tuning/03_survival_llm.ipynb`

### Pipeline

```python
from lightningrod import (
    LightningRod, QuestionPipeline, TopicTreeSeedGenerator,
    QuestionGenerator, FreeResponseAnswerType, WebSearchLabeler,
)

lr = LightningRod()

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
import json, tinker

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

# Small model appropriate for focused domain with ~100s of examples
# For larger datasets (1000+), use openai/gpt-oss-120b
BASE_MODEL = "Qwen/Qwen3-8B-Instruct"
service = tinker.ServiceClient()
trainer = service.create_lora_training_client(base_model=BASE_MODEL, train_unembed=False)
adam = tinker.AdamParams(learning_rate=2e-4)

for epoch in range(3):
    result = trainer.forward_backward(datums, loss_fn="cross_entropy").result()
    trainer.optim_step(adam).result()
    # loss: 1.49 → 1.46 → 1.40
```

---

## Example 2: Medical Textbooks (2A — Document Q&A)

Generate free-response Q&A from 6 medical textbooks. `QuestionAndLabelGenerator` pulls Q and A from chunks — no labeler.

> **Source**: `llm_forecasting/notebooks/client_work/takeoff41/dataset_generation.ipynb`

```python
from lightningrod import QuestionAndLabelGenerator, AnswerTypes

# 3,466 chunks from 6 textbooks (4000 tokens, 200 overlap, header-recursive splitting)

qa_config = QuestionAndLabelGenerator(
    answer_type=AnswerTypes.free_response(),
    questions_per_seed=3,
    instructions=(
        "Generate questions testing understanding of clinical nutrition concepts, "
        "medical procedures, and evidence-based practices. Specific, proper terminology. "
        "Answers should cite specific values/ranges when mentioned."
    ),
)
```

| Book | Q&A Pairs |
|------|-----------|
| ASPEN Parenteral Nutrition | 1,504 |
| ASPEN Fluids & Electrolytes | 1,127 |
| ASPEN Pediatric Nutrition | 3,787 |
| Handbook | 1,347 |
| NBNSC Book | 908 |
| Pediatric Nutrition | 1,666 |
| **Total** | **10,339** |

---

## Example 3: Call Transcripts (Conversation SFT)

Build SFT data from existing phone conversations. No Q&A generation — conversations ARE the data. Filter junk, score quality, convert to chat format.

> **Source**: `llm_forecasting/notebooks/client_work/caremaze/sft_dataset.ipynb`

```python
from lightningrodlabs.entities.model.model_config import ModelConfig

# Score conversations 0-5 with a rubric via large model
MODEL = ModelConfig.open_router("qwen/qwen3-235b-a22b-2507")
# 0=unusable, 1=poor, 2=below average, 3=acceptable, 4=good, 5=excellent

# 7,451 calls → 2,455 after junk filter → 1,268 at score >= 3
def to_sft(call):
    return {"messages": [
        {"role": "assistant" if t["speaker"] == "Caller" else "user", "content": t["text"]}
        for t in call.turns
    ]}
```

---

## Things to Watch For

- **2A**: Use `QuestionAndLabelGenerator`, not `WebSearchLabeler` — answers are in the documents
- **2B**: `WebSearchLabeler` is correct — the web provides answers for topic-generated questions
- **Quality filter always.** `FilterCriteria(min_score=0.7)`, score cutoffs, or agreement checks
- **System prompt matters.** Shapes persona and gets baked into training data
- **Match `questions_per_seed` to density:** topic tree nodes → 10, doc chunks (4000) → 3, doc chunks (2000) → 2, short text → 1
