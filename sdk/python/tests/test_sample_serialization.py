import json
from unittest.mock import MagicMock

import pyarrow as pa

from lightningrod._generated.models.news_context import NewsContext
from lightningrod._generated.models.rag_context import RAGContext
from lightningrod._generated.models.sample import Sample
from lightningrod._generated.models.seed import Seed
from lightningrod._generated.models.question import Question
from lightningrod._generated.types import UNSET
from lightningrod.client import Datasets
from lightningrod.dataset import table_to_samples


class TestTableToSamples:
    def test_parses_news_context_from_table(self) -> None:
        context_json: str = json.dumps([
            {
                "context_type": "NEWS_CONTEXT",
                "rendered_context": "Article about AI advances",
                "search_query": "artificial intelligence news"
            }
        ])
        
        table: pa.Table = pa.table({
            "question_text": ["Will AI advance?"],
            "context": [context_json],
        })
        
        samples = table_to_samples(table)
        
        assert len(samples) == 1
        assert isinstance(samples[0].context, list)
        assert len(samples[0].context) == 1
        assert isinstance(samples[0].context[0], NewsContext)
        assert samples[0].context[0].rendered_context == "Article about AI advances"
        assert samples[0].context[0].search_query == "artificial intelligence news"

    def test_parses_rag_context_from_table(self) -> None:
        context_json: str = json.dumps([
            {
                "context_type": "RAG_CONTEXT",
                "rendered_context": "Retrieved document content",
                "document_id": "doc-123"
            }
        ])
        
        table: pa.Table = pa.table({
            "question_text": ["What is the answer?"],
            "context": [context_json],
        })
        
        samples = table_to_samples(table)
        
        assert len(samples) == 1
        assert isinstance(samples[0].context, list)
        assert len(samples[0].context) == 1
        assert isinstance(samples[0].context[0], RAGContext)
        assert samples[0].context[0].rendered_context == "Retrieved document content"
        assert samples[0].context[0].document_id == "doc-123"

    def test_parses_mixed_context_types(self) -> None:
        context_json: str = json.dumps([
            {
                "context_type": "NEWS_CONTEXT",
                "rendered_context": "News article",
                "search_query": "breaking news"
            },
            {
                "context_type": "RAG_CONTEXT",
                "rendered_context": "Document content",
                "document_id": "doc-456"
            }
        ])
        
        table: pa.Table = pa.table({
            "question_text": ["Complex question"],
            "context": [context_json],
        })
        
        samples = table_to_samples(table)
        
        assert len(samples) == 1
        assert isinstance(samples[0].context, list)
        assert len(samples[0].context) == 2
        assert isinstance(samples[0].context[0], NewsContext)
        assert isinstance(samples[0].context[1], RAGContext)

    def test_handles_null_context(self) -> None:
        table: pa.Table = pa.table({
            "question_text": ["Simple question"],
            "context": [None],
        })
        
        samples = table_to_samples(table)
        
        assert len(samples) == 1
        assert samples[0].context is UNSET

    def test_handles_missing_context_column(self) -> None:
        table: pa.Table = pa.table({
            "question_text": ["Question without context"],
        })
        
        samples = table_to_samples(table)
        
        assert len(samples) == 1
        assert samples[0].context is UNSET

    def test_parses_full_sample_with_context(self) -> None:
        context_json: str = json.dumps([
            {
                "context_type": "NEWS_CONTEXT",
                "rendered_context": "Relevant news",
                "search_query": "topic search"
            }
        ])
        
        table: pa.Table = pa.table({
            "seed_text": ["Original seed content"],
            "url": ["https://example.com"],
            "question_text": ["Will this happen?"],
            "label": ["0.75"],
            "label_confidence": [0.9],
            "resolution_date": [None],
            "context": [context_json],
            "prompt": ["Rendered prompt text"],
            "custom_field": ["extra data"],
        })
        
        samples = table_to_samples(table)
        
        assert len(samples) == 1
        sample = samples[0]
        
        assert isinstance(sample.seed, Seed)
        assert sample.seed.seed_text == "Original seed content"
        assert sample.seed.url == "https://example.com"
        
        assert isinstance(sample.question, Question)
        assert sample.question.question_text == "Will this happen?"
        
        from lightningrod._generated.models.label import Label
        from lightningrod._generated.models.sample_meta import SampleMeta
        
        assert isinstance(sample.label, Label)
        assert sample.label.label == "0.75"
        assert sample.label.label_confidence == 0.9
        
        assert isinstance(sample.context, list)
        assert len(sample.context) == 1
        assert isinstance(sample.context[0], NewsContext)
        
        assert sample.prompt == "Rendered prompt text"
        
        assert isinstance(sample.meta, SampleMeta)
        assert sample.meta["custom_field"] == "extra data"

    def test_parses_multiple_rows(self) -> None:
        news_context: str = json.dumps([{"context_type": "NEWS_CONTEXT", "rendered_context": "News", "search_query": "q1"}])
        rag_context: str = json.dumps([{"context_type": "RAG_CONTEXT", "rendered_context": "Doc", "document_id": "d1"}])
        
        table: pa.Table = pa.table({
            "question_text": ["Q1", "Q2", "Q3"],
            "context": [news_context, rag_context, None],
        })
        
        samples = table_to_samples(table)
        
        assert len(samples) == 3
        
        assert isinstance(samples[0].context, list)
        assert isinstance(samples[0].context[0], NewsContext)
        
        assert isinstance(samples[1].context, list)
        assert isinstance(samples[1].context[0], RAGContext)
        
        assert samples[2].context is UNSET

    def test_empty_context_list_parsed(self) -> None:
        table: pa.Table = pa.table({
            "question_text": ["Question"],
            "context": [json.dumps([])],
        })
        
        samples = table_to_samples(table)
        
        assert len(samples) == 1
        assert samples[0].context == []


class TestSampleRoundTrip:
    """Test that samples can be serialized to table and deserialized back."""
    
    def test_round_trip_with_news_context(self) -> None:
        original_sample: Sample = Sample.from_dict({
            "seed": {"seed_text": "Original news article"},
            "question": {"question_text": "Will this happen?"},
            "context": [
                {
                    "context_type": "NEWS_CONTEXT",
                    "rendered_context": "Related news content",
                    "search_query": "topic search"
                }
            ],
            "prompt": "Rendered prompt"
        })
        
        mock_client: MagicMock = MagicMock()
        datasets: Datasets = Datasets(mock_client)
        table: pa.Table = datasets._samples_to_table([original_sample])
        
        restored_samples = table_to_samples(table)
        
        assert len(restored_samples) == 1
        restored: Sample = restored_samples[0]
        
        assert isinstance(restored.seed, Seed)
        assert restored.seed.seed_text == "Original news article"
        
        assert isinstance(restored.question, Question)
        assert restored.question.question_text == "Will this happen?"
        
        assert isinstance(restored.context, list)
        assert len(restored.context) == 1
        assert isinstance(restored.context[0], NewsContext)
        assert restored.context[0].rendered_context == "Related news content"
        assert restored.context[0].search_query == "topic search"
        
        assert restored.prompt == "Rendered prompt"

    def test_round_trip_with_mixed_contexts(self) -> None:
        original_sample: Sample = Sample.from_dict({
            "question": {"question_text": "Complex question"},
            "context": [
                {
                    "context_type": "NEWS_CONTEXT",
                    "rendered_context": "News",
                    "search_query": "query1"
                },
                {
                    "context_type": "RAG_CONTEXT",
                    "rendered_context": "Document",
                    "document_id": "doc-123"
                }
            ]
        })
        
        mock_client: MagicMock = MagicMock()
        datasets: Datasets = Datasets(mock_client)
        table: pa.Table = datasets._samples_to_table([original_sample])
        
        restored_samples = table_to_samples(table)
        
        assert len(restored_samples) == 1
        restored: Sample = restored_samples[0]
        
        assert isinstance(restored.context, list)
        assert len(restored.context) == 2
        assert isinstance(restored.context[0], NewsContext)
        assert isinstance(restored.context[1], RAGContext)
        assert restored.context[1].document_id == "doc-123"

    def test_round_trip_without_context(self) -> None:
        original_sample: Sample = Sample.from_dict({
            "seed": {"seed_text": "Just a seed"},
            "question": {"question_text": "Simple question"}
        })
        
        mock_client: MagicMock = MagicMock()
        datasets: Datasets = Datasets(mock_client)
        table: pa.Table = datasets._samples_to_table([original_sample])
        
        restored_samples = table_to_samples(table)
        
        assert len(restored_samples) == 1
        restored: Sample = restored_samples[0]
        
        assert restored.context is UNSET
