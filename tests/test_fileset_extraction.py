from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional
from unittest.mock import MagicMock

import pytest

from lightningrod._generated.models.file_set_metadata_schema_input import (
    FileSetMetadataSchemaInput,
)
from lightningrod._generated.models.metadata_field_definition_input import (
    MetadataFieldDefinitionInput,
)
from lightningrod._generated.models.metadata_field_type import MetadataFieldType
from lightningrod.filesets.extraction import (
    _build_json_schema,
    _coerce_value,
    _read_text_for_extraction,
    extract_metadata_for_files,
)


def _schema() -> FileSetMetadataSchemaInput:
    return FileSetMetadataSchemaInput(
        fields=[
            MetadataFieldDefinitionInput(
                name="ticker",
                field_type=MetadataFieldType.STRING,
                required=True,
                description="Company ticker",
                extraction_hint="the stock ticker symbol mentioned",
            ),
            MetadataFieldDefinitionInput(
                name="year",
                field_type=MetadataFieldType.NUMBER,
                required=False,
                extraction_hint="fiscal year",
            ),
        ]
    )


def _make_openai_stub(responses_by_filename: Dict[str, Any]) -> MagicMock:
    """Build a fake OpenAI client. Each call inspects the user message to
    figure out which filename was sent, then returns the queued response
    (a dict to serialize as JSON, or an Exception to raise)."""
    client = MagicMock()

    def _create(*, model: str, messages: List[Dict[str, str]], response_format: Dict[str, Any]):
        user_content = messages[-1]["content"]
        for fn, payload in responses_by_filename.items():
            if f"file named '{fn}'" in user_content:
                if isinstance(payload, Exception):
                    raise payload
                completion = MagicMock()
                completion.choices = [MagicMock()]
                completion.choices[0].message.content = json.dumps(payload)
                return completion
        raise AssertionError(f"Unexpected call; no matching filename in: {user_content[:120]}")

    client.chat.completions.create.side_effect = _create
    return client


def test_build_json_schema_translates_fields() -> None:
    schema = _schema()
    js = _build_json_schema(schema)

    assert js["type"] == "object"
    assert js["additionalProperties"] is False
    assert js["required"] == ["ticker"]  # only required=True field listed

    props = js["properties"]
    assert props["ticker"]["type"] == "string"
    assert props["year"]["type"] == "number"
    assert "stock ticker symbol" in props["ticker"]["description"]
    assert "Company ticker" in props["ticker"]["description"]
    assert "fiscal year" in props["year"]["description"]


def test_coerce_value_handles_number_strings() -> None:
    assert _coerce_value("2024", MetadataFieldType.NUMBER) == 2024
    assert _coerce_value("3.14", MetadataFieldType.NUMBER) == pytest.approx(3.14)
    assert _coerce_value(2024, MetadataFieldType.NUMBER) == 2024
    assert _coerce_value("abc", MetadataFieldType.NUMBER) is None
    assert _coerce_value(42, MetadataFieldType.STRING) == "42"


def test_read_text_truncates_and_skips_unsupported(tmp_path: Path) -> None:
    txt = tmp_path / "doc.txt"
    txt.write_text("A" * 50_000, encoding="utf-8")
    out = _read_text_for_extraction(txt, max_chars=1_000)
    assert out is not None
    assert len(out) == 1_000

    pdf = tmp_path / "doc.pdf"
    pdf.write_bytes(b"%PDF-1.4 not a real pdf")
    assert _read_text_for_extraction(pdf, max_chars=1_000) is None


def test_read_text_handles_non_utf8_bytes(tmp_path: Path) -> None:
    f = tmp_path / "broken.txt"
    f.write_bytes(b"hello \xff\xfe world")
    out = _read_text_for_extraction(f, max_chars=1_000)
    assert out is not None
    assert "hello" in out
    assert "world" in out


def test_extract_metadata_for_files_returns_typed_dict(tmp_path: Path) -> None:
    a = tmp_path / "a.txt"
    b = tmp_path / "b.txt"
    a.write_text("Apple Q1 2024 report", encoding="utf-8")
    b.write_text("Microsoft FY 2023", encoding="utf-8")

    client = _make_openai_stub({
        "a.txt": {"ticker": "AAPL", "year": "2024"},
        "b.txt": {"ticker": "MSFT", "year": 2023},
    })

    result = extract_metadata_for_files(
        file_paths=[a, b],
        schema=_schema(),
        api_key="sk-test",
        base_url="https://api.example.com",
        openai_client=client,
    )

    assert result == {
        "a.txt": {"ticker": "AAPL", "year": 2024},
        "b.txt": {"ticker": "MSFT", "year": 2023},
    }


