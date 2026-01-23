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
from lightningrod._errors import handle_response_error

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
        
        response = create_file_upload_files_post.sync_detailed(
            client=self._client,
            body=request_body
        )
        
        parsed = handle_response_error(response, "get upload URL")
        
        upload_headers: dict[str, str] = {
            "Content-Length": str(file_size)
        }
        if parsed.mime_type:
            upload_headers["Content-Type"] = parsed.mime_type
        
        with httpx.Client() as http_client:
            with open(path, "rb") as f:
                upload_response = http_client.put(
                    parsed.upload_url,
                    content=f,
                    headers=upload_headers,
                    timeout=1800.0
                )
                upload_response.raise_for_status()
        
        return parsed
