---
name: workflow-architecture
description: File-based workflow structure for Lightningrod projects. Use when creating or modifying project files, understanding agent ownership boundaries, reading/writing shared state, or coordinating back-propagation between agents.
---

# Workflow Architecture

Each stage of the pipeline lives in its own plain Python file. Files are independently runnable — rerunning `eval.py` never affects `train.py`, rerunning `train.py` never affects `dataset.py`, and so on.

## Project file structure

```
<project>/
  state.py      # Shared state utilities — copied from .claude/templates/state.py, never modified
  state.json    # Shared run state: resource IDs only (read/written by all agents)
  seeds.py      # Seed preparation (owned by seeds specialist)
  dataset.py    # Dataset generation (owned by dataset-generator)
  prepare.py    # prepare_for_training config (owned by dataset-generator, imported by train + eval)
  train.py      # Fine-tuning (owned by fine-tuner)
  eval.py       # Evaluation (owned by fine-tuner — separate from training)
```

## Project initialization

Before any agent writes code, the orchestrator initializes the project directory by running the setup script from the repo:

```bash
python .claude/templates/setup.py <project_dir>
```

This copies `state.py` from `.claude/templates/` and creates a blank `state.json`. It is idempotent — safe to run again if the directory already exists.

Agents never write state management or client initialization inline. They always import from `state.py`:

```python
from state import get_client, State

lr = get_client()
state = State.load()

# Read a field — raises automatically if not yet populated
dataset_id = state.dataset_id

# input_dataset_id is Optional — returns None for news/GDELT seeds
if state.input_dataset_id:
    input_dataset = lr.datasets.get(state.input_dataset_id)

# Write back
state.model_id = job.model_id
state.save()
```

## File ownership — strict

Each agent may only create or modify its own file(s). No agent touches another agent's file.

| File | Owner | Can modify |
|------|-------|-----------|
| `seeds.py` | seeds specialist (whichever is active) | seeds specialist only |
| `dataset.py` | dataset-generator | dataset-generator only |
| `prepare.py` | dataset-generator | dataset-generator only |
| `train.py` | fine-tuner | fine-tuner only |
| `eval.py` | fine-tuner | fine-tuner only |
| `state.json` | all agents | all agents (read + write) |

## state.json — shared run state

Resource IDs only — no config. Each script reads its inputs from `state.json` at startup and writes its outputs after creating a resource.

```json
{
  "input_dataset_id": "ds_abc123",
  "dataset_id": "ds_def456",
  "model_id": null
}
```

**Important:** `train_dataset_id` and `test_dataset_id` do not exist as stored resources and must never appear in `state.json`. The `prepare_for_training` config lives in `prepare.py` (see below), not in `state.json`. Config belongs in code; IDs belong in state.

Keys are set to `null` until the responsible script has been run. Use `get_state(key)` from `state.py` to read a value that must exist — it raises a clear error with the current state if it's missing or null.

## What each file does

### seeds.py
- Configures and validates the seed source (news query, BigQuery SQL, file ingestion, etc.)
- For file/BigQuery sources: runs ingestion and creates a Lightningrod input dataset
- For news/GDELT sources: validates the config and optionally previews a few seeds
- Writes `input_dataset_id` to `state.json` (set to `null` for news/GDELT — seed generator is inline)

### dataset.py
- Reads `input_dataset_id` from `state.json` (or uses inline seed generator for news/GDELT)
- Configures and runs the `QuestionPipeline` with `MAX_QUESTIONS = 10` by default
- Calls `get_datasets()` from `prepare.py` to validate the split is healthy (correct volume, no leakage, clean dedup)
- Writes `dataset_id` to `state.json`

### prepare.py
- Defines and exports `get_datasets(dataset_id) -> (train_ds, test_ds)` — the single source of truth for `prepare_for_training` config
- Imported by `dataset.py` (for validation), `train.py`, and `eval.py`
- When the dataset-generator adjusts filter/split params, this is the only file that changes

```python
# prepare.py
import lightningrod as lr
from lightningrod import prepare_for_training, FilterParams, DedupParams, SplitParams

def get_datasets(dataset_id):
    dataset = lr.datasets.get(dataset_id)
    return prepare_for_training(
        dataset,
        filter=FilterParams(days_to_resolution_range=(1, 60)),
        dedup=DedupParams(),
        split=SplitParams(strategy="temporal", test_size=0.2),
    )
```

### train.py
- Reads `dataset_id` from `state.json`
- Calls `from prepare import get_datasets; train_ds, _ = get_datasets(dataset_id)`
- Estimates cost, then runs `lr.training.run(...)`
- Writes `model_id` to `state.json`

### eval.py
- Reads `dataset_id` and `model_id` from `state.json`
- Calls `from prepare import get_datasets; _, test_ds = get_datasets(dataset_id)`
- Runs `lr.evals.run(...)` and prints results
- Writes nothing — safe to rerun any number of times without side effects

## Back-propagation protocol

When a downstream agent determines that an upstream stage needs to change, it **never modifies the upstream file directly**. Instead:

1. **Fine-tuner → dataset-generator**: Fine-tuner reports specific issues to the orchestrator (e.g. "too few test samples after split", "questions are too easy — binary accuracy near 100%"). Orchestrator delegates to dataset-generator with those get_statements. Dataset-generator modifies `dataset.py` and reruns it. New IDs are written to `state.json`. Fine-tuner then reruns `train.py`.

2. **Fine-tuner → seeds specialist**: If the root cause is seed quality (not enough diversity, wrong date range), fine-tuner reports to orchestrator. Orchestrator delegates to the seeds specialist to modify `seeds.py` and rerun. Then dataset-generator reruns `dataset.py`. Then fine-tuner reruns `train.py`.

3. **Dataset-generator → seeds specialist**: If `prepare_for_training` fails due to seed volume or quality, dataset-generator reports to orchestrator. Seeds specialist modifies `seeds.py`, reruns, new `input_dataset_id` is written. Dataset-generator reruns `dataset.py`.

**Rule: information flows downstream automatically via `state.json`. Change requests flow upstream via the orchestrator.**

## Rerunnability rules

| Script | Safe to rerun? | Side effects |
|--------|---------------|--------------|
| `seeds.py` | Yes | Creates a new input dataset (new ID written to state) |
| `dataset.py` | Yes | Creates a new dataset (new IDs written to state) |
| `train.py` | Yes | Starts a new training job (new model_id written to state) — costs money |
| `eval.py` | Yes, freely | No side effects, no cost impact |