def test_extract_metadata_skips_unsupported_files(tmp_path: Path) -> None:
    txt = tmp_path / "good.txt"
    pdf = tmp_path / "skip.pdf"
    txt.write_text("some content", encoding="utf-8")
    pdf.write_bytes(b"%PDF-1.4")

    client = _make_openai_stub({
        "good.txt": {"ticker": "NVDA", "year": 2024},
    })

    result = extract_metadata_for_files(
        file_paths=[txt, pdf],
        schema=_schema(),
        api_key="sk-test",
        base_url="https://api.example.com",
        openai_client=client,
    )

    assert set(result.keys()) == {"good.txt"}
    # The PDF should never have triggered an LLM call.
    assert client.chat.completions.create.call_count == 1


def test_extract_metadata_isolates_per_file_failures(tmp_path: Path) -> None:
    a = tmp_path / "ok.txt"
    b = tmp_path / "broken.txt"
    a.write_text("ok file", encoding="utf-8")
    b.write_text("broken file", encoding="utf-8")

    client = _make_openai_stub({
        "ok.txt": {"ticker": "AAPL"},
        "broken.txt": RuntimeError("boom"),
    })

    result = extract_metadata_for_files(
        file_paths=[a, b],
        schema=_schema(),
        api_key="sk-test",
        base_url="https://api.example.com",
        openai_client=client,
    )

    assert result == {"ok.txt": {"ticker": "AAPL"}}


def test_extract_metadata_raises_for_empty_schema() -> None:
    empty = FileSetMetadataSchemaInput(fields=[])
    with pytest.raises(ValueError, match="no fields"):
        extract_metadata_for_files(
            file_paths=[],
            schema=empty,
            api_key="sk-test",
            base_url="https://api.example.com",
            openai_client=MagicMock(),
        )


def test_extract_metadata_drops_null_values(tmp_path: Path) -> None:
    f = tmp_path / "partial.txt"
    f.write_text("no ticker here", encoding="utf-8")

    client = _make_openai_stub({
        "partial.txt": {"ticker": None, "year": 2024},
    })

    result = extract_metadata_for_files(
        file_paths=[f],
        schema=_schema(),
        api_key="sk-test",
        base_url="https://api.example.com",
        openai_client=client,
    )

    assert result == {"partial.txt": {"year": 2024}}


# ---------------------------------------------------------------------------
# FileSetsClient integration: auto_extract_metadata flag merge + schema check.
# ---------------------------------------------------------------------------


@dataclass
class _FakeFileSet:
    metadata_schema: Optional[FileSetMetadataSchemaInput]


def _make_fileset_client(
    schema: Optional[FileSetMetadataSchemaInput],
    extracted: Dict[str, Dict[str, Any]],
    capture: Dict[str, Any],
):
    """Build a real FileSetsClient subclass so upload_files' auto-extract
    branch runs, with the network-touching bits overridden."""
    from lightningrod.filesets import client as client_mod

    class _TestClient(client_mod.FileSetsClient):
        def __init__(self) -> None:  # skip real auth client wiring
            self._client = None  # type: ignore[assignment]

        def get(self, file_set_id: str):  # type: ignore[override]
            return _FakeFileSet(metadata_schema=schema)

        def extract_metadata(  # type: ignore[override]
            self, file_set_id, file_paths, **kwargs
        ):
            return dict(extracted)

        def _upload_with_transfer_manager(  # type: ignore[override]
            self, file_set_id, paths, metadata, max_workers
        ):
            capture["metadata"] = metadata
            capture["paths"] = list(paths)
            return client_mod.UploadResult(succeeded=len(paths), failed=0, errors=[])

    return _TestClient()


def test_upload_files_auto_extract_merges_with_user_metadata(tmp_path: Path) -> None:
    a = tmp_path / "a.txt"
    b = tmp_path / "b.txt"
    a.write_text("content a", encoding="utf-8")
    b.write_text("content b", encoding="utf-8")

    captured: Dict[str, Any] = {}
    client = _make_fileset_client(
        schema=_schema(),
        extracted={
            "a.txt": {"ticker": "AAPL", "year": 2024},
            "b.txt": {"ticker": "MSFT", "year": 2023},
        },
        capture=captured,
    )

    result = client.upload_files(
        file_set_id="fs-1",
        file_paths=[a, b],
        metadata={"a.txt": {"ticker": "OVERRIDE"}},  # user wins on conflict
        auto_extract_metadata=True,
    )

    assert result.succeeded == 2
    assert captured["metadata"] == {
        "a.txt": {"ticker": "OVERRIDE", "year": 2024},
        "b.txt": {"ticker": "MSFT", "year": 2023},
    }


def test_upload_files_auto_extract_without_user_metadata(tmp_path: Path) -> None:
    f = tmp_path / "a.txt"
    f.write_text("content", encoding="utf-8")

    captured: Dict[str, Any] = {}
    client = _make_fileset_client(
        schema=_schema(),
        extracted={"a.txt": {"ticker": "AAPL"}},
        capture=captured,
    )

    client.upload_files(
        file_set_id="fs-1",
        file_paths=[f],
        auto_extract_metadata=True,
    )

    assert captured["metadata"] == {"a.txt": {"ticker": "AAPL"}}
