from __future__ import annotations

from io import BytesIO
from pathlib import Path
from typing import TYPE_CHECKING
from urllib.parse import urlparse

import httpx

from lightningrod._display import _is_notebook, display_error, run_eval_live_display
from lightningrod._generated.api.evaluations import (
    create_eval_job_evaluations_post,
    get_eval_results_evaluations_eval_id_results_get,
    get_eval_job_evaluations_eval_id_get,
    list_eval_jobs_evaluations_get,
)
from lightningrod._generated.client import AuthenticatedClient
from lightningrod._generated.models import (
    EvalModel,
    EvalResultsDownloadResponse,
    ReasoningComparisonOptions,
)
from lightningrod._generated.models.create_eval_job_request import CreateEvalJobRequest
from lightningrod._generated.models.eval_job import EvalJob
from lightningrod._generated.models.eval_job_list_response import EvalJobListResponse
from lightningrod._generated.models.eval_job_status import EvalJobStatus
from lightningrod._generated.models.training_job import TrainingJob
from lightningrod._generated.types import UNSET, Unset
from lightningrod._errors import handle_response_error
from lightningrod.training.client import (
    SFTTrainingConfig,
    TrainingMethodConfig,
    sample_dataset_to_config,
)
from lightningrod.datasets.dataset import SampleDataset

if TYPE_CHECKING:
    import pandas as pd


def _safe_filename(value: str) -> str:
    return (
        "".join(c if c.isalnum() or c in "._-" else "_" for c in value).strip("_")
        or "results"
    )


