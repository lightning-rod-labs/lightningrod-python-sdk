from typing import List, Optional
import asyncio

from lightningrod._generated.models.sample import Sample
from lightningrod.datasets.client import DatasetSamplesClient

class Dataset:
    """
    Represents a dataset in Lightning Rod.
    
    A dataset contains rows of sample data. Use this class to access 
    dataset metadata and download the actual samples.
    
    Note: Datasets should only be created through LightningRod methods,
    not instantiated directly.
    
    Attributes:
        id: Unique identifier for the dataset
        num_rows: Number of rows in the dataset
    
    Example:
        >>> client = LightningRod(api_key="your-api-key")
        >>> config = QuestionPipeline(...)
        >>> dataset = client.transforms.run(config)
        >>> samples = dataset.to_samples()
        >>> print(f"Dataset has {len(samples)} samples")
    """
    
    def __init__(
        self,
        id: str,
        num_rows: int,
        datasets_client: DatasetSamplesClient
    ):
        self.id: str = id
        self.num_rows: int = num_rows
        self._datasets_client: DatasetSamplesClient = datasets_client
        self._samples: Optional[List[Sample]] = None
    
    def download(self) -> List[Sample]:
        """
        Download all samples from the dataset via the paginated API.
        
        Returns:
            List of Sample objects
        
        Example:
            >>> client = LightningRod(api_key="your-api-key")
            >>> dataset = client.pipeline(config).run()
            >>> samples = dataset.download()
            >>> for sample in samples:
            ...     print(sample.seed.seed_text)
        """
        self._samples = self._datasets_client.list(self.id)
        return self._samples

    def samples(self) -> List[Sample]:
        """
        Get all samples from the dataset. 
        Automatically downloads the samples if they haven't been downloaded yet.
        
        Returns:
            List of Sample objects
        """
        if not self._samples:
            self.download()
        return self._samples

class AsyncDataset:
    """
    Async wrapper for Dataset.
    
    This class provides an async interface to Dataset operations by running
    the synchronous operations in a thread pool using asyncio.to_thread.
    
    Note: AsyncDatasets should only be created through AsyncLightningRod methods,
    not instantiated directly.
    
    Attributes:
        id: Unique identifier for the dataset
        num_rows: Number of rows in the dataset
    
    Example:
        >>> client = AsyncLightningRod(api_key="your-api-key")
        >>> config = QuestionPipeline(...)
        >>> dataset = await client.transforms.run(config)
        >>> samples = await dataset.to_samples()
        >>> print(f"Dataset has {len(samples)} samples")
    """
    
    def __init__(self, sync_dataset: Dataset):
        self._sync_dataset: Dataset = sync_dataset
    
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
            >>> client = AsyncLightningRod(api_key="your-api-key")
            >>> config = QuestionPipeline(...)
            >>> dataset = await client.transforms.run(config)
            >>> samples = await dataset.to_samples()
            >>> for sample in samples:
            ...     print(sample.seed.seed_text)
        """
        return await asyncio.to_thread(self._sync_dataset.to_samples)