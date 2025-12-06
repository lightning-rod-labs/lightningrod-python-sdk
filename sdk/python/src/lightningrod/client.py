import base64
import time
from io import BytesIO
from typing import Any, List, Optional

import attrs
import httpx
import pyarrow as pa
import pyarrow.csv as pa_csv
import pyarrow.parquet as pq

from lightningrod._generated.client import AuthenticatedClient
from lightningrod._generated.models import (
    DatasetMetadata,
    TransformJob,
    TransformJobStatus,
    CreateTransformJobRequest,
    HTTPValidationError,
)
from lightningrod._generated.models.sample import Sample
from lightningrod._generated.models.seed import Seed
from lightningrod._generated.models.question import Question
from lightningrod._generated.models.label import Label
from lightningrod._generated.types import UNSET, Unset
from lightningrod._generated.api.datasets import get_dataset_datasets_dataset_id_get
from lightningrod._generated.api.transform_jobs import (
    create_transform_job_transform_jobs_post,
    get_transform_job_transform_jobs_job_id_get,
)
from lightningrod.dataset import Dataset
from lightningrod.pipeline import TransformPipeline, TransformConfig


class Datasets:
    """
    Dataset operations for Lightning Rod.
    
    Access via client.datasets property.
    
    Example:
        >>> client = LightningRodClient(api_key="your-api-key")
        >>> dataset = client.datasets.get("dataset-123")
        >>> new_dataset = client.datasets.from_csv("data.csv")
    """
    
    def __init__(self, client: "LightningRodClient"):
        self._client = client
    
    def get(self, dataset_id: str) -> Dataset:
        """
        Get a dataset by its ID.
        
        Args:
            dataset_id: The ID of the dataset to retrieve
        
        Returns:
            Dataset instance with metadata loaded
        
        Raises:
            Exception: If the API returns an error
        
        Example:
            >>> client = LightningRodClient(api_key="your-api-key")
            >>> dataset = client.datasets.get("dataset-123")
            >>> table = dataset.to_arrow()
        """
        dataset_metadata: DatasetMetadata | HTTPValidationError | None = get_dataset_datasets_dataset_id_get.sync(
            dataset_id=dataset_id,
            client=self._client._generated_client,
        )
        
        if isinstance(dataset_metadata, HTTPValidationError):
            raise Exception(f"Failed to get dataset: {dataset_metadata.detail}")
        elif dataset_metadata is None:
            raise Exception("Failed to get dataset: received None response")
        
        schema_bytes: bytes = base64.b64decode(dataset_metadata.schema_base64)
        schema: pa.Schema = pa.ipc.read_schema(pa.py_buffer(schema_bytes))
        
        return Dataset(
            id=dataset_metadata.id,
            num_rows=dataset_metadata.num_rows,
            schema=schema,
            client=self._client
        )
    
    def from_pyarrow(self, table: pa.Table) -> Dataset:
        """
        Create a dataset by uploading a PyArrow Table.
        
        This method:
        1. Requests a signed upload URL from the API
        2. Serializes the table to Parquet format
        3. Uploads the Parquet file to cloud storage
        4. Creates a dataset record from the uploaded file
        
        Args:
            table: PyArrow Table to upload
        
        Returns:
            Dataset instance for the created dataset
        
        Raises:
            Exception: If the upload or dataset creation fails
        
        Example:
            >>> import pyarrow as pa
            >>> client = LightningRodClient(api_key="your-api-key")
            >>> table = pa.table({"col1": [1, 2, 3], "col2": ["a", "b", "c"]})
            >>> dataset = client.datasets.from_pyarrow(table)
            >>> print(f"Created dataset: {dataset.id}")
        """
        http_client: httpx.Client = self._client._generated_client.get_httpx_client()
        
        upload_url_response: httpx.Response = http_client.post("/datasets/upload-url")
        upload_url_response.raise_for_status()
        upload_url_data: dict = upload_url_response.json()
        upload_id: str = upload_url_data["upload_id"]
        signed_url: str = upload_url_data["url"]
        
        buffer = BytesIO()
        pq.write_table(table, buffer)
        parquet_bytes: bytes = buffer.getvalue()
        
        upload_response: httpx.Response = httpx.put(
            signed_url,
            content=parquet_bytes,
            headers={"Content-Type": "application/octet-stream"}
        )
        upload_response.raise_for_status()
        
        create_response: httpx.Response = http_client.post(
            "/datasets/from-upload",
            json={"upload_id": upload_id}
        )
        create_response.raise_for_status()
        dataset_data: dict = create_response.json()
        
        schema_bytes: bytes = base64.b64decode(dataset_data["schema_base64"])
        schema: pa.Schema = pa.ipc.read_schema(pa.py_buffer(schema_bytes))
        
        return Dataset(
            id=dataset_data["id"],
            num_rows=dataset_data["num_rows"],
            schema=schema,
            client=self._client
        )
    
    def from_samples(self, samples: List[Sample]) -> Dataset:
        """
        Create a dataset from a list of Sample objects.
        
        This method:
        1. Converts Sample objects to a flat PyArrow Table
        2. Flattens nested objects (Seed, Question, Label) into top-level columns
        3. Uploads the table to create a dataset
        
        Args:
            samples: List of Sample objects to convert and upload
        
        Returns:
            Dataset instance for the created dataset
        
        Raises:
            Exception: If the upload or dataset creation fails
        
        Example:
            >>> from lightningrod._generated.models import Sample, Seed, Question
            >>> client = LightningRodClient(api_key="your-api-key")
            >>> samples = [Sample(sample_id="1", seed=Seed(seed_text="text"), ...)]
            >>> dataset = client.datasets.from_samples(samples)
        """
        table: pa.Table = self._samples_to_table(samples)
        return self.from_pyarrow(table)
    
    def from_csv(self, path: str) -> Dataset:
        """
        Create a dataset from a CSV file.
        
        Args:
            path: Path to the CSV file
        
        Returns:
            Dataset instance for the created dataset
        
        Raises:
            Exception: If the file cannot be read or upload fails
        
        Example:
            >>> client = LightningRodClient(api_key="your-api-key")
            >>> dataset = client.datasets.from_csv("data.csv")
            >>> print(f"Created dataset: {dataset.id}")
        """
        table: pa.Table = pa_csv.read_csv(path)
        return self.from_pyarrow(table)
    
    def from_pandas(self, df: "pandas.DataFrame") -> Dataset:
        """
        Create a dataset from a Pandas DataFrame.
        
        Args:
            df: Pandas DataFrame to upload
        
        Returns:
            Dataset instance for the created dataset
        
        Raises:
            Exception: If the conversion or upload fails
        
        Example:
            >>> import pandas as pd
            >>> client = LightningRodClient(api_key="your-api-key")
            >>> df = pd.DataFrame({"col1": [1, 2, 3], "col2": ["a", "b", "c"]})
            >>> dataset = client.datasets.from_pandas(df)
            >>> print(f"Created dataset: {dataset.id}")
        """
        table: pa.Table = pa.Table.from_pandas(df)
        return self.from_pyarrow(table)
    
    def from_lists(
        self,
        seeds: List[Seed],
        questions: List[Question],
        labels: List[Label]
    ) -> Dataset:
        """
        Create a dataset from parallel lists of Seeds, Questions, and Labels.
        
        All lists must be the same length. Each index represents one sample.
        
        Args:
            seeds: List of Seed objects
            questions: List of Question objects
            labels: List of Label objects
        
        Returns:
            Dataset instance for the created dataset
        
        Raises:
            ValueError: If the lists have different lengths
            Exception: If the upload or dataset creation fails
        
        Example:
            >>> from lightningrod._generated.models import Seed, Question, Label
            >>> client = LightningRodClient(api_key="your-api-key")
            >>> seeds = [Seed(seed_text="news article 1"), Seed(seed_text="news article 2")]
            >>> questions = [Question(question_text="Q1?"), Question(question_text="Q2?")]
            >>> labels = [Label(label=True), Label(label=False)]
            >>> dataset = client.datasets.from_lists(seeds, questions, labels)
        """
        if not (len(seeds) == len(questions) == len(labels)):
            raise ValueError(
                f"All lists must have the same length. "
                f"Got seeds={len(seeds)}, questions={len(questions)}, labels={len(labels)}"
            )
        
        samples: List[Sample] = [
            Sample(
                seed=seeds[i],
                question=questions[i],
                label=labels[i],
            )
            for i in range(len(seeds))
        ]
        return self.from_samples(samples)
    
    def _samples_to_table(self, samples: List[Sample]) -> pa.Table:
        """Convert a list of Sample objects to a PyArrow Table."""
        import json
        
        if not samples:
            raise ValueError("Cannot create dataset from empty samples list")
        
        def get_field_names(cls: type) -> set[str]:
            return {f.name for f in attrs.fields(cls) if f.name != "additional_properties"}
        
        seed_fields: set[str] = get_field_names(Seed)
        question_fields: set[str] = get_field_names(Question)
        label_fields: set[str] = get_field_names(Label)
        
        rows: List[dict] = []
        all_columns: set[str] = set()
        
        for sample in samples:
            row: dict = {}
            
            if sample.seed is not None and sample.seed is not UNSET:
                for field_name in seed_fields:
                    value = getattr(sample.seed, field_name)
                    if value is not UNSET:
                        row[field_name] = value
            
            if sample.question is not None and sample.question is not UNSET:
                for field_name in question_fields:
                    value = getattr(sample.question, field_name)
                    if value is not UNSET:
                        row[field_name] = value
            
            if sample.label is not None and sample.label is not UNSET:
                for field_name in label_fields:
                    value = getattr(sample.label, field_name)
                    if value is not UNSET:
                        row[field_name] = value
            
            if isinstance(sample.context, list):
                row["context"] = json.dumps([ctx.to_dict() for ctx in sample.context])
            
            if isinstance(sample.prompt, str):
                row["prompt"] = sample.prompt
            
            if not isinstance(sample.meta, Unset) and sample.meta is not None:
                meta_dict: dict = sample.meta.to_dict()
                row.update(meta_dict)
            
            all_columns.update(row.keys())
            rows.append(row)
        
        for row in rows:
            for col in all_columns:
                if col not in row:
                    row[col] = None
        
        column_data: dict[str, list] = {col: [] for col in all_columns}
        for row in rows:
            for col in all_columns:
                column_data[col].append(row[col])
        
        return pa.table(column_data)


