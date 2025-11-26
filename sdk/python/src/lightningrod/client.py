from typing import Optional
from lightningrod._generated.client import AuthenticatedClient
from lightningrod._generated.models.dataset_metadata import DatasetMetadata
from lightningrod._generated.api.datasets import get_dataset_datasets_dataset_id_get


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
    
    def get_version(self) -> str:
        """
        Get the SDK version.
        
        Returns:
            SDK version string
        """
        return "0.1.0"
    
    def get_dataset(self, dataset_id: str) -> DatasetMetadata:
        """
        Get dataset metadata including ID, row count, and schema.
        
        Args:
            dataset_id: The ID of the dataset to retrieve
        
        Returns:
            Dataset metadata response containing dataset information
        
        Raises:
            Exception: If the API returns an error
        
        Example:
            >>> client = LightningRodClient(api_key="your-api-key")
            >>> dataset = client.get_dataset("dataset-123")
            >>> print(dataset.dataset.dataset_id)
        """
        return get_dataset_datasets_dataset_id_get.sync(
            dataset_id=dataset_id,
            client=self._generated_client,
        )
        
