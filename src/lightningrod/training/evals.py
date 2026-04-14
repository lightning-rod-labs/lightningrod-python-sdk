from __future__ import annotations

from lightningrod._display import _is_notebook, display_error, run_eval_live_display
from lightningrod._generated.api.evaluations import (
    create_eval_job_evaluations_post,
    get_eval_job_evaluations_eval_id_get,
    list_eval_jobs_evaluations_get,
)
from lightningrod._generated.client import AuthenticatedClient
from lightningrod._generated.models import EvalModel
from lightningrod._generated.models.create_eval_job_request import CreateEvalJobRequest
from lightningrod._generated.models.eval_job import EvalJob
from lightningrod._generated.models.eval_job_list_response import EvalJobListResponse
from lightningrod._generated.models.eval_job_status import EvalJobStatus
from lightningrod._generated.models.training_job import TrainingJob
from lightningrod._generated.types import Unset
from lightningrod._errors import handle_response_error
from lightningrod.training.client import (
    SFTTrainingConfig,
    TrainingMethodConfig,
    sample_dataset_to_config,
)
from lightningrod.datasets.dataset import SampleDataset


class EvalsClient:
    def __init__(self, client: AuthenticatedClient):
        self._client = client

    def create(
        self,
        dataset: SampleDataset,
        models: list[EvalModel],
    ) -> EvalJob:
        dataset_config = sample_dataset_to_config(dataset)
        body = CreateEvalJobRequest(
            models=models,
            dataset=dataset_config,
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

    def run(
        self,
        config: TrainingMethodConfig,
        job: TrainingJob,
        dataset: SampleDataset,
        *,
        extra_models: list[EvalModel] | None = None,
    ) -> EvalJob:
        """Create an eval job, poll until completion, and show live progress in notebooks.

        The benchmark always includes two models, in order: the **base** checkpoint
        (`config.base_model_id`) and the **fine-tuned** model (`job.model_id`). You do not
        pass these explicitly. Use ``extra_models`` only for additional models (e.g.
        third-party baselines).

        Raises:
            NotImplementedError: If ``config`` is :class:`~lightningrod.training.client.SFTTrainingConfig`
                (SFT eval metrics are not implemented yet). Use :meth:`create` for a custom model list.
            ValueError: If ``job.model_id`` is missing (training not finished).
        """
        if isinstance(config, SFTTrainingConfig):
            raise NotImplementedError(
                "Evaluation metrics for SFT training are not implemented yet. Use GRPO with "
                "evals.run(), or use lr.evals.create(...) to define a custom eval model list."
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

        eval_job = self.create(models=models, dataset=dataset)

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