"""LLM-based metadata extraction for FileSet uploads.

Given a FileSet metadata schema (whose fields may include an
``extraction_hint``) and a list of files, ask an LLM to populate the
schema for each file. The returned dict matches the shape
``FileSetsClient.upload_files`` expects for its ``metadata`` argument.
"""

from __future__ import annotations

import base64
import io
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple, Union

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
IMAGE_SUFFIXES = {
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".webp": "image/webp",
    ".gif": "image/gif",
}

DEFAULT_MODEL = "gpt-4.1-mini"
DEFAULT_MAX_CHARS = 20_000
DEFAULT_RENDER_SCALE = 2.0


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


def _is_supported_path(path: Path, *, use_vision: bool = False) -> bool:
    suffix = path.suffix.lower()
    if suffix in TEXT_SUFFIXES or suffix in PDF_SUFFIXES:
        return True
    if use_vision and suffix in IMAGE_SUFFIXES:
        return True
    return False


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


def _render_pdf_pages_as_images(
    path: Path,
    max_pages: Optional[int],
    scale: float = DEFAULT_RENDER_SCALE,
) -> List[Tuple[bytes, str]]:
    """Render PDF pages to PNG bytes using pypdfium2 + Pillow.

    Returns a list of ``(png_bytes, mime_type)``, one per rendered page.
    Honors ``max_pages`` (first N pages). Returns ``[]`` if the PDF can't
    be opened.
    """
    import pypdfium2 as pdfium  # eager ImportError is checked upstream

    try:
        pdf = pdfium.PdfDocument(str(path))
    except Exception:
        return []

    n_pages = len(pdf)
    if max_pages is not None:
        n_pages = min(n_pages, max_pages)

    out: List[Tuple[bytes, str]] = []
    try:
        for i in range(n_pages):
            page = pdf[i]
            bitmap = page.render(scale=scale)
            pil_image = bitmap.to_pil()
            buf = io.BytesIO()
            pil_image.save(buf, format="PNG")
            out.append((buf.getvalue(), "image/png"))
    finally:
        try:
            pdf.close()
        except Exception:
            pass
    return out


def _read_image_file(path: Path) -> Optional[Tuple[bytes, str]]:
    """Read a supported image file as ``(bytes, mime_type)``."""
    mime = IMAGE_SUFFIXES.get(path.suffix.lower())
    if mime is None:
        return None
    try:
        data = path.read_bytes()
    except OSError:
        return None
    return (data, mime)


def _images_for_vision(
    path: Path,
    max_pages: Optional[int],
) -> List[Tuple[bytes, str]]:
    """Produce the list of images to feed the vision model for this file.

    PDFs are rendered page-by-page; supported image files pass through as a
    single-element list. Returns ``[]`` for unsupported types.
    """
    suffix = path.suffix.lower()
    if suffix in PDF_SUFFIXES:
        return _render_pdf_pages_as_images(path, max_pages)
    if suffix in IMAGE_SUFFIXES:
        img = _read_image_file(path)
        return [img] if img is not None else []
    return []


def _build_json_schema(
    schema: Any,
    skip_fields: Optional[Iterable[str]] = None,
) -> Dict[str, Any]:
    """Translate a FileSet metadata schema into an OpenAI-compatible JSON schema.

    ``skip_fields`` omits the named fields from the output schema - used when
    the caller has already supplied a value for those fields and the LLM
    shouldn't bother re-extracting them.
    """
    skip: set = set(skip_fields) if skip_fields else set()
    properties: Dict[str, Any] = {}
    required: List[str] = []
    for field in _schema_fields(schema):
        if field.name in skip:
            continue
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


def _coerce_result(
    raw: Dict[str, Any],
    schema: Any,
    skip_fields: Optional[Iterable[str]] = None,
) -> Dict[str, Any]:
    skip: set = set(skip_fields) if skip_fields else set()
    out: Dict[str, Any] = {}
    for field in _schema_fields(schema):
        if field.name in skip:
            continue
        if field.name in raw:
            coerced = _coerce_value(raw[field.name], field.field_type)
            if coerced is not None:
                out[field.name] = coerced
    return out


