"""LLM-based metadata extraction for FileSet uploads.

Given a FileSet metadata schema (whose fields may include an
``extraction_hint``) and a list of files, ask an LLM to populate the
schema for each file. The returned dict matches the shape
``FileSetsClient.upload_files`` expects for its ``metadata`` argument.
"""

from __future__ import annotations

import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from lightningrod._generated.models.metadata_field_type import MetadataFieldType
from lightningrod._generated.types import Unset


TEXT_SUFFIXES = {
    ".txt",
    ".md",
    ".csv",
    ".json",
    ".html",
    ".htm",
    ".xml",
    ".yaml",
    ".yml",
    ".log",
}
PDF_SUFFIXES = {".pdf"}

DEFAULT_MODEL = "gpt-4.1-mini"
DEFAULT_MAX_CHARS = 20_000


def _is_set(value: Any) -> bool:
    return value is not None and not isinstance(value, Unset)


def _schema_fields(schema: Any) -> List[Any]:
    """Return the list of field definitions from either the input or response schema object."""
    fields = getattr(schema, "fields", None)
    if not _is_set(fields):
        return []
    return list(fields)


def _validate_extraction_options(
    max_chars: int,
    max_pages: Optional[int],
    max_workers: int,
) -> None:
    if max_chars <= 0:
        raise ValueError("max_chars must be greater than 0.")
    if max_pages is not None and max_pages <= 0:
        raise ValueError("max_pages must be greater than 0 when provided.")
    if max_workers <= 0:
        raise ValueError("max_workers must be greater than 0.")


def _metadata_key(path: Path) -> str:
    return path.name


def _is_supported_path(path: Path) -> bool:
    suffix = path.suffix.lower()
    return suffix in TEXT_SUFFIXES or suffix in PDF_SUFFIXES


def _validate_unique_metadata_keys(paths: List[Path]) -> None:
    seen: Dict[str, Path] = {}
    duplicates: List[str] = []
    for path in paths:
        key = _metadata_key(path)
        if key in seen:
            duplicates.append(key)
        else:
            seen[key] = path
    if duplicates:
        names = ", ".join(sorted(set(duplicates)))
        raise ValueError(
            "Cannot extract metadata for files with duplicate names: "
            f"{names}. Metadata is keyed by filename, so each file name must be unique."
        )


def _read_text_for_extraction(path: Path, max_chars: int) -> Optional[str]:
    """Read a plain-text file, truncating to ``max_chars``.

    Returns ``None`` if the suffix isn't a recognized plain-text type or the
    file can't be opened.
    """
    if path.suffix.lower() not in TEXT_SUFFIXES:
        return None
    try:
        with open(path, "rb") as f:
            raw = f.read(max_chars * 4)
    except OSError:
        return None
    text = raw.decode("utf-8", errors="replace")
    if len(text) > max_chars:
        text = text[:max_chars]
    return text


def _read_pdf_for_extraction(
    path: Path,
    max_chars: int,
    max_pages: Optional[int],
) -> Optional[str]:
    """Extract text from a PDF using ``pypdf``.

    Honors ``max_pages`` (first N pages) and truncates to ``max_chars``.
    Returns ``None`` if the PDF can't be opened.
    """
    from pypdf import PdfReader  # eager ImportError is checked upstream

    try:
        reader = PdfReader(str(path))
    except Exception:
        return None

    pages = reader.pages
    if max_pages is not None:
        pages = pages[:max_pages]

    chunks: List[str] = []
    total = 0
    for page in pages:
        try:
            text = page.extract_text() or ""
        except Exception:
            text = ""
        if not text:
            continue
        chunks.append(text)
        total += len(text)
        if total >= max_chars:
            break

    if not chunks:
        return None
    out = "\n\n".join(chunks)
    if len(out) > max_chars:
        out = out[:max_chars]
    return out


