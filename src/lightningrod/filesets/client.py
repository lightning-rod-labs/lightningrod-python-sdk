import json
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Union

import requests

from lightningrod._generated.models import (
    FileSet,
    CreateFileSetRequest,
    FileSetMetadataSchemaInput,
    BatchUploadRequest,
    BatchUploadResponse,
)
from lightningrod._generated.api.file_sets import (
    create_file_set_filesets_post,
    get_file_set_filesets_file_set_id_get,
    list_file_sets_filesets_get,
    generate_batch_upload_urls_filesets_file_set_id_upload_folder_post,
)
from lightningrod._generated.client import AuthenticatedClient
from lightningrod._generated.types import Unset
from lightningrod._errors import handle_response_error
from lightningrod.filesets.extraction import (
    DEFAULT_MAX_CHARS,
    DEFAULT_MODEL,
    extract_metadata_for_files,
)


@dataclass
class UploadResult:
    """Result of a file upload operation."""
    succeeded: int
    failed: int
    errors: List[str]


@dataclass
class UploadCredentials:
    """Short-lived, scoped GCS credentials for direct uploads."""
    token: str
    expiry: str
    bucket: str
    folder: str


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

    def get_upload_credentials(self, file_set_id: str) -> UploadCredentials:
        """Get short-lived, write-only GCS credentials for direct uploads.

        These credentials allow uploading files directly to GCS using the
        Transfer Manager, bypassing the signed URL approach. The credentials
        are scoped to only allow writes to the fileset's folder.

        Args:
            file_set_id: The ID of the FileSet to upload to

        Returns:
            UploadCredentials with token, expiry, bucket, and folder
        """
        response = self._client.get_httpx_client().request(
            method="post",
            url=f"/filesets/{file_set_id}/upload-credentials",
        )
        if response.status_code != 200:
            raise Exception(f"Failed to get upload credentials: {response.text}")
        data = response.json()
        return UploadCredentials(**data)

    def _upload_with_transfer_manager(
        self,
        file_set_id: str,
        file_paths: List[Path],
        metadata: Optional[Dict[str, Dict[str, Any]]],
        max_workers: int,
    ) -> UploadResult:
        """Upload files using GCS Transfer Manager for better scaling.

        This method uses downscoped GCS credentials and the Transfer Manager
        for efficient parallel uploads, supporting 100k+ files.
        """
        try:
            from google.cloud import storage
            from google.cloud.storage import transfer_manager
            from google.oauth2 import credentials as oauth2_credentials
        except ImportError:
            raise ImportError(
                "google-cloud-storage is required for Transfer Manager uploads. "
                "Install with: pip install 'lightningrod-ai[transfer]' or pip install google-cloud-storage"
            )

        creds = self.get_upload_credentials(file_set_id)
        oauth_creds = oauth2_credentials.Credentials(creds.token)
        storage_client = storage.Client(credentials=oauth_creds, project="lightningrod-prod")
        bucket = storage_client.bucket(creds.bucket)

        # Find common parent directory for relative paths
        if len(file_paths) == 1:
            common_parent = file_paths[0].parent
        else:
            common_parent = Path(os.path.commonpath([str(p.parent) for p in file_paths]))

        relative_paths = [str(p.relative_to(common_parent)) for p in file_paths]

        # Upload files with Transfer Manager
        results = transfer_manager.upload_many_from_filenames(
            bucket,
            relative_paths,
            source_directory=str(common_parent),
            blob_name_prefix=creds.folder,
            max_workers=max_workers,
        )

        # Count results
        succeeded = sum(1 for r in results if not isinstance(r, Exception))
        failed = sum(1 for r in results if isinstance(r, Exception))
        errors = [f"{p}: {r}" for p, r in zip(relative_paths, results) if isinstance(r, Exception)]

        # Upload manifest if metadata provided
        if metadata and succeeded > 0:
            try:
                manifest_blob = bucket.blob(f"{creds.folder}_manifest.json")
                manifest_data = {
                    fn: {k: (v.isoformat() if hasattr(v, 'isoformat') else v) for k, v in meta.items()}
                    for fn, meta in metadata.items()
                }
                manifest_blob.upload_from_string(
                    json.dumps(manifest_data),
                    content_type="application/json"
                )
            except Exception as e:
                errors.append(f"_manifest.json: {e}")

        return UploadResult(succeeded=succeeded, failed=failed, errors=errors)

    def _upload_with_progress(
        self,
        file_set_id: str,
        file_paths: List[Path],
        metadata: Optional[Dict[str, Dict[str, Any]]],
        max_workers: int,
    ) -> UploadResult:
        """Upload files with progress reporting.

        This method uploads files individually (not using Transfer Manager batch)
        to enable progress tracking for each file.
        """
        try:
            from google.cloud import storage
            from google.oauth2 import credentials as oauth2_credentials
        except ImportError:
            raise ImportError(
                "google-cloud-storage is required for progress uploads. "
                "Install with: pip install 'lightningrod-ai[transfer]' or pip install google-cloud-storage"
            )

        import sys
        import time as time_module

        creds = self.get_upload_credentials(file_set_id)
        oauth_creds = oauth2_credentials.Credentials(creds.token)
        storage_client = storage.Client(credentials=oauth_creds, project="lightningrod-prod")
        bucket = storage_client.bucket(creds.bucket)

        succeeded = 0
        failed = 0
        errors: List[str] = []
        total = len(file_paths)
        start_time = time_module.time()
        last_print_time = start_time

        def upload_single(path: Path) -> None:
            blob = bucket.blob(f"{creds.folder}{path.name}")
            blob.upload_from_filename(str(path))

        print(f"Uploading {total} files...")

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {executor.submit(upload_single, p): p for p in file_paths}
            for future in as_completed(futures):
                path = futures[future]
                try:
                    future.result()
                    succeeded += 1
                except Exception as e:
                    failed += 1
                    errors.append(f"{path.name}: {e}")

                # Print progress every 2 seconds or at milestones
                completed = succeeded + failed
                now = time_module.time()
                if now - last_print_time >= 2.0 or completed == total or completed % 500 == 0:
                    elapsed = now - start_time
                    rate = completed / elapsed if elapsed > 0 else 0
                    eta = (total - completed) / rate if rate > 0 else 0
                    pct = 100 * completed / total
                    print(f"\r  Progress: {completed}/{total} ({pct:.0f}%) - {rate:.1f} files/s - ETA: {eta:.0f}s", end="")
                    sys.stdout.flush()
                    last_print_time = now

        print()  # Newline after progress

        # Upload manifest if metadata provided
        if metadata and succeeded > 0:
            try:
                manifest_blob = bucket.blob(f"{creds.folder}_manifest.json")
                manifest_data = {
                    fn: {k: (v.isoformat() if hasattr(v, 'isoformat') else v) for k, v in meta.items()}
                    for fn, meta in metadata.items()
                }
                manifest_blob.upload_from_string(
                    json.dumps(manifest_data),
                    content_type="application/json"
                )
            except Exception as e:
                errors.append(f"_manifest.json: {e}")

        return UploadResult(succeeded=succeeded, failed=failed, errors=errors)

    def extract_metadata(
        self,
        file_set_id: str,
        file_paths: List[Union[str, Path]],
        *,
        model: str = DEFAULT_MODEL,
        max_chars: int = DEFAULT_MAX_CHARS,
        max_pages: Optional[int] = None,
        max_workers: int = 10,
    ) -> Dict[str, Dict[str, Any]]:
        """Extract per-file metadata using an LLM, guided by the FileSet's schema.

        Fetches the FileSet's metadata schema (set at
        :meth:`FileSetsClient.create`) and, for each supplied file, asks an
        LLM to extract values for every field. The returned dict is in the
        shape :meth:`upload_files` expects for its ``metadata`` argument, so
        callers can inspect or edit it before uploading.

        Supports plain-text files (``.txt``, ``.md``, ``.csv``, ``.json``,
        ``.html``, ``.htm``, ``.xml``, ``.yaml``, ``.yml``, ``.log``) and
        PDFs. Unsupported files are silently skipped.

        Requires the ``extract`` optional dependency
        (``pip install 'lightningrod-ai[extract]'``), which bundles
        ``openai`` and ``pypdf``.

        Args:
            file_set_id: The ID of the FileSet whose metadata schema should
                guide extraction.
            file_paths: Files to extract metadata from.
            model: Model id to call (defaults to ``gpt-4.1-mini``).
            max_chars: Max characters of file text to include in the prompt.
            max_pages: For PDFs, only read the first N pages (e.g.
                ``max_pages=1`` for cover-page-only extraction). Ignored
                for plain-text files.
            max_workers: Parallelism for per-file LLM calls.

        Returns:
            Mapping of ``filename`` -> extracted metadata dict. Files that
            failed extraction or whose type is not supported are omitted.

        Raises:
            ValueError: If the FileSet has no metadata schema defined.
        """
        file_set = self.get(file_set_id)
        schema = file_set.metadata_schema
        if schema is None or isinstance(schema, Unset):
            raise ValueError(
                f"FileSet '{file_set_id}' has no metadata schema. "
                "Create the FileSet with a metadata_schema to use auto-extraction."
            )

        token = self._client.token
        base_url = self._client._base_url

        return extract_metadata_for_files(
            file_paths=file_paths,
            schema=schema,
            api_key=token,
            base_url=base_url,
            model=model,
            max_chars=max_chars,
            max_pages=max_pages,
            max_workers=max_workers,
        )

    def upload_files(
        self,
        file_set_id: str,
        file_paths: List[Union[str, Path]],
        metadata: Optional[Dict[str, Dict[str, Any]]] = None,
        max_workers: int = 10,
        use_transfer_manager: bool = True,
        show_progress: bool = False,
        auto_extract_metadata: bool = False,
        extraction_max_pages: Optional[int] = None,
    ) -> UploadResult:
        """Upload files to a FileSet with optional metadata.

        This is a high-level method that handles all the complexity of uploading
        files to a FileSet, including getting signed URLs, uploading files in
        parallel, and uploading the metadata manifest.

        By default, uses GCS Transfer Manager for efficient parallel uploads
        that scale to 100k+ files. Falls back to signed URLs if google-cloud-storage
        is not installed or if use_transfer_manager=False.

        Args:
            file_set_id: The ID of the FileSet to upload to
            file_paths: List of file paths to upload
            metadata: Optional dict mapping filename -> metadata dict.
                      Each metadata dict can contain any fields defined in
                      the FileSet's metadata schema, plus an optional "file_date"
                      field (ISO format string or datetime).
            max_workers: Maximum number of parallel upload threads (default: 10)
            use_transfer_manager: If True (default), use GCS Transfer Manager for
                                  efficient uploads. Requires google-cloud-storage.
                                  Set to False to use signed URLs instead.
            show_progress: If True, display a progress bar during upload.
                          Requires google-cloud-storage. Note: progress mode
                          uploads files individually rather than using Transfer
                          Manager batch upload.
            auto_extract_metadata: If True, use an LLM to auto-extract metadata
                          for each file based on the FileSet's metadata schema
                          (see :meth:`extract_metadata`). Any values supplied
                          via ``metadata`` take precedence over extracted ones.
            extraction_max_pages: Only applies when ``auto_extract_metadata=True``.
                          For PDFs, read only the first N pages during
                          extraction (e.g. ``extraction_max_pages=1`` for
                          cover-page-only extraction). Ignored for text files.

        Returns:
            UploadResult with counts of succeeded/failed uploads and error messages

        Example:
            # Simple upload without metadata
            result = lr.filesets.upload_files(fileset.id, ["doc1.pdf", "doc2.pdf"])

            # Upload with progress bar
            result = lr.filesets.upload_files(fileset.id, files, show_progress=True)

            # Upload with metadata
            result = lr.filesets.upload_files(
                fileset.id,
                ["report_q1.pdf", "report_q2.pdf"],
                metadata={
                    "report_q1.pdf": {"ticker": "AAPL", "quarter": "Q1 2024"},
                    "report_q2.pdf": {"ticker": "AAPL", "quarter": "Q2 2024"},
                }
            )

            # Auto-extract metadata via LLM using the fileset's schema
            result = lr.filesets.upload_files(
                fileset.id,
                ["report_q1.txt", "report_q2.txt"],
                auto_extract_metadata=True,
            )
        """
        # Convert paths to Path objects
        paths = [Path(p) for p in file_paths]

        # Auto-extract metadata if requested; user-supplied values win on conflict.
        if auto_extract_metadata:
            extracted = self.extract_metadata(
                file_set_id, paths, max_pages=extraction_max_pages
            )
            if metadata:
                merged: Dict[str, Dict[str, Any]] = {
                    fn: dict(meta) for fn, meta in extracted.items()
                }
                for fn, meta in metadata.items():
                    merged.setdefault(fn, {}).update(meta)
                metadata = merged
            else:
                metadata = extracted

        # Use progress bar if requested (takes priority over transfer manager)
        if show_progress:
            try:
                return self._upload_with_progress(
                    file_set_id, paths, metadata, max_workers
                )
            except ImportError:
                # Fall back to non-progress mode
                pass

        # Try Transfer Manager if enabled (no progress support)
        if use_transfer_manager:
            try:
                return self._upload_with_transfer_manager(
                    file_set_id, paths, metadata, max_workers
                )
            except ImportError:
                # Fall back to signed URLs if google-cloud-storage not installed
                pass

        # Signed URL approach (fallback)
        file_names = [p.name for p in paths]

        # Get signed upload URLs
        upload_response = self.upload_folder(file_set_id, file_names)
        urls = upload_response.upload_urls.additional_properties

        succeeded = 0
        failed = 0
        errors: List[str] = []

        def upload_single_file(path: Path) -> None:
            """Upload a single file to its signed URL."""
            url = urls[path.name]
            with open(path, "rb") as f:
                content = f.read()
            headers = {"Content-Type": "application/octet-stream"}
            response = requests.put(url, data=content, headers=headers)
            response.raise_for_status()

        # Upload files in parallel
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {executor.submit(upload_single_file, p): p for p in paths}
            for future in as_completed(futures):
                path = futures[future]
                try:
                    future.result()
                    succeeded += 1
                except Exception as e:
                    failed += 1
                    errors.append(f"{path.name}: {e}")

        # Upload metadata manifest if provided
        if metadata:
            manifest_url = urls.get("_manifest.json")
            if manifest_url:
                try:
                    # Convert any datetime objects to ISO format strings
                    manifest_data = {}
                    for filename, meta in metadata.items():
                        manifest_data[filename] = {
                            k: (v.isoformat() if hasattr(v, 'isoformat') else v)
                            for k, v in meta.items()
                        }

                    manifest_content = json.dumps(manifest_data).encode("utf-8")
                    headers = {"Content-Type": "application/json"}
                    response = requests.put(manifest_url, data=manifest_content, headers=headers)
                    response.raise_for_status()
                except Exception as e:
                    errors.append(f"_manifest.json: {e}")

        return UploadResult(succeeded=succeeded, failed=failed, errors=errors)

    def upload_directory(
        self,
        file_set_id: str,
        directory: Union[str, Path],
        pattern: str = "*",
        metadata_fn: Optional[Callable[[Path], Optional[Dict[str, Any]]]] = None,
        max_workers: int = 10,
        use_transfer_manager: bool = True,
        show_progress: bool = False,
        auto_extract_metadata: bool = False,
        extraction_max_pages: Optional[int] = None,
    ) -> UploadResult:
        """Upload all files from a directory to a FileSet.

        Args:
            file_set_id: The ID of the FileSet to upload to
            directory: Path to the directory containing files to upload
            pattern: Glob pattern for files to include (default: "*" for all files)
            metadata_fn: Optional function that takes a file path and returns
                        a metadata dict for that file, or None to skip metadata.
            max_workers: Maximum number of parallel upload threads (default: 10)
            use_transfer_manager: If True (default), use GCS Transfer Manager for
                                  efficient uploads. Requires google-cloud-storage.
            show_progress: If True, display a progress bar during upload.
            auto_extract_metadata: If True, use an LLM to auto-extract metadata
                          for each file based on the FileSet's metadata schema.
                          If ``metadata_fn`` is also provided, its values take
                          precedence over extracted ones.
            extraction_max_pages: Only applies when ``auto_extract_metadata=True``.
                          For PDFs, read only the first N pages during
                          extraction. Ignored for text files.

        Returns:
            UploadResult with counts of succeeded/failed uploads and error messages

        Example:
            # Upload all PDFs from a directory
            result = lr.filesets.upload_directory(
                fileset.id,
                "/path/to/reports",
                pattern="*.pdf"
            )

            # Upload with progress bar
            result = lr.filesets.upload_directory(
                fileset.id,
                "/path/to/reports",
                show_progress=True
            )

            # Upload with metadata derived from filenames
            def get_metadata(path):
                # e.g., "AAPL_Q1_2024.pdf" -> {"ticker": "AAPL", "quarter": "Q1 2024"}
                parts = path.stem.split("_")
                return {"ticker": parts[0], "quarter": f"{parts[1]} {parts[2]}"}

            result = lr.filesets.upload_directory(
                fileset.id,
                "/path/to/reports",
                pattern="*.pdf",
                metadata_fn=get_metadata
            )
        """
        directory = Path(directory)
        if not directory.is_dir():
            raise ValueError(f"Not a directory: {directory}")

        # Find all matching files
        file_paths = list(directory.glob(pattern))
        if not file_paths:
            return UploadResult(succeeded=0, failed=0, errors=[])

        # Build metadata dict if function provided
        metadata: Optional[Dict[str, Dict[str, Any]]] = None
        if metadata_fn:
            metadata = {}
            for path in file_paths:
                meta = metadata_fn(path)
                if meta:
                    metadata[path.name] = meta

        return self.upload_files(
            file_set_id=file_set_id,
            file_paths=file_paths,
            metadata=metadata,
            max_workers=max_workers,
            use_transfer_manager=use_transfer_manager,
            show_progress=show_progress,
            auto_extract_metadata=auto_extract_metadata,
            extraction_max_pages=extraction_max_pages,
        )
