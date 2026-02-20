from __future__ import annotations

import csv
import glob
import re
from pathlib import Path
from typing import Any

from lightningrod._generated.models import Label, Sample, SampleMeta, Seed

_DEFAULT_CSV_TEXT_COLUMNS = ("text", "seed_text", "content")
_DEFAULT_CSV_LABEL_COLUMN = "label"

_SUPPORTED_FILE_TYPES = {"txt", "text", "md", "markdown", "pdf", "csv"}


def _sanitize_text(text: str) -> str:
    """
    Remove characters that are problematic for database storage.
    
    PostgreSQL cannot store null bytes (\\u0000) in text fields.
    This function removes such characters while preserving valid Unicode.
    """
    text = text.replace("\x00", "")
    text = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", "", text)
    return text


def _read_text_file(path: Path) -> str:
    """Read a plain text file."""
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def _read_markdown_file(path: Path) -> str:
    """Read a markdown file (treated as plain text)."""
    return _read_text_file(path)


def _read_pdf_file(path: Path) -> str:
    """Read a PDF file and extract text."""
    try:
        import PyPDF2
    except ImportError:
        raise ImportError(
            "PDF support requires either PyPDF2. "
            "Install with: pip install PyPDF2"
        )
    else:
        text_parts: list[str] = []
        with open(path, "rb") as f:
            pdf_reader = PyPDF2.PdfReader(f)
            for page in pdf_reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text_parts.append(_sanitize_text(page_text))
        return "\n\n".join(text_parts)


def _read_csv_rows(path: Path) -> list[dict[str, str]]:
    """Read a CSV file and return rows as list of dicts."""
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)


def _read_csv_file(path: Path) -> str:
    """Read a CSV file and convert to text format."""
    rows = _read_csv_rows(path)
    if not rows:
        return ""

    fieldnames = list(rows[0].keys())
    text_parts: list[str] = [f"CSV File: {path.name}", f"Columns: {', '.join(fieldnames)}", ""]

    for idx, row in enumerate(rows, 1):
        text_parts.append(f"Row {idx}:")
        for field in fieldnames:
            value = row.get(field, "")
            if value:
                text_parts.append(f"  {field}: {value}")
        text_parts.append("")

    return "\n".join(text_parts)


def _csv_rows_to_samples(
    path: Path,
    rows: list[dict[str, str]],
    text_column: str,
    label_column: str | None,
    metadata: dict[str, Any],
) -> list[Sample]:
    samples: list[Sample] = []
    for idx, row in enumerate(rows):
        text_val = row.get(text_column, "")
        if not text_val or not str(text_val).strip():
            continue
        seed_text = _sanitize_text(str(text_val).strip())

        label_obj = None
        if label_column and label_column in row:
            label_val = row.get(label_column, "")
            if label_val is not None and str(label_val).strip():
                label_obj = Label(label=str(label_val).strip(), label_confidence=1.0)

        meta_dict = {**metadata, "row_index": idx, "file_name": path.name, "file_type": "csv"}
        sample_meta = SampleMeta.from_dict(meta_dict)
        sample = Sample(seed=Seed(seed_text=seed_text), label=label_obj, meta=sample_meta)
        samples.append(sample)
    return samples


def _read_file_content(path: Path, file_type: str) -> str:
    """Read file content based on file extension."""
    
    if file_type not in _SUPPORTED_FILE_TYPES:
        supported_str = ", ".join(sorted(_SUPPORTED_FILE_TYPES))
        raise ValueError(
            f"Unsupported file type: {file_type}. "
            f"Supported file types: {supported_str}"
        )
    
    if file_type in {"txt", "text"}:
        return _read_text_file(path)
    elif file_type in {"md", "markdown"}:
        return _read_markdown_file(path)
    elif file_type == "pdf":
        return _read_pdf_file(path)
    elif file_type == "csv":
        return _read_csv_file(path)
    else:
        raise ValueError(f"Unsupported file type: {file_type}")


def chunk_text(
    text: str,
    chunk_size: int = 1000,
    chunk_overlap: int = 100,
    separators: list[str] | None = None,
) -> list[str]:
    """
    Split text into chunks using RecursiveCharacterTextSplitter.

    Args:
        text: The text to split
        chunk_size: Maximum size of each chunk
        chunk_overlap: Number of characters to overlap between chunks
        separators: List of separators to try in order. Defaults to ["\\n\\n", "\\n", ". ", " ", ""]

    Returns:
        List of text chunks

    Raises:
        ImportError: If langchain-text-splitters is not installed
    """
    if separators is None:
        separators = ["\n\n", "\n", ". ", " ", ""]
    try:
        from langchain_text_splitters import RecursiveCharacterTextSplitter
    except ImportError:
        raise ImportError(
            "langchain-text-splitters is required for text splitting. "
            "Install it with: pip install langchain-text-splitters"
        )

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        separators=separators,
    )

    return text_splitter.split_text(text)


