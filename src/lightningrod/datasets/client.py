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
from lightningrod._errors import handle_response_error


class DatasetSamplesClient:
    def __init__(self, client: AuthenticatedClient):
        self._client: AuthenticatedClient = client
    
    def list(self, dataset_id: str) -> List[Sample]:
        samples: List[Sample] = []
        cursor: Optional[str] = None
        
        while True:
            response = get_dataset_samples_datasets_dataset_id_samples_get.sync_detailed(
                dataset_id=dataset_id,
                client=self._client,
                limit=100,
                cursor=cursor,
            )
            
            parsed = handle_response_error(response, "fetch samples")
            
            samples.extend(parsed.samples)
            
            if not parsed.has_more:
                break
            if isinstance(parsed.next_cursor, Unset) or parsed.next_cursor is None:
                break
            cursor = str(parsed.next_cursor)
        
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
            >>> lr = LightningRod(api_key="your-api-key")
            >>> samples = [Sample(seed=Seed(...), ...), ...]
            >>> lr.datasets.upload(samples)
        """
        request = UploadSamplesRequest(samples=samples)
        
        response = upload_samples_datasets_dataset_id_samples_post.sync_detailed(
            dataset_id=dataset_id,
            client=self._client,
            body=request,
        )
        
        handle_response_error(response, "upload samples")


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
            >>> lr = LightningRod(api_key="your-api-key")
            >>> dataset = lr.datasets.create()
            >>> print(f"Created dataset: {dataset.id}")
        """
        response = create_dataset_datasets_post.sync_detailed(
            client=self._client,
        )
        
        create_result = handle_response_error(response, "create dataset")
        
        dataset_response = get_dataset_datasets_dataset_id_get.sync_detailed(
            dataset_id=create_result.id,
            client=self._client,
        )
        dataset_result = handle_response_error(dataset_response, "get dataset")
        
        return Dataset(
            id=dataset_result.id,
            num_rows=dataset_result.num_rows,
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
            >>> lr = LightningRod(api_key="your-api-key")
            >>> samples = [Sample(seed=Seed(...), ...), ...]
            >>> dataset = lr.datasets.create_from_samples(samples, batch_size=1000)
            >>> print(f"Created dataset with {dataset.num_rows} samples")
        """
        dataset = self.create()
        
        for i in range(0, len(samples), batch_size):
            batch = samples[i:i + batch_size]
            self._dataset_samples_client.upload(dataset.id, batch)
        
        dataset_response = get_dataset_datasets_dataset_id_get.sync_detailed(
            dataset_id=dataset.id,
            client=self._client,
        )
        dataset_result = handle_response_error(dataset_response, "refresh dataset")
        
        dataset.num_rows = dataset_result.num_rows
        return dataset
    
    def get(self, dataset_id: str) -> Dataset:
        """
        Get a dataset by ID.
        
        Args:
            dataset_id: ID of the dataset to retrieve
            
        Returns:
            Dataset object
            
        Example:
            >>> lr = LightningRod(api_key="your-api-key")
            >>> dataset = lr.datasets.get("dataset-id-here")
        """
        dataset_response = get_dataset_datasets_dataset_id_get.sync_detailed(
            dataset_id=dataset_id,
            client=self._client,
        )
        dataset_result = handle_response_error(dataset_response, "get dataset")
        
        return Dataset(
            id=dataset_result.id,
            num_rows=dataset_result.num_rows,
            datasets_client=self._dataset_samples_client
        )
