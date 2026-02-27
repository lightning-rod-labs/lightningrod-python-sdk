from attr import dataclass
from lightningrod._display import _is_notebook, display_error, run_training_live_display
from lightningrod._generated.api.training_jobs import (
    create_training_job_training_jobs_post,
    estimate_training_cost_training_jobs_cost_estimation_post,
    get_training_job_training_jobs_job_id_get,
    list_training_jobs_training_jobs_get,
)
from lightningrod._generated.client import AuthenticatedClient
from lightningrod._generated.models.create_training_job_request import CreateTrainingJobRequest
from lightningrod._generated.models.estimate_training_cost_request import (
    EstimateTrainingCostRequest,
)
from lightningrod._generated.models.estimate_training_cost_response import (
    EstimateTrainingCostResponse,
)
from lightningrod._generated.models.training_job import TrainingJob
from lightningrod._generated.models.training_job_list_response import TrainingJobListResponse
from lightningrod._generated.models.training_job_status import TrainingJobStatus
from lightningrod._generated.types import UNSET, Unset
from lightningrod._errors import handle_response_error

@dataclass
class TrainingConfig:
    input_dataset_id: str | None = None
    dataset_path: str | None = None
    name: str | None = None
    base_model: str | None = None
    training_steps: int | None = None
    batch_size: int | None = None
    lora_rank: int | None = None

class TrainingClient:
    def __init__(self, client: AuthenticatedClient):
        self._client = client

    def create(
        self,
        config: TrainingConfig,
    ) -> TrainingJob:
        body = CreateTrainingJobRequest(
            input_dataset_id=config.input_dataset_id,
            dataset_path=config.dataset_path,
            name=config.name,
            base_model=config.base_model,
            training_steps=config.training_steps,
            batch_size=config.batch_size,
            lora_rank=config.lora_rank,
        )
        response = create_training_job_training_jobs_post.sync_detailed(
            client=self._client,
            body=body,
        )
        return handle_response_error(response, "create training job")

    def estimate_cost(
        self,
        config: TrainingConfig,
    ) -> EstimateTrainingCostResponse:
        body = EstimateTrainingCostRequest(
            input_dataset_id=config.input_dataset_id,
            dataset_path=config.dataset_path,
            base_model=config.base_model,
            training_steps=config.training_steps,
            batch_size=config.batch_size,
            lora_rank=config.lora_rank,
        )
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
        poll_interval: float = 15,
    ) -> TrainingJob:
        job = self.create(config=config)

        job_id = job.id

        def poll() -> tuple[TrainingJob, bool]:
            current = self.get(job_id)
            is_running = current.status in (TrainingJobStatus.RUNNING, TrainingJobStatus.STARTING)
            return current, is_running

        run_training_live_display(poll, poll_interval=poll_interval, initial_job=job)

        job = self.get(job_id)
        if job.status == TrainingJobStatus.FAILED:
            error_msg = (
                job.error_message
                if not isinstance(job.error_message, Unset) and job.error_message
                else "Unknown error"
            )
            display_error(error_msg, title="Training Failed", job=job)
            if not _is_notebook():
                raise Exception(f"Training job {job.id} failed: {error_msg}")

        return job
