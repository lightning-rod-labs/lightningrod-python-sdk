from typing import List, Optional, Dict, Any, TYPE_CHECKING
import asyncio

from lightningrod._generated.models.sample import Sample

if TYPE_CHECKING:
    from lightningrod.datasets.client import DatasetSamplesClient
    from lightningrod.training.samples import AnswerType

class SampleDataset:
    """
    Represents a dataset of samples in Lightning Rod.
    
    A dataset contains rows of sample data. Use this class to access 
    dataset metadata and download the actual samples.
    
    Note: Datasets should only be created through LightningRod methods,
    not instantiated directly.
    
    Attributes:
        id: Unique identifier for the dataset
        num_rows: Number of rows in the dataset
        prompt_template: Optional template string for formatting prompts. When set,
            used by preview_prompts() and passed to training/eval API calls.
    
    Example:
        >>> lr = LightningRod(api_key="your-api-key")
        >>> config = QuestionPipeline(...)
        >>> dataset = lr.transforms.run(config)
        >>> samples = dataset.to_samples()
        >>> print(f"Dataset has {len(samples)} samples")
    """
    id: str
    sample_ids: Optional[List[str]]
    num_rows: int
    prompt_template: Optional[str]
    multiple_choice_options: Optional[str]

    def __init__(
        self,
        id: str,
        num_rows: int,
        datasets_client: "DatasetSamplesClient",
        sample_ids: Optional[List[str]] = None,
        samples: Optional[List[Sample]] = None,
        prompt_template: Optional[str] = None,
        multiple_choice_options: Optional[str] = None,
    ):
        self.id: str = id
        self.num_rows: int = num_rows
        self._datasets_client: "DatasetSamplesClient" = datasets_client
        self.prompt_template: Optional[str] = prompt_template
        self.multiple_choice_options: Optional[str] = multiple_choice_options
        if samples is not None:
            self._samples: Optional[List[Sample]] = samples
            self.sample_ids: Optional[List[str]] = [s.id for s in samples]
            self.num_rows = len(samples)
        else:
            self._samples: Optional[List[Sample]] = None
            self.sample_ids: Optional[List[str]] = sample_ids

    def subset(self, sample_ids: List[str]) -> "SampleDataset":
        by_id = {s.id: s for s in self.samples()}
        samples = [by_id[i] for i in sample_ids if i in by_id]
        return SampleDataset(
            id=self.id,
            num_rows=len(samples),
            datasets_client=self._datasets_client,
            samples=samples,
            prompt_template=self.prompt_template,
            multiple_choice_options=self.multiple_choice_options,
        )

    def exclude(self, sample_ids: List[str]) -> "SampleDataset":
        excluded_ids = set(sample_ids)
        samples = [sample for sample in self.samples() if sample.id not in excluded_ids]
        return SampleDataset(
            id=self.id,
            num_rows=len(samples),
            datasets_client=self._datasets_client,
            samples=samples,
            prompt_template=self.prompt_template,
            multiple_choice_options=self.multiple_choice_options,
        )

    def preview_prompts(
        self,
        include_assistant: bool = False,
        n: int = 3,
    ) -> List[Dict[str, Any]]:
        from lightningrod.training.samples import to_messages

        samples_list = self.samples()[:n]
        return [
            to_messages(s, template=self.prompt_template, include_assistant=include_assistant)
            for s in samples_list
        ]

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
        if self._samples is not None:
            return self._samples
        self._samples = self._datasets_client.list(self.id)
        return self._samples

    def samples(self) -> List[Sample]:
        """
        Get all samples from the dataset. 
        Automatically downloads the samples if they haven't been downloaded yet.
        
        Returns:
            List of Sample objects
        """
        if self._samples is not None:
            return self._samples
        self.download()
        if self.sample_ids is not None:
            id_set = set(self.sample_ids)
            self._samples = [s for s in self._samples if s.id in id_set]
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

    def flattened(self) -> List[Dict[str, Any]]:
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
            >>> rows = dataset.flattened()
            >>> import pandas as pd
            >>> df = pd.DataFrame(rows)
        """
        from lightningrod.training.samples import to_record

        return [to_record(s) for s in self.samples()]

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
    
    def __init__(self, sync_dataset: SampleDataset):
        self._sync_dataset: SampleDataset = sync_dataset
    
    @property
    def id(self) -> str:
        return self._sync_dataset.id
    
    @property
    def num_rows(self) -> int:
        return self._sync_dataset.num_rows

    @property
    def prompt_template(self) -> Optional[str]:
        return self._sync_dataset.prompt_template

    @prompt_template.setter
    def prompt_template(self, value: Optional[str]) -> None:
        self._sync_dataset.prompt_template = value

    @property
    def multiple_choice_options(self) -> Optional[str]:
        return self._sync_dataset.multiple_choice_options

    @multiple_choice_options.setter
    def multiple_choice_options(self, value: Optional[str]) -> None:
        self._sync_dataset.multiple_choice_options = value

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

    async def flattened(self) -> List[Dict[str, Any]]:
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
            >>> rows = await dataset.flattened()
            >>> import pandas as pd
            >>> df = pd.DataFrame(rows)
        """
        return await asyncio.to_thread(self._sync_dataset.flattened)

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

    def subset(self, sample_ids: List[str]) -> "AsyncDataset":
        return AsyncDataset(self._sync_dataset.subset(sample_ids))

    def exclude(self, sample_ids: List[str]) -> "AsyncDataset":
        return AsyncDataset(self._sync_dataset.exclude(sample_ids))