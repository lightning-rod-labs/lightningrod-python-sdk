import base64
from typing import TYPE_CHECKING

import fsspec
import pyarrow as pa
import pyarrow.parquet as pq

from lightningrod._generated.api.datasets import (
    get_dataset_download_url_datasets_dataset_id_download_url_get,
)
from lightningrod._generated.models import DatasetDownloadUrlResponse, HTTPValidationError

if TYPE_CHECKING:
    from lightningrod.client import LightningRodClient


class Dataset:
    """
    Represents a dataset in Lightning Rod.
    
    A dataset contains rows of data stored in Parquet format in cloud storage.
    Use this class to access dataset metadata and download the actual data.
    
    Note: Datasets should only be created through LightningRodClient methods,
    not instantiated directly.
    
    Attributes:
        id: Unique identifier for the dataset
        num_rows: Number of rows in the dataset
        schema: PyArrow schema for the dataset
    
    Example:
        >>> client = LightningRodClient(api_key="your-api-key")
        >>> dataset = client.get_dataset("dataset-123")
        >>> table = dataset.to_arrow()
        >>> print(f"Dataset has {len(table)} rows")
    """
    
    def __init__(
        self,
        id: str,
        num_rows: int,
        schema: pa.Schema,
        client: "LightningRodClient"
    ):
        self.id: str = id
        self.num_rows: int = num_rows
        self.schema: pa.Schema = schema
        self._client: "LightningRodClient" = client
    
    def to_arrow(self) -> pa.Table:
        """
        Download the dataset and return it as a PyArrow Table.
        
        This method:
        1. Requests a signed download URL from the API
        2. Downloads the Parquet file from cloud storage
        3. Parses it into a PyArrow Table
        
        Returns:
            PyArrow Table containing the dataset rows
        
        Raises:
            Exception: If the download fails or the file cannot be parsed
        
        Example:
            >>> client = LightningRodClient(api_key="your-api-key")
            >>> dataset = client.get_dataset("dataset-123")
            >>> table = dataset.to_arrow()
            >>> df = table.to_pandas()
        """
        result: DatasetDownloadUrlResponse | HTTPValidationError | None = get_dataset_download_url_datasets_dataset_id_download_url_get.sync(
            dataset_id=self.id,
            client=self._client._generated_client,
        )

        if isinstance(result, HTTPValidationError):
            raise Exception(f"Failed to get download URL: {result.detail}")
        elif result is None:
            raise Exception("Failed to get download URL: received None response")
        
        return self._read_parquet_from_signed_url(result.url)
    
    def _read_parquet_from_signed_url(self, url: str) -> pa.Table:
        """
        Download and read a Parquet file from a signed URL.
        
        Args:
            url: Signed URL to download from
        
        Returns:
            PyArrow Table with the data
        """
        with fsspec.open(url, mode="rb", cache_type="readahead", block_size=4*1024*1024) as f:
            table: pa.Table = pq.read_table(f)
        return table

