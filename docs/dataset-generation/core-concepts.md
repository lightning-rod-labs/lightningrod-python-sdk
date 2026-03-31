---
icon: puzzle-piece
---

# Core Concepts

The dataset generation system is built around four concepts: **samples** (the data unit), **transforms** (dataset generation pipeline) and **datasets** (collections of samples). Understanding these makes the rest of the docs easier to follow.

## Sample

The fundamental unit of data. A sample contains:

| Field | Description |
|-------|-------------|
| `seed` | Raw starting data (news articles, documents, etc.) |
| `question` | Forecasting question generated from the seed |
| `label` | Ground truth answer with confidence score |
| `prompt` | Formatted prompt ready for model input |
| `context` | Additional context (news, RAG results) |
| `meta` | Custom metadata |
| `is_valid` | Whether the sample passed validation (default: True) |

Samples flow through the pipeline: seeds produce questions, questions get labeled, and the result is a sample ready for training or analysis.

## Transform

A dataset generation pipeline that processes data through multiple stages. Pipelines chain components:

- **Seed generator** — Produces raw data
- **Question generator** — Creates questions from seeds
- **Labeler** — Resolves questions with ground truth
- **Context generators** (optional) — Add relevant context
- **Renderer** (optional) — Format prompts

`QuestionPipeline` is the main orchestrator. You configure each stage and run it via `lr.transforms.run(config)`.

When you run a pipeline, the SDK submits a job to the server. The job executes the pipeline stages and produces an output dataset.

## Dataset

A collection of samples. Datasets serve as:

- **Input** — Feed custom samples into a pipeline via `input_dataset`
- **Output** — The result of `lr.transforms.run()` is a dataset

Datasets have an `id` and `num_rows`. Use `dataset.download()` or `dataset.samples()` to fetch samples, and `dataset.flattened()` for a flat list of dicts.