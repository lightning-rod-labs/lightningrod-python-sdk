from __future__ import annotations

from attrs import define
from lightningrod._display import _is_notebook, display_error, run_training_live_display
from lightningrod._generated.api.training_jobs import (
    create_training_job_training_jobs_post,
    estimate_training_cost_training_jobs_cost_estimation_post,
    get_training_job_training_jobs_job_id_get,
    list_training_jobs_training_jobs_get,
)
from lightningrod._generated.client import AuthenticatedClient
from lightningrod._generated.models import TrainingConfig
from lightningrod._generated.models.create_training_job_request import CreateTrainingJobRequest
from lightningrod._generated.models.estimate_training_cost_request import (
    EstimateTrainingCostRequest,
)
from lightningrod._generated.models.estimate_training_cost_response import (
    EstimateTrainingCostResponse,
)
from lightningrod._generated.models.training_config import TrainingConfig as ApiTrainingConfig
from lightningrod._generated.models.training_job import TrainingJob
from lightningrod._generated.models.training_job_list_response import TrainingJobListResponse
from lightningrod._generated.models.training_job_status import TrainingJobStatus
from lightningrod._generated.models.sample_dataset_config import SampleDatasetConfig
from lightningrod._generated.types import UNSET, Unset
from lightningrod._errors import handle_response_error
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from lightningrod.datasets.dataset import SampleDataset


@define
class TrainingConfig:
    base_model_id: str
    training_steps: int
    batch_size: int | None = None
    lora_rank: int | None = None
    learning_rate: float | None = None
    adam_beta1: float | None = None
    adam_beta2: float | None = None
    num_rollouts: int | None = None
    max_response_length: int | None = None
    start_idx: int | None = None


def sample_dataset_to_config(
    dataset: "SampleDataset",
) -> SampleDatasetConfig:
    ids = dataset.sample_ids if dataset.sample_ids is not None else [s.id for s in dataset.samples()]
    return SampleDatasetConfig(
        id=dataset.id,
        sample_ids=ids,
        prompt_template=dataset.prompt_template if dataset.prompt_template is not None else UNSET,
        multiple_choice_options=dataset.multiple_choice_options if dataset.multiple_choice_options is not None else UNSET,
    )

def _build_config(
    config: TrainingConfig,
    dataset: "SampleDataset",
) -> ApiTrainingConfig:
    dataset_config = sample_dataset_to_config(dataset)
    return ApiTrainingConfig(
        dataset=dataset_config,
        base_model_id=config.base_model_id,
        training_steps=config.training_steps,
        batch_size=config.batch_size if config.batch_size is not None else UNSET,
        lora_rank=config.lora_rank if config.lora_rank is not None else UNSET,
        learning_rate=config.learning_rate if config.learning_rate is not None else UNSET,
        adam_beta1=config.adam_beta1 if config.adam_beta1 is not None else UNSET,
        adam_beta2=config.adam_beta2 if config.adam_beta2 is not None else UNSET,
        num_rollouts=config.num_rollouts if config.num_rollouts is not None else UNSET,
        max_response_length=config.max_response_length if config.max_response_length is not None else UNSET,
        start_idx=config.start_idx if config.start_idx is not None else UNSET,
    )


class TrainingClient:
    def __init__(self, client: AuthenticatedClient):
        self._client = client

    def create(
        self,
        config: TrainingConfig,
        dataset: "SampleDataset",
        name: str | None = None,
    ) -> TrainingJob:
        full_config = _build_config(config, dataset)
        body = CreateTrainingJobRequest(
            config=full_config,
            name=name,
        )
        response = create_training_job_training_jobs_post.sync_detailed(
            client=self._client,
            body=body,
        )
        return handle_response_error(response, "create training job")

    def estimate_cost(
        self,
        config: TrainingConfig,
        dataset: "SampleDataset",
    ) -> EstimateTrainingCostResponse:
        full_config = _build_config(config, dataset)
        body = EstimateTrainingCostRequest(config=full_config)
        response = estimate_training_cost_training_jobs_cost_estimation_post.sync_detailed(
            client=self._client,
            body=body,
        )
        return handle_response_error(response, "estimate training cost")

    def get(self, job_id: str) -> TrainingJob:
        response = get_training_job_training_jobs_job_id_get.sync_detailed(
            job_id=job_id,
            client=self._client,
        )
        return handle_response_error(response, "get training job")

    def list(
        self,
        *,
        page: int = 1,
        limit: int = 10,
        status: str | None = None,
    ) -> TrainingJobListResponse:
        response = list_training_jobs_training_jobs_get.sync_detailed(
            client=self._client,
            page=page,
            limit=limit,
            status=status if status is not None else UNSET,
        )
        return handle_response_error(response, "list training jobs")

    def run(
        self,
        config: TrainingConfig,
        dataset: "SampleDataset",
        name: str | None = None,
        poll_interval: float = 15,
    ) -> TrainingJob:
        job = self.create(
            config=config,
            dataset=dataset,
            name=name,
        )

        if job.status == TrainingJobStatus.FAILED:
            error_msg = (
                job.error_message
                if not isinstance(job.error_message, Unset) and job.error_message
                else "Unknown error"
            )
            display_error(error_msg, title="Training Failed", job=job)
            if not _is_notebook():
                raise Exception(f"Training job {job.id} failed: {error_msg}")

        def poll() -> TrainingJob:
            # Update to return the latest job object at the end
            nonlocal job
            job = self.get(job.id)
            return job

        run_training_live_display(poll, poll_interval=poll_interval, initial_job=job)

        return job