def chunks_to_samples(
    chunks: list[str],
    metadata: dict[str, Any] | None = None,
) -> list[Sample]:
    """
    Convert a list of text chunks into Sample objects.

    Args:
        chunks: List of text chunks to convert
        metadata: Additional metadata to include in SampleMeta (optional)

    Returns:
        List of Sample objects
    """
    samples: list[Sample] = []
    total_chunks = len(chunks)

    for idx, chunk_text in enumerate(chunks):
        seed = Seed(seed_text=chunk_text)

        meta_dict: dict[str, Any] = {}
        meta_dict["chunk_index"] = idx
        meta_dict["total_chunks"] = total_chunks

        if metadata:
            meta_dict.update(metadata)

        sample_meta = SampleMeta.from_dict(meta_dict)
        sample = Sample(seed=seed, meta=sample_meta)
        samples.append(sample)

    return samples


def file_to_samples(
    file_path: str | Path,
    metadata: dict[str, Any] = {},
    chunk_size: int = 1000,
    chunk_overlap: int = 100,
    *,
    csv_text_column: str | None = None,
    csv_label_column: str | None = None,
) -> list[Sample]:
    """
    Read a file, split it into chunks, and convert to Sample objects.

    Supported file types: .txt, .text, .md, .markdown, .pdf, .csv

    For CSV files: creates one sample per row (no chunking). Uses standard column
    names (text/seed_text/content for seed, label for label) unless overridden.

    Args:
        file_path: Path to the file to read
        metadata: Additional metadata to include in SampleMeta (optional)
        chunk_size: Maximum size of each chunk (ignored for CSV)
        chunk_overlap: Number of characters to overlap between chunks (ignored for CSV)
        csv_text_column: CSV column for seed text. Default: first of text, seed_text, content
        csv_label_column: CSV column for label. Default: label

    Returns:
        List of Sample objects

    Raises:
        FileNotFoundError: If the file doesn't exist
        ValueError: If the file type is not supported
        ImportError: If required dependencies (langchain-text-splitters, PyPDF2) are not installed
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    inferred_file_type = path.suffix.lower().lstrip(".")
    meta = dict(metadata)

    if inferred_file_type == "csv":
        rows = _read_csv_rows(path)
        if not rows:
            return []
        columns = list(rows[0].keys())
        text_col = csv_text_column
        if text_col is None:
            for c in _DEFAULT_CSV_TEXT_COLUMNS:
                if c in columns:
                    text_col = c
                    break
        if text_col is None:
            raise ValueError(
                f"CSV has no text column. Expected one of {list(_DEFAULT_CSV_TEXT_COLUMNS)}, "
                f"or pass csv_text_column."
            )
        label_col = csv_label_column if csv_label_column is not None else (
            _DEFAULT_CSV_LABEL_COLUMN if _DEFAULT_CSV_LABEL_COLUMN in columns else None
        )
        return _csv_rows_to_samples(path, rows, text_col, label_col, meta)

    text = _read_file_content(path, file_type=inferred_file_type)
    chunks = chunk_text(text, chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    meta.update({"file_name": path.name, "file_type": inferred_file_type})
    return chunks_to_samples(chunks, metadata=meta)


def files_to_samples(
    pattern: str,
    metadata: dict[str, Any] | None = None,
    chunk_size: int = 1000,
    chunk_overlap: int = 100,
    *,
    csv_text_column: str | None = None,
    csv_label_column: str | None = None,
) -> list[Sample]:
    """
    Process multiple files matching a glob pattern and convert to Sample objects.

    Supported file types: .txt, .text, .md, .markdown, .pdf, .csv

    Args:
        pattern: Glob pattern to match files (e.g., "data/*.txt", "reports/**/*.pdf")
        metadata: Additional metadata to include in SampleMeta (optional)
        chunk_size: Maximum size of each chunk
        chunk_overlap: Number of characters to overlap between chunks
        csv_text_column: CSV column for seed text (CSV files only)
        csv_label_column: CSV column for label (CSV files only)

    Returns:
        List of Sample objects from all matching files

    Raises:
        ValueError: If no files match the pattern or if any file type is not supported
        ImportError: If required dependencies are not installed
    """
    if metadata is None:
        metadata = {}

    matched_files = sorted(glob.glob(pattern, recursive=True))
    if not matched_files:
        raise ValueError(f"No files found matching pattern: {pattern}")

    all_samples: list[Sample] = []
    for file_path_str in matched_files:
        file_path = Path(file_path_str)
        if not file_path.is_file():
            continue
        file_samples = file_to_samples(
            file_path,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            metadata=metadata,
            csv_text_column=csv_text_column,
            csv_label_column=csv_label_column,
        )
        all_samples.extend(file_samples)
    return all_samples
