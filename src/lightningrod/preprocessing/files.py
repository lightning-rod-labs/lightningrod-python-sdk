from __future__ import annotations

import csv
import glob
from pathlib import Path
from typing import Any

from lightningrod._generated.models import Sample, SampleMeta, Seed

_SUPPORTED_FILE_TYPES = {"txt", "text", "md", "markdown", "pdf", "csv"}


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
                    text_parts.append(page_text)
        return "\n\n".join(text_parts)


def _read_csv_file(path: Path) -> str:
    """Read a CSV file and convert to text format."""
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows: list[dict[str, str]] = list(reader)
    
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
) -> list[Sample]:
    """
    Read a file, split it into chunks, and convert to Sample objects.

    Supported file types: .txt, .text, .md, .markdown, .pdf, .csv

    Args:
        file_path: Path to the file to read
        metadata: Additional metadata to include in SampleMeta (optional)
        chunk_size: Maximum size of each chunk
        chunk_overlap: Number of characters to overlap between chunks

    Returns:
        List of Sample objects

    Raises:
        FileNotFoundError: If the file doesn't exist
        ValueError: If the file type is not supported
        ImportError: If required dependencies (langchain-text-splitters, PyPDF2/pdfplumber) are not installed
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    inferred_file_type = path.suffix.lower().lstrip(".")
    text = _read_file_content(path, file_type=inferred_file_type)

    chunks = chunk_text(text, chunk_size=chunk_size, chunk_overlap=chunk_overlap)

    metadata.update({"file_name": path.name, "file_type": inferred_file_type})
    return chunks_to_samples(
        chunks,
        metadata=metadata,
    )


def files_to_samples(
    pattern: str,
    metadata: dict[str, Any] | None = None,
    chunk_size: int = 1000,
    chunk_overlap: int = 100,
) -> list[Sample]:
    """
    Process multiple files matching a glob pattern and convert to Sample objects.

    Supported file types: .txt, .text, .md, .markdown, .pdf, .csv

    Args:
        pattern: Glob pattern to match files (e.g., "data/*.txt", "reports/**/*.pdf")
        metadata: Additional metadata to include in SampleMeta (optional)
        chunk_size: Maximum size of each chunk
        chunk_overlap: Number of characters to overlap between chunks

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
        )
        all_samples.extend(file_samples)
    
    return all_samples
