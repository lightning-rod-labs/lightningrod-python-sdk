from pathlib import Path
from typing import Any, List, Optional

from lightningrod._generated.models import (
    FileSet,
    ListFileSetFilesResponse,
    HTTPValidationError,
    CreateFileSetRequest,
    CreateFileSetFileRequest,
    CreateFileSetFileRequestMetadataType0,
    FileSetFile,
)
from lightningrod._generated.api.file_sets import (
    create_file_set_filesets_post,
    get_file_set_filesets_file_set_id_get,
    list_file_sets_filesets_get,
    add_file_to_set_filesets_file_set_id_files_post,
    list_files_in_set_filesets_file_set_id_files_get,
)
from lightningrod._generated.client import AuthenticatedClient
from lightningrod.files.client import FilesClient

class FileSetFilesClient:
    def __init__(self, client: AuthenticatedClient, files_client: FilesClient):
        self._client: AuthenticatedClient = client
        self._files_client: FilesClient = files_client

    def upload(
        self,
        file_set_id: str,
        file_path: str | Path,
        metadata: Optional[dict[str, Any]] = None
    ) -> FileSetFile:
        file = self._files_client.upload(file_path)
        return self.add(file_set_id, file.id, metadata)
    
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
            client=self._client,
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
            client=self._client,
            cursor=cursor if cursor else None,
            limit=limit
        )
        
        if isinstance(response, HTTPValidationError):
            raise Exception(f"Failed to list files in set: {response.detail}")
        if response is None:
            raise Exception("Failed to list files in set: received None response")
        
        return response


class FileSetsClient:
    def __init__(self, client: AuthenticatedClient, files_client: FilesClient):
        self._client = client
        self.files = FileSetFilesClient(client, files_client)
    
    def create(
        self,
        name: str,
        description: Optional[str] = None
    ) -> FileSet:
        request = CreateFileSetRequest(name=name)
        if description is not None:
            request.description = description
        
        response = create_file_set_filesets_post.sync(
            client=self._client,
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
            client=self._client
        )
        
        if isinstance(response, HTTPValidationError):
            raise Exception(f"Failed to get file set: {response.detail}")
        if response is None:
            raise Exception("Failed to get file set: received None response")
        
        return response
    
    def list(self) -> List[FileSet]:
        response = list_file_sets_filesets_get.sync(client=self._client)
        
        if isinstance(response, HTTPValidationError):
            raise Exception(f"Failed to list file sets: {response.detail}")
        if response is None:
            raise Exception("Failed to list file sets: received None response")
        
        return response.file_sets