def _read_file_for_extraction(
    path: Path,
    max_chars: int,
    max_pages: Optional[int],
) -> Optional[str]:
    """Dispatch to the right reader based on suffix.

    Returns ``None`` for unsupported file types so callers can skip them.
    """
    suffix = path.suffix.lower()
    if suffix in PDF_SUFFIXES:
        return _read_pdf_for_extraction(path, max_chars, max_pages)
    if suffix in TEXT_SUFFIXES:
        return _read_text_for_extraction(path, max_chars)
    return None


def _build_json_schema(schema: Any) -> Dict[str, Any]:
    """Translate a FileSet metadata schema into an OpenAI-compatible JSON schema."""
    properties: Dict[str, Any] = {}
    required: List[str] = []
    for field in _schema_fields(schema):
        ftype = field.field_type
        if ftype == MetadataFieldType.NUMBER:
            json_type = "number"
        else:
            json_type = "string"

        description_parts: List[str] = []
        if _is_set(getattr(field, "description", None)):
            description_parts.append(str(field.description))
        if _is_set(getattr(field, "extraction_hint", None)):
            description_parts.append(f"Extraction hint: {field.extraction_hint}")
        prop: Dict[str, Any] = {"type": [json_type, "null"]}
        if description_parts:
            prop["description"] = " ".join(description_parts)
        properties[field.name] = prop

        is_required = getattr(field, "required", False)
        if _is_set(is_required) and bool(is_required):
            required.append(field.name)

    json_schema: Dict[str, Any] = {
        "type": "object",
        "properties": properties,
        "additionalProperties": False,
    }
    if required:
        json_schema["required"] = required
    return json_schema


def _coerce_value(value: Any, ftype: MetadataFieldType) -> Any:
    """Coerce an LLM-returned value to the declared field type."""
    if value is None:
        return None
    if ftype == MetadataFieldType.NUMBER:
        if isinstance(value, bool):
            return None
        if isinstance(value, (int, float)):
            return value
        try:
            text = str(value).strip()
            if not text:
                return None
            if "." in text:
                return float(text)
            return int(text)
        except (TypeError, ValueError):
            return None
    return str(value)


def _coerce_result(raw: Dict[str, Any], schema: Any) -> Dict[str, Any]:
    out: Dict[str, Any] = {}
    for field in _schema_fields(schema):
        if field.name in raw:
            coerced = _coerce_value(raw[field.name], field.field_type)
            if coerced is not None:
                out[field.name] = coerced
    return out


def _build_prompt(text: str, schema: Any, filename: str) -> str:
    field_lines = []
    for field in _schema_fields(schema):
        hint = field.extraction_hint if _is_set(getattr(field, "extraction_hint", None)) else ""
        desc = field.description if _is_set(getattr(field, "description", None)) else ""
        parts = [f"- {field.name} ({field.field_type.value})"]
        if desc:
            parts.append(f"description: {desc}")
        if hint:
            parts.append(f"hint: {hint}")
        field_lines.append("; ".join(parts))
    fields_block = "\n".join(field_lines) if field_lines else "(no fields)"
    return (
        f"Extract metadata for the file named '{filename}'.\n\n"
        f"Fields to extract:\n{fields_block}\n\n"
        "If a value is not present in the document, return null for that field. "
        "Return a JSON object matching the provided schema.\n\n"
        "Document contents:\n"
        f"---\n{text}\n---"
    )


def _extract_one(
    client: Any,
    path: Path,
    schema: Any,
    json_schema: Dict[str, Any],
    model: str,
    max_chars: int,
    max_pages: Optional[int],
) -> Optional[Dict[str, Any]]:
    text = _read_file_for_extraction(path, max_chars, max_pages)
    if text is None:
        return None

    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": (
                    "You extract structured metadata from documents. "
                    "Respond with a single JSON object matching the schema."
                ),
            },
            {"role": "user", "content": _build_prompt(text, schema, path.name)},
        ],
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "file_metadata",
                "schema": json_schema,
                "strict": False,
            },
        },
    )
    content = response.choices[0].message.content
    if not content:
        return None
    parsed = json.loads(content)
    if not isinstance(parsed, dict):
        return None
    return _coerce_result(parsed, schema)


