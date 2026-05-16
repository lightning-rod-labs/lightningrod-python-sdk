from __future__ import annotations

import base64
import hashlib
import json
import mimetypes
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

DEFAULT_VISUAL_DOCUMENT_MODEL = "gpt-4o"
DEFAULT_VISUAL_DOCUMENT_DPI = 180
DEFAULT_VISUAL_DOCUMENT_IMAGE_DETAIL = "high"
DEFAULT_VISUAL_DOCUMENT_MAX_OUTPUT_TOKENS = 4096

DEFAULT_VISUAL_DOCUMENT_PROMPT = """Create a concise executive source summary for this page.

Return source facts and business statements only. Do not generate questions.
Capture visible high-signal metrics, dates, units, actuals, budgets, forecasts, targets, variances, personnel updates, acquisition activity, operational updates, risks, and forward-looking statements.
Explain charts, graphs, and tables as trends, comparisons, approximate values, and business implications. Preserve important values without mechanically reproducing every dense table cell.
Clearly distinguish actual/current performance from budgets, forecasts, projections, goals, and management commentary.
Mark unclear or illegible items as unclear. Do not invent missing values.
"""

_SYSTEM_PROMPT = (
    "You convert image-heavy business documents into executive seed summaries "
    "for downstream forecasting dataset generation."
)
_IMAGE_SUFFIXES = {".gif", ".jpeg", ".jpg", ".png", ".webp"}
_SUPPORTED_SUFFIXES = {".pdf", *_IMAGE_SUFFIXES}
_METADATA_ORDER = ("file_date", "company_name", "doc_type")


@dataclass
class VisualDocumentPage:
    """Generated summary for one page of a visual document."""

    source_path: Path
    page_number: int
    total_pages: int
    text_path: Path
    text: str
    metadata: dict[str, Any]


@dataclass
class VisualDocumentConversionResult:
    """Result of converting a visual document into page-level text summaries."""

    source_path: Path
    output_dir: Path
    pages: list[VisualDocumentPage]
    metadata: dict[str, Any]

    @property
    def file_paths(self) -> list[Path]:
        return [page.text_path for page in self.pages]

    def upload_metadata(
        self,
        metadata: dict[str, Any] | None = None,
    ) -> dict[str, dict[str, Any]]:
        """Return ``filename -> metadata`` for uploading generated text files."""
        result: dict[str, dict[str, Any]] = {}
        for page in self.pages:
            page_metadata = dict(self.metadata)
            if metadata:
                page_metadata.update(metadata)
            page_metadata.update(page.metadata)
            result[page.text_path.name] = page_metadata
        return result


def convert_visual_document_to_text_pages(
    document_path: str | Path,
    *,
    openai_client: Any,
    output_dir: str | Path | None = None,
    model: str = DEFAULT_VISUAL_DOCUMENT_MODEL,
    pages: Iterable[int] | None = None,
    metadata: dict[str, Any] | None = None,
    overwrite: bool = False,
    show_progress: bool = False,
) -> VisualDocumentConversionResult:
    """Convert a PDF or page image into page-level executive seed summaries."""
    source_path = Path(document_path).expanduser().resolve()
    if not source_path.is_file():
        raise FileNotFoundError(f"File not found: {document_path}")
    if source_path.suffix.lower() not in _SUPPORTED_SUFFIXES:
        supported = ", ".join(sorted(_SUPPORTED_SUFFIXES))
        raise ValueError(f"Unsupported visual document type. Supported types: {supported}")

    output_stem = _safe_stem(source_path)
    target_dir = (
        Path(output_dir).expanduser().resolve()
        if output_dir is not None
        else source_path.parent / f"{output_stem}_visual_text_pages"
    )
    target_dir.mkdir(parents=True, exist_ok=True)

    converted_pages: list[VisualDocumentPage] = []
    for page_number, total_pages, image_bytes, mime_type in _page_images(
        source_path,
        pages=pages,
    ):
        text_path = target_dir / f"{output_stem}__page_{page_number:04d}.txt"
        page_metadata = _page_metadata(
            source_path=source_path,
            page_number=page_number,
            total_pages=total_pages,
            model=model,
        )

        if text_path.exists() and not overwrite:
            text = text_path.read_text(encoding="utf-8")
        else:
            if show_progress:
                print(f"Summarizing {source_path.name} page {page_number}/{total_pages}...")
            prompt = _page_prompt(
                source_path=source_path,
                page_number=page_number,
                total_pages=total_pages,
                metadata=metadata,
            )
            summary = _describe_image(
                openai_client=openai_client,
                image_bytes=image_bytes,
                mime_type=mime_type,
                model=model,
                prompt=prompt,
            )
            text = _format_page_text(
                summary,
                source_path=source_path,
                page_number=page_number,
                total_pages=total_pages,
                model=model,
            )
            text_path.write_text(text, encoding="utf-8")

        converted_pages.append(
            VisualDocumentPage(
                source_path=source_path,
                page_number=page_number,
                total_pages=total_pages,
                text_path=text_path,
                text=text,
                metadata=page_metadata,
            )
        )

    return VisualDocumentConversionResult(
        source_path=source_path,
        output_dir=target_dir,
        pages=converted_pages,
        metadata=dict(metadata or {}),
    )


