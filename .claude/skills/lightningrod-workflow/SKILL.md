---
name: lightningrod-workflow
description: Orchestration flow for Lightningrod dataset generation. Use when planning workflows, deciding when to backtrack, choosing domain-level vocabulary, structuring notebooks, enforcing minimal-output iteration, or routing data sources.
---

# Lightningrod Workflow

## Flow

1. User states high-level goal (e.g. "generate a political forecasting dataset")
2. Orchestrator creates plan in plain language
3. Seeds specialist → seed sourcing cells
4. Transform specialist → pipeline and run cells
5. Notebook uses minimal limits (max_questions=10) for demo

## When to backtrack

- User says "that's not what I meant" or "the questions are wrong"
- Pipeline fails or produces poor samples → consider seeds adjustment
- Identify which step caused the mismatch; re-invoke that specialist with clarified domain-level requirements

## Domain-level vocabulary (orchestrator only)

Use these terms with users and when delegating to specialists. Do not use SDK class names.

| Domain term | SDK equivalent |
|-------------|----------------|
| news articles | NewsSeedGenerator |
| GDELT events | GdeltSeedGenerator |
| user's documents / file set | FileSetSeedGenerator, FileSetQuerySeedGenerator, files_to_samples |
| forecasting questions | ForwardLookingQuestionGenerator |
| template-based questions | TemplateQuestionGenerator |
| yes/no labels | BinaryAnswerType |
| numeric labels | ContinuousAnswerType |
| multiple choice | MultipleChoiceAnswerType |
| free-form text | FreeResponseAnswerType |
| web search for answers | WebSearchLabeler |

## Data source routing

| User situation | Action |
|----------------|--------|
| Has own documents | Delegate seeds specialist: "user's documents at path X" |
| Wants news / GDELT | Delegate seeds specialist: "news-based seeds, date range, topic" |
| Has domain, no data | Delegate seeds specialist: "explore public datasets for domain X" (Kaggle, Hugging Face, GitHub) |

## Notebook structure

1. Setup — pip install, load API key, LightningRod client
2. Seed sourcing — seed generator config
3. Pipeline — QuestionPipeline with generator, labeler, answer type
4. Run — lr.transforms.run(pipeline, max_questions=10)
5. Output — dataset.flattened(), sample inspection

## Minimal-output iteration

- Default max_questions=10 (or 5–20) for demo
- Restrict date ranges, search queries, file counts when exploring
- Scale up only when user confirms output looks right
- Use estimate_cost() before scaling; show cost implications
