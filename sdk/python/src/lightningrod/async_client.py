import asyncio
from typing import List, Optional

from lightningrod._generated.models import TransformJob
from lightningrod._generated.models.sample import Sample
from lightningrod.client import LightningRodClient, TransformConfig
from lightningrod.async_dataset import AsyncDataset
from lightningrod.async_pipeline import AsyncTransformPipeline


class AsyncLightningRodClient:
    """
    Async Python client for the Lightning Rod API.
    
    This client provides an async interface to Lightning Rod's AI-powered forecasting
    dataset generation platform by wrapping the synchronous client and running
    operations in a thread pool.
    
    Args:
        api_key: Your Lightning Rod API key
        base_url: Base URL for the API (defaults to production)
    
    Example:
        >>> client = AsyncLightningRodClient(api_key="your-api-key")
        >>> dataset = await client.pipeline(config).run()
        >>> samples = await dataset.to_samples()
    """
    
    def __init__(
        self,
        api_key: str,
        base_url: str = "https://api.lightningrod.ai/api/public/v1"
    ):
        self._sync_client: LightningRodClient = LightningRodClient(
            api_key=api_key,
            base_url=base_url
        )
    
    def pipeline(self, config: TransformConfig) -> AsyncTransformPipeline:
        """
        Create a pipeline builder for executing transforms.
        
        This provides a fluent API for running transforms:
        await client.pipeline(config).run(dataset)
        
        Args:
            config: Transform configuration (NewsSeedGenerator, Pipeline, etc.)
        
        Returns:
            AsyncTransformPipeline instance for chaining
        
        Example:
            >>> client = AsyncLightningRodClient(api_key="your-api-key")
            >>> config = NewsSeedGenerator(...)
            >>> dataset = await client.pipeline(config).run()
        """
        return AsyncTransformPipeline(self, config)
    
    async def create_dataset(self, samples: List[Sample], batch_size: int = 1000) -> AsyncDataset:
        """
        Upload samples to create a new dataset.
        
        Args:
            samples: List of Sample objects to upload
            batch_size: Number of samples to upload per batch (default 1000)
        
        Returns:
            AsyncDataset instance for the created dataset
        
        Example:
            >>> from lightningrod import Sample, Seed
            >>> samples = [Sample(seed=Seed(seed_text="Article..."))]
            >>> dataset = await client.create_dataset(samples)
            >>> output = await client.pipeline(config).run(dataset)
        """
        sync_dataset = await asyncio.to_thread(
            self._sync_client.create_dataset,
            samples,
            batch_size
        )
        return AsyncDataset(sync_dataset)
    
    async def run(
        self,
        config: TransformConfig,
        dataset: Optional[AsyncDataset] = None,
        max_seeds: Optional[int] = None
    ) -> AsyncDataset:
        """
        Submit a transform job and wait for it to complete.
        
        This method will:
        1. Submit the transform job to the API
        2. Poll every 15 seconds to check the job status
        3. Return the output dataset when the job completes
        
        All operations are run in a thread pool to avoid blocking the event loop.
        
        Args:
            config: Transform configuration (NewsSeedGenerator, Pipeline, etc.)
            dataset: Optional input dataset. If None, the transform runs without input data.
            max_seeds: Optional limit on number of seeds to generate.
        
        Returns:
            AsyncDataset instance for the output dataset
        
        Raises:
            Exception: If the job fails or API returns an error
        
        Example:
            >>> client = AsyncLightningRodClient(api_key="your-api-key")
            >>> config = NewsSeedGenerator(...)
            >>> output_dataset = await client.run(config)
        """
        sync_dataset = dataset._sync_dataset if dataset else None
        
        result_sync_dataset = await asyncio.to_thread(
            self._sync_client._run,
            config,
            sync_dataset,
            max_seeds
        )
        
        return AsyncDataset(result_sync_dataset)
    
    async def submit(
        self,
        config: TransformConfig,
        dataset: Optional[AsyncDataset] = None,
        max_seeds: Optional[int] = None
    ) -> TransformJob:
        """
        Submit a transform job without waiting for completion.
        
        Args:
            config: Transform configuration (NewsSeedGenerator, Pipeline, etc.)
            dataset: Optional input dataset. If None, the transform runs without input data.
            max_seeds: Optional limit on number of seeds to generate.
        
        Returns:
            TransformJob instance representing the submitted job
        
        Raises:
            Exception: If the submission fails or API returns an error
        
        Example:
            >>> client = AsyncLightningRodClient(api_key="your-api-key")
            >>> config = NewsSeedGenerator(...)
            >>> job = await client.submit(config)
            >>> print(f"Job ID: {job.id}, Status: {job.status}")
        """
        sync_dataset = dataset._sync_dataset if dataset else None
        
        return await asyncio.to_thread(
            self._sync_client._submit,
            config,
            sync_dataset,
            max_seeds
        )
