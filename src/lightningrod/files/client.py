from pathlib import Path

import httpx

from lightningrod._generated.models import (
    HTTPValidationError,
    CreateFileUploadRequest,
    CreateFileUploadResponse,
)
from lightningrod._generated.api.files import (
    create_file_upload_files_post,
)
import mimetypes
from lightningrod._generated.client import AuthenticatedClient

class FilesClient:
    def __init__(self, client: AuthenticatedClient):
        self._client: AuthenticatedClient = client
    
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
            client=self._client,
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
