import time
import mimetypes
from pathlib import Path
from typing import Any, List, Optional

import httpx

from lightningrod._generated.client import AuthenticatedClient
from lightningrod._generated.models import (
    FileSet,
    ListFileSetFilesResponse,
    TransformJob,
    TransformJobStatus,
    CreateTransformJobRequest,
    HTTPValidationError,
    CreateFileSetRequest,
    CreateFileUploadRequest,
    CreateFileUploadResponse,
    CreateFileSetFileRequest,
    CreateFileSetFileRequestMetadataType0,
    FileSetFile,
)
from lightningrod._generated.models.sample import Sample
from lightningrod._generated.models.upload_samples_request import UploadSamplesRequest
from lightningrod._generated.api.datasets import (
    create_dataset_datasets_post,
    get_dataset_datasets_dataset_id_get,
    get_dataset_samples_datasets_dataset_id_samples_get,
    upload_samples_datasets_dataset_id_samples_post,
)
from lightningrod._generated.api.transform_jobs import (
    create_transform_job_transform_jobs_post,
    get_transform_job_transform_jobs_job_id_get,
)
from lightningrod._generated.api.files import (
    create_file_upload_files_post,
)
from lightningrod._generated.api.file_sets import (
    create_file_set_filesets_post,
    get_file_set_filesets_file_set_id_get,
    list_file_sets_filesets_get,
    add_file_to_set_filesets_file_set_id_files_post,
    list_files_in_set_filesets_file_set_id_files_get,
)
from lightningrod._generated.types import Unset
from lightningrod.dataset import Dataset
from lightningrod.pipeline import TransformPipeline



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
        >>> dataset = client.pipeline(config).run()
        >>> samples = dataset.to_samples()
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
    
    def create_dataset(self, samples: List[Sample], batch_size: int = 1000) -> Dataset:
        """
        Upload samples to create a new dataset.
        
        Args:
            samples: List of Sample objects to upload
            batch_size: Number of samples to upload per batch (default 1000)
        
        Returns:
            Dataset instance for the created dataset
        
        Example:
            >>> from lightningrod import Sample, Seed
            >>> samples = [Sample(seed=Seed(seed_text="Article..."))]
            >>> dataset = client.create_dataset(samples)
            >>> output = client.pipeline(config).run(dataset)
        """
        create_response = create_dataset_datasets_post.sync(client=self._generated_client)
        if create_response is None:
            raise Exception("Failed to create dataset: received None response")
        dataset_id: str = create_response.id
        
        total_uploaded: int = 0
        for i in range(0, len(samples), batch_size):
            batch = samples[i:i + batch_size]
            request = UploadSamplesRequest(samples=batch)
            response = upload_samples_datasets_dataset_id_samples_post.sync(
                dataset_id=dataset_id,
                client=self._generated_client,
                body=request,
            )
            if isinstance(response, HTTPValidationError):
                raise Exception(f"Failed to upload samples: {response.detail}")
            if response is None:
                raise Exception("Failed to upload samples: received None response")
            total_uploaded = response.total
        
        return Dataset(
            id=dataset_id,
            num_rows=total_uploaded,
            client=self
        )
    
    def _fetch_all_samples(self, dataset_id: str) -> List[Sample]:
        """Fetch all samples from a dataset via the paginated API."""
        samples: List[Sample] = []
        cursor: Optional[str] = None
        
        while True:
            response = get_dataset_samples_datasets_dataset_id_samples_get.sync(
                dataset_id=dataset_id,
                client=self._generated_client,
                limit=100,
                cursor=cursor,
            )
            
            if isinstance(response, HTTPValidationError):
                raise Exception(f"Failed to fetch samples: {response.detail}")
            if response is None:
                raise Exception("Failed to fetch samples: received None response")
            
            samples.extend(response.samples)
            
            if not response.has_more:
                break
            if isinstance(response.next_cursor, Unset) or response.next_cursor is None:
                break
            cursor = str(response.next_cursor)
        
        return samples
    
    def _run(
        self,
        config: Any,
        dataset: Optional[Dataset] = None,
        max_questions: Optional[int] = None
    ) -> Dataset:
        """Internal method to run a transform job and wait for completion."""
        job: TransformJob = self._submit(config, dataset, max_questions)
        
        while job.status == TransformJobStatus.RUNNING:
            time.sleep(15)
            job_response = get_transform_job_transform_jobs_job_id_get.sync(
                job_id=job.id,
                client=self._generated_client,
            )
            if isinstance(job_response, HTTPValidationError):
                raise Exception(f"Failed to get transform job: {job_response.detail}")
            if job_response is None:
                raise Exception("Failed to get transform job: received None response")
            job = job_response
        
        if job.status == TransformJobStatus.FAILED:
            raise Exception(f"Transform job {job.id} failed")
        
        if job.status == TransformJobStatus.COMPLETED:
            if job.output_dataset_id is None:
                raise Exception(f"Transform job {job.id} completed but has no output dataset")
            
            dataset_response = get_dataset_datasets_dataset_id_get.sync(
                dataset_id=job.output_dataset_id,
                client=self._generated_client,
            )
            if isinstance(dataset_response, HTTPValidationError):
                raise Exception(f"Failed to get dataset: {dataset_response.detail}")
            if dataset_response is None:
                raise Exception("Failed to get dataset: received None response")
            
            return Dataset(
                id=dataset_response.id,
                num_rows=dataset_response.num_rows,
                client=self
            )
        
        raise Exception(f"Unexpected job status: {job.status}")
    
    def _submit(
        self,
        config: Any,
        dataset: Optional[Dataset] = None,
        max_questions: Optional[int] = None
    ) -> TransformJob:
        """Internal method to submit a transform job without waiting."""
        request: CreateTransformJobRequest = CreateTransformJobRequest(
            config=config,
            input_dataset_id=dataset.id if dataset else None,
            max_questions=max_questions
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
    
    def upload_file(
        self,
        file_path: str | Path
    ) -> CreateFileUploadResponse:
        """
        Upload a file to LightningRod storage via direct GCS upload.
        
        This method:
        1. Gets a signed upload URL from the API
        2. Uploads the file directly to GCS using the signed URL
        3. Returns file information
        
        To add the file to a FileSet with metadata, use FileSet.upload_file() 
        or FileSet.add_file().
        
        Args:
            file_path: Path to the file to upload
        
        Returns:
            CreateFileUploadResponse with file information including LightningRod storage path
        
        Example:
            >>> file = client.upload_file("document.pdf")
            >>> print(f"Uploaded to {file.cloud_storage_path}")
        """
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        # Get file metadata
        file_size: int = path.stat().st_size
        mime_type, _ = mimetypes.guess_type(str(path))
        
        # Request signed upload URL from API
        request_body = CreateFileUploadRequest(
            filename=path.name,
            size_bytes=file_size,
            mime_type=mime_type
        )
        
        response = create_file_upload_files_post.sync(
            client=self._generated_client,
            body=request_body
        )
        
        if isinstance(response, HTTPValidationError):
            raise Exception(f"Failed to get upload URL: {response.detail}")
        if response is None:
            raise Exception("Failed to get upload URL: received None response")
        
        # Upload file directly to GCS using signed URL (streaming upload)
        upload_headers: dict[str, str] = {
            "Content-Length": str(file_size)
        }
        if response.mime_type:
            upload_headers["Content-Type"] = response.mime_type
        
        with httpx.Client() as http_client:
            with open(path, "rb") as f:
                upload_response = http_client.put(
                    response.upload_url,
                    content=f,
                    headers=upload_headers,
                    timeout=1800.0  # 15 minute timeout for large files
                )
                upload_response.raise_for_status()
        
        return response
    
    def create_file_set(
        self,
        name: str,
        description: Optional[str] = None
    ) -> FileSet:
        """
        Create a new FileSet.
        
        Args:
            name: Human-readable name for the FileSet
            description: Optional description of the FileSet's purpose
        
        Returns:
            FileSet instance
        
        Example:
            >>> file_set = client.create_file_set(
            ...     name="SEC Filings 2024",
            ...     description="All SEC filings from 2024"
            ... )
        """
        request = CreateFileSetRequest(name=name)
        if description is not None:
            request.description = description
        
        response = create_file_set_filesets_post.sync(
            client=self._generated_client,
            body=request
        )
        
        if isinstance(response, HTTPValidationError):
            raise Exception(f"Failed to create file set: {response.detail}")
        if response is None:
            raise Exception("Failed to create file set: received None response")
        
        return response
    
    def get_file_set(self, file_set_id: str) -> FileSet:
        """
        Get a FileSet by ID.
        
        Args:
            file_set_id: ID of the FileSet to retrieve
        
        Returns:
            FileSet instance
        
        Example:
            >>> file_set = client.get_file_set("file-set-id")
        """
        response = get_file_set_filesets_file_set_id_get.sync(
            file_set_id=file_set_id,
            client=self._generated_client
        )
        
        if isinstance(response, HTTPValidationError):
            raise Exception(f"Failed to get file set: {response.detail}")
        if response is None:
            raise Exception("Failed to get file set: received None response")
        
        return response
    
    def list_file_sets(self) -> List[FileSet]:
        """
        List all FileSets for the organization.
        
        Returns:
            List of FileSet instances
        
        Example:
            >>> file_sets = client.list_file_sets()
            >>> for fs in file_sets:
            ...     print(f"{fs.name}: {fs.file_count} files")
        """

        # Pagination is not needed yet, since we have a hard limit on the number of FileSets per organization
        response = list_file_sets_filesets_get.sync(client=self._generated_client)
        
        if isinstance(response, HTTPValidationError):
            raise Exception(f"Failed to list file sets: {response.detail}")
        if response is None:
            raise Exception("Failed to list file sets: received None response")
        
        return response.file_sets
    
    def  add_file_to_set(
        self,
        file_id: str,
        file_set_id: str,
        metadata: Optional[dict[str, Any]]
    ) -> FileSetFile:
        """Add a file to a FileSet."""
        request = CreateFileSetFileRequest(
            file_id=file_id,
            metadata=CreateFileSetFileRequestMetadataType0.from_dict(metadata) if metadata else None
        )
        
        response = add_file_to_set_filesets_file_set_id_files_post.sync(
            file_set_id=file_set_id,
            client=self._generated_client,
            body=request
        )
        
        if isinstance(response, HTTPValidationError):
            raise Exception(f"Failed to add file to set: {response.detail}")
        if response is None:
            raise Exception("Failed to add file to set: received None response")
        
        return response
    
    def list_files_in_set(self, file_set_id: str, cursor: Optional[str] = None) -> ListFileSetFilesResponse:
        """
        List files in a FileSet.
        
        Args:
            file_set_id: ID of the FileSet to list files from
            cursor: Cursor for pagination (file id)
        Returns:
            List of FileInSetResponse instances
        
        Example:
            >>> files = client.list_files_in_set("file-set-id")
            >>> for file in files:
            ...     print(f"{file.original_file_name}: {file.size_bytes} bytes")
        """
        response = list_files_in_set_filesets_file_set_id_files_get.sync(
            file_set_id=file_set_id,
            client=self._generated_client,
            cursor=cursor if cursor else None,
            limit=100
        )
        
        if isinstance(response, HTTPValidationError):
            raise Exception(f"Failed to list files in set: {response.detail}")
        if response is None:
            raise Exception("Failed to list files in set: received None response")
        
        return response