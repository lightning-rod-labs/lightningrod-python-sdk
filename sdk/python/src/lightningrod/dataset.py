import base64
from typing import TYPE_CHECKING, List

import attrs
import fsspec
import pyarrow as pa
import pyarrow.parquet as pq

from lightningrod._generated.api.datasets import (
    get_dataset_download_url_datasets_dataset_id_download_url_get,
)
from lightningrod._generated.models import DatasetDownloadUrlResponse, HTTPValidationError
from lightningrod._generated.models.sample import Sample
from lightningrod._generated.models.seed import Seed
from lightningrod._generated.models.question import Question
from lightningrod._generated.models.label import Label
from lightningrod._generated.models.sample_meta import SampleMeta

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
    
    def to_samples(self) -> List[Sample]:
        """
        Download the dataset and convert it to a list of Sample objects.
        
        This method:
        1. Downloads the dataset as a PyArrow Table
        2. Parses each row into a structured Sample object
        3. Maps flattened columns to nested structures (Seed, Question, Label)
        
        Column mappings:
        - sample_id -> Sample.sample_id
        - seed_text, url, seed_creation_date -> Sample.seed (Seed object)
        - question_text -> Sample.question (Question object)
        - label, label_confidence, resolution_date -> Sample.label (Label object)
        - All other columns -> Sample.meta
        
        Returns:
            List of Sample objects
        
        Example:
            >>> client = LightningRodClient(api_key="your-api-key")
            >>> dataset = client.get_dataset("dataset-123")
            >>> samples = dataset.to_samples()
            >>> print(f"First sample: {samples[0].sample_id}")
        """
        table: pa.Table = self.to_arrow()
        samples: List[Sample] = []
        
        def get_field_names(cls) -> set[str]:
            return {f.name for f in attrs.fields(cls) if f.name != "additional_properties"}
        
        seed_fields = get_field_names(Seed)
        question_fields = get_field_names(Question)
        label_fields = get_field_names(Label)
        sample_fields = get_field_names(Sample)
        
        known_columns = seed_fields | question_fields | label_fields | sample_fields
        available_columns = set(table.column_names)
        
        for row_idx in range(len(table)):
            row = {col: table[col][row_idx].as_py() for col in table.column_names}
            
            sample_id: str = row.get("sample_id", f"sample_{row_idx}")
            
            seed: Seed | None = None
            seed_data = {k: v for k, v in row.items() if k in seed_fields and v is not None}
            if seed_data and "seed_text" in seed_data:
                for field in seed_fields:
                    if field not in seed_data and field in available_columns:
                        seed_data[field] = row.get(field)
                seed = Seed.from_dict(seed_data)
            
            question: Question | None = None
            question_data = {k: v for k, v in row.items() if k in question_fields and v is not None}
            if question_data:
                question = Question.from_dict(question_data)
            
            label: Label | None = None
            label_data = {k: v for k, v in row.items() if k in label_fields and v is not None}
            if label_data and "label" in label_data:
                for field in label_fields:
                    if field not in label_data and field in available_columns:
                        label_data[field] = row.get(field)
                label = Label.from_dict(label_data)
            
            meta_dict = {k: v for k, v in row.items() if k not in known_columns}
            meta: SampleMeta = SampleMeta.from_dict(meta_dict)
            
            sample: Sample = Sample(
                sample_id=sample_id,
                seed=seed,
                question=question,
                label=label,
                meta=meta,
            )
            
            samples.append(sample)
        
        return samples