class LightningRodClient:
    """
    Python client for the Lightning Rod API.
    
    This client provides access to Lightning Rod's AI-powered forecasting
    dataset generation platform.
    
    Args:
        api_key: Your Lightning Rod API key
        base_url: Base URL for the API (defaults to production)
    
    Example:
        >>> client = LightningRodClient(api_key="your-api-key")
        >>> dataset = client.datasets.get("dataset-123")
    """
    
    def __init__(
        self,
        api_key: str,
        base_url: str = "https://api.lightningrod.ai/api/public/v1"
    ):
        self.api_key: str = api_key
        self.base_url: str = base_url.rstrip("/")
        self._generated_client: AuthenticatedClient = AuthenticatedClient(
            base_url=self.base_url,
            token=api_key,
            prefix="Bearer",
            auth_header_name="Authorization",
        )
        self._datasets: Datasets = Datasets(self)
    
    @property
    def datasets(self) -> Datasets:
        """Access dataset operations."""
        return self._datasets
    
    def pipeline(self, config: Any) -> TransformPipeline:
        """
        Create a pipeline builder for executing transforms.
        
        Args:
            config: Transform configuration (NewsSeedGenerator, Pipeline, etc.)
        
        Returns:
            TransformPipeline instance for chaining
        
        Example:
            >>> client = LightningRodClient(api_key="your-api-key")
            >>> config = NewsSeedGenerator(...)
            >>> dataset = client.pipeline(config).run()
        """
        return TransformPipeline(self, config)
    
    def _run(
        self,
        config: Any,
        dataset: Optional[Dataset] = None,
        max_seeds: Optional[int] = None
    ) -> Dataset:
        """Internal method to run a transform job and wait for completion."""
        job: TransformJob = self._submit(config, dataset, max_seeds)
        
        while job.status == TransformJobStatus.RUNNING:
            time.sleep(15)
            job = get_transform_job_transform_jobs_job_id_get.sync(
                job_id=job.id,
                client=self._generated_client,
            )
        
        if job.status == TransformJobStatus.FAILED:
            raise Exception(f"Transform job {job.id} failed")
        
        if job.status == TransformJobStatus.COMPLETED:
            if job.output_dataset_id is None:
                raise Exception(f"Transform job {job.id} completed but has no output dataset")
            
            return self.datasets.get(job.output_dataset_id)
        
        raise Exception(f"Unexpected job status: {job.status}")
    
    def _submit(
        self,
        config: Any,
        dataset: Optional[Dataset] = None,
        max_seeds: Optional[int] = None
    ) -> TransformJob:
        """Internal method to submit a transform job without waiting."""
        request: CreateTransformJobRequest = CreateTransformJobRequest(
            config=config,
            input_dataset_id=dataset.id if dataset else None,
            max_seeds=max_seeds
        )
        
        response = create_transform_job_transform_jobs_post.sync(
            client=self._generated_client,
            body=request,
        )

        if isinstance(response, HTTPValidationError):
            raise Exception(f"Failed to submit transform job: {response.detail}")
        elif response is None:
            raise Exception("Failed to submit transform job: received None response")
        
        return response