def _page_images(
    source_path: Path,
    *,
    pages: Iterable[int] | None,
) -> list[tuple[int, int, bytes, str]]:
    if source_path.suffix.lower() == ".pdf":
        return _render_pdf_pages(source_path, pages=pages)

    selected_pages = _select_pages(total_pages=1, pages=pages)
    mime_type = mimetypes.guess_type(str(source_path))[0] or "image/png"
    image_bytes = source_path.read_bytes()
    return [(page_number, 1, image_bytes, mime_type) for page_number in selected_pages]


def _render_pdf_pages(
    source_path: Path,
    *,
    pages: Iterable[int] | None,
) -> list[tuple[int, int, bytes, str]]:
    try:
        import fitz
    except ImportError as exc:
        raise ImportError(
            "Visual PDF conversion requires PyMuPDF. "
            "Install with: pip install 'lightningrod-ai[visual]'."
        ) from exc

    rendered_pages: list[tuple[int, int, bytes, str]] = []
    with fitz.open(str(source_path)) as document:
        total_pages = document.page_count
        matrix = fitz.Matrix(DEFAULT_VISUAL_DOCUMENT_DPI / 72, DEFAULT_VISUAL_DOCUMENT_DPI / 72)
        for page_number in _select_pages(total_pages=total_pages, pages=pages):
            page = document.load_page(page_number - 1)
            pixmap = page.get_pixmap(matrix=matrix, alpha=False)
            rendered_pages.append((page_number, total_pages, pixmap.tobytes("png"), "image/png"))
    return rendered_pages


def _select_pages(total_pages: int, pages: Iterable[int] | None) -> list[int]:
    if total_pages < 1:
        raise ValueError("Document has no pages")
    if pages is None:
        return list(range(1, total_pages + 1))

    selected_pages = list(dict.fromkeys(pages))
    if not selected_pages:
        raise ValueError("pages must include at least one page number")
    for page in selected_pages:
        if page < 1 or page > total_pages:
            raise ValueError(f"Page {page} is out of range for a {total_pages}-page document")
    return selected_pages


def _page_prompt(
    *,
    source_path: Path,
    page_number: int,
    total_pages: int,
    metadata: dict[str, Any] | None,
) -> str:
    parts = [
        f"Source document: {source_path.name}",
        f"Page number: {page_number}",
        f"Total pages: {total_pages}",
    ]
    if metadata:
        parts.extend(
            [
                "",
                "Canonical document metadata supplied by the caller:",
                _metadata_text(metadata),
                (
                    "Use these metadata values as canonical source context. "
                    "If file_date is provided, treat it as the document date and "
                    "do not infer dates from filenames or upload timestamps."
                ),
            ]
        )
    parts.extend(["", DEFAULT_VISUAL_DOCUMENT_PROMPT])
    return "\n".join(parts)


def _metadata_text(metadata: dict[str, Any]) -> str:
    ordered_keys = [
        key for key in _METADATA_ORDER if key in metadata
    ] + sorted(key for key in metadata if key not in _METADATA_ORDER)
    return "\n".join(
        f"- {key}: {_metadata_value_to_text(metadata[key])}" for key in ordered_keys
    )


def _metadata_value_to_text(value: Any) -> str:
    if hasattr(value, "isoformat"):
        return str(value.isoformat())
    if isinstance(value, (dict, list, tuple)):
        return json.dumps(value, sort_keys=True, default=str)
    return str(value)


def _describe_image(
    *,
    openai_client: Any,
    image_bytes: bytes,
    mime_type: str,
    model: str,
    prompt: str,
) -> str:
    responses = getattr(openai_client, "responses", None)
    if responses is not None and hasattr(responses, "create"):
        try:
            return _describe_image_with_responses(
                responses=responses,
                image_bytes=image_bytes,
                mime_type=mime_type,
                model=model,
                prompt=prompt,
            )
        except Exception:
            if not _has_chat_completions(openai_client):
                raise

    chat = getattr(openai_client, "chat", None)
    completions = getattr(chat, "completions", None)
    if completions is not None and hasattr(completions, "create"):
        return _describe_image_with_chat_completions(
            completions=completions,
            image_bytes=image_bytes,
            mime_type=mime_type,
            model=model,
            prompt=prompt,
        )

    raise TypeError(
        "openai_client must expose either client.responses.create(...) "
        "or client.chat.completions.create(...)."
    )


