from lightningrod._generated.client import AuthenticatedClient
from lightningrod.datasets.client import DatasetSamplesClient, DatasetsClient
from lightningrod.organization.client import OrganizationsClient
from lightningrod.transforms.client import TransformsClient
from lightningrod.utils import config
from lightningrod.files.client import FilesClient
from lightningrod.filesets.client import FileSetsClient


class LightningRod:
    """
    Python SDK for the Lightning Rod API.
    
    Args:
        api_key: Your Lightning Rod API key
        base_url: Base URL for the API (defaults to production)
    
    Example:
        >>> lr = LightningRod(api_key="your-api-key")
        >>> config = QuestionPipeline(...)
        >>> dataset = lr.transforms.run(config)
        >>> samples = dataset.to_samples()
    """
    
    def __init__(
        self,
        api_key: str,
        base_url: str = "https://api.lightningrod.ai/api/public/v1"
    ):

        # Allow overriding the base url from the environment variables.
        # This is only used for local development, 
        # so that we don't have to pass this variable in on the public notebook examples.
        base_url = config.get_config_value("LIGHTNINGROD_BASE_URL", base_url)

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
        self.organization: OrganizationsClient = OrganizationsClient(self._generated_client)
        self.files: FilesClient = FilesClient(self._generated_client)
        self.filesets: FileSetsClient = FileSetsClient(self._generated_client, self.files)