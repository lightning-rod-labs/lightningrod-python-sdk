from typing import TYPE_CHECKING, Optional, Union

from lightningrod._generated.models import (
    TransformJob,
    NewsSeedGenerator,
    GdeltSeedGenerator,
    Pipeline,
    QuestionGenerator,
    QuestionPipeline,
    WebSearchLabeler,
)

if TYPE_CHECKING:
    from lightningrod.client import LightningRodClient
    from lightningrod.dataset import Dataset

TransformConfig = Union[NewsSeedGenerator, GdeltSeedGenerator, Pipeline, QuestionGenerator, QuestionPipeline, WebSearchLabeler]


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
        return self._client._run(self._config, dataset)
    
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
        return self._client._submit(self._config, dataset)
    
    def batch(self, size: int, dataset: Optional["Dataset"] = None) -> "Dataset":
        """
        Execute the transform with a batch size limit and wait for completion.
        
        For seed generators (NewsSeedGenerator, GdeltSeedGenerator), limits the
        number of seeds generated. For transforms with input datasets, limits
        the number of input rows processed.
        
        Args:
            size: Maximum number of items to process
            dataset: Optional input dataset. If None, the transform runs without input data.
        
        Returns:
            Dataset instance for the output dataset
        
        Raises:
            Exception: If the job fails or API returns an error
        
        Example:
            >>> output = client.pipeline(config).batch(100)
            >>> output = client.pipeline(config).batch(100, input_dataset)
        """
        return self._client._run(self._config, dataset, batch_size=size)

