from typing import TYPE_CHECKING, Optional, Any

from lightningrod._generated.models import TransformJob

if TYPE_CHECKING:
    from lightningrod.async_client import AsyncLightningRodClient
    from lightningrod.async_dataset import AsyncDataset


class AsyncTransformPipeline:
    """
    An async fluent builder for executing transform jobs.
    
    This class provides a builder pattern for running transforms asynchronously,
    allowing usage like: await client.pipeline(config).run(dataset)
    
    Args:
        client: The AsyncLightningRodClient instance
        config: Transform configuration (NewsSeedGenerator, Pipeline, etc.)
    
    Example:
        >>> client = AsyncLightningRodClient(api_key="your-api-key")
        >>> config = NewsSeedGenerator(...)
        >>> dataset = await client.pipeline(config).run()
    """
    
    def __init__(self, client: "AsyncLightningRodClient", config: Any):
        self._client: "AsyncLightningRodClient" = client
        self._config: Any = config
    
    async def run(self, dataset: Optional["AsyncDataset"] = None) -> "AsyncDataset":
        """
        Execute the transform and wait for completion.
        
        Args:
            dataset: Optional input dataset. If None, the transform runs without input data.
        
        Returns:
            AsyncDataset instance for the output dataset
        
        Raises:
            Exception: If the job fails or API returns an error
        
        Example:
            >>> output = await client.pipeline(config).run()
            >>> output = await client.pipeline(config).run(input_dataset)
        """
        return await self._client.run(self._config, dataset)
    
    async def submit(self, dataset: Optional["AsyncDataset"] = None, max_questions: Optional[int] = None) -> TransformJob:
        """
        Submit the transform without waiting for completion.
        
        Args:
            dataset: Optional input dataset. If None, the transform runs without input data.
            max_questions: Optional limit on questions to generate. Pipeline early-stops when reached.
        
        Returns:
            TransformJob instance representing the submitted job
        
        Raises:
            Exception: If the submission fails or API returns an error
        
        Example:
            >>> job = await client.pipeline(config).submit()
            >>> print(f"Job ID: {job.id}")
        """
        return await self._client.submit(self._config, dataset, max_questions=max_questions)
    
    async def batch(self, size: int, dataset: Optional["AsyncDataset"] = None) -> "AsyncDataset":
        """
        Execute the transform with a limit on seeds generated and wait for completion.
        
        For seed generators (NewsSeedGenerator, GdeltSeedGenerator), limits the
        number of seeds generated.
        
        Args:
            size: Maximum number of seeds to generate
            dataset: Optional input dataset. If None, the transform runs without input data.
        
        Returns:
            AsyncDataset instance for the output dataset
        
        Raises:
            Exception: If the job fails or API returns an error
        
        Example:
            >>> output = await client.pipeline(config).batch(100)
            >>> output = await client.pipeline(config).batch(100, input_dataset)
        """
        return await self._client.run(self._config, dataset, max_seeds=size)

