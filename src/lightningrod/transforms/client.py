import time
from typing import Optional, Union

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
)
from lightningrod._generated.api.datasets import (
    get_dataset_datasets_dataset_id_get,
)
from lightningrod._generated.api.transform_jobs import (
    create_transform_job_transform_jobs_post,
    get_transform_job_transform_jobs_job_id_get,
)
from lightningrod.datasets.dataset import Dataset
from lightningrod._generated.client import AuthenticatedClient
from lightningrod.datasets.client import DatasetSamplesClient

TransformConfig = Union[FileSetQuerySeedGenerator, FileSetSeedGenerator, ForwardLookingQuestionGenerator, GdeltSeedGenerator, NewsSeedGenerator, QuestionAndLabelGenerator, QuestionGenerator, QuestionPipeline, QuestionRenderer, WebSearchLabeler]

class TransformJobsClient:
    def __init__(self, client: AuthenticatedClient):
        self._client = client
    
    def get(self, job_id: str) -> TransformJob:
        response = get_transform_job_transform_jobs_job_id_get.sync(
            job_id=job_id,
            client=self._client,
        )
        if isinstance(response, HTTPValidationError):
            raise Exception(f"Failed to get transform job: {response.detail}")
        if response is None:
            raise Exception("Failed to get transform job: received None response")
        return response


class TransformsClient:
    def __init__(self, client: AuthenticatedClient, dataset_samples_client: DatasetSamplesClient):
        self._client: AuthenticatedClient = client
        self._dataset_samples_client: DatasetSamplesClient = dataset_samples_client
        self.jobs = TransformJobsClient(client)
    
    def run(
        self,
        config: TransformConfig,
        input_dataset: Optional[Union[Dataset, str]] = None,
        max_questions: Optional[int] = None
    ) -> Dataset:
        job: TransformJob = self.submit(config, input_dataset, max_questions)
        
        while job.status == TransformJobStatus.RUNNING:
            time.sleep(15)
            job = self.jobs.get(job.id)
        
        if job.status == TransformJobStatus.FAILED:
            raise Exception(f"Transform job {job.id} failed")
        
        if job.status == TransformJobStatus.COMPLETED:
            if job.output_dataset_id is None:
                raise Exception(f"Transform job {job.id} completed but has no output dataset")
            
            dataset_response = get_dataset_datasets_dataset_id_get.sync(
                dataset_id=job.output_dataset_id,
                client=self._client,
            )
            if isinstance(dataset_response, HTTPValidationError):
                raise Exception(f"Failed to get dataset: {dataset_response.detail}")
            if dataset_response is None:
                raise Exception("Failed to get dataset: received None response")
            
            return Dataset(
                id=dataset_response.id,
                num_rows=dataset_response.num_rows,
                datasets_client=self._dataset_samples_client
            )
        
        raise Exception(f"Unexpected job status: {job.status}")
    
    def submit(
        self,
        config: TransformConfig,
        input_dataset: Optional[Union[Dataset, str]] = None,
        max_questions: Optional[int] = None
    ) -> TransformJob:
        dataset_id: Optional[str] = None
        if isinstance(input_dataset, Dataset):
            dataset_id = input_dataset.id
        elif isinstance(input_dataset, str):
            dataset_id = input_dataset
        request: CreateTransformJobRequest = CreateTransformJobRequest(
            config=config,
            input_dataset_id=dataset_id,
            max_questions=max_questions
        )
        
        response = create_transform_job_transform_jobs_post.sync(
            client=self._client,
            body=request,
        )

        if isinstance(response, HTTPValidationError):
            raise Exception(f"Failed to submit transform job: {response.detail}")
        elif response is None:
            raise Exception("Failed to submit transform job: received None response")
        
        return response
