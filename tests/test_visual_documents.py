from __future__ import annotations

import inspect
import os
import subprocess
import sys
from types import SimpleNamespace
from typing import Any

import pytest

os.environ.setdefault("LIGHTNINGROD_API_KEY", "test-api-key")

from lightningrod.filesets.client import FileSetsClient, UploadResult
from lightningrod.preprocessing.visual_documents import (
    convert_visual_document_to_text_pages,
)


class FakeResponses:
    def __init__(self, output_text: str = "Revenue table and chart description.") -> None:
        self.output_text = output_text
        self.calls: list[dict[str, Any]] = []

    def create(self, **kwargs: Any) -> SimpleNamespace:
        self.calls.append(kwargs)
        return SimpleNamespace(output_text=self.output_text)


class FakeResponsesClient:
    def __init__(self, output_text: str = "Revenue table and chart description.") -> None:
        self.responses = FakeResponses(output_text)


class FailingResponses:
    def create(self, **kwargs: Any) -> None:
        raise RuntimeError("Responses API is not supported")


class FakeChatCompletions:
    def __init__(self, output_text: str = "Chat-completions vision description.") -> None:
        self.output_text = output_text
        self.calls: list[dict[str, Any]] = []

    def create(self, **kwargs: Any) -> SimpleNamespace:
        self.calls.append(kwargs)
        message = SimpleNamespace(content=self.output_text)
        return SimpleNamespace(choices=[SimpleNamespace(message=message)])


class FakeChatClient:
    def __init__(self, output_text: str = "Chat-completions vision description.") -> None:
        self.chat = SimpleNamespace(completions=FakeChatCompletions(output_text))


class DualClient:
    def __init__(self) -> None:
        self.responses = FailingResponses()
        self.chat = SimpleNamespace(completions=FakeChatCompletions("Fallback summary."))


class CapturingFileSetsClient(FileSetsClient):
    def __init__(self) -> None:
        pass

    def upload_files(
        self,
        file_set_id,
        file_paths,
        metadata=None,
        max_workers=10,
        use_transfer_manager=True,
        show_progress=False,
    ) -> UploadResult:
        self.captured_file_set_id = file_set_id
        self.captured_file_paths = file_paths
        self.captured_metadata = metadata
        return UploadResult(succeeded=len(file_paths), failed=0, errors=[])


def test_public_interface_is_small() -> None:
    parameters = set(inspect.signature(convert_visual_document_to_text_pages).parameters)

    assert parameters == {
        "document_path",
        "openai_client",
        "output_dir",
        "model",
        "pages",
        "metadata",
        "overwrite",
        "show_progress",
    }
    assert not hasattr(FileSetsClient, "upload_visual_document_pages")
    assert not hasattr(FileSetsClient, "upload_visual_document_directory")


def test_importing_preprocessing_does_not_require_lightningrod_api_key() -> None:
    env = os.environ.copy()
    env.pop("LIGHTNINGROD_API_KEY", None)
    env["PYTHONPATH"] = "src"

    result = subprocess.run(
        [
            sys.executable,
            "-c",
            "from lightningrod.preprocessing.visual_documents import convert_visual_document_to_text_pages; print(convert_visual_document_to_text_pages.__name__)",
        ],
        cwd=os.getcwd(),
        env=env,
        capture_output=True,
        text=True,
        timeout=5,
    )

    assert result.returncode == 0
    assert result.stdout.strip() == "convert_visual_document_to_text_pages"


def test_convert_image_to_page_text_uses_responses_api(tmp_path) -> None:
    source = tmp_path / "Board Deck.png"
    source.write_bytes(b"fake image bytes")
    openai_client = FakeResponsesClient()

    result = convert_visual_document_to_text_pages(
        source,
        openai_client=openai_client,
        output_dir=tmp_path / "out",
        model="gpt-test",
    )

    assert len(result.file_paths) == 1
    assert result.file_paths[0].name.startswith("Board_Deck__")
    assert result.file_paths[0].name.endswith("__page_0001.txt")
    text = result.file_paths[0].read_text(encoding="utf-8")
    assert "Source document: Board Deck.png" in text
    assert "Source page: 1 of 1" in text
    assert "Model: gpt-test" in text
    assert "Revenue table and chart description." in text

    request = openai_client.responses.calls[0]
    assert request["model"] == "gpt-test"
    prompt = request["input"][1]["content"][0]["text"]
    assert "executive source summary" in prompt
    assert "Do not generate questions." in prompt
    image_part = request["input"][1]["content"][1]
    assert image_part["type"] == "input_image"
    assert image_part["image_url"].startswith("data:image/png;base64,")
    assert image_part["detail"] == "high"


def test_metadata_is_added_to_prompt_and_upload_metadata(tmp_path) -> None:
    source = tmp_path / "ExampleCo_upload_2025-05-15.png"
    source.write_bytes(b"fake image bytes")
    openai_client = FakeResponsesClient()

    result = convert_visual_document_to_text_pages(
        source,
        openai_client=openai_client,
        output_dir=tmp_path / "out",
        metadata={
            "file_date": "2025-03-31",
            "company_name": "ExampleCo",
            "doc_type": "board_deck",
        },
    )

    prompt = openai_client.responses.calls[0]["input"][1]["content"][0]["text"]
    assert "- file_date: 2025-03-31" in prompt
    assert "- company_name: ExampleCo" in prompt
    assert "do not infer dates from filenames" in prompt

    metadata = next(iter(result.upload_metadata().values()))
    assert metadata["file_date"] == "2025-03-31"
    assert metadata["company_name"] == "ExampleCo"
    assert metadata["source_file_name"] == "ExampleCo_upload_2025-05-15.png"
    assert "source_file_path" not in metadata
    assert metadata["source_page_number"] == 1
    assert metadata["visual_seed_dpi"] == 180