def _describe_fields(
    schema: Any,
    skip_fields: Optional[Iterable[str]] = None,
) -> str:
    skip: set = set(skip_fields) if skip_fields else set()
    field_lines: List[str] = []
    for field in _schema_fields(schema):
        if field.name in skip:
            continue
        hint = field.extraction_hint if _is_set(getattr(field, "extraction_hint", None)) else ""
        desc = field.description if _is_set(getattr(field, "description", None)) else ""
        parts = [f"- {field.name} ({field.field_type.value})"]
        if desc:
            parts.append(f"description: {desc}")
        if hint:
            parts.append(f"hint: {hint}")
        field_lines.append("; ".join(parts))
    return "\n".join(field_lines) if field_lines else "(no fields)"


def _build_prompt(
    text: str,
    schema: Any,
    filename: str,
    skip_fields: Optional[Iterable[str]] = None,
) -> str:
    return (
        f"Extract metadata for the file named '{filename}'.\n\n"
        f"Fields to extract:\n{_describe_fields(schema, skip_fields)}\n\n"
        "If a value is not present in the document, return null for that field. "
        "Return a JSON object matching the provided schema.\n\n"
        "Document contents:\n"
        f"---\n{text}\n---"
    )


def _build_vision_prompt(
    schema: Any,
    filename: str,
    n_images: int,
    skip_fields: Optional[Iterable[str]] = None,
) -> str:
    unit = "page" if n_images == 1 else "pages"
    return (
        f"Extract metadata for the file named '{filename}'.\n\n"
        f"You are shown {n_images} {unit} of the document as image(s).\n\n"
        f"Fields to extract:\n{_describe_fields(schema, skip_fields)}\n\n"
        "If a value is not visible in the provided page(s), return null for that field. "
        "Return a JSON object matching the provided schema."
    )


def _build_messages_text(
    text: str,
    schema: Any,
    filename: str,
    skip_fields: Optional[Iterable[str]] = None,
) -> List[Dict[str, Any]]:
    return [
        {
            "role": "system",
            "content": (
                "You extract structured metadata from documents. "
                "Respond with a single JSON object matching the schema."
            ),
        },
        {"role": "user", "content": _build_prompt(text, schema, filename, skip_fields)},
    ]


def _build_messages_vision(
    images: List[Tuple[bytes, str]],
    schema: Any,
    filename: str,
    skip_fields: Optional[Iterable[str]] = None,
) -> List[Dict[str, Any]]:
    parts: List[Dict[str, Any]] = [
        {
            "type": "text",
            "text": _build_vision_prompt(schema, filename, len(images), skip_fields),
        },
    ]
    for image_bytes, mime in images:
        b64 = base64.b64encode(image_bytes).decode("ascii")
        parts.append({
            "type": "image_url",
            "image_url": {"url": f"data:{mime};base64,{b64}"},
        })
    return [
        {
            "role": "system",
            "content": (
                "You extract structured metadata from document images. "
                "Respond with a single JSON object matching the schema."
            ),
        },
        {"role": "user", "content": parts},
    ]


