from typing import List, Optional, Dict, Any, TYPE_CHECKING
import asyncio

from lightningrod._generated.models.sample import Sample
from lightningrod.training.samples import to_record, AnswerType

if TYPE_CHECKING:
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
        >>> lr = LightningRod(api_key="your-api-key")
        >>> config = QuestionPipeline(...)
        >>> dataset = lr.transforms.run(config)
        >>> samples = dataset.to_samples()
        >>> print(f"Dataset has {len(samples)} samples")
    """
    
    def __init__(
        self,
        id: str,
        num_rows: int,
        datasets_client: "DatasetSamplesClient"
    ):
        self.id: str = id
        self.num_rows: int = num_rows
        self._datasets_client: "DatasetSamplesClient" = datasets_client
        self._samples: Optional[List[Sample]] = None
    
    def download(self) -> List[Sample]:
        """
        Download all samples from the dataset via the paginated API.
        
        Returns:
            List of Sample objects
        
        Example:
            >>> lr = LightningRod(api_key="your-api-key")
            >>> dataset = lr.transforms.run(config)
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

    def to_samples(self) -> List[Sample]:
        """
        Download all samples from the dataset via the paginated API.
        
        Returns:
            List of Sample objects
        
        Example:
            >>> lr = LightningRod(api_key="your-api-key")
            >>> config = QuestionPipeline(...)
            >>> dataset = lr.transforms.run(config)
            >>> samples = dataset.to_samples()
            >>> for sample in samples:
            ...     print(sample.seed.seed_text)
        """
        return self.samples()

    def flattened(self, answer_type: AnswerType) -> List[Dict[str, Any]]:
        """
        Convert all samples to a list of dictionaries.
        Automatically downloads the samples if they haven't been downloaded yet.
        
        Handles different question types (Question, ForwardLookingQuestion) and
        extracts relevant fields from labels, seeds, and prompts.
        
        Returns:
            List of dictionaries, each representing a sample row
        
        Example:
            >>> lr = LightningRod(api_key="your-api-key")
            >>> config = QuestionPipeline(...)
            >>> dataset = lr.transforms.run(config)
            >>> rows = dataset.flattened(answer_type)
            >>> import pandas as pd
            >>> df = pd.DataFrame(rows)
        """
        return [to_record(s, answer_type) for s in self.samples()]

    def valid_count(self) -> int:
        """
        Count the number of valid samples in the dataset.
        Requires samples to be downloaded first (use dataset.download() or dataset.samples()).
        
        Raises:
            ValueError: If samples have not been downloaded yet.
        
        Returns:
            Number of valid samples (where is_valid is True)
        
        Example:
            >>> lr = LightningRod(api_key="your-api-key")
            >>> config = QuestionPipeline(...)
            >>> dataset = lr.transforms.run(config)
            >>> dataset.download()
            >>> valid = dataset.valid_count()
            >>> print(f"Dataset has {valid} valid samples")
        """
        if self._samples is None:
            raise ValueError("Samples must be downloaded first. Call dataset.download() or dataset.samples() before using valid_count().")
        
        count = 0
        for sample in self._samples:
            if sample.is_valid is True:
                count += 1
        return count


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
        >>> lr = AsyncLightningRod(api_key="your-api-key")
        >>> config = QuestionPipeline(...)
        >>> dataset = await lr.transforms.run(config)
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
            >>> lr = AsyncLightningRod(api_key="your-api-key")
            >>> config = QuestionPipeline(...)
            >>> dataset = await lr.transforms.run(config)
            >>> samples = await dataset.to_samples()
            >>> for sample in samples:
            ...     print(sample.seed.seed_text)
        """
        return await asyncio.to_thread(self._sync_dataset.to_samples)

    async def flattened(self, answer_type: AnswerType) -> List[Dict[str, Any]]:
        """
        Convert all samples to a list of dictionaries.
        Automatically downloads the samples if they haven't been downloaded yet.
        
        All operations are run in a thread pool to avoid blocking the event loop.
        
        Handles different question types (Question, ForwardLookingQuestion) and
        extracts relevant fields from labels, seeds, and prompts.
        
        Returns:
            List of dictionaries, each representing a sample row
        
        Example:
            >>> lr = AsyncLightningRod(api_key="your-api-key")
            >>> config = QuestionPipeline(...)
            >>> dataset = await lr.transforms.run(config)
            >>> rows = await dataset.flattened(answer_type)
            >>> import pandas as pd
            >>> df = pd.DataFrame(rows)
        """
        return await asyncio.to_thread(self._sync_dataset.flattened, answer_type)

    async def valid_count(self) -> int:
        """
        Count the number of valid samples in the dataset.
        Requires samples to be downloaded first (use await dataset.to_samples()).
        
        All operations are run in a thread pool to avoid blocking the event loop.
        
        Raises:
            ValueError: If samples have not been downloaded yet.
        
        Returns:
            Number of valid samples (where is_valid is True)
        
        Example:
            >>> lr = AsyncLightningRod(api_key="your-api-key")
            >>> config = QuestionPipeline(...)
            >>> dataset = await lr.transforms.run(config)
            >>> await dataset.to_samples()
            >>> valid = await dataset.valid_count()
            >>> print(f"Dataset has {valid} valid samples")
        """
        return await asyncio.to_thread(self._sync_dataset.valid_count)