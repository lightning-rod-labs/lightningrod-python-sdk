import time
from typing import Optional, Union

from lightningrod._display import display_error, display_warning
from lightningrod._generated.models import (
    FileSetQuerySeedGenerator,
    FileSetSeedGenerator,
    ForwardLookingQuestionGenerator,
    GdeltSeedGenerator,
    NewsSeedGenerator,
    QuestionAndLabelGenerator,
    QuestionGenerator,
    QuestionPipeline,
    QuestionRenderer,
    TransformJob,
    TransformJobStatus,
    CreateTransformJobRequest,
    HTTPValidationError,
    WebSearchLabeler,
    EstimateCostRequest,
    EstimateCostResponse,
)
from lightningrod._generated.api.datasets import (
    get_dataset_datasets_dataset_id_get,
)
from lightningrod._generated.api.transform_jobs import (
    create_transform_job_transform_jobs_post,
    get_transform_job_transform_jobs_job_id_get,
    cost_estimation_transform_jobs_cost_estimation_post
)
from lightningrod.datasets.dataset import Dataset
from lightningrod._generated.client import AuthenticatedClient
from lightningrod.datasets.client import DatasetSamplesClient
from lightningrod._generated.types import Unset
from lightningrod._errors import handle_response_error

TransformConfig = Union[FileSetQuerySeedGenerator, FileSetSeedGenerator, ForwardLookingQuestionGenerator, GdeltSeedGenerator, NewsSeedGenerator, QuestionAndLabelGenerator, QuestionGenerator, QuestionPipeline, QuestionRenderer, WebSearchLabeler]

class TransformJobsClient:
    def __init__(self, client: AuthenticatedClient):
        self._client = client
    
    def get(self, job_id: str) -> TransformJob:
        response = get_transform_job_transform_jobs_job_id_get.sync_detailed(
            job_id=job_id,
            client=self._client,
        )
        return handle_response_error(response, "get transform job")


class TransformsClient:
    def __init__(self, client: AuthenticatedClient, dataset_samples_client: DatasetSamplesClient):
        self._client: AuthenticatedClient = client
        self._dataset_samples_client: DatasetSamplesClient = dataset_samples_client
        self.jobs = TransformJobsClient(client)
    
    def run(
        self,
        config: TransformConfig,
        input_dataset: Optional[Union[Dataset, str]] = None,
        max_questions: Optional[int] = None,
        max_cost_dollars: Optional[float] = None
    ) -> Dataset:
        job: TransformJob = self.submit(config, input_dataset, max_questions, max_cost_dollars)
        
        while job.status == TransformJobStatus.RUNNING:
            time.sleep(15)
            job = self.jobs.get(job.id)
        
        if job.status == TransformJobStatus.FAILED:
            error_msg = job.error_message if (not isinstance(job.error_message, Unset) and job.error_message) else "Unknown error"
            display_error(error_msg, title="Job Failed", job=job)
            raise Exception(f"Transform job {job.id} failed: {error_msg}")

        if job.status == TransformJobStatus.COMPLETED:
            if job.output_dataset_id is None:
                raise Exception(f"Transform job {job.id} completed but has no output dataset")
            
            dataset_response = get_dataset_datasets_dataset_id_get.sync_detailed(
                dataset_id=job.output_dataset_id,
                client=self._client,
            )
            dataset_result = handle_response_error(dataset_response, "get dataset")
            
            return Dataset(
                id=dataset_result.id,
                num_rows=dataset_result.num_rows,
                datasets_client=self._dataset_samples_client
            )
        
        raise Exception(f"Unexpected job status: {job.status}")
    
    def submit(
        self,
        config: TransformConfig,
        input_dataset: Optional[Union[Dataset, str]] = None,
        max_questions: Optional[int] = None,
        max_cost_dollars: Optional[float] = None
    ) -> TransformJob:
        dataset_id: Optional[str] = None
        if isinstance(input_dataset, Dataset):
            dataset_id = input_dataset.id
        elif isinstance(input_dataset, str):
            dataset_id = input_dataset
        request: CreateTransformJobRequest = CreateTransformJobRequest(
            config=config,
            input_dataset_id=dataset_id,
            max_questions=max_questions,
            max_cost_dollars=max_cost_dollars,
        )
        
        response = create_transform_job_transform_jobs_post.sync_detailed(
            client=self._client,
            body=request,
        )

        job: TransformJob = handle_response_error(response, "submit transform job")

        if not isinstance(job.error_message, Unset) and job.error_message is not None:
            display_error(job.error_message, title="Error", job=job)
            raise Exception(f"Transform job {job.id} error: {job.error_message}")
        if not isinstance(job.warning_message, Unset) and job.warning_message is not None:
            display_warning(job.warning_message)

        return job

    def estimate_cost(self, config: TransformConfig, max_questions: Optional[int] = None) -> float:
        response = cost_estimation_transform_jobs_cost_estimation_post.sync_detailed(
            client=self._client,
            body=EstimateCostRequest(
                config=config,
                max_questions=max_questions,
            ),
        )
        parsed: EstimateCostResponse = handle_response_error(response, "estimate cost")
        return parsed.total_cost_dollars