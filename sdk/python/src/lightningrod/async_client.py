import asyncio
from typing import Optional

from lightningrod._generated.models import (
    TransformJob,
    NewsSeedGenerator,
    Pipeline,
    QuestionGenerator,
    QuestionPipeline,
    WebSearchLabeler,
)
from lightningrod.client import LightningRodClient, TransformConfig
from lightningrod.async_dataset import AsyncDataset


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
        >>> dataset = await client.get_dataset("dataset-123")
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
    
    async def get_dataset(self, dataset_id: str) -> AsyncDataset:
        """
        Get a dataset by its ID.
        
        Args:
            dataset_id: The ID of the dataset to retrieve
        
        Returns:
            AsyncDataset instance with metadata loaded
        
        Raises:
            Exception: If the API returns an error
        
        Example:
            >>> client = AsyncLightningRodClient(api_key="your-api-key")
            >>> dataset = await client.get_dataset("dataset-123")
            >>> table = await dataset.to_arrow()
        """
        sync_dataset = await asyncio.to_thread(
            self._sync_client.get_dataset,
            dataset_id
        )
        return AsyncDataset(sync_dataset)
    
    async def run(
        self,
        config: TransformConfig,
        dataset: Optional[AsyncDataset] = None
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
        
        Returns:
            AsyncDataset instance for the output dataset
        
        Raises:
            Exception: If the job fails or API returns an error
        
        Example:
            >>> from lightningrod._generated.models import QuestionPipeline
            >>> client = AsyncLightningRodClient(api_key="your-api-key")
            >>> config = QuestionPipeline(config_type="QUESTION_PIPELINE", ...)
            >>> output_dataset = await client.run(config)
        """
        sync_dataset = dataset._sync_dataset if dataset else None
        
        result_sync_dataset = await asyncio.to_thread(
            self._sync_client.run,
            config,
            sync_dataset
        )
        
        return AsyncDataset(result_sync_dataset)
    
    async def submit(
        self,
        config: TransformConfig,
        dataset: Optional[AsyncDataset] = None
    ) -> TransformJob:
        """
        Submit a transform job without waiting for completion.
        
        Args:
            config: Transform configuration (NewsSeedGenerator, Pipeline, etc.)
            dataset: Optional input dataset. If None, the transform runs without input data.
        
        Returns:
            TransformJob instance representing the submitted job
        
        Raises:
            Exception: If the submission fails or API returns an error
        
        Example:
            >>> from lightningrod._generated.models import QuestionPipeline
            >>> client = AsyncLightningRodClient(api_key="your-api-key")
            >>> config = QuestionPipeline(config_type="QUESTION_PIPELINE", ...)
            >>> job = await client.submit(config)
            >>> print(f"Job ID: {job.id}, Status: {job.status}")
        """
        sync_dataset = dataset._sync_dataset if dataset else None
        
        return await asyncio.to_thread(
            self._sync_client.submit,
            config,
            sync_dataset
        )

