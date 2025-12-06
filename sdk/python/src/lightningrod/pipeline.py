from typing import TYPE_CHECKING, Optional

from lightningrod._generated.models import TransformJob
from lightningrod.client import TransformConfig

if TYPE_CHECKING:
    from lightningrod.client import LightningRodClient
    from lightningrod.dataset import Dataset


class TransformPipeline:
    """
    A fluent builder for executing transform jobs.
    
    This class provides a builder pattern for running transforms,
    allowing usage like: client.pipeline(config).run(dataset)
    
    Args:
        client: The LightningRodClient instance
        config: Transform configuration (NewsSeedGenerator, Pipeline, etc.)
    
    Example:
        >>> client = LightningRodClient(api_key="your-api-key")
        >>> config = NewsSeedGenerator(...)
        >>> dataset = client.pipeline(config).run()
    """
    
    def __init__(self, client: "LightningRodClient", config: TransformConfig):
        self._client: "LightningRodClient" = client
        self._config: TransformConfig = config
    
    def run(self, dataset: Optional["Dataset"] = None) -> "Dataset":
        """
        Execute the transform and wait for completion.
        
        Args:
            dataset: Optional input dataset. If None, the transform runs without input data.
        
        Returns:
            Dataset instance for the output dataset
        
        Raises:
            Exception: If the job fails or API returns an error
        
        Example:
            >>> output = client.pipeline(config).run()
            >>> output = client.pipeline(config).run(input_dataset)
        """
        return self._client.run(self._config, dataset)
    
    def submit(self, dataset: Optional["Dataset"] = None) -> TransformJob:
        """
        Submit the transform without waiting for completion.
        
        Args:
            dataset: Optional input dataset. If None, the transform runs without input data.
        
        Returns:
            TransformJob instance representing the submitted job
        
        Raises:
            Exception: If the submission fails or API returns an error
        
        Example:
            >>> job = client.pipeline(config).submit()
            >>> print(f"Job ID: {job.id}")
        """
        return self._client.submit(self._config, dataset)