def _has_chat_completions(openai_client: Any) -> bool:
    chat = getattr(openai_client, "chat", None)
    completions = getattr(chat, "completions", None)
    return completions is not None and hasattr(completions, "create")


def _describe_image_with_responses(
    *,
    responses: Any,
    image_bytes: bytes,
    mime_type: str,
    model: str,
    prompt: str,
) -> str:
    response = responses.create(
        model=model,
        input=[
            {
                "role": "system",
                "content": [{"type": "input_text", "text": _SYSTEM_PROMPT}],
            },
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": prompt},
                    {
                        "type": "input_image",
                        "image_url": _image_data_url(image_bytes, mime_type),
                        "detail": DEFAULT_VISUAL_DOCUMENT_IMAGE_DETAIL,
                    },
                ],
            },
        ],
        max_output_tokens=DEFAULT_VISUAL_DOCUMENT_MAX_OUTPUT_TOKENS,
    )
    return _extract_response_text(response)


def _describe_image_with_chat_completions(
    *,
    completions: Any,
    image_bytes: bytes,
    mime_type: str,
    model: str,
    prompt: str,
) -> str:
    response = completions.create(
        model=model,
        messages=[
            {"role": "system", "content": _SYSTEM_PROMPT},
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": _image_data_url(image_bytes, mime_type),
                            "detail": DEFAULT_VISUAL_DOCUMENT_IMAGE_DETAIL,
                        },
                    },
                ],
            },
        ],
        max_tokens=DEFAULT_VISUAL_DOCUMENT_MAX_OUTPUT_TOKENS,
    )
    return _extract_response_text(response)


def _extract_response_text(response: Any) -> str:
    if isinstance(response, dict):
        if isinstance(response.get("output_text"), str):
            return response["output_text"].strip()
        choices = response.get("choices") or []
        if choices:
            return _content_to_text(choices[0].get("message", {}).get("content"))
        return _output_to_text(response.get("output", []))

    output_text = getattr(response, "output_text", None)
    if isinstance(output_text, str):
        return output_text.strip()

    choices = getattr(response, "choices", None) or []
    if choices:
        message = getattr(choices[0], "message", None)
        return _content_to_text(getattr(message, "content", ""))

    return _output_to_text(getattr(response, "output", []))


def _content_to_text(content: Any) -> str:
    if isinstance(content, str):
        return content.strip()
    if not isinstance(content, list):
        return ""
    parts: list[str] = []
    for item in content:
        text = item.get("text") if isinstance(item, dict) else getattr(item, "text", None)
        if isinstance(text, str):
            parts.append(text)
    return "\n".join(parts).strip()


def _output_to_text(output: Any) -> str:
    parts: list[str] = []
    for item in output or []:
        content = item.get("content") if isinstance(item, dict) else getattr(item, "content", [])
        text = _content_to_text(content)
        if text:
            parts.append(text)
    return "\n".join(parts).strip()


def _format_page_text(
    summary: str,
    *,
    source_path: Path,
    page_number: int,
    total_pages: int,
    model: str,
) -> str:
    header = [
        f"Source document: {source_path.name}",
        f"Source page: {page_number} of {total_pages}",
        f"Page number: {page_number}",
        f"Total pages: {total_pages}",
        f"Model: {model}",
        f"Render DPI: {DEFAULT_VISUAL_DOCUMENT_DPI}",
        f"Image detail: {DEFAULT_VISUAL_DOCUMENT_IMAGE_DETAIL}",
    ]
    return "\n".join(header) + f"\n\n{summary.strip()}\n"


def _page_metadata(
    *,
    source_path: Path,
    page_number: int,
    total_pages: int,
    model: str,
) -> dict[str, Any]:
    return {
        "source_file_name": source_path.name,
        "source_file_label": source_path.name,
        "source_file_type": source_path.suffix.lower().lstrip("."),
        "source_page_number": page_number,
        "source_total_pages": total_pages,
        "visual_seed_model": model,
        "visual_seed_dpi": DEFAULT_VISUAL_DOCUMENT_DPI,
        "visual_seed_image_detail": DEFAULT_VISUAL_DOCUMENT_IMAGE_DETAIL,
    }


def _safe_stem(path: Path) -> str:
    stem = re.sub(r"[^A-Za-z0-9._-]+", "_", path.stem).strip("._-")
    stem = stem or "visual_document"
    path_hash = hashlib.sha1(str(path).encode("utf-8")).hexdigest()[:8]
    return f"{stem}__{path_hash}"


def _image_data_url(image_bytes: bytes, mime_type: str) -> str:
    return f"data:{mime_type};base64,{base64.b64encode(image_bytes).decode('utf-8')}"
