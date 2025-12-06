import json
from typing import Any, TYPE_CHECKING, List

import attrs
import fsspec
import pyarrow as pa
import pyarrow.parquet as pq

from lightningrod._generated.api.datasets import (
    get_dataset_download_url_datasets_dataset_id_download_url_get,
)
from lightningrod._generated.models import DatasetDownloadUrlResponse, HTTPValidationError
from lightningrod._generated.models.label import Label
from lightningrod._generated.models.question import Question
from lightningrod._generated.models.sample import Sample
from lightningrod._generated.models.seed import Seed

if TYPE_CHECKING:
    from lightningrod.client import LightningRodClient


def table_to_samples(table: pa.Table) -> List[Sample]:
    """
    Convert a PyArrow Table to a list of Sample objects.
    
    Maps flattened parquet columns to nested Sample structure:
    - seed_text, url, seed_creation_date -> Sample.seed
    - question_text -> Sample.question
    - label, label_confidence, resolution_date -> Sample.label
    - context (JSON string) -> Sample.context (parsed to NewsContext/RAGContext)
    - prompt -> Sample.prompt
    - All other columns -> Sample.meta
    
    Args:
        table: PyArrow Table with flattened sample columns
        
    Returns:
        List of Sample objects
    """
    samples: List[Sample] = []
    
    def get_field_names(cls) -> set[str]:
        return {f.name for f in attrs.fields(cls) if f.name != "additional_properties"}
    
    seed_fields: set[str] = get_field_names(Seed)
    question_fields: set[str] = get_field_names(Question)
    label_fields: set[str] = get_field_names(Label)
    known_columns: set[str] = seed_fields | question_fields | label_fields | {"context", "prompt"}
    
    for row_idx in range(len(table)):
        row: dict[str, Any] = {col: table[col][row_idx].as_py() for col in table.column_names}
        
        sample_dict: dict[str, Any] = {}
        
        seed_data: dict[str, Any] = {k: v for k, v in row.items() if k in seed_fields}
        if seed_data.get("seed_text"):
            sample_dict["seed"] = seed_data
        
        question_data: dict[str, Any] = {k: v for k, v in row.items() if k in question_fields}
        if question_data.get("question_text"):
            sample_dict["question"] = question_data
        
        label_data: dict[str, Any] = {k: v for k, v in row.items() if k in label_fields}
        if label_data.get("label") is not None:
            sample_dict["label"] = label_data
        
        context_json: str | None = row.get("context")
        if context_json:
            sample_dict["context"] = json.loads(context_json)
        
        if row.get("prompt"):
            sample_dict["prompt"] = row["prompt"]
        
        meta_data: dict[str, Any] = {k: v for k, v in row.items() if k not in known_columns}
        if meta_data:
            sample_dict["meta"] = meta_data
        
        samples.append(Sample.from_dict(sample_dict))
    
    return samples


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
    
    def to_samples(self) -> List[Sample]:
        """
        Download the dataset and convert it to a list of Sample objects.
        
        Returns:
            List of Sample objects
        
        Example:
            >>> client = LightningRodClient(api_key="your-api-key")
            >>> dataset = client.get_dataset("dataset-123")
            >>> samples = dataset.to_samples()
            >>> print(f"Got {len(samples)} samples")
        """
        return table_to_samples(self.to_arrow())
    
    def to_huggingface(self, repo_id: str, private: bool = True) -> None:
        """
        Push the dataset to HuggingFace Hub.
        
        Requires the `datasets` package and HuggingFace authentication
        (via `huggingface-cli login` or HF_TOKEN environment variable).
        
        Args:
            repo_id: HuggingFace repository ID (e.g., "username/dataset-name")
            private: Whether the dataset should be private (default: True)
        
        Example:
            >>> dataset = client.pipeline(config).run()
            >>> dataset.to_huggingface("myorg/forecasting-questions")
        """
        from datasets import Dataset as HFDataset
        
        table: pa.Table = self.to_arrow()
        hf_dataset: HFDataset = HFDataset(table)
        hf_dataset.push_to_hub(repo_id, private=private)

