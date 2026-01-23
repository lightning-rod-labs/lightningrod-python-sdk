from typing import List

from lightningrod._generated.client import AuthenticatedClient
from lightningrod._generated.models.sample import Sample
from lightningrod.datasets.client import DatasetSamplesClient, DatasetsClient
from lightningrod.datasets.dataset import Dataset
from lightningrod.files.client import FilesClient
from lightningrod.filesets.client import FileSetsClient
from lightningrod.transforms.client import TransformsClient


class LightningRod:
    """
    Python SDK for the Lightning Rod API.
    
    Args:
        api_key: Your Lightning Rod API key
        base_url: Base URL for the API (defaults to production)
    
    Example:
        >>> client = LightningRod(api_key="your-api-key")
        >>> config = QuestionPipeline(...)
        >>> dataset = client.transforms.run(config)
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
        
        self._dataset_samples: DatasetSamplesClient = DatasetSamplesClient(self._generated_client)
        self.transforms: TransformsClient = TransformsClient(self._generated_client, self._dataset_samples)
        self.datasets: DatasetsClient = DatasetsClient(self._generated_client, self._dataset_samples)
         # TODO(filesets): Enable when filesets are publicly supported
        # self.files: FilesClient = FilesClient(self._generated_client)
        # self.filesets: FileSetsClient = FileSetsClient(self._generated_client, self.files)