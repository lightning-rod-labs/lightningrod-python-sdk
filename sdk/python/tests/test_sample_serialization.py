"""Tests for Sample serialization and deserialization in the SDK."""

from lightningrod._generated.models.forward_looking_question import ForwardLookingQuestion
from lightningrod._generated.models.label import Label
from lightningrod._generated.models.news_context import NewsContext
from lightningrod._generated.models.question import Question
from lightningrod._generated.models.rag_context import RAGContext
from lightningrod._generated.models.sample import Sample
from lightningrod._generated.models.seed import Seed
from lightningrod._generated.types import UNSET


class TestQuestionDiscrimination:
    """Test that Question types are properly discriminated."""

    def test_basic_question_from_dict(self) -> None:
        data = {
            "question_type": "QUESTION",
            "question_text": "Will it rain?"
        }
        question = Question.from_dict(data)
        assert question.question_text == "Will it rain?"
        assert question.question_type == "QUESTION"

    def test_forward_looking_question_from_dict(self) -> None:
        data = {
            "question_type": "FORWARD_LOOKING_QUESTION",
            "question_text": "Will it rain tomorrow?",
            "date_close": "2024-12-25T00:00:00",
            "event_date": "2024-12-24T00:00:00",
            "resolution_criteria": "Check weather reports"
        }
        question = ForwardLookingQuestion.from_dict(data)
        assert question.question_text == "Will it rain tomorrow?"
        assert question.question_type == "FORWARD_LOOKING_QUESTION"
        assert question.resolution_criteria == "Check weather reports"

    def test_question_rejects_wrong_type(self) -> None:
        data = {
            "question_type": "FORWARD_LOOKING_QUESTION",
            "question_text": "Will it rain?"
        }
        try:
            Question.from_dict(data)
            assert False, "Should have raised ValueError"
        except (ValueError, KeyError):
            pass

    def test_forward_looking_question_rejects_wrong_type(self) -> None:
        data = {
            "question_type": "QUESTION",
            "question_text": "Will it rain?",
            "date_close": "2024-12-25T00:00:00",
            "event_date": "2024-12-24T00:00:00",
            "resolution_criteria": "Check weather"
        }
        try:
            ForwardLookingQuestion.from_dict(data)
            assert False, "Should have raised ValueError"
        except ValueError:
            pass


class TestContextDiscrimination:
    """Test that Context types are properly discriminated."""

    def test_news_context_from_dict(self) -> None:
        data = {
            "context_type": "NEWS_CONTEXT",
            "rendered_context": "Article about AI",
            "search_query": "artificial intelligence news"
        }
        context = NewsContext.from_dict(data)
        assert context.rendered_context == "Article about AI"
        assert context.search_query == "artificial intelligence news"

    def test_rag_context_from_dict(self) -> None:
        data = {
            "context_type": "RAG_CONTEXT",
            "rendered_context": "Retrieved document",
            "document_id": "doc-123"
        }
        context = RAGContext.from_dict(data)
        assert context.rendered_context == "Retrieved document"
        assert context.document_id == "doc-123"


class TestSampleDeserialization:
    """Test Sample deserialization from dict."""

    def test_sample_with_seed(self) -> None:
        data = {
            "seed": {
                "seed_text": "Original article content",
                "url": "https://example.com"
            }
        }
        sample = Sample.from_dict(data)
        assert isinstance(sample.seed, Seed)
        assert sample.seed.seed_text == "Original article content"
        assert sample.seed.url == "https://example.com"

    def test_sample_with_basic_question(self) -> None:
        data = {
            "question": {
                "question_type": "QUESTION",
                "question_text": "Will this happen?"
            }
        }
        sample = Sample.from_dict(data)
        assert isinstance(sample.question, Question)
        assert sample.question.question_text == "Will this happen?"

    def test_sample_with_forward_looking_question(self) -> None:
        data = {
            "question": {
                "question_type": "FORWARD_LOOKING_QUESTION",
                "question_text": "Will this happen tomorrow?",
                "date_close": "2024-12-25T00:00:00",
                "event_date": "2024-12-24T00:00:00",
                "resolution_criteria": "Check news"
            }
        }
        sample = Sample.from_dict(data)
        assert isinstance(sample.question, ForwardLookingQuestion)
        assert sample.question.resolution_criteria == "Check news"

    def test_sample_with_news_context(self) -> None:
        data = {
            "context": [
                {
                    "context_type": "NEWS_CONTEXT",
                    "rendered_context": "News article",
                    "search_query": "breaking news"
                }
            ]
        }
        sample = Sample.from_dict(data)
        assert isinstance(sample.context, list)
        assert len(sample.context) == 1
        assert isinstance(sample.context[0], NewsContext)
        assert sample.context[0].search_query == "breaking news"

    def test_sample_with_rag_context(self) -> None:
        data = {
            "context": [
                {
                    "context_type": "RAG_CONTEXT",
                    "rendered_context": "Document content",
                    "document_id": "doc-456"
                }
            ]
        }
        sample = Sample.from_dict(data)
        assert isinstance(sample.context, list)
        assert len(sample.context) == 1
        assert isinstance(sample.context[0], RAGContext)
        assert sample.context[0].document_id == "doc-456"

    def test_sample_with_mixed_contexts(self) -> None:
        data = {
            "context": [
                {"context_type": "NEWS_CONTEXT", "rendered_context": "News", "search_query": "q1"},
                {"context_type": "RAG_CONTEXT", "rendered_context": "Doc", "document_id": "d1"},
            ]
        }
        sample = Sample.from_dict(data)
        assert len(sample.context) == 2
        assert isinstance(sample.context[0], NewsContext)
        assert isinstance(sample.context[1], RAGContext)

    def test_sample_with_label(self) -> None:
        data = {
            "label": {
                "label": "0.75",
                "label_confidence": 0.9
            }
        }
        sample = Sample.from_dict(data)
        assert isinstance(sample.label, Label)
        assert sample.label.label == "0.75"
        assert sample.label.label_confidence == 0.9

    def test_sample_is_valid_field(self) -> None:
        data = {"is_valid": False}
        sample = Sample.from_dict(data)
        assert sample.is_valid is False

    def test_sample_is_valid_defaults_true_when_provided(self) -> None:
        data = {"is_valid": True}
        sample = Sample.from_dict(data)
        assert sample.is_valid is True

    def test_sample_null_context(self) -> None:
        data = {"context": None}
        sample = Sample.from_dict(data)
        assert sample.context is None

    def test_sample_missing_fields_are_unset(self) -> None:
        sample = Sample.from_dict({})
        assert sample.seed is UNSET
        assert sample.question is UNSET
        assert sample.label is UNSET
        assert sample.prompt is UNSET
        assert sample.context is UNSET


class TestSampleRoundTrip:
    """Test that samples can be serialized and deserialized."""

    def test_full_sample_roundtrip(self) -> None:
        original_data = {
            "seed": {"seed_text": "Original article"},
            "question": {
                "question_type": "FORWARD_LOOKING_QUESTION",
                "question_text": "Future question?",
                "date_close": "2024-12-25T00:00:00",
                "event_date": "2024-12-24T00:00:00",
                "resolution_criteria": "Check outcome"
            },
            "label": {"label": "0.8", "label_confidence": 0.95},
            "context": [
                {"context_type": "NEWS_CONTEXT", "rendered_context": "Context", "search_query": "search"}
            ],
            "prompt": "Rendered prompt",
            "is_valid": True
        }

        sample = Sample.from_dict(original_data)
        serialized = sample.to_dict()
        restored = Sample.from_dict(serialized)

        assert restored.seed.seed_text == "Original article"
        assert isinstance(restored.question, ForwardLookingQuestion)
        assert restored.question.resolution_criteria == "Check outcome"
        assert restored.label.label == "0.8"
        assert isinstance(restored.context[0], NewsContext)
        assert restored.prompt == "Rendered prompt"
        assert restored.is_valid is True
