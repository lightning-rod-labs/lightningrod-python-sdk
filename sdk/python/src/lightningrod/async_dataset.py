import asyncio
from typing import TYPE_CHECKING, List

from lightningrod._generated.models.sample import Sample

if TYPE_CHECKING:
    from lightningrod.dataset import Dataset


class AsyncDataset:
    """
    Async wrapper for Dataset.
    
    This class provides an async interface to Dataset operations by running
    the synchronous operations in a thread pool using asyncio.to_thread.
    
    Note: AsyncDatasets should only be created through AsyncLightningRodClient methods,
    not instantiated directly.
    
    Attributes:
        id: Unique identifier for the dataset
        num_rows: Number of rows in the dataset
    
    Example:
        >>> client = AsyncLightningRodClient(api_key="your-api-key")
        >>> dataset = await client.pipeline(config).run()
        >>> samples = await dataset.to_samples()
        >>> print(f"Dataset has {len(samples)} samples")
    """
    
    def __init__(self, sync_dataset: "Dataset"):
        self._sync_dataset: "Dataset" = sync_dataset
    
    @property
    def id(self) -> str:
        return self._sync_dataset.id
    
    @property
    def num_rows(self) -> int:
        return self._sync_dataset.num_rows
    
    async def to_samples(self) -> List[Sample]:
        """
        Download all samples from the dataset via the paginated API.
        
        All operations are run in a thread pool to avoid blocking the event loop.
        
        Returns:
            List of Sample objects
        
        Example:
            >>> client = AsyncLightningRodClient(api_key="your-api-key")
            >>> dataset = await client.pipeline(config).run()
            >>> samples = await dataset.to_samples()
            >>> for sample in samples:
            ...     print(sample.seed.seed_text)
        """
        return await asyncio.to_thread(self._sync_dataset.to_samples)
