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
from lightningrod._generated.api.datasets import (
    get_dataset_datasets_dataset_id_get,
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
from lightningrod.dataset import Dataset
from lightningrod.pipeline import TransformPipeline


class PipelineResource:
    def __init__(self, client: "LightningRodClient"):
        self._client = client
    
    def create(self, config: Any) -> TransformPipeline:
        return TransformPipeline(self._client, config)
    
    def __call__(self, config: Any) -> TransformPipeline:
        return self.create(config)


class TransformJobsResource:
    def __init__(self, client: "LightningRodClient"):
        self._client = client
    
    def get(self, job_id: str) -> TransformJob:
        response = get_transform_job_transform_jobs_job_id_get.sync(
            job_id=job_id,
            client=self._client._generated_client,
        )
        if isinstance(response, HTTPValidationError):
            raise Exception(f"Failed to get transform job: {response.detail}")
        if response is None:
            raise Exception("Failed to get transform job: received None response")
        return response


class TransformsResource:
    def __init__(self, client: "LightningRodClient"):
        self._client = client
        self.jobs = TransformJobsResource(client)
    
    def run(
        self,
        config: Any,
        dataset_id: Optional[str] = None,
        max_questions: Optional[int] = None
    ) -> Dataset:
        job: TransformJob = self.submit(config, dataset_id, max_questions)
        
        while job.status == TransformJobStatus.RUNNING:
            time.sleep(15)
            job = self.jobs.get(job.id)
        
        if job.status == TransformJobStatus.FAILED:
            raise Exception(f"Transform job {job.id} failed")
        
        if job.status == TransformJobStatus.COMPLETED:
            if job.output_dataset_id is None:
                raise Exception(f"Transform job {job.id} completed but has no output dataset")
            
            dataset_response = get_dataset_datasets_dataset_id_get.sync(
                dataset_id=job.output_dataset_id,
                client=self._client._generated_client,
            )
            if isinstance(dataset_response, HTTPValidationError):
                raise Exception(f"Failed to get dataset: {dataset_response.detail}")
            if dataset_response is None:
                raise Exception("Failed to get dataset: received None response")
            
            return Dataset(
                id=dataset_response.id,
                num_rows=dataset_response.num_rows,
                client=self._client
            )
        
        raise Exception(f"Unexpected job status: {job.status}")
    
    def submit(
        self,
        config: Any,
        dataset_id: Optional[str] = None,
        max_questions: Optional[int] = None
    ) -> TransformJob:
        request: CreateTransformJobRequest = CreateTransformJobRequest(
            config=config,
            input_dataset_id=dataset_id,
            max_questions=max_questions
        )
        
        response = create_transform_job_transform_jobs_post.sync(
            client=self._client._generated_client,
            body=request,
        )

        if isinstance(response, HTTPValidationError):
            raise Exception(f"Failed to submit transform job: {response.detail}")
        elif response is None:
            raise Exception("Failed to submit transform job: received None response")
        
        return response


class FilesResource:
    def __init__(self, client: "LightningRodClient"):
        self._client = client
    
    def upload(self, file_path: str | Path) -> CreateFileUploadResponse:
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        file_size: int = path.stat().st_size
        mime_type, _ = mimetypes.guess_type(str(path))
        
        request_body = CreateFileUploadRequest(
            filename=path.name,
            size_bytes=file_size,
            mime_type=mime_type
        )
        
        response = create_file_upload_files_post.sync(
            client=self._client._generated_client,
            body=request_body
        )
        
        if isinstance(response, HTTPValidationError):
            raise Exception(f"Failed to get upload URL: {response.detail}")
        if response is None:
            raise Exception("Failed to get upload URL: received None response")
        
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
                    timeout=1800.0
                )
                upload_response.raise_for_status()
        
        return response


class FileSetFilesResource:
    def __init__(self, client: "LightningRodClient"):
        self._client = client
    
    def add(
        self,
        file_set_id: str,
        file_id: str,
        metadata: Optional[dict[str, Any]] = None
    ) -> FileSetFile:
        request = CreateFileSetFileRequest(
            file_id=file_id,
            metadata=CreateFileSetFileRequestMetadataType0.from_dict(metadata) if metadata else None
        )
        
        response = add_file_to_set_filesets_file_set_id_files_post.sync(
            file_set_id=file_set_id,
            client=self._client._generated_client,
            body=request
        )
        
        if isinstance(response, HTTPValidationError):
            raise Exception(f"Failed to add file to set: {response.detail}")
        if response is None:
            raise Exception("Failed to add file to set: received None response")
        
        return response
    
    def list(
        self,
        file_set_id: str,
        cursor: Optional[str] = None,
        limit: int = 100
    ) -> ListFileSetFilesResponse:
        response = list_files_in_set_filesets_file_set_id_files_get.sync(
            file_set_id=file_set_id,
            client=self._client._generated_client,
            cursor=cursor if cursor else None,
            limit=limit
        )
        
        if isinstance(response, HTTPValidationError):
            raise Exception(f"Failed to list files in set: {response.detail}")
        if response is None:
            raise Exception("Failed to list files in set: received None response")
        
        return response


class FileSetsResource:
    def __init__(self, client: "LightningRodClient"):
        self._client = client
        self.files = FileSetFilesResource(client)
    
    def create(
        self,
        name: str,
        description: Optional[str] = None
    ) -> FileSet:
        request = CreateFileSetRequest(name=name)
        if description is not None:
            request.description = description
        
        response = create_file_set_filesets_post.sync(
            client=self._client._generated_client,
            body=request
        )
        
        if isinstance(response, HTTPValidationError):
            raise Exception(f"Failed to create file set: {response.detail}")
        if response is None:
            raise Exception("Failed to create file set: received None response")
        
        return response
    
    def get(self, file_set_id: str) -> FileSet:
        response = get_file_set_filesets_file_set_id_get.sync(
            file_set_id=file_set_id,
            client=self._client._generated_client
        )
        
        if isinstance(response, HTTPValidationError):
            raise Exception(f"Failed to get file set: {response.detail}")
        if response is None:
            raise Exception("Failed to get file set: received None response")
        
        return response
    
    def list(self) -> List[FileSet]:
        response = list_file_sets_filesets_get.sync(client=self._client._generated_client)
        
        if isinstance(response, HTTPValidationError):
            raise Exception(f"Failed to list file sets: {response.detail}")
        if response is None:
            raise Exception("Failed to list file sets: received None response")
        
        return response.file_sets


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
        
        self.pipeline: PipelineResource = PipelineResource(self)
        self.transforms: TransformsResource = TransformsResource(self)
        self.files: FilesResource = FilesResource(self)
        self.filesets: FileSetsResource = FileSetsResource(self)