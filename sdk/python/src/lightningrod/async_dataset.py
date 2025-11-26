import asyncio
from typing import TYPE_CHECKING

import pyarrow as pa

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
        schema: PyArrow schema for the dataset
    
    Example:
        >>> client = AsyncLightningRodClient(api_key="your-api-key")
        >>> dataset = await client.get_dataset("dataset-123")
        >>> table = await dataset.to_arrow()
        >>> print(f"Dataset has {len(table)} rows")
    """
    
    def __init__(self, sync_dataset: "Dataset"):
        self._sync_dataset: "Dataset" = sync_dataset
    
    @property
    def id(self) -> str:
        return self._sync_dataset.id
    
    @property
    def num_rows(self) -> int:
        return self._sync_dataset.num_rows
    
    @property
    def schema(self) -> pa.Schema:
        return self._sync_dataset.schema
    
    async def to_arrow(self) -> pa.Table:
        """
        Download the dataset and return it as a PyArrow Table.
        
        This method:
        1. Requests a signed download URL from the API
        2. Downloads the Parquet file from cloud storage
        3. Parses it into a PyArrow Table
        
        All operations are run in a thread pool to avoid blocking the event loop.
        
        Returns:
            PyArrow Table containing the dataset rows
        
        Raises:
            Exception: If the download fails or the file cannot be parsed
        
        Example:
            >>> client = AsyncLightningRodClient(api_key="your-api-key")
            >>> dataset = await client.get_dataset("dataset-123")
            >>> table = await dataset.to_arrow()
            >>> df = table.to_pandas()
        """
        return await asyncio.to_thread(self._sync_dataset.to_arrow)