def extract_metadata_for_files(
    file_paths: List[Union[str, Path]],
    schema: Any,
    *,
    api_key: Optional[str] = None,
    base_url: Optional[str] = None,
    model: str = DEFAULT_MODEL,
    max_chars: int = DEFAULT_MAX_CHARS,
    max_pages: Optional[int] = None,
    max_workers: int = 10,
    openai_client: Any = None,
) -> Dict[str, Dict[str, Any]]:
    """Extract per-file metadata from a list of files using an LLM.

    Supports plain-text files (``.txt``, ``.md``, ``.csv``, ``.json``,
    ``.html``, ``.htm``, ``.xml``, ``.yaml``, ``.yml``, ``.log``) and PDFs.

    Args:
        file_paths: Files to extract metadata from.
        schema: A ``FileSetMetadataSchema`` or ``FileSetMetadataSchemaInput``
            describing the fields to populate. Each field's ``extraction_hint``
            (if set) is passed to the model.
        api_key: LightningRod API key. Required unless ``openai_client`` is
            provided. Used to authenticate against the LR-hosted
            OpenAI-compatible endpoint.
        base_url: LightningRod API base URL (e.g. the SDK client's ``base_url``).
            Required unless ``openai_client`` is provided. The OpenAI proxy is
            reached at ``{base_url}/openai``.
        model: Model id to call. Defaults to ``gpt-4.1-mini``.
        max_chars: Max characters of file text to include in the prompt.
        max_pages: For PDFs, only read the first N pages. Ignored for
            plain-text files. Useful when the metadata lives on e.g. a
            cover page and later pages would waste context.
        max_workers: Parallelism for per-file LLM calls.
        openai_client: Optional pre-configured client (primarily for testing).
            If provided, ``api_key``/``base_url`` are ignored.

    Returns:
        Mapping of ``filename`` -> extracted metadata dict. Files that failed
        extraction or whose type is not supported are omitted.
    """
    _validate_extraction_options(max_chars, max_pages, max_workers)

    if not _schema_fields(schema):
        raise ValueError("Cannot extract metadata: schema has no fields.")

    paths = [Path(p) for p in file_paths]
    if not paths:
        return {}
    supported_paths = [path for path in paths if _is_supported_path(path)]
    if not supported_paths:
        return {}
    _validate_unique_metadata_keys(supported_paths)

    has_pdf = any(p.suffix.lower() in PDF_SUFFIXES for p in supported_paths)
    if has_pdf:
        try:
            import pypdf  # noqa: F401  (checked eagerly for a clear error)
        except ImportError:
            raise ImportError(
                "pypdf is required to extract metadata from PDF files. "
                "Install with: pip install 'lightningrod-ai[extract]' or pip install pypdf"
            )

    if openai_client is None:
        if not api_key:
            raise ValueError("api_key is required when openai_client is not provided.")
        if not base_url:
            raise ValueError("base_url is required when openai_client is not provided.")
        try:
            from openai import OpenAI
        except ImportError:
            raise ImportError(
                "openai is required for metadata extraction. "
                "Install with: pip install 'lightningrod-ai[extract]' or pip install openai"
            )
        openai_client = OpenAI(
            api_key=api_key,
            base_url=f"{base_url.rstrip('/')}/openai",
        )

    json_schema = _build_json_schema(schema)

    results: Dict[str, Dict[str, Any]] = {}

    def _task(path: Path) -> Optional[Dict[str, Any]]:
        return _extract_one(
            openai_client, path, schema, json_schema, model, max_chars, max_pages
        )

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(_task, p): p for p in supported_paths}
        for future in as_completed(futures):
            path = futures[future]
            try:
                extracted = future.result()
            except Exception:
                continue
            if extracted:
                results[_metadata_key(path)] = extracted

    return results
