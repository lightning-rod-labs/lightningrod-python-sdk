from typing import List, Optional

from lightningrod._generated.models import (
    HTTPValidationError,
    UploadSamplesRequest,
)
from lightningrod._generated.models.sample import Sample
from lightningrod._generated.api.datasets import (
    create_dataset_datasets_post,
    get_dataset_datasets_dataset_id_get,
    get_dataset_samples_datasets_dataset_id_samples_get,
    upload_samples_datasets_dataset_id_samples_post,
)
from lightningrod._generated.types import Unset
from lightningrod._generated.client import AuthenticatedClient
from lightningrod.datasets.dataset import Dataset


class DatasetSamplesClient:
    def __init__(self, client: AuthenticatedClient):
        self._client: AuthenticatedClient = client
    
    def list(self, dataset_id: str) -> List[Sample]:
        samples: List[Sample] = []
        cursor: Optional[str] = None
        
        while True:
            response = get_dataset_samples_datasets_dataset_id_samples_get.sync(
                dataset_id=dataset_id,
                client=self._client,
                limit=100,
                cursor=cursor,
            )
            
            if isinstance(response, HTTPValidationError):
                raise Exception(f"Failed to fetch samples: {response.detail}")
            if response is None:
                raise Exception("Failed to fetch samples: received None response")
            
            samples.extend(response.samples)
            
            if not response.has_more:
                break
            if isinstance(response.next_cursor, Unset) or response.next_cursor is None:
                break
            cursor = str(response.next_cursor)
        
        return samples
    
    def upload(
        self,
        dataset_id: str,
        samples: List[Sample],
    ) -> None:
        """
        Upload samples to an existing dataset.
        
        Args:
            dataset_id: ID of the dataset to upload samples to
            samples: List of Sample objects to upload
            
        Example:
            >>> client = LightningRod(api_key="your-api-key")
            >>> dataset = client.datasets.create()
            >>> samples = [Sample(seed=Seed(...), ...), ...]
            >>> client._dataset_samples.upload_samples(dataset.id, samples)
        """
        request = UploadSamplesRequest(samples=samples)
        
        response = upload_samples_datasets_dataset_id_samples_post.sync(
            dataset_id=dataset_id,
            client=self._client,
            body=request,
        )
        
        if isinstance(response, HTTPValidationError):
            raise Exception(f"Failed to upload samples: {response.detail}")
        if response is None:
            raise Exception("Failed to upload samples: received None response")


class DatasetsClient:
    def __init__(self, client: AuthenticatedClient, dataset_samples_client: DatasetSamplesClient):
        self._client: AuthenticatedClient = client
        self._dataset_samples_client: DatasetSamplesClient = dataset_samples_client
    
    def create(self) -> Dataset:
        """
        Create a new empty dataset.
        
        Returns:
            Dataset object representing the newly created dataset
            
        Example:
            >>> client = LightningRod(api_key="your-api-key")
            >>> dataset = client.datasets.create()
            >>> print(f"Created dataset: {dataset.id}")
        """
        response = create_dataset_datasets_post.sync(
            client=self._client,
        )
        
        if isinstance(response, HTTPValidationError):
            raise Exception(f"Failed to create dataset: {response.detail}")
        if response is None:
            raise Exception("Failed to create dataset: received None response")
        
        dataset_response = get_dataset_datasets_dataset_id_get.sync(
            dataset_id=response.id,
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
    
    def create_from_samples(
        self,
        samples: List[Sample],
        batch_size: int = 1000,
    ) -> Dataset:
        """
        Create a new dataset and upload samples to it.
        
        This is a convenience method that creates a dataset and uploads all samples
        in batches. Useful for creating input datasets from a collection of seeds.
        
        Args:
            samples: List of Sample objects to upload
            batch_size: Number of samples to upload per batch (default: 1000)
            
        Returns:
            Dataset object with all samples uploaded
            
        Example:
            >>> client = LightningRod(api_key="your-api-key")
            >>> samples = [Sample(seed=Seed(...), ...), ...]
            >>> dataset = client.datasets.create_with_samples(samples, batch_size=1000)
            >>> print(f"Created dataset with {dataset.num_rows} samples")
        """
        dataset = self.create()
        
        for i in range(0, len(samples), batch_size):
            batch = samples[i:i + batch_size]
            self._dataset_samples_client.upload(dataset.id, batch)
        
        dataset_response = get_dataset_datasets_dataset_id_get.sync(
            dataset_id=dataset.id,
            client=self._client,
        )
        if isinstance(dataset_response, HTTPValidationError):
            raise Exception(f"Failed to refresh dataset: {dataset_response.detail}")
        if dataset_response is None:
            raise Exception("Failed to refresh dataset: received None response")
        
        dataset.num_rows = dataset_response.num_rows
        return dataset
    
    def get(self, dataset_id: str) -> Dataset:
        """
        Get a dataset by ID.
        
        Args:
            dataset_id: ID of the dataset to retrieve
            
        Returns:
            Dataset object
            
        Example:
            >>> client = LightningRod(api_key="your-api-key")
            >>> dataset = client.datasets.get("dataset-id-here")
        """
        dataset_response = get_dataset_datasets_dataset_id_get.sync(
            dataset_id=dataset_id,
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
