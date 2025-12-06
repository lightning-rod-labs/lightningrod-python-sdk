import asyncio
from typing import List, Optional

import pyarrow as pa

from lightningrod._generated.models import (
    TransformJob,
    NewsSeedGenerator,
    Pipeline,
    QuestionGenerator,
    QuestionPipeline,
    WebSearchLabeler,
)
from lightningrod._generated.models.sample import Sample
from lightningrod._generated.models.seed import Seed
from lightningrod._generated.models.question import Question
from lightningrod._generated.models.label import Label
from lightningrod.client import LightningRodClient, TransformConfig
from lightningrod.async_dataset import AsyncDataset


class AsyncDatasets:
    """
    Async dataset operations for Lightning Rod.
    
    Access via client.datasets property.
    
    Example:
        >>> client = AsyncLightningRodClient(api_key="your-api-key")
        >>> dataset = await client.datasets.get("dataset-123")
        >>> new_dataset = await client.datasets.from_csv("data.csv")
    """
    
    def __init__(self, client: "AsyncLightningRodClient"):
        self._client = client
    
    async def get(self, dataset_id: str) -> AsyncDataset:
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
            >>> dataset = await client.datasets.get("dataset-123")
            >>> table = await dataset.to_arrow()
        """
        sync_dataset = await asyncio.to_thread(
            self._client._sync_client.datasets.get,
            dataset_id
        )
        return AsyncDataset(sync_dataset)
    
    async def from_pyarrow(self, table: pa.Table) -> AsyncDataset:
        """
        Create a dataset by uploading a PyArrow Table.
        
        This method:
        1. Requests a signed upload URL from the API
        2. Serializes the table to Parquet format
        3. Uploads the Parquet file to cloud storage
        4. Creates a dataset record from the uploaded file
        
        All operations are run in a thread pool to avoid blocking the event loop.
        
        Args:
            table: PyArrow Table to upload
        
        Returns:
            AsyncDataset instance for the created dataset
        
        Raises:
            Exception: If the upload or dataset creation fails
        
        Example:
            >>> import pyarrow as pa
            >>> client = AsyncLightningRodClient(api_key="your-api-key")
            >>> table = pa.table({"col1": [1, 2, 3], "col2": ["a", "b", "c"]})
            >>> dataset = await client.datasets.from_pyarrow(table)
            >>> print(f"Created dataset: {dataset.id}")
        """
        sync_dataset = await asyncio.to_thread(
            self._client._sync_client.datasets.from_pyarrow,
            table
        )
        return AsyncDataset(sync_dataset)
    
    async def from_samples(self, samples: List[Sample]) -> AsyncDataset:
        """
        Create a dataset from a list of Sample objects.
        
        This method:
        1. Converts Sample objects to a flat PyArrow Table
        2. Flattens nested objects (Seed, Question, Label) into top-level columns
        3. Uploads the table to create a dataset
        
        All operations are run in a thread pool to avoid blocking the event loop.
        
        Args:
            samples: List of Sample objects to convert and upload
        
        Returns:
            AsyncDataset instance for the created dataset
        
        Raises:
            Exception: If the upload or dataset creation fails
        
        Example:
            >>> from lightningrod._generated.models import Sample, Seed, Question
            >>> client = AsyncLightningRodClient(api_key="your-api-key")
            >>> samples = [Sample(sample_id="1", seed=Seed(seed_text="text"), ...)]
            >>> dataset = await client.datasets.from_samples(samples)
        """
        sync_dataset = await asyncio.to_thread(
            self._client._sync_client.datasets.from_samples,
            samples
        )
        return AsyncDataset(sync_dataset)
    
    async def from_csv(self, path: str) -> AsyncDataset:
        """
        Create a dataset from a CSV file.
        
        Args:
            path: Path to the CSV file
        
        Returns:
            AsyncDataset instance for the created dataset
        
        Raises:
            Exception: If the file cannot be read or upload fails
        
        Example:
            >>> client = AsyncLightningRodClient(api_key="your-api-key")
            >>> dataset = await client.datasets.from_csv("data.csv")
            >>> print(f"Created dataset: {dataset.id}")
        """
        sync_dataset = await asyncio.to_thread(
            self._client._sync_client.datasets.from_csv,
            path
        )
        return AsyncDataset(sync_dataset)
    
    async def from_pandas(self, df: "pandas.DataFrame") -> AsyncDataset:
        """
        Create a dataset from a Pandas DataFrame.
        
        Args:
            df: Pandas DataFrame to upload
        
        Returns:
            AsyncDataset instance for the created dataset
        
        Raises:
            Exception: If the conversion or upload fails
        
        Example:
            >>> import pandas as pd
            >>> client = AsyncLightningRodClient(api_key="your-api-key")
            >>> df = pd.DataFrame({"col1": [1, 2, 3], "col2": ["a", "b", "c"]})
            >>> dataset = await client.datasets.from_pandas(df)
            >>> print(f"Created dataset: {dataset.id}")
        """
        sync_dataset = await asyncio.to_thread(
            self._client._sync_client.datasets.from_pandas,
            df
        )
        return AsyncDataset(sync_dataset)
    
    async def from_lists(
        self,
        seeds: List[Seed],
        questions: List[Question],
        labels: List[Label]
    ) -> AsyncDataset:
        """
        Create a dataset from parallel lists of Seeds, Questions, and Labels.
        
        All lists must be the same length. Each index represents one sample.
        
        Args:
            seeds: List of Seed objects
            questions: List of Question objects
            labels: List of Label objects
        
        Returns:
            AsyncDataset instance for the created dataset
        
        Raises:
            ValueError: If the lists have different lengths
            Exception: If the upload or dataset creation fails
        
        Example:
            >>> from lightningrod._generated.models import Seed, Question, Label
            >>> client = AsyncLightningRodClient(api_key="your-api-key")
            >>> seeds = [Seed(seed_text="news article 1"), Seed(seed_text="news article 2")]
            >>> questions = [Question(question_text="Q1?"), Question(question_text="Q2?")]
            >>> labels = [Label(label=True), Label(label=False)]
            >>> dataset = await client.datasets.from_lists(seeds, questions, labels)
        """
        sync_dataset = await asyncio.to_thread(
            self._client._sync_client.datasets.from_lists,
            seeds,
            questions,
            labels
        )
        return AsyncDataset(sync_dataset)


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
        >>> dataset = await client.datasets.get("dataset-123")
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
        self._datasets: AsyncDatasets = AsyncDatasets(self)
    
    @property
    def datasets(self) -> AsyncDatasets:
        """Access dataset operations."""
        return self._datasets
    
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
