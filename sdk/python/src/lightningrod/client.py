import time
from typing import Any, List, Optional

from lightningrod._generated.client import AuthenticatedClient
from lightningrod._generated.models import (
    TransformJob,
    TransformJobStatus,
    CreateTransformJobRequest,
    HTTPValidationError,
)
from lightningrod._generated.models.sample import Sample
from lightningrod._generated.models.upload_samples_request import UploadSamplesRequest
from lightningrod._generated.models.upload_samples_response import UploadSamplesResponse
from lightningrod._generated.api.datasets import (
    create_dataset_datasets_post,
    get_dataset_datasets_dataset_id_get,
    get_dataset_samples_datasets_dataset_id_samples_get,
    upload_samples_datasets_dataset_id_samples_post,
)
from lightningrod._generated.api.transform_jobs import (
    create_transform_job_transform_jobs_post,
    get_transform_job_transform_jobs_job_id_get,
)
from lightningrod.dataset import Dataset
from lightningrod.pipeline import TransformPipeline, TransformConfig


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
        >>> dataset = client.pipeline(config).run()
        >>> samples = dataset.to_samples()
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
    
    def pipeline(self, config: Any) -> TransformPipeline:
        """
        Create a pipeline builder for executing transforms.
        
        Args:
            config: Transform configuration (NewsSeedGenerator, Pipeline, etc.)
        
        Returns:
            TransformPipeline instance for chaining
        
        Example:
            >>> client = LightningRodClient(api_key="your-api-key")
            >>> config = NewsSeedGenerator(...)
            >>> dataset = client.pipeline(config).run()
        """
        return TransformPipeline(self, config)
    
    def create_dataset(self, samples: List[Sample], batch_size: int = 1000) -> Dataset:
        """
        Upload samples to create a new dataset.
        
        Args:
            samples: List of Sample objects to upload
            batch_size: Number of samples to upload per batch (default 1000)
        
        Returns:
            Dataset instance for the created dataset
        
        Example:
            >>> from lightningrod import Sample, Seed
            >>> samples = [Sample(seed=Seed(seed_text="Article..."))]
            >>> dataset = client.create_dataset(samples)
            >>> output = client.pipeline(config).run(dataset)
        """
        create_response = create_dataset_datasets_post.sync(client=self._generated_client)
        if create_response is None:
            raise Exception("Failed to create dataset: received None response")
        dataset_id: str = create_response.id
        
        total_uploaded: int = 0
        for i in range(0, len(samples), batch_size):
            batch = samples[i:i + batch_size]
            request = UploadSamplesRequest(samples=batch)
            response = upload_samples_datasets_dataset_id_samples_post.sync(
                dataset_id=dataset_id,
                client=self._generated_client,
                body=request,
            )
            if isinstance(response, HTTPValidationError):
                raise Exception(f"Failed to upload samples: {response.detail}")
            if response is None:
                raise Exception("Failed to upload samples: received None response")
            total_uploaded = response.total
        
        return Dataset(
            id=dataset_id,
            num_rows=total_uploaded,
            client=self
        )
    
    def _fetch_all_samples(self, dataset_id: str) -> List[Sample]:
        """Fetch all samples from a dataset via the paginated API."""
        samples: List[Sample] = []
        cursor: Optional[str] = None
        
        while True:
            response = get_dataset_samples_datasets_dataset_id_samples_get.sync(
                dataset_id=dataset_id,
                client=self._generated_client,
                limit=1000,
                cursor=cursor,
            )
            
            if isinstance(response, HTTPValidationError):
                raise Exception(f"Failed to fetch samples: {response.detail}")
            if response is None:
                raise Exception("Failed to fetch samples: received None response")
            
            samples.extend(response.samples)
            
            if not response.has_more:
                break
            cursor = response.next_cursor
        
        return samples
    
    def _run(
        self,
        config: Any,
        dataset: Optional[Dataset] = None,
        max_seeds: Optional[int] = None
    ) -> Dataset:
        """Internal method to run a transform job and wait for completion."""
        job: TransformJob = self._submit(config, dataset, max_seeds)
        
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
            
            dataset_response = get_dataset_datasets_dataset_id_get.sync(
                dataset_id=job.output_dataset_id,
                client=self._generated_client,
            )
            if isinstance(dataset_response, HTTPValidationError):
                raise Exception(f"Failed to get dataset: {dataset_response.detail}")
            if dataset_response is None:
                raise Exception("Failed to get dataset: received None response")
            
            return Dataset(
                id=dataset_response.id,
                num_rows=dataset_response.num_rows,
                client=self
            )
        
        raise Exception(f"Unexpected job status: {job.status}")
    
    def _submit(
        self,
        config: Any,
        dataset: Optional[Dataset] = None,
        max_seeds: Optional[int] = None
    ) -> TransformJob:
        """Internal method to submit a transform job without waiting."""
        request: CreateTransformJobRequest = CreateTransformJobRequest(
            config=config,
            input_dataset_id=dataset.id if dataset else None,
            max_seeds=max_seeds
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
