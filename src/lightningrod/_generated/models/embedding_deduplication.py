from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Literal, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.embedding_deduplication_synonyms import EmbeddingDeduplicationSynonyms


T = TypeVar("T", bound="EmbeddingDeduplication")


@_attrs_define
class EmbeddingDeduplication:
    """
    Attributes:
        config_type (Literal['EMBEDDING_DEDUPLICATION'] | Unset): Type of transform configuration Default:
            'EMBEDDING_DEDUPLICATION'.
        fields (list[str] | Unset): Fields to concatenate into the embedding input. Options: ['question_text',
            'seed_text', 'seed_url', 'date_close', 'event_date', 'prediction_date', 'resolution_criteria',
            'resolution_date', 'label']
        key_fields (list[str] | Unset): Optional structured fields that must match exactly before two items are
            considered duplication candidates. With keys set, an embedding index is maintained per-key-bucket and only items
            sharing the same key tuple are compared. Recommended for forecasting questions: include date_close and/or
            event_date so questions about different dates can never be merged even if they're semantically similar. Options:
            ['question_text', 'seed_text', 'seed_url', 'date_close', 'event_date', 'prediction_date', 'resolution_criteria',
            'resolution_date', 'label']
        similarity_threshold (float | Unset): Cosine similarity at/above which two items are considered duplicates.
            Default: 0.92.
        synonyms (EmbeddingDeduplicationSynonyms | Unset): Regex pattern -> replacement, applied case-insensitively
            before embedding. Use this to collapse domain-specific surface variants (tickers/abbreviations, agency names,
            verb synonyms) onto a single form. By far the biggest individual contributor to dedup quality on the eval (~+25%
            PR-AUC). Bad aliases can silently create false-positive duplicates, so review additions carefully.
        normalize_numbers (bool | Unset): Collapse number variants so '$40 billion' / '$40B' / '40,000,000,000' / 'half
            a million' all map to the same string. Marginal lift on its own but composes with synonyms; turn on whenever
            questions mention quantities. Default: False.
        strip_patterns (list[str] | Unset): Regexes deleted (replaced with '') from the text before embedding, applied
            in order. Use to drop domain boilerplate the caller wants ignored — e.g. leading question stems ('^(will|is)
            (the )?') or SEC-filing tickers ('(NASDAQ: IDCC)'). No defaults ship here; supply patterns for your corpus.
        embedding_model (str | Unset): fastembed model name. Must be one of ALLOWED_EMBEDDING_MODELS — the set vetted on
            the dedup quality eval. Default BAAI/bge-small-en-v1.5 (lightweight, CPU-friendly). Default: 'BAAI/bge-small-
            en-v1.5'.
        max_elements (int | Unset): hnswlib index capacity. Default: 1000000.
        ef_construction (int | Unset): hnswlib construction-time ef parameter. Default: 200.
        m (int | Unset): hnswlib graph degree parameter. Default: 16.
        ef_search (int | Unset): hnswlib query-time ef parameter. Default: 64.
    """

    config_type: Literal["EMBEDDING_DEDUPLICATION"] | Unset = "EMBEDDING_DEDUPLICATION"
    fields: list[str] | Unset = UNSET
    key_fields: list[str] | Unset = UNSET
    similarity_threshold: float | Unset = 0.92
    synonyms: EmbeddingDeduplicationSynonyms | Unset = UNSET
    normalize_numbers: bool | Unset = False
    strip_patterns: list[str] | Unset = UNSET
    embedding_model: str | Unset = "BAAI/bge-small-en-v1.5"
    max_elements: int | Unset = 1000000
    ef_construction: int | Unset = 200
    m: int | Unset = 16
    ef_search: int | Unset = 64
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        config_type = self.config_type

        fields: list[str] | Unset = UNSET
        if not isinstance(self.fields, Unset):
            fields = self.fields

        key_fields: list[str] | Unset = UNSET
        if not isinstance(self.key_fields, Unset):
            key_fields = self.key_fields

        similarity_threshold = self.similarity_threshold

        synonyms: dict[str, Any] | Unset = UNSET
        if not isinstance(self.synonyms, Unset):
            synonyms = self.synonyms.to_dict()

        normalize_numbers = self.normalize_numbers

        strip_patterns: list[str] | Unset = UNSET
        if not isinstance(self.strip_patterns, Unset):
            strip_patterns = self.strip_patterns

        embedding_model = self.embedding_model

        max_elements = self.max_elements

        ef_construction = self.ef_construction

        m = self.m

        ef_search = self.ef_search

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if config_type is not UNSET:
            field_dict["config_type"] = config_type
        if fields is not UNSET:
            field_dict["fields"] = fields
        if key_fields is not UNSET:
            field_dict["key_fields"] = key_fields
        if similarity_threshold is not UNSET:
            field_dict["similarity_threshold"] = similarity_threshold
        if synonyms is not UNSET:
            field_dict["synonyms"] = synonyms
        if normalize_numbers is not UNSET:
            field_dict["normalize_numbers"] = normalize_numbers
        if strip_patterns is not UNSET:
            field_dict["strip_patterns"] = strip_patterns
        if embedding_model is not UNSET:
            field_dict["embedding_model"] = embedding_model
        if max_elements is not UNSET:
            field_dict["max_elements"] = max_elements
        if ef_construction is not UNSET:
            field_dict["ef_construction"] = ef_construction
        if m is not UNSET:
            field_dict["M"] = m
        if ef_search is not UNSET:
            field_dict["ef_search"] = ef_search

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.embedding_deduplication_synonyms import EmbeddingDeduplicationSynonyms

        d = dict(src_dict)
        config_type = cast(Literal["EMBEDDING_DEDUPLICATION"] | Unset, d.pop("config_type", UNSET))
        if config_type != "EMBEDDING_DEDUPLICATION" and not isinstance(config_type, Unset):
            raise ValueError(f"config_type must match const 'EMBEDDING_DEDUPLICATION', got '{config_type}'")

        fields = cast(list[str], d.pop("fields", UNSET))

        key_fields = cast(list[str], d.pop("key_fields", UNSET))

        similarity_threshold = d.pop("similarity_threshold", UNSET)

        _synonyms = d.pop("synonyms", UNSET)
        synonyms: EmbeddingDeduplicationSynonyms | Unset
        if isinstance(_synonyms, Unset):
            synonyms = UNSET
        else:
            synonyms = EmbeddingDeduplicationSynonyms.from_dict(_synonyms)

        normalize_numbers = d.pop("normalize_numbers", UNSET)

        strip_patterns = cast(list[str], d.pop("strip_patterns", UNSET))

        embedding_model = d.pop("embedding_model", UNSET)

        max_elements = d.pop("max_elements", UNSET)

        ef_construction = d.pop("ef_construction", UNSET)

        m = d.pop("M", UNSET)

        ef_search = d.pop("ef_search", UNSET)

        embedding_deduplication = cls(
            config_type=config_type,
            fields=fields,
            key_fields=key_fields,
            similarity_threshold=similarity_threshold,
            synonyms=synonyms,
            normalize_numbers=normalize_numbers,
            strip_patterns=strip_patterns,
            embedding_model=embedding_model,
            max_elements=max_elements,
            ef_construction=ef_construction,
            m=m,
            ef_search=ef_search,
        )

        embedding_deduplication.additional_properties = d
        return embedding_deduplication

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