def test_existing_output_is_reused_unless_overwrite_is_true(tmp_path) -> None:
    source = tmp_path / "Board Deck.png"
    source.write_bytes(b"fake image bytes")
    output_dir = tmp_path / "out"

    first = convert_visual_document_to_text_pages(
        source,
        openai_client=FakeResponsesClient("First summary."),
        output_dir=output_dir,
    )
    second_client = FakeResponsesClient("Second summary should not be called.")
    second = convert_visual_document_to_text_pages(
        source,
        openai_client=second_client,
        output_dir=output_dir,
    )
    third = convert_visual_document_to_text_pages(
        source,
        openai_client=FakeResponsesClient("Third summary."),
        output_dir=output_dir,
        overwrite=True,
    )

    assert second.pages[0].text == first.pages[0].text
    assert second_client.responses.calls == []
    assert "Third summary." in third.pages[0].text


def test_generated_filenames_include_hash_to_avoid_duplicate_basenames(tmp_path) -> None:
    first = tmp_path / "a" / "Investment Memo.png"
    second = tmp_path / "b" / "Investment Memo.png"
    first.parent.mkdir()
    second.parent.mkdir()
    first.write_bytes(b"first fake image bytes")
    second.write_bytes(b"second fake image bytes")
    output_dir = tmp_path / "out"

    first_result = convert_visual_document_to_text_pages(
        first,
        openai_client=FakeResponsesClient(),
        output_dir=output_dir,
    )
    second_result = convert_visual_document_to_text_pages(
        second,
        openai_client=FakeResponsesClient(),
        output_dir=output_dir,
    )

    first_name = first_result.file_paths[0].name
    second_name = second_result.file_paths[0].name
    assert first_name != second_name
    assert first_name.startswith("Investment_Memo__")
    assert second_name.startswith("Investment_Memo__")
    assert first_name.endswith("__page_0001.txt")
    assert second_name.endswith("__page_0001.txt")


def test_chat_completions_is_used_when_responses_is_unavailable(tmp_path) -> None:
    source = tmp_path / "Board Deck.jpg"
    source.write_bytes(b"fake image bytes")
    openai_client = FakeChatClient()

    result = convert_visual_document_to_text_pages(
        source,
        openai_client=openai_client,
        output_dir=tmp_path / "out",
    )

    assert "Chat-completions vision description." in result.pages[0].text
    request = openai_client.chat.completions.calls[0]
    assert request["messages"][1]["content"][1]["image_url"]["url"].startswith(
        "data:image/jpeg;base64,"
    )


def test_responses_failure_falls_back_to_chat_completions(tmp_path) -> None:
    source = tmp_path / "Board Deck.png"
    source.write_bytes(b"fake image bytes")

    result = convert_visual_document_to_text_pages(
        source,
        openai_client=DualClient(),
        output_dir=tmp_path / "out",
    )

    assert "Fallback summary." in result.pages[0].text


def test_conversion_result_uploads_with_existing_fileset_upload(tmp_path) -> None:
    source = tmp_path / "Board Deck.png"
    source.write_bytes(b"fake image bytes")
    conversion = convert_visual_document_to_text_pages(
        source,
        openai_client=FakeResponsesClient(),
        output_dir=tmp_path / "out",
        metadata={"file_date": "2025-03-31"},
    )
    client = CapturingFileSetsClient()

    upload = client.upload_files(
        "fs-123",
        conversion.file_paths,
        metadata=conversion.upload_metadata(),
        use_transfer_manager=False,
    )

    assert upload.succeeded == 1
    assert client.captured_file_set_id == "fs-123"
    assert client.captured_file_paths == conversion.file_paths
    metadata = next(iter(client.captured_metadata.values()))
    assert metadata["file_date"] == "2025-03-31"


def test_convert_pdf_renders_one_page_summary_with_source_metadata(tmp_path) -> None:
    fitz = pytest.importorskip("fitz")
    source = tmp_path / "Tiny Deck.pdf"
    document = fitz.open()
    page = document.new_page(width=240, height=160)
    page.insert_text((24, 80), "Revenue up 20% vs budget")
    document.save(str(source))
    document.close()

    result = convert_visual_document_to_text_pages(
        source,
        openai_client=FakeResponsesClient("PDF page summary."),
        output_dir=tmp_path / "out",
        model="gpt-test",
    )

    assert len(result.file_paths) == 1
    assert result.file_paths[0].name.startswith("Tiny_Deck__")
    assert result.file_paths[0].name.endswith("__page_0001.txt")
    assert "PDF page summary." in result.pages[0].text
    metadata = next(iter(result.upload_metadata().values()))
    assert metadata["source_file_type"] == "pdf"
    assert metadata["source_page_number"] == 1
