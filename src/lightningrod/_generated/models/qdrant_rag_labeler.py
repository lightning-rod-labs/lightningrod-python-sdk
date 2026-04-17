from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Literal, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.binary_answer_type import BinaryAnswerType
    from ..models.continuous_answer_type import ContinuousAnswerType
    from ..models.continuous_value_only_answer_type import ContinuousValueOnlyAnswerType
    from ..models.free_response_answer_type import FreeResponseAnswerType
    from ..models.model_config import ModelConfig
    from ..models.multiple_choice_answer_type import MultipleChoiceAnswerType
    from ..models.qdrant_rag_labeler_payload_filters_type_0 import QdrantRAGLabelerPayloadFiltersType0


T = TypeVar("T", bound="QdrantRAGLabeler")


@_attrs_define
class QdrantRAGLabeler:
    """Configuration for Qdrant RAG Labeler transform.

    Attributes:
        config_type (Literal['QDRANT_RAG_LABELER'] | Unset):  Default: 'QDRANT_RAG_LABELER'.
        file_set_id (None | str | Unset): FileSet ID to load Qdrant collection from GCS snapshot.
        collection_name (None | str | Unset): Qdrant collection to query (required when using direct injection).
        embedding_model (str | Unset): FastEmbed model name for query embedding. Default: 'BAAI/bge-small-en-v1.5'.
        index_chunk_size (int | Unset): Chunk size to use when building the backing FileSet Qdrant index. Default: 1500.
        index_chunk_overlap (int | Unset): Chunk overlap to use when building the backing FileSet Qdrant index. Default:
            150.
        extraction_model (ModelConfig | None | Unset): LLM model for structured label extraction. Defaults to
            gemini-2.5-flash.
        top_k (int | Unset): Number of chunks to retrieve Default: 5.
        temporal_direction (None | str | Unset): 'before' or 'after' relative to seed date, or None for no filter.
        payload_filters (None | QdrantRAGLabelerPayloadFiltersType0 | Unset): Payload filters as {payload_key: meta_key}
            mapping.
        confidence_threshold (float | Unset): Minimum confidence threshold for including labels. Default: 0.9.
        answer_type (BinaryAnswerType | ContinuousAnswerType | ContinuousValueOnlyAnswerType | FreeResponseAnswerType |
            MultipleChoiceAnswerType | None | Unset): Expected answer type to guide the labeler.
        timestamp_key (str | Unset):  Default: 'timestamp'.
        text_key (str | Unset):  Default: 'text'.
        source_key (str | Unset):  Default: 'source_file'.
    """

    config_type: Literal["QDRANT_RAG_LABELER"] | Unset = "QDRANT_RAG_LABELER"
    file_set_id: None | str | Unset = UNSET
    collection_name: None | str | Unset = UNSET
    embedding_model: str | Unset = "BAAI/bge-small-en-v1.5"
    index_chunk_size: int | Unset = 1500
    index_chunk_overlap: int | Unset = 150
    extraction_model: ModelConfig | None | Unset = UNSET
    top_k: int | Unset = 5
    temporal_direction: None | str | Unset = UNSET
    payload_filters: None | QdrantRAGLabelerPayloadFiltersType0 | Unset = UNSET
    confidence_threshold: float | Unset = 0.9
    answer_type: (
        BinaryAnswerType
        | ContinuousAnswerType
        | ContinuousValueOnlyAnswerType
        | FreeResponseAnswerType
        | MultipleChoiceAnswerType
        | None
        | Unset
    ) = UNSET
    timestamp_key: str | Unset = "timestamp"
    text_key: str | Unset = "text"
    source_key: str | Unset = "source_file"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.binary_answer_type import BinaryAnswerType
        from ..models.continuous_answer_type import ContinuousAnswerType
        from ..models.continuous_value_only_answer_type import ContinuousValueOnlyAnswerType
        from ..models.free_response_answer_type import FreeResponseAnswerType
        from ..models.model_config import ModelConfig
        from ..models.multiple_choice_answer_type import MultipleChoiceAnswerType
        from ..models.qdrant_rag_labeler_payload_filters_type_0 import QdrantRAGLabelerPayloadFiltersType0

        config_type = self.config_type

        file_set_id: None | str | Unset
        if isinstance(self.file_set_id, Unset):
            file_set_id = UNSET
        else:
            file_set_id = self.file_set_id

        collection_name: None | str | Unset
        if isinstance(self.collection_name, Unset):
            collection_name = UNSET
        else:
            collection_name = self.collection_name

        embedding_model = self.embedding_model

        index_chunk_size = self.index_chunk_size

        index_chunk_overlap = self.index_chunk_overlap

        extraction_model: dict[str, Any] | None | Unset
        if isinstance(self.extraction_model, Unset):
            extraction_model = UNSET
        elif isinstance(self.extraction_model, ModelConfig):
            extraction_model = self.extraction_model.to_dict()
        else:
            extraction_model = self.extraction_model

        top_k = self.top_k

        temporal_direction: None | str | Unset
        if isinstance(self.temporal_direction, Unset):
            temporal_direction = UNSET
        else:
            temporal_direction = self.temporal_direction

        payload_filters: dict[str, Any] | None | Unset
        if isinstance(self.payload_filters, Unset):
            payload_filters = UNSET
        elif isinstance(self.payload_filters, QdrantRAGLabelerPayloadFiltersType0):
            payload_filters = self.payload_filters.to_dict()
        else:
            payload_filters = self.payload_filters

        confidence_threshold = self.confidence_threshold

        answer_type: dict[str, Any] | None | Unset
        if isinstance(self.answer_type, Unset):
            answer_type = UNSET
        elif isinstance(self.answer_type, BinaryAnswerType):
            answer_type = self.answer_type.to_dict()
        elif isinstance(self.answer_type, MultipleChoiceAnswerType):
            answer_type = self.answer_type.to_dict()
        elif isinstance(self.answer_type, ContinuousAnswerType):
            answer_type = self.answer_type.to_dict()
        elif isinstance(self.answer_type, ContinuousValueOnlyAnswerType):
            answer_type = self.answer_type.to_dict()
        elif isinstance(self.answer_type, FreeResponseAnswerType):
            answer_type = self.answer_type.to_dict()
        else:
            answer_type = self.answer_type

        timestamp_key = self.timestamp_key

        text_key = self.text_key

        source_key = self.source_key

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if config_type is not UNSET:
            field_dict["config_type"] = config_type
        if file_set_id is not UNSET:
            field_dict["file_set_id"] = file_set_id
        if collection_name is not UNSET:
            field_dict["collection_name"] = collection_name
        if embedding_model is not UNSET:
            field_dict["embedding_model"] = embedding_model
        if index_chunk_size is not UNSET:
            field_dict["index_chunk_size"] = index_chunk_size
        if index_chunk_overlap is not UNSET:
            field_dict["index_chunk_overlap"] = index_chunk_overlap
        if extraction_model is not UNSET:
            field_dict["extraction_model"] = extraction_model
        if top_k is not UNSET:
            field_dict["top_k"] = top_k
        if temporal_direction is not UNSET:
            field_dict["temporal_direction"] = temporal_direction
        if payload_filters is not UNSET:
            field_dict["payload_filters"] = payload_filters
        if confidence_threshold is not UNSET:
            field_dict["confidence_threshold"] = confidence_threshold
        if answer_type is not UNSET:
            field_dict["answer_type"] = answer_type
        if timestamp_key is not UNSET:
            field_dict["timestamp_key"] = timestamp_key
        if text_key is not UNSET:
            field_dict["text_key"] = text_key
        if source_key is not UNSET:
            field_dict["source_key"] = source_key

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.binary_answer_type import BinaryAnswerType
        from ..models.continuous_answer_type import ContinuousAnswerType
        from ..models.continuous_value_only_answer_type import ContinuousValueOnlyAnswerType
        from ..models.free_response_answer_type import FreeResponseAnswerType
        from ..models.model_config import ModelConfig
        from ..models.multiple_choice_answer_type import MultipleChoiceAnswerType
        from ..models.qdrant_rag_labeler_payload_filters_type_0 import QdrantRAGLabelerPayloadFiltersType0

        d = dict(src_dict)
        config_type = cast(Literal["QDRANT_RAG_LABELER"] | Unset, d.pop("config_type", UNSET))
        if config_type != "QDRANT_RAG_LABELER" and not isinstance(config_type, Unset):
            raise ValueError(f"config_type must match const 'QDRANT_RAG_LABELER', got '{config_type}'")

        def _parse_file_set_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        file_set_id = _parse_file_set_id(d.pop("file_set_id", UNSET))

        def _parse_collection_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        collection_name = _parse_collection_name(d.pop("collection_name", UNSET))

        embedding_model = d.pop("embedding_model", UNSET)

        index_chunk_size = d.pop("index_chunk_size", UNSET)

        index_chunk_overlap = d.pop("index_chunk_overlap", UNSET)

        def _parse_extraction_model(data: object) -> ModelConfig | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                extraction_model_type_0 = ModelConfig.from_dict(data)

                return extraction_model_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(ModelConfig | None | Unset, data)

        extraction_model = _parse_extraction_model(d.pop("extraction_model", UNSET))

        top_k = d.pop("top_k", UNSET)

        def _parse_temporal_direction(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        temporal_direction = _parse_temporal_direction(d.pop("temporal_direction", UNSET))

        def _parse_payload_filters(data: object) -> None | QdrantRAGLabelerPayloadFiltersType0 | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                payload_filters_type_0 = QdrantRAGLabelerPayloadFiltersType0.from_dict(data)

                return payload_filters_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | QdrantRAGLabelerPayloadFiltersType0 | Unset, data)

        payload_filters = _parse_payload_filters(d.pop("payload_filters", UNSET))

        confidence_threshold = d.pop("confidence_threshold", UNSET)

        def _parse_answer_type(
            data: object,
        ) -> (
            BinaryAnswerType
            | ContinuousAnswerType
            | ContinuousValueOnlyAnswerType
            | FreeResponseAnswerType
            | MultipleChoiceAnswerType
            | None
            | Unset
        ):
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                answer_type_type_0_type_0 = BinaryAnswerType.from_dict(data)

                return answer_type_type_0_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                answer_type_type_0_type_1 = MultipleChoiceAnswerType.from_dict(data)

                return answer_type_type_0_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                answer_type_type_0_type_2 = ContinuousAnswerType.from_dict(data)

                return answer_type_type_0_type_2
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                answer_type_type_0_type_3 = ContinuousValueOnlyAnswerType.from_dict(data)

                return answer_type_type_0_type_3
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                answer_type_type_0_type_4 = FreeResponseAnswerType.from_dict(data)

                return answer_type_type_0_type_4
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(
                BinaryAnswerType
                | ContinuousAnswerType
                | ContinuousValueOnlyAnswerType
                | FreeResponseAnswerType
                | MultipleChoiceAnswerType
                | None
                | Unset,
                data,
            )

        answer_type = _parse_answer_type(d.pop("answer_type", UNSET))

        timestamp_key = d.pop("timestamp_key", UNSET)

        text_key = d.pop("text_key", UNSET)

        source_key = d.pop("source_key", UNSET)

        qdrant_rag_labeler = cls(
            config_type=config_type,
            file_set_id=file_set_id,
            collection_name=collection_name,
            embedding_model=embedding_model,
            index_chunk_size=index_chunk_size,
            index_chunk_overlap=index_chunk_overlap,
            extraction_model=extraction_model,
            top_k=top_k,
            temporal_direction=temporal_direction,
            payload_filters=payload_filters,
            confidence_threshold=confidence_threshold,
            answer_type=answer_type,
            timestamp_key=timestamp_key,
            text_key=text_key,
            source_key=source_key,
        )

        qdrant_rag_labeler.additional_properties = d
        return qdrant_rag_labeler

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
