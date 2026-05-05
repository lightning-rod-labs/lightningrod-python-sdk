# AGENTS.md

## What This Is

Python SDK for Lightning Rod — an AI-powered platform for generating forecasting datasets to train LLMs. Users build `QuestionPipeline` configs (seed generators → question generators → labelers) and run them via `lr.transforms.run(pipeline)` to produce labeled datasets.

## Commands

```bash
make install-dev          # Install with dev deps (editable mode)
make test                 # Run all tests: pytest tests/ -v
python -m pytest tests/test_tabular.py -v   # Single test file
python -m pytest tests/test_tabular.py::test_name -v  # Single test
make generate             # Regenerate _generated/ client (requires local API on :8080)
make bump-patch           # Version bump (also: bump-minor, bump-major)
make publish-new-version  # Build + upload to PyPI
```

## Architecture

### Source layout (`src/lightningrod/`)

- **`client.py`** — `LightningRod` is the main entry point. Instantiates sub-clients for each API domain (transforms, datasets, training, evals, files, filesets, organization). Also provides `lr.predict()` via OpenAI-compatible API.
- **`_generated/`** — Auto-generated from `openapi/openapi.json` via `openapi-python-client`. **Do not edit manually** — run `make generate` instead (needs the API server running locally on port 8080).
- **`transforms/`** — `TransformsClient` orchestrates pipeline jobs: create, poll, cancel, cost estimation. `lr.transforms.run()` is the primary user-facing method.
- **`datasets/`** — `SampleDataset` / `AsyncDataset` wrap API results with `.to_samples()`, `.flattened()`, `.to_dataframe()`. `DatasetsClient` handles CRUD. `linting.py` provides dataset quality analysis.
- **`training/`** — `TrainingClient` for fine-tuning jobs (GRPO/SFT configs). `EvalsClient` for evaluation runs. `samples.py` has `prepare_for_training()` for filtering/dedup/splitting.
- **`files/` + `filesets/`** — Upload and manage custom document collections.
- **`utils/`** — Helpers: `config.py` (env var overrides), `models.py` (OpenRouter integration), `examples.py` (example factories for answer types), `sample.py` (sample creation), `tabular.py` (tabular data handling), `metrics.py`.
- **`_display.py`** — Rich-based terminal/notebook display for job progress and lint results.
- **`_errors.py`** — Centralized API error handling.
- **`__init__.py`** — Re-exports all public types from `_generated.models` plus SDK utilities. This is the public API surface — all pipeline components, answer types, and configs are importable from `lightningrod` directly.

### Key patterns

- All API calls go through `_generated.client.AuthenticatedClient` (httpx-based, Bearer auth).
- Pipeline types (`QuestionPipeline`, seed generators, labelers, answer types) are Pydantic/attrs models defined in `_generated/models/` — the SDK re-exports them from `__init__.py`.
- `notebooks/` has user-facing examples (getting started, evaluation, fine-tuning, custom filesets).
- `docs/` contains GitBook documentation source.

### Code generation flow

The `_generated/` package is produced by `scripts/generate.py`, which fetches `openapi.json` from a local API server and runs `openapi-python-client`. When the API adds new endpoints or models, regenerate and then update imports in `__init__.py` and the relevant sub-client.

## SDK Agent (`agents/lightningrod-assistant`)

A Claude Code agent that sits on top of the SDK and guides users through forecasting dataset generation and fine-tuning flows. It is a standalone component — it uses the SDK as a library but has its own system prompt, skills, and MCP integration. Also distributed as a Claude Code plugin (see `.claude-plugin/`).

### Agent definition

`agents/lightningrod-assistant.md` (symlinked from `.claude/agents/`) — the full system prompt. Defines the agent's personality (domain-first, opinionated, no menus), the step-by-step flow (understand topic → draft example questions → build pipeline → test at scale → review → train → eval), hard constraints (never switch data sources as a quality fix, never invent custom filtering, etc.), answer type selection logic, environment setup rules, and the SDK surface reference.

Key behavioral rules baked into the agent prompt:
- First response is always text with drafted example questions — no tool calls.
- Uses `AskUserQuestion` for all clarifications, never plain-text question lists.
- Writes to `./userland/<project-name>/` by default.
- Runs notebook cells one at a time, never batch-executes.
- Picks data sources and answer types opinionatedly — does not present options as menus.
- Always calls `estimate_cost()` before scaling up.
- Compares trained models against gpt-5 in eval.

### Skills (`skills/`)

Skills live in the top-level `skills/` directory (symlinked from `.claude/skills` for Claude Code compatibility). Each skill is a `SKILL.md` file containing reference patterns, production configs, and domain knowledge the agent loads on demand. This placement makes skills discoverable by other agent frameworks (Hermes, OpenClaw, Codex) in addition to Claude Code. See `docs/agents.md` for cross-tool installation instructions.

| Skill | Purpose |
|-------|---------|
| **`lightningrod-assistant`** | End-to-end orchestration skill mirroring the Claude Code agent prompt. Lets non-Claude-Code frameworks (Hermes, OpenClaw, Codex) get the same flow, constraints, and vocabulary. |
| **`examples-guide`** | Decision tree: forward-looking (GRPO) vs content learning (SFT) vs tabular. Starting point for new projects. |
| **`forward-looking-examples`** | Production GRPO configs: golf, Trump policy, military strikes, Foresight/GDELT, FileSet RAG. The go-to reference for forecasting pipelines. |
| **`content-learning-examples`** | SFT patterns: TopicTree + WebSearch (survival guide), FileSet + QuestionAndLabel (medical textbooks). |
| **`tabular-examples`** | Structured data → Sample mapping: `create_sample()`, `TemplateQuestionGenerator`, supply chain shock detection walkthrough. |
| **`bigquery-seeds`** | BigQuery seed patterns. Key detail: no GCP credentials needed — LR manages access internally. Includes known-queryable public datasets. |
| **`custom-dataset-seeds`** | File/CSV/PDF → seeds via `preprocessing.files_to_samples()`, FileSet uploads, and `CsvSeedGenerator`. |
| **`public-dataset-exploration`** | Finding raw datasets on Kaggle, HuggingFace, GitHub when the user has a domain but no data. |
| **`transform-pipeline-verification`** | Post-`run()` inspection pattern: download samples, spot-check quality, iterate before scaling. |

### MCP integration

The agent connects to the Lightning Rod docs MCP server (`docs.lightningrod.ai/~gitbook/mcp`) and uses `mcp__lightningrod-docs__search-docs` to look up SDK documentation on demand.

### Developing the agent

When modifying the agent, keep these layers separate:
- **Agent prompt** (`lightningrod-assistant.md`) — behavioral rules, flow structure, communication style. Changes here affect how the agent interacts with users.
- **Skills** (`skills/*/SKILL.md`) — reference patterns, production configs, code examples. Changes here affect what the agent knows about specific SDK features.
- **SDK itself** (`src/lightningrod/`) — the actual library. The agent consumes it; changes here may require updating skills to reflect new APIs or patterns.
