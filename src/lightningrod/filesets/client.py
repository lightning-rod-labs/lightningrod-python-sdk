from typing import List, Optional

from lightningrod._generated.models import (
    FileSet,
    CreateFileSetRequest,
    FileSetMetadataSchemaInput,
    BatchUploadRequest,
    BatchUploadResponse,
    BuildIndexRequest,
    BuildIndexResponse,
)
from lightningrod._generated.api.file_sets import (
    create_file_set_filesets_post,
    get_file_set_filesets_file_set_id_get,
    list_file_sets_filesets_get,
    generate_batch_upload_urls_filesets_file_set_id_upload_folder_post,
    build_qdrant_index_filesets_file_set_id_build_index_post,
)
from lightningrod._generated.client import AuthenticatedClient
from lightningrod._errors import handle_response_error


class FileSetsClient:
    def __init__(self, client: AuthenticatedClient):
        self._client = client

    def create(
        self,
        name: str,
        description: Optional[str] = None,
        metadata_schema: Optional[FileSetMetadataSchemaInput] = None,
    ) -> FileSet:
        request = CreateFileSetRequest(name=name)
        if description is not None:
            request.description = description
        if metadata_schema is not None:
            request.metadata_schema = metadata_schema

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

    def upload_folder(
        self,
        file_set_id: str,
        file_names: List[str],
    ) -> BatchUploadResponse:
        """Generate signed URLs for batch file upload to GCS.

        Args:
            file_set_id: The ID of the FileSet to upload to
            file_names: List of filenames to generate upload URLs for

        Returns:
            BatchUploadResponse containing folder_path and upload_urls mapping
        """
        request = BatchUploadRequest(file_names=file_names)

        response = generate_batch_upload_urls_filesets_file_set_id_upload_folder_post.sync_detailed(
            file_set_id=file_set_id,
            client=self._client,
            body=request
        )

        return handle_response_error(response, "generate batch upload URLs")

    def build_index(
        self,
        file_set_id: str,
        chunk_size: int = 1500,
        chunk_overlap: int = 150,
        embedding_model: str = "BAAI/bge-small-en-v1.5",
    ) -> BuildIndexResponse:
        """Build Qdrant vector index from uploaded files.

        Args:
            file_set_id: The ID of the FileSet to index
            chunk_size: Characters per text chunk (default: 1500)
            chunk_overlap: Overlap between consecutive chunks (default: 150)
            embedding_model: FastEmbed model for embeddings (default: BAAI/bge-small-en-v1.5)

        Returns:
            BuildIndexResponse containing collection_name, chunk_count, and file_count
        """
        request = BuildIndexRequest(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            embedding_model=embedding_model,
        )

        response = build_qdrant_index_filesets_file_set_id_build_index_post.sync_detailed(
            file_set_id=file_set_id,
            client=self._client,
            body=request
        )

        return handle_response_error(response, "build Qdrant index")
