# Lightningrod Claude Code Agents

Two agent setups for different use cases.

## lightningrod-assistant (default)

General-purpose SDK assistant. Works in any setup — scripts, notebooks, existing projects, one-off experiments. Has full domain knowledge about seeds, transforms, answer types, training, and evaluation. Communicates in high-level domain terms and asks clarifying questions before jumping into implementation.

**Best for:**
- Learning the SDK
- One-off scripts or notebook experiments
- Integrating Lightningrod into existing projects
- Debugging and exploring data
- Any task that doesn't need the structured multi-file workflow

## workflow-orchestrator

Structured multi-file workflow with specialist subagents. Produces a set of Python files (`seeds.py`, `dataset.py`, `prepare.py`, `train.py`, `eval.py`) with shared state via `state.json`. Enforces file ownership rules and back-propagation protocol between agents.

**Best for:**
- Full end-to-end dataset generation + fine-tuning pipelines
- Projects that benefit from the structured file-per-stage pattern
- Internal / power-user workflows

Invoke via slash commands:
- `/generate-dataset` — full pipeline from goals to dataset
- `/fine-tune` — training and evaluation workflow
- `/estimate-cost` — cost estimation for a pipeline

## Skills (shared domain knowledge)

Skills encode reusable domain knowledge. Both agents share most skills:

| Skill | Used by | Purpose |
|-------|---------|---------|
| examples-guide | both | Decision tree for choosing training patterns |
| forward-looking-examples | both | GRPO training examples (golf, Trump, military, GDELT) |
| content-learning-examples | both | SFT training examples (topic trees, document Q&A) |
| tabular-examples | both | Tabular data processing (CSV, BigQuery, structured data) |
| bigquery-seeds | both | BigQuery seed sourcing patterns |
| custom-dataset-seeds | both | File/CSV/PDF seed conversion |
| public-dataset-exploration | both | Finding datasets on Kaggle/HuggingFace/GitHub |
| transform-pipeline-verification | both | Pipeline verification and explore.py patterns |
| workflow-architecture | orchestrator only | File ownership, state.json contract, back-propagation |

## Switching the default agent

Edit `.claude/settings.json`:

```json
{"agent": "lightningrod-assistant"}
```

or

```json
{"agent": "workflow-orchestrator"}
```
