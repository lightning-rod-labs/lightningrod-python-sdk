from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Literal, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.temporal_constraint import TemporalConstraint
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.binary_answer_type import BinaryAnswerType
    from ..models.continuous_answer_type import ContinuousAnswerType
    from ..models.free_response_answer_type import FreeResponseAnswerType
    from ..models.multiple_choice_answer_type import MultipleChoiceAnswerType


T = TypeVar("T", bound="FileSetRAGLabeler")


@_attrs_define
class FileSetRAGLabeler:
    """Configuration for FileSet RAG Labeler transform.

    Attributes:
        file_set_id (str): FileSet ID to query for labeling
        config_type (Literal['FILESET_RAG_LABELER'] | Unset): Type of transform configuration Default:
            'FILESET_RAG_LABELER'.
        metadata_filter_keys (list[str] | Unset): Keys from seed's file_metadata for dynamic filtering (e.g.,
            ['ticker'])
        metadata_filter (None | str | Unset): Static AIP-160 metadata filter (combined with dynamic via AND)
        system_instruction (None | str | Unset): Optional system instruction for the Gemini RAG query
        confidence_threshold (float | Unset): Minimum confidence threshold for including questions Default: 0.9.
        answer_type (BinaryAnswerType | ContinuousAnswerType | FreeResponseAnswerType | MultipleChoiceAnswerType | None
            | Unset): The type of answer expected, used to guide the labeler
        temporal_constraint (None | TemporalConstraint | Unset): Filter documents by date relative to seed date. AFTER
            (>) for resolution docs, BEFORE (<=) for historical only.
        date_metadata_key (str | Unset): Gemini metadata key storing unix timestamp for temporal filtering Default:
            'file_date'.
        model (str | Unset): Gemini model for RAG query Default: 'gemini-3-flash-preview'.
    """

    file_set_id: str
    config_type: Literal["FILESET_RAG_LABELER"] | Unset = "FILESET_RAG_LABELER"
    metadata_filter_keys: list[str] | Unset = UNSET
    metadata_filter: None | str | Unset = UNSET
    system_instruction: None | str | Unset = UNSET
    confidence_threshold: float | Unset = 0.9
    answer_type: (
        BinaryAnswerType | ContinuousAnswerType | FreeResponseAnswerType | MultipleChoiceAnswerType | None | Unset
    ) = UNSET
    temporal_constraint: None | TemporalConstraint | Unset = UNSET
    date_metadata_key: str | Unset = "file_date"
    model: str | Unset = "gemini-3-flash-preview"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.binary_answer_type import BinaryAnswerType
        from ..models.continuous_answer_type import ContinuousAnswerType
        from ..models.free_response_answer_type import FreeResponseAnswerType
        from ..models.multiple_choice_answer_type import MultipleChoiceAnswerType

        file_set_id = self.file_set_id

        config_type = self.config_type

        metadata_filter_keys: list[str] | Unset = UNSET
        if not isinstance(self.metadata_filter_keys, Unset):
            metadata_filter_keys = self.metadata_filter_keys

        metadata_filter: None | str | Unset
        if isinstance(self.metadata_filter, Unset):
            metadata_filter = UNSET
        else:
            metadata_filter = self.metadata_filter

        system_instruction: None | str | Unset
        if isinstance(self.system_instruction, Unset):
            system_instruction = UNSET
        else:
            system_instruction = self.system_instruction

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
        elif isinstance(self.answer_type, FreeResponseAnswerType):
            answer_type = self.answer_type.to_dict()
        else:
            answer_type = self.answer_type

        temporal_constraint: None | str | Unset
        if isinstance(self.temporal_constraint, Unset):
            temporal_constraint = UNSET
        elif isinstance(self.temporal_constraint, TemporalConstraint):
            temporal_constraint = self.temporal_constraint.value
        else:
            temporal_constraint = self.temporal_constraint

        date_metadata_key = self.date_metadata_key

        model = self.model

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "file_set_id": file_set_id,
            }
        )
        if config_type is not UNSET:
            field_dict["config_type"] = config_type
        if metadata_filter_keys is not UNSET:
            field_dict["metadata_filter_keys"] = metadata_filter_keys
        if metadata_filter is not UNSET:
            field_dict["metadata_filter"] = metadata_filter
        if system_instruction is not UNSET:
            field_dict["system_instruction"] = system_instruction
        if confidence_threshold is not UNSET:
            field_dict["confidence_threshold"] = confidence_threshold
        if answer_type is not UNSET:
            field_dict["answer_type"] = answer_type
        if temporal_constraint is not UNSET:
            field_dict["temporal_constraint"] = temporal_constraint
        if date_metadata_key is not UNSET:
            field_dict["date_metadata_key"] = date_metadata_key
        if model is not UNSET:
            field_dict["model"] = model

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.binary_answer_type import BinaryAnswerType
        from ..models.continuous_answer_type import ContinuousAnswerType
        from ..models.free_response_answer_type import FreeResponseAnswerType
        from ..models.multiple_choice_answer_type import MultipleChoiceAnswerType

        d = dict(src_dict)
        file_set_id = d.pop("file_set_id")

        config_type = cast(Literal["FILESET_RAG_LABELER"] | Unset, d.pop("config_type", UNSET))
        if config_type != "FILESET_RAG_LABELER" and not isinstance(config_type, Unset):
            raise ValueError(f"config_type must match const 'FILESET_RAG_LABELER', got '{config_type}'")

        metadata_filter_keys = cast(list[str], d.pop("metadata_filter_keys", UNSET))

        def _parse_metadata_filter(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        metadata_filter = _parse_metadata_filter(d.pop("metadata_filter", UNSET))

        def _parse_system_instruction(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        system_instruction = _parse_system_instruction(d.pop("system_instruction", UNSET))

        confidence_threshold = d.pop("confidence_threshold", UNSET)

        def _parse_answer_type(
            data: object,
        ) -> BinaryAnswerType | ContinuousAnswerType | FreeResponseAnswerType | MultipleChoiceAnswerType | None | Unset:
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
                answer_type_type_0_type_3 = FreeResponseAnswerType.from_dict(data)

                return answer_type_type_0_type_3
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(
                BinaryAnswerType
                | ContinuousAnswerType
                | FreeResponseAnswerType
                | MultipleChoiceAnswerType
                | None
                | Unset,
                data,
            )

        answer_type = _parse_answer_type(d.pop("answer_type", UNSET))

        def _parse_temporal_constraint(data: object) -> None | TemporalConstraint | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                temporal_constraint_type_0 = TemporalConstraint(data)

                return temporal_constraint_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | TemporalConstraint | Unset, data)

        temporal_constraint = _parse_temporal_constraint(d.pop("temporal_constraint", UNSET))

        date_metadata_key = d.pop("date_metadata_key", UNSET)

        model = d.pop("model", UNSET)

        file_set_rag_labeler = cls(
            file_set_id=file_set_id,
            config_type=config_type,
            metadata_filter_keys=metadata_filter_keys,
            metadata_filter=metadata_filter,
            system_instruction=system_instruction,
            confidence_threshold=confidence_threshold,
            answer_type=answer_type,
            temporal_constraint=temporal_constraint,
            date_metadata_key=date_metadata_key,
            model=model,
        )

        file_set_rag_labeler.additional_properties = d
        return file_set_rag_labeler

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