class EvalsClient:
    def __init__(self, client: AuthenticatedClient):
        self._client = client

    def create(
        self,
        dataset: SampleDataset,
        models: list[EvalModel],
        *,
        reasoning_comparison: ReasoningComparisonOptions | None | Unset = UNSET,
    ) -> EvalJob:
        dataset_config = sample_dataset_to_config(dataset)
        body = CreateEvalJobRequest(
            models=models,
            dataset=dataset_config,
            reasoning_comparison=reasoning_comparison,
        )
        response = create_eval_job_evaluations_post.sync_detailed(
            client=self._client,
            body=body,
        )
        return handle_response_error(response, "create eval job")

    def get(self, eval_id: str) -> EvalJob:
        response = get_eval_job_evaluations_eval_id_get.sync_detailed(
            eval_id=eval_id,
            client=self._client,
        )
        return handle_response_error(response, "get eval job")

    def list(
        self,
        *,
        page: int = 1,
        limit: int = 10,
    ) -> EvalJobListResponse:
        response = list_eval_jobs_evaluations_get.sync_detailed(
            client=self._client,
            page=page,
            limit=limit,
        )
        return handle_response_error(response, "list eval jobs")

    def get_results(self, eval_id: str) -> EvalResultsDownloadResponse:
        """Get signed download URLs for eval rollout results."""
        response = get_eval_results_evaluations_eval_id_results_get.sync_detailed(
            eval_id=eval_id,
            client=self._client,
        )
        return handle_response_error(response, "get eval results")

    def download_results(
        self,
        eval_id: str,
        output_dir: str | Path = ".",
        *,
        timeout: float = 1800.0,
    ) -> dict[str, Path]:
        """Download eval rollout result files and return paths by model id."""
        downloads = self.get_results(eval_id).results.additional_properties
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        paths: dict[str, Path] = {}
        with httpx.Client() as http_client:
            for model_id, download in downloads.items():
                suffix = Path(urlparse(download.download_url).path).suffix or ".parquet"
                path = (
                    output_path
                    / f"{_safe_filename(eval_id)}_{_safe_filename(model_id)}{suffix}"
                )
                with http_client.stream(
                    "GET", download.download_url, timeout=timeout
                ) as response:
                    response.raise_for_status()
                    with path.open("wb") as file:
                        for chunk in response.iter_bytes():
                            file.write(chunk)
                paths[model_id] = path

        return paths

    def load_results(
        self,
        eval_id: str,
        *,
        timeout: float = 1800.0,
    ) -> dict[str, "pd.DataFrame"]:
        """Load eval rollout parquet files as pandas DataFrames by model id."""
        try:
            import pandas as pd
        except ImportError as exc:
            raise ImportError(
                "pandas is required to load eval results as DataFrames. "
                "Install it with `pip install pandas`."
            ) from exc

        downloads = self.get_results(eval_id).results.additional_properties
        dataframes: dict[str, pd.DataFrame] = {}
        with httpx.Client() as http_client:
            for model_id, download in downloads.items():
                response = http_client.get(download.download_url, timeout=timeout)
                response.raise_for_status()
                dataframes[model_id] = pd.read_parquet(BytesIO(response.content))

        return dataframes

    def run(
        self,
        dataset: SampleDataset,
        models: list[EvalModel],
        *,
        reasoning_comparison: ReasoningComparisonOptions | None | Unset = UNSET,
    ) -> EvalJob:
        """Create an eval job, poll until completion, and show live progress in notebooks.

        For the usual base-vs-fine-tuned benchmark after GRPO training, use
        :meth:`run_from_training_job` instead; it fills in models from the training config and job.
        """
        eval_job = self.create(
            models=models,
            dataset=dataset,
            reasoning_comparison=reasoning_comparison,
        )

        if eval_job.status == EvalJobStatus.FAILED:
            error_msg = (
                eval_job.error_message
                if not isinstance(eval_job.error_message, Unset) and eval_job.error_message
                else "Unknown error"
            )
            display_error(error_msg, title="Eval Failed", job=eval_job)
            if not _is_notebook():
                raise Exception(f"Eval job {eval_job.id} failed: {error_msg}")

        def poll() -> EvalJob:
            nonlocal eval_job
            eval_job = self.get(eval_job.id)
            return eval_job

        run_eval_live_display(poll, initial_job=eval_job)
        return eval_job

    def run_from_training_job(
        self,
        config: TrainingMethodConfig,
        job: TrainingJob,
        dataset: SampleDataset,
        *,
        extra_models: list[EvalModel] | None = None,
        reasoning_comparison_sample_size: int = 0,
    ) -> EvalJob:
        """Like :meth:`run` but builds the model list from training state.

        The benchmark includes two models, in order: the **base** checkpoint
        (``config.base_model_id``) and the **fine-tuned** model (``job.model_id``). Use
        ``extra_models`` only for additional models (e.g. third-party baselines).
        Set ``reasoning_comparison_sample_size`` to compare base vs. fine-tuned reasoning.
        Set ``reasoning_comparison_sample_size`` to 0 to disable reasoning comparison.

        Raises:
            NotImplementedError: If ``config`` is :class:`~lightningrod.training.client.SFTTrainingConfig`
                (SFT eval metrics are not implemented yet). Use :meth:`run` or :meth:`create` for a custom model list.
            ValueError: If ``job.model_id`` is missing (training not finished).
        """
        if isinstance(config, SFTTrainingConfig):
            raise NotImplementedError(
                "Evaluation metrics for SFT training are not implemented yet. Use GRPO with "
                "evals.run_from_training_job(), or use lr.evals.run(...) / lr.evals.create(...) "
                "to define a custom eval model list."
            )

        finetuned_id = job.model_id
        if isinstance(finetuned_id, Unset) or finetuned_id is None:
            raise ValueError(
                "Training job has no model_id yet; wait until training completes before running evals."
            )

        models: list[EvalModel] = [
            EvalModel(model_id=config.base_model_id, label="Base"),
            EvalModel(model_id=finetuned_id, label="Fine-tuned"),
        ]
        if extra_models:
            models.extend(extra_models)

        reasoning_options: ReasoningComparisonOptions | Unset = UNSET
        if reasoning_comparison_sample_size > 0:
            reasoning_options = ReasoningComparisonOptions(
                base_model_id=config.base_model_id,
                trained_model_id=finetuned_id,
                n=reasoning_comparison_sample_size,
            )

        return self.run(
            dataset,
            models,
            reasoning_comparison=reasoning_options,
        )