def _extract_one(
    client: Any,
    path: Path,
    schema: Any,
    model: str,
    max_chars: int,
    max_pages: Optional[int],
    use_vision: bool,
    skip_fields: Optional[Iterable[str]] = None,
) -> Optional[Dict[str, Any]]:
    json_schema = _build_json_schema(schema, skip_fields=skip_fields)
    # If every schema field was supplied by the caller, there's nothing to
    # ask the model about.
    if not json_schema.get("properties"):
        return None

    if use_vision and path.suffix.lower() in IMAGE_SUFFIXES:
        images = _images_for_vision(path, max_pages)
        if not images:
            return None
        messages = _build_messages_vision(images, schema, path.name, skip_fields)
    elif use_vision and path.suffix.lower() in PDF_SUFFIXES:
        images = _images_for_vision(path, max_pages)
        if not images:
            return None
        messages = _build_messages_vision(images, schema, path.name, skip_fields)
    else:
        text = _read_file_for_extraction(path, max_chars, max_pages)
        if text is None:
            return None
        messages = _build_messages_text(text, schema, path.name, skip_fields)

    response = client.chat.completions.create(
        model=model,
        messages=messages,
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
    return _coerce_result(parsed, schema, skip_fields)


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
    use_vision: bool = False,
    existing_metadata: Optional[Dict[str, Dict[str, Any]]] = None,
    openai_client: Any = None,
) -> Dict[str, Dict[str, Any]]:
    """Extract per-file metadata from a list of files using an LLM.

    Supports plain-text files (``.txt``, ``.md``, ``.csv``, ``.json``,
    ``.html``, ``.htm``, ``.xml``, ``.yaml``, ``.yml``, ``.log``) and PDFs.
    With ``use_vision=True``, PDFs are rendered to images and sent to a
    vision model (useful for scanned docs, complex layouts, or when the
    metadata lives in charts/figures), and image files
    (``.png``, ``.jpg``, ``.jpeg``, ``.webp``, ``.gif``) become supported
    inputs.

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
        model: Model id to call. Defaults to ``gpt-4.1-mini`` (supports vision).
        max_chars: Max characters of file text to include in the prompt.
            Ignored in vision mode.
        max_pages: For PDFs, only read/render the first N pages. Ignored for
            plain-text and (non-PDF) image files. Useful when the metadata
            lives on e.g. a cover page and later pages would waste context.
        max_workers: Parallelism for per-file LLM calls.
        use_vision: If True, send PDFs (as rendered page images) and image
            files to a vision model instead of extracting text. Requires
            ``pypdfium2`` and ``pillow`` (for PDFs); installed by the
            ``extract`` extra.
        existing_metadata: Optional mapping of ``filename -> {field: value}``
            for fields the caller has already supplied. For each file, those
            fields are omitted from the model's schema and prompt, so the
            LLM only fills in the gaps. If every schema field is already
            supplied for a file, the LLM isn't called for that file at all.
        openai_client: Optional pre-configured client (primarily for testing).
            If provided, ``api_key``/``base_url`` are ignored.

    Returns:
        Mapping of ``filename`` -> extracted metadata dict. Files that failed
        extraction or whose type is not supported are omitted. Only the
        fields the LLM was asked about appear in each entry; any
        ``existing_metadata`` values are not echoed back.
    """
    _validate_extraction_options(max_chars, max_pages, max_workers)

    if not _schema_fields(schema):
        raise ValueError("Cannot extract metadata: schema has no fields.")

    paths = [Path(p) for p in file_paths]
    if not paths:
        return {}
    supported_paths = [path for path in paths if _is_supported_path(path, use_vision=use_vision)]
    if not supported_paths:
        return {}
    _validate_unique_metadata_keys(supported_paths)

    has_pdf = any(p.suffix.lower() in PDF_SUFFIXES for p in supported_paths)

    # Only require pypdf when PDFs will go through the text path.
    if has_pdf and not use_vision:
        try:
            import pypdf  # noqa: F401
        except ImportError:
            raise ImportError(
                "pypdf is required to extract text from PDF files. "
                "Install with: pip install 'lightningrod-ai[extract]' or pip install pypdf. "
                "Alternatively, pass use_vision=True to send PDFs to a vision model."
            )

    # Vision path needs pypdfium2+Pillow for PDFs; image files don't need any lib.
    if use_vision and has_pdf:
        try:
            import pypdfium2  # noqa: F401
        except ImportError:
            raise ImportError(
                "pypdfium2 is required to render PDFs for vision extraction. "
                "Install with: pip install 'lightningrod-ai[extract]' or pip install pypdfium2"
            )
        try:
            import PIL  # noqa: F401
        except ImportError:
            raise ImportError(
                "Pillow is required to render PDFs for vision extraction. "
                "Install with: pip install 'lightningrod-ai[extract]' or pip install pillow"
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

    schema_field_names = {f.name for f in _schema_fields(schema)}
    existing = existing_metadata or {}

    results: Dict[str, Dict[str, Any]] = {}

    def _task(path: Path) -> Optional[Dict[str, Any]]:
        provided = existing.get(_metadata_key(path), {})
        # Only count keys the caller actually filled in (a None means "I don't
        # know" so let the model take a shot).
        skip_fields = {
            name for name, value in provided.items()
            if name in schema_field_names and value is not None
        }
        return _extract_one(
            openai_client, path, schema,
            model, max_chars, max_pages, use_vision,
            skip_fields=skip_fields if skip_fields else None,
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
