---
icon: clipboard-check
---

# Evaluation

Run evals on your trained model against a test dataset. Access via `lr.evals` on your `LightningRod` client.

## EvalModel

Specify each model to evaluate when using [`create`](#create) or [`run`](#run) (you supply the full list). For [`run_from_training_job`](#run_from_training_job), the SDK adds the base and fine-tuned models for you; use `EvalModel` only for [`extra_models`](#run_from_training_job).

| Parameter | Type | Required | Default | Description |
|-----------|------|---------|---------|-------------|
| `model_id` | str | Yes | — | Model ID to evaluate (trained model or any supported model) |
| `label` | `str \| None` | No | None | Human-readable label shown in results display |

```python
from lightningrod import EvalModel

EvalModel(model_id=job.model_id, label="my-fine-tune")
```

## Methods

### create

Create an eval job without waiting. You pass the **complete** list of models to compare:

```python
from lightningrod import EvalModel

eval_job = lr.evals.create(
    dataset=test_dataset,
    models=[EvalModel(model_id=job.model_id, label="my-fine-tune")],
)
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `dataset` | SampleDataset | — | Test dataset |
| `models` | `list[EvalModel]` | — | Models to evaluate |
| `reasoning_comparison` | `ReasoningComparisonOptions \| None` | Unset | Optional reasoning comparison config (see [Reasoning Comparison](#reasoning-comparison)) |

### run

Create an eval job and poll until completion. In notebooks, shows a live progress display. You pass the **full** `models` list (same idea as [`create`](#create), but waited).

```python
from lightningrod import EvalModel

eval_job = lr.evals.run(
    test_dataset,
    [
        EvalModel(model_id=config.base_model_id, label="Base"),
        EvalModel(model_id=training_job.model_id, label="Fine-tuned"),
    ],
)
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `dataset` | SampleDataset | — | Test dataset (e.g. test split). |
| `models` | `list[EvalModel]` | — | Models to evaluate (complete list). |
| `reasoning_comparison` | `ReasoningComparisonOptions \| None` | Unset | Optional reasoning comparison config (see [Reasoning Comparison](#reasoning-comparison)) |

### run_from_training_job

Same waiting behavior as [`run`](#run), but builds the model list from your training config and completed job.

The benchmark **always** includes two models, in order:

1. **Base** — `config.base_model_id` (label `"Base"`).
2. **Fine-tuned** — `job.model_id` after training completes (label `"Fine-tuned"`).

You do not pass these explicitly. Use **`extra_models`** only for additional models (e.g. OpenAI baselines).

**SFT:** `run_from_training_job` raises `NotImplementedError` if `config` is `SFTTrainingConfig`, because SFT-specific eval metrics are not implemented yet. Use **GRPO** with `run_from_training_job`, or use [`run`](#run) / [`create`](#create) with your own `EvalModel` list.

```python
from lightningrod import EvalModel

eval_job = lr.evals.run_from_training_job(
    config,
    training_job,
    test_dataset,
    extra_models=[
        EvalModel(model_id="openai/gpt-5.4", label="GPT-5.4"),
    ],
)
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `config` | `GRPOTrainingConfig \| SFTTrainingConfig` | — | Same training config you used with `lr.training.run` (SFT raises until supported). |
| `job` | `TrainingJob` | — | Completed job from `lr.training.run`; must have `model_id` set. |
| `dataset` | SampleDataset | — | Test dataset (e.g. test split). |
| `extra_models` | `list[EvalModel] \| None` | `None` | Optional extra models appended after Base and Fine-tuned. |
| `reasoning_comparison_sample_size` | `int` | `0` | Number of sample pairs for reasoning comparison between base and fine-tuned models. Set to `0` to disable. |

### get

Fetch a single eval job by ID:

```python
eval_job = lr.evals.get(eval_id)
```

### list

List eval jobs with pagination:

```python
response = lr.evals.list(page=1, limit=10)
for job in response.jobs:
    print(job.id, job.status)
```

## print\_eval

Pretty-print eval results:

```python
from lightningrod import training

eval_job = lr.evals.run_from_training_job(config, training_job, test_dataset)
training.print_eval(eval_job)
```

## Evaluating Intermediate Checkpoints

`run_from_training_job` always evaluates the **final** `job.model_id` as the fine-tuned slot. To compare intermediate checkpoints, swap in a different checkpoint as one of the `EvalModel` entries, or evaluate several checkpoints in one job, use **`run`** / **`create`** and pass the full `EvalModel` list yourself.

After training finishes, a completed **`TrainingJob`** exposes:

- **`job.model_id`** — the final trained adapter (same ID `run_from_training_job` uses as `"Fine-tuned"`).
- **`job.model_id_by_step`** — a mapping from **training step** to checkpoint **model ID**. Keys are strings (e.g. `"10"`, `"20"`). Values are the same model ID strings you pass to `EvalModel`. Inspect which steps exist on your job (`print(job.model_id_by_step)` or iterate keys) instead of assuming a particular step number.

Checkpoint cadence follows your [`save_frequency`](training.md) (and server defaults when omitted). Which step keys appear depends on the run; read them from the completed job.

`model_id_by_step` may be `None` or unset for some job states; only use keys that are actually present. SFT workflows that cannot use `run_from_training_job` for metrics still use the same pattern: build an explicit list of `EvalModel`s, including IDs from `model_id_by_step` when available.

Use [`run`](#run) if you want the same waited, live progress behavior as elsewhere; use [`create`](#create) if you only need to submit the eval and poll or fetch it yourself.

```python
from lightningrod import EvalModel
from lightningrod.training import print_eval

job = lr.training.run(config, dataset=train_dataset)

# Illustrative: pick a step that exists on your job (see job.model_id_by_step)
checkpoint_model_id = job.model_id_by_step["10"]

eval_job = lr.evals.run(
    test_dataset,
    [
        EvalModel(model_id=config.base_model_id, label="Base"),
        EvalModel(model_id=checkpoint_model_id, label="step-10"),
        EvalModel(model_id=job.model_id, label="final"),
    ],
)
print_eval(eval_job)
```

Same models with [`create`](#create) (no built-in wait; fetch or poll `eval_job.id` as needed):

```python
checkpoint_model_id = job.model_id_by_step["10"]  # illustrative; use a key from your job

eval_job = lr.evals.create(
    dataset=test_dataset,
    models=[
        EvalModel(model_id=checkpoint_model_id, label="step-10"),
        EvalModel(model_id=job.model_id, label="final"),
    ],
)
print_eval(eval_job)
```

## Reasoning Comparison

Compare the reasoning quality of two models side-by-side using an LLM judge. The judge evaluates `n` sample pairs and produces a report accessible on the completed `EvalJob`.

### ReasoningComparisonOptions

```python
from lightningrod import ReasoningComparisonOptions
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `model_a_id` | `str` | — | First model ID (typically the base model) |
| `model_b_id` | `str` | — | Second model ID (typically the fine-tuned model) |
| `judge_model_id` | `str` | `"anthropic/claude-sonnet-4.6"` | Model used as the judge |
| `n` | `int` | `10` | Number of sample pairs to compare |
| `instructions` | `str` | `"Compare the reasoning quality of the two models."` | Custom instructions for the judge |

### With `run` or `create`

Pass a `ReasoningComparisonOptions` directly:

```python
from lightningrod import ReasoningComparisonOptions

eval_job = lr.evals.run(
    test_dataset,
    [
        EvalModel(model_id=config.base_model_id, label="Base"),
        EvalModel(model_id=job.model_id, label="Fine-tuned"),
    ],
    reasoning_comparison=ReasoningComparisonOptions(
        model_a_id=config.base_model_id,
        model_b_id=job.model_id,
        n=20,
    ),
)
```

### With `run_from_training_job`

Use the shorthand `reasoning_comparison_sample_size` parameter — the SDK fills in `model_a_id` (base) and `model_b_id` (fine-tuned) for you:

```python
eval_job = lr.evals.run_from_training_job(
    config,
    training_job,
    test_dataset,
    reasoning_comparison_sample_size=20,
)
```

The reasoning comparison report is available on the completed job as `eval_job.reasoning_comparison_report`.

## Downloading Results

After an eval completes, download the per-model rollout results as Parquet files.

### get_results

Get signed download URLs for eval result files:

```python
response = lr.evals.get_results(eval_id)
# response.results is a dict of model_id -> {download_url, expires_at}
```

### download_results

Download result files to disk:

```python
paths = lr.evals.download_results(eval_id, output_dir="./results")
# paths is a dict of model_id -> Path
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `eval_id` | `str` | — | Eval job ID |
| `output_dir` | `str \| Path` | `"."` | Directory to save files |
| `timeout` | `float` | `1800.0` | HTTP download timeout in seconds |

### load_results

Load result files directly into pandas DataFrames (requires `pandas`):

```python
dataframes = lr.evals.load_results(eval_id)
# dataframes is a dict of model_id -> pd.DataFrame
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `eval_id` | `str` | — | Eval job ID |
| `timeout` | `float` | `1800.0` | HTTP download timeout in seconds |

## Example

```python
from lightningrod import EvalModel
from lightningrod.training import print_eval

eval_job = lr.evals.create(
    dataset=test_dataset,
    models=[
        EvalModel(model_id=job.model_id, label="fine-tuned"),
        EvalModel(model_id="openai/gpt-4.1", label="baseline"),
    ],
)
print_eval(eval_job)
```

See [notebooks/getting_started/05_grpo_training.ipynb](../../notebooks/getting_started/05_grpo_training.ipynb) for the full GRPO workflow including `evals.run_from_training_job`.
