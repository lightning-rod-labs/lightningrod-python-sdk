from lightningrod._generated.client import AuthenticatedClient
from lightningrod.datasets.client import DatasetSamplesClient, DatasetsClient
from lightningrod.organization.client import OrganizationsClient
from lightningrod.transforms.client import TransformsClient
from lightningrod.training.client import TrainingClient
from lightningrod.training.evals import EvalsClient
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
        self.training: TrainingClient = TrainingClient(self._generated_client)
        self.evals: EvalsClient = EvalsClient(self._generated_client)
        self.files: FilesClient = FilesClient(self._generated_client)
        self.filesets: FileSetsClient = FileSetsClient(self._generated_client)

    def predict(
        self,
        model_id: str,
        prompt: str,
        system_prompt: str = "Answer as a probability between 0 and 1 between <answer></answer> tags.",
        **kwargs,
    ) -> str:
        try:
            from openai import OpenAI
        except ImportError:
            raise ImportError("Run `pip install openai` to use lr.predict().")
        client = OpenAI(api_key=self.api_key, base_url=f"{self.base_url}/openai")
        response = client.chat.completions.create(
            model=model_id,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt},
            ],
            **kwargs,
        )
        return response.choices[0].message.content