from __future__ import annotations

import json
import sys
import types
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
    _read_file_for_extraction,
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

    def _create(
        *,
        model: str,
        messages: List[Dict[str, str]],
        response_format: Dict[str, Any],
    ):
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
    assert props["ticker"]["type"] == ["string", "null"]
    assert props["year"]["type"] == ["number", "null"]
    assert "stock ticker symbol" in props["ticker"]["description"]
    assert "Company ticker" in props["ticker"]["description"]
    assert "fiscal year" in props["year"]["description"]


def test_coerce_value_handles_number_strings() -> None:
    assert _coerce_value("2024", MetadataFieldType.NUMBER) == 2024
    assert _coerce_value("3.14", MetadataFieldType.NUMBER) == pytest.approx(3.14)
    assert _coerce_value(2024, MetadataFieldType.NUMBER) == 2024
    assert _coerce_value(True, MetadataFieldType.NUMBER) is None
    assert _coerce_value("abc", MetadataFieldType.NUMBER) is None
    assert _coerce_value(42, MetadataFieldType.STRING) == "42"


def test_read_text_truncates_and_skips_non_text(tmp_path: Path) -> None:
    txt = tmp_path / "doc.txt"
    txt.write_text("A" * 50_000, encoding="utf-8")
    out = _read_text_for_extraction(txt, max_chars=1_000)
    assert out is not None
    assert len(out) == 1_000

    # The plain-text reader itself does not handle PDFs; dispatch handles those.
    pdf = tmp_path / "doc.pdf"
    pdf.write_bytes(b"%PDF-1.4 not a real pdf")
    assert _read_text_for_extraction(pdf, max_chars=1_000) is None


def test_read_file_dispatcher_skips_unknown_types(tmp_path: Path) -> None:
    unknown = tmp_path / "mystery.xyz"
    unknown.write_text("whatever", encoding="utf-8")
    assert _read_file_for_extraction(unknown, max_chars=1_000, max_pages=None) is None


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


def test_extract_metadata_accepts_injected_client_without_auth_details(tmp_path: Path) -> None:
    f = tmp_path / "a.txt"
    f.write_text("Apple Q1 2024 report", encoding="utf-8")

    client = _make_openai_stub({"a.txt": {"ticker": "AAPL", "year": "2024"}})

    result = extract_metadata_for_files(
        file_paths=[f],
        schema=_schema(),
        openai_client=client,
    )

    assert result == {"a.txt": {"ticker": "AAPL", "year": 2024}}


def test_extract_metadata_skips_unsupported_files(tmp_path: Path) -> None:
    txt = tmp_path / "good.txt"
    unknown = tmp_path / "skip.xyz"
    txt.write_text("some content", encoding="utf-8")
    unknown.write_text("opaque", encoding="utf-8")

    client = _make_openai_stub({
        "good.txt": {"ticker": "NVDA", "year": 2024},
    })

    result = extract_metadata_for_files(
        file_paths=[txt, unknown],
        schema=_schema(),
        api_key="sk-test",
        base_url="https://api.example.com",
        openai_client=client,
    )

    assert set(result.keys()) == {"good.txt"}
    # The unknown file should never have triggered an LLM call.
    assert client.chat.completions.create.call_count == 1


def test_extract_metadata_skips_unsupported_files_without_client(tmp_path: Path) -> None:
    unknown = tmp_path / "skip.xyz"
    unknown.write_text("opaque", encoding="utf-8")

    result = extract_metadata_for_files(
        file_paths=[unknown],
        schema=_schema(),
    )

    assert result == {}


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


def test_extract_metadata_validates_options(tmp_path: Path) -> None:
    f = tmp_path / "a.txt"
    f.write_text("content", encoding="utf-8")

    with pytest.raises(ValueError, match="max_chars"):
        extract_metadata_for_files(
            file_paths=[f],
            schema=_schema(),
            max_chars=0,
            openai_client=MagicMock(),
        )

    with pytest.raises(ValueError, match="max_pages"):
        extract_metadata_for_files(
            file_paths=[f],
            schema=_schema(),
            max_pages=0,
            openai_client=MagicMock(),
        )

    with pytest.raises(ValueError, match="max_workers"):
        extract_metadata_for_files(
            file_paths=[f],
            schema=_schema(),
            max_workers=0,
            openai_client=MagicMock(),
        )


def test_extract_metadata_rejects_duplicate_filenames(tmp_path: Path) -> None:
    one = tmp_path / "one"
    two = tmp_path / "two"
    one.mkdir()
    two.mkdir()
    a = one / "report.txt"
    b = two / "report.txt"
    a.write_text("content a", encoding="utf-8")
    b.write_text("content b", encoding="utf-8")

    with pytest.raises(ValueError, match="duplicate names"):
        extract_metadata_for_files(
            file_paths=[a, b],
            schema=_schema(),
            openai_client=MagicMock(),
        )


def _install_fake_pypdf(
    monkeypatch: pytest.MonkeyPatch,
    pages_by_path: Dict[str, List[str]],
) -> None:
    """Inject a minimal fake ``pypdf`` module into sys.modules.

    ``pages_by_path`` maps the absolute path string of each PDF to the list
    of page texts the fake PdfReader should return.
    """

    class _FakePage:
        def __init__(self, text: str) -> None:
            self._text = text

        def extract_text(self) -> str:
            return self._text

    class _FakeReader:
        def __init__(self, path: str) -> None:
            if path not in pages_by_path:
                raise FileNotFoundError(path)
            self.pages = [_FakePage(t) for t in pages_by_path[path]]

    module = types.ModuleType("pypdf")
    module.PdfReader = _FakeReader  # type: ignore[attr-defined]
    monkeypatch.setitem(sys.modules, "pypdf", module)


def test_extract_metadata_reads_pdf(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    pdf = tmp_path / "report.pdf"
    pdf.write_bytes(b"%PDF-stub")
    _install_fake_pypdf(
        monkeypatch,
        {str(pdf): ["Cover: AAPL FY2024", "Body text that's long"]},
    )

    captured_prompts: List[str] = []

    def _create(*, model, messages, response_format):
        captured_prompts.append(messages[-1]["content"])
        completion = MagicMock()
        completion.choices = [MagicMock()]
        completion.choices[0].message.content = json.dumps(
            {"ticker": "AAPL", "year": 2024}
        )
        return completion

    client = MagicMock()
    client.chat.completions.create.side_effect = _create

    result = extract_metadata_for_files(
        file_paths=[pdf],
        schema=_schema(),
        api_key="sk-test",
        base_url="https://api.example.com",
        openai_client=client,
    )

    assert result == {"report.pdf": {"ticker": "AAPL", "year": 2024}}
    # Both pages' text should have made it into the prompt by default.
    assert "Cover: AAPL FY2024" in captured_prompts[0]
    assert "Body text that's long" in captured_prompts[0]


def test_extract_metadata_respects_max_pages(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    pdf = tmp_path / "report.pdf"
    pdf.write_bytes(b"%PDF-stub")
    _install_fake_pypdf(
        monkeypatch,
        {
            str(pdf): [
                "FIRST PAGE ONLY",
                "SECRET FROM PAGE TWO",
                "MORE SECRETS FROM PAGE THREE",
            ]
        },
    )

    captured_prompts: List[str] = []

    def _create(*, model, messages, response_format):
        captured_prompts.append(messages[-1]["content"])
        completion = MagicMock()
        completion.choices = [MagicMock()]
        completion.choices[0].message.content = json.dumps({"ticker": "AAPL"})
        return completion

    client = MagicMock()
    client.chat.completions.create.side_effect = _create

    result = extract_metadata_for_files(
        file_paths=[pdf],
        schema=_schema(),
        api_key="sk-test",
        base_url="https://api.example.com",
        max_pages=1,
        openai_client=client,
    )

    assert "report.pdf" in result
    prompt = captured_prompts[0]
    assert "FIRST PAGE ONLY" in prompt
    assert "SECRET FROM PAGE TWO" not in prompt
    assert "MORE SECRETS FROM PAGE THREE" not in prompt


def test_extract_metadata_raises_when_pypdf_missing(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    pdf = tmp_path / "no_pypdf.pdf"
    pdf.write_bytes(b"%PDF-stub")

    # Simulate pypdf not being installed.
    monkeypatch.setitem(sys.modules, "pypdf", None)

    with pytest.raises(ImportError, match="pypdf is required"):
        extract_metadata_for_files(
            file_paths=[pdf],
            schema=_schema(),
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
            capture["extraction_kwargs"] = kwargs
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
    assert captured["extraction_kwargs"] == {
        "model": "gpt-4.1-mini",
        "max_chars": 20_000,
        "max_pages": None,
        "max_workers": 10,
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


def test_upload_files_auto_extract_passes_tuning_options(tmp_path: Path) -> None:
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
        extraction_model="gpt-test",
        extraction_max_chars=1234,
        extraction_max_pages=1,
        extraction_max_workers=2,
    )

    assert captured["extraction_kwargs"] == {
        "model": "gpt-test",
        "max_chars": 1234,
        "max_pages": 1,
        "max_workers": 2,
    }
