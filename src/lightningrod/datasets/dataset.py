from typing import List, Optional, Dict, Any
import asyncio

from lightningrod._generated.models.sample import Sample
from lightningrod._generated.models.forward_looking_question import ForwardLookingQuestion
from lightningrod._generated.models.question import Question
from lightningrod._generated.models.news_context import NewsContext
from lightningrod._generated.models.rag_context import RAGContext
from lightningrod._generated.models.sample_meta import SampleMeta
from lightningrod._generated.types import UNSET, Unset
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

    def to_samples(self) -> List[Sample]:
        """
        Download all samples from the dataset via the paginated API.
        
        Returns:
            List of Sample objects
        
        Example:
            >>> client = LightningRod(api_key="your-api-key")
            >>> config = QuestionPipeline(...)
            >>> dataset = client.transforms.run(config)
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
            >>> client = LightningRod(api_key="your-api-key")
            >>> config = QuestionPipeline(...)
            >>> dataset = client.transforms.run(config)
            >>> rows = dataset.flattened()
            >>> import pandas as pd
            >>> df = pd.DataFrame(rows)
        """
        samples = self.samples()
        return [self._sample_to_dict(sample) for sample in samples]

    def _sample_to_dict(self, sample: Sample) -> Dict[str, Any]:
        row: Dict[str, Any] = {}
        
        if sample.question and not isinstance(sample.question, Unset):
            if isinstance(sample.question, ForwardLookingQuestion):
                row['question.question_text'] = sample.question.question_text
                row['question.date_close'] = sample.question.date_close.isoformat()
                row['question.event_date'] = sample.question.event_date.isoformat()
                row['question.resolution_criteria'] = sample.question.resolution_criteria
                if sample.question.prediction_date is not None and not isinstance(sample.question.prediction_date, Unset):
                    row['question.prediction_date'] = sample.question.prediction_date.isoformat()
            elif isinstance(sample.question, Question):
                row['question.question_text'] = sample.question.question_text
            else:
                question_text = getattr(sample.question, 'question_text', None)
                if question_text is not None:
                    row['question.question_text'] = question_text
        
        if sample.label and not isinstance(sample.label, Unset):
            row['label.label'] = sample.label.label
            row['label.label_confidence'] = sample.label.label_confidence
            if sample.label.resolution_date is not None and not isinstance(sample.label.resolution_date, Unset):
                row['label.resolution_date'] = sample.label.resolution_date.isoformat()
            if sample.label.reasoning is not None and not isinstance(sample.label.reasoning, Unset):
                row['label.reasoning'] = sample.label.reasoning
            if sample.label.answer_sources is not None and not isinstance(sample.label.answer_sources, Unset):
                row['label.answer_sources'] = sample.label.answer_sources
        
        if sample.prompt and not isinstance(sample.prompt, Unset):
            row['prompt'] = sample.prompt
        
        if sample.seed and not isinstance(sample.seed, Unset):
            row['seed.seed_text'] = sample.seed.seed_text
            if sample.seed.url is not None and not isinstance(sample.seed.url, Unset):
                row['seed.url'] = sample.seed.url
            if sample.seed.seed_creation_date is not None and not isinstance(sample.seed.seed_creation_date, Unset):
                row['seed.seed_creation_date'] = sample.seed.seed_creation_date.isoformat()
            if sample.seed.search_query is not None and not isinstance(sample.seed.search_query, Unset):
                row['seed.search_query'] = sample.seed.search_query
        
        if sample.is_valid is not None and not isinstance(sample.is_valid, Unset):
            row['is_valid'] = sample.is_valid
        
        if sample.context is not None and not isinstance(sample.context, Unset):
            for idx, ctx in enumerate(sample.context):
                if isinstance(ctx, NewsContext):
                    row[f'context.{idx}.rendered_context'] = ctx.rendered_context
                    row[f'context.{idx}.search_query'] = ctx.search_query
                    row[f'context.{idx}.context_type'] = ctx.context_type
                elif isinstance(ctx, RAGContext):
                    row[f'context.{idx}.rendered_context'] = ctx.rendered_context
                    row[f'context.{idx}.document_id'] = ctx.document_id
                    row[f'context.{idx}.context_type'] = ctx.context_type
        
        if sample.meta is not None and not isinstance(sample.meta, Unset):
            if isinstance(sample.meta, SampleMeta):
                for key, value in sample.meta.additional_properties.items():
                    row[f'meta.{key}'] = value
        
        if sample.additional_properties:
            for key, value in sample.additional_properties.items():
                row[f'additional_properties.{key}'] = value
        
        return row

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
            >>> client = AsyncLightningRod(api_key="your-api-key")
            >>> config = QuestionPipeline(...)
            >>> dataset = await client.transforms.run(config)
            >>> rows = await dataset.flattened()
            >>> import pandas as pd
            >>> df = pd.DataFrame(rows)
        """
        return await asyncio.to_thread(self._sync_dataset.flattened)