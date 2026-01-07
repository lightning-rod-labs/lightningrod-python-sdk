import time
from typing import Any, List, Optional

import httpx

from lightningrod._generated.client import AuthenticatedClient
from lightningrod._generated.models import (
    TransformJob,
    TransformJobStatus,
    CreateTransformJobRequest,
    HTTPValidationError,
)
from lightningrod._generated.models.sample import Sample
from lightningrod._generated.api.datasets import get_dataset_samples_datasets_dataset_id_samples_get
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
            
            http_client: httpx.Client = self._generated_client.get_httpx_client()
            response: httpx.Response = http_client.get(f"/datasets/{job.output_dataset_id}")
            response.raise_for_status()
            data: dict = response.json()
            
            return Dataset(
                id=data["id"],
                num_rows=data["num_rows"],
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
