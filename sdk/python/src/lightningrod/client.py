import base64
import time
from typing import Optional

import pyarrow as pa

from lightningrod._generated.client import AuthenticatedClient
from lightningrod._generated.models import (
    DatasetMetadata,
    TransformJob,
    TransformJobStatus,
    CreateTransformJobRequest,
    NewsSeedGenerator,
    Pipeline,
    QuestionGenerator,
    QuestionPipeline,
    WebSearchLabeler,
    HTTPValidationError,
)
from lightningrod._generated.api.datasets import get_dataset_datasets_dataset_id_get
from lightningrod._generated.api.transform_jobs import (
    create_transform_job_transform_jobs_post,
    get_transform_job_transform_jobs_job_id_get,
)
from lightningrod.dataset import Dataset

TransformConfig = NewsSeedGenerator | Pipeline | QuestionGenerator | QuestionPipeline | WebSearchLabeler


class LightningRodClient:
    """
    Python client for the Lightning Rod API.
    
    This client provides access to Lightning Rod's AI-powered forecasting
    dataset generation platform.
    
    Args:
        api_key: Your Lightning Rod API key
        base_url: Base URL for the API (defaults to production)
    
    Example:
        >>> client = LightningRodClient(api_key="your-api-key")
        >>> dataset = client.get_dataset("dataset-123")
    """
    
    def __init__(
        self,
        api_key: str,
        base_url: str = "https://api.lightningrod.ai/api/public/v1"
    ):
        self.api_key: str = api_key
        self.base_url: str = base_url.rstrip("/")
        self._generated_client: AuthenticatedClient = AuthenticatedClient(
            base_url=self.base_url,
            token=api_key,
            prefix="Bearer",
            auth_header_name="Authorization",
        )
    
    def get_dataset(self, dataset_id: str) -> Dataset:
        """
        Get a dataset by its ID.
        
        Args:
            dataset_id: The ID of the dataset to retrieve
        
        Returns:
            Dataset instance with metadata loaded
        
        Raises:
            Exception: If the API returns an error
        
        Example:
            >>> client = LightningRodClient(api_key="your-api-key")
            >>> dataset = client.get_dataset("dataset-123")
            >>> table = dataset.to_arrow()
        """
        dataset_metadata: DatasetMetadata | HTTPValidationError | None = get_dataset_datasets_dataset_id_get.sync(
            dataset_id=dataset_id,
            client=self._generated_client,
        )
        
        if isinstance(dataset_metadata, HTTPValidationError):
            raise Exception(f"Failed to get dataset: {dataset_metadata.detail}")
        elif dataset_metadata is None:
            raise Exception("Failed to get dataset: received None response")
        
        schema_bytes: bytes = base64.b64decode(dataset_metadata.schema_base64)
        schema: pa.Schema = pa.ipc.read_schema(pa.py_buffer(schema_bytes))
        
        return Dataset(
            id=dataset_metadata.id,
            num_rows=dataset_metadata.num_rows,
            schema=schema,
            client=self
        )
    
    def run(
        self,
        config: TransformConfig,
        dataset: Optional[Dataset] = None
    ) -> Dataset:
        """
        Submit a transform job and wait for it to complete.
        
        This method will:
        1. Submit the transform job to the API
        2. Poll every 15 seconds to check the job status
        3. Return the output dataset when the job completes
        
        Args:
            config: Transform configuration (NewsSeedGenerator, Pipeline, etc.)
            dataset: Optional input dataset. If None, the transform runs without input data.
        
        Returns:
            Dataset instance for the output dataset
        
        Raises:
            Exception: If the job fails or API returns an error
        
        Example:
            >>> from lightningrod._generated.models import QuestionPipeline
            >>> client = LightningRodClient(api_key="your-api-key")
            >>> config = QuestionPipeline(config_type="QUESTION_PIPELINE", ...)
            >>> output_dataset = client.run(config)
        """
        job: TransformJob = self.submit(config, dataset)
        
        while job.status == TransformJobStatus.RUNNING:
            time.sleep(15)
            job = get_transform_job_transform_jobs_job_id_get.sync(
                job_id=job.id,
                client=self._generated_client,
            )
        
        if job.status == TransformJobStatus.FAILED:
            raise Exception(f"Transform job {job.id} failed")
        
        if job.status == TransformJobStatus.COMPLETED:
            if job.output_dataset_id is None:
                raise Exception(f"Transform job {job.id} completed but has no output dataset")
            
            return self.get_dataset(job.output_dataset_id)
        
        raise Exception(f"Unexpected job status: {job.status}")
    
    def submit(
        self,
        config: TransformConfig,
        dataset: Optional[Dataset] = None
    ) -> TransformJob:
        """
        Submit a transform job without waiting for completion.
        
        Args:
            config: Transform configuration (NewsSeedGenerator, Pipeline, etc.)
            dataset: Optional input dataset. If None, the transform runs without input data.
        
        Returns:
            TransformJob instance representing the submitted job
        
        Raises:
            Exception: If the submission fails or API returns an error
        
        Example:
            >>> from lightningrod._generated.models import QuestionPipeline
            >>> client = LightningRodClient(api_key="your-api-key")
            >>> config = QuestionPipeline(config_type="QUESTION_PIPELINE", ...)
            >>> job = client.submit(config)
            >>> print(f"Job ID: {job.id}, Status: {job.status}")
        """
        request: CreateTransformJobRequest = CreateTransformJobRequest(
            config=config,
            input_dataset_id=dataset.id if dataset else None
        )
        
        response = create_transform_job_transform_jobs_post.sync(
            client=self._generated_client,
            body=request,
        )

        if isinstance(response, HTTPValidationError):
            raise Exception(f"Failed to submit transform job: {response.detail}")
        elif response is None:
            raise Exception("Failed to submit transform job: received None response")
        
        return response
