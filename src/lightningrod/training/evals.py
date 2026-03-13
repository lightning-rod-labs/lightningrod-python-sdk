from lightningrod._display import _is_notebook, display_error, run_eval_live_display
from lightningrod._generated.api.evaluations import (
    create_eval_job_evaluations_post,
    get_eval_job_evaluations_eval_id_get,
    list_eval_jobs_evaluations_get,
)
from lightningrod._generated.client import AuthenticatedClient
from lightningrod._generated.models import SampleDatasetConfig
from lightningrod._generated.models.create_eval_job_request import CreateEvalJobRequest
from lightningrod._generated.models.eval_job import EvalJob
from lightningrod._generated.models.eval_job_list_response import EvalJobListResponse
from lightningrod._generated.models.training_job_status import TrainingJobStatus
from lightningrod._generated.types import UNSET, Unset
from lightningrod._errors import handle_response_error
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from lightningrod.datasets.dataset import SampleDataset


def _dataset_for_api(
    dataset: "SampleDataset | SampleDatasetConfig",
    prompt_template: str | None = None,
) -> SampleDatasetConfig:
    from lightningrod.datasets.dataset import SampleDataset

    if not isinstance(dataset, SampleDataset):
        return dataset
    ids = dataset.sample_ids if dataset.sample_ids is not None else [s.id for s in dataset.samples()]
    return SampleDatasetConfig(
        id=dataset.id,
        sample_ids=ids,
        prompt_template=prompt_template if prompt_template is not None else UNSET,
    )


class EvalsClient:
    def __init__(self, client: AuthenticatedClient):
        self._client = client

    def create(
        self,
        model_id: str,
        dataset: "SampleDataset | SampleDatasetConfig",
        *,
        prompt_template: str | None = None,
        benchmark_model_id: str | None = None,
        temperature: float = 0.0,
    ) -> EvalJob:
        dataset = _dataset_for_api(dataset, prompt_template=prompt_template)
        body = CreateEvalJobRequest(
            model_id=model_id,
            dataset=dataset,
            benchmark_model_id=benchmark_model_id if benchmark_model_id is not None else UNSET,
            temperature=temperature,
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
        model_id: str,
        dataset: "SampleDataset | SampleDatasetConfig",
        *,
        prompt_template: str | None = None,
        benchmark_model_id: str | None = None,
        temperature: float = 0.0,
        poll_interval: float = 15,
    ) -> EvalJob:
        job = self.create(
            model_id=model_id,
            dataset=dataset,
            prompt_template=prompt_template,
            benchmark_model_id=benchmark_model_id,
            temperature=temperature,
        )

        if job.status == TrainingJobStatus.FAILED:
            error_msg = (
                job.error_message
                if not isinstance(job.error_message, Unset) and job.error_message
                else "Unknown error"
            )
            display_error(error_msg, title="Eval Failed", job=job)
            if not _is_notebook():
                raise Exception(f"Eval job {job.id} failed: {error_msg}")

        def poll() -> EvalJob:
            nonlocal job
            job = self.get(job.id)
            return job

        run_eval_live_display(poll, poll_interval=poll_interval, initial_job=job)
        return job
