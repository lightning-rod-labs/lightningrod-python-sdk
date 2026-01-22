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
from lightningrod._errors import handle_response_error

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
        
        response = add_file_to_set_filesets_file_set_id_files_post.sync_detailed(
            file_set_id=file_set_id,
            client=self._client,
            body=request
        )
        
        return handle_response_error(response, "add file to set")
    
    def list(
        self,
        file_set_id: str,
        cursor: Optional[str] = None,
        limit: int = 100
    ) -> ListFileSetFilesResponse:
        response = list_files_in_set_filesets_file_set_id_files_get.sync_detailed(
            file_set_id=file_set_id,
            client=self._client,
            cursor=cursor if cursor else None,
            limit=limit
        )
        
        return handle_response_error(response, "list files in set")


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
        
        response = create_file_set_filesets_post.sync_detailed(
            client=self._client,
            body=request
        )
        
        return handle_response_error(response, "create file set")
    
    def get(self, file_set_id: str) -> FileSet:
        response = get_file_set_filesets_file_set_id_get.sync_detailed(
            file_set_id=file_set_id,
            client=self._client
        )
        
        return handle_response_error(response, "get file set")
    
    def list(self) -> List[FileSet]:
        response = list_file_sets_filesets_get.sync_detailed(client=self._client)
        
        parsed = handle_response_error(response, "list file sets")
        return parsed.file_sets
