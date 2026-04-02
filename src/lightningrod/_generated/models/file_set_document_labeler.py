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
    from ..models.model_config import ModelConfig
    from ..models.multiple_choice_answer_type import MultipleChoiceAnswerType


T = TypeVar("T", bound="FileSetDocumentLabeler")


@_attrs_define
class FileSetDocumentLabeler:
    """Configuration for FileSet Document Labeler transform.

    Resolves a single document from a FileSet based on temporal ordering,
    downloads the full text, and uses an LLM to extract a structured label.

        Attributes:
            file_set_id (str): FileSet ID to resolve documents from
            config_type (Literal['FILESET_DOCUMENT_LABELER'] | Unset): Type of transform configuration Default:
                'FILESET_DOCUMENT_LABELER'.
            temporal_constraint (TemporalConstraint | Unset): Temporal filtering direction relative to the seed document's
                date.

                Uses the `file_date` metadata key (unix timestamp int) stored on each
                Gemini document by fileset_file_processor.

                BEFORE: file_date <= seed_timestamp  (RAG context: no lookahead bias, multi-doc)
                AFTER:  file_date >  seed_timestamp  (RAG labels: find resolutions, multi-doc)
                NEXT_DOCUMENT: first file after seed_timestamp (single-doc resolution)
                PREVIOUS_DOCUMENT: most recent file before seed_timestamp (single-doc resolution)
                EQUAL: file_date == seed_timestamp (exact match, single-doc)
            metadata_filter_keys (list[str] | Unset): Optional keys from sample's file_metadata for exact-match filtering
                (e.g., ['district'])
            confidence_threshold (float | Unset): Minimum confidence threshold for valid labels Default: 0.7.
            answer_type (BinaryAnswerType | ContinuousAnswerType | FreeResponseAnswerType | MultipleChoiceAnswerType | None
                | Unset): The type of answer expected, used to guide the labeler
            model (ModelConfig | None | Unset): Model for label extraction. Defaults to gemini-2.5-flash.
            system_instruction (None | str | Unset): Domain-specific system instruction for the labeler (e.g., 'You are
                labeling Federal Reserve Beige Book forecasting questions.')
    """

    file_set_id: str
    config_type: Literal["FILESET_DOCUMENT_LABELER"] | Unset = "FILESET_DOCUMENT_LABELER"
    temporal_constraint: TemporalConstraint | Unset = UNSET
    metadata_filter_keys: list[str] | Unset = UNSET
    confidence_threshold: float | Unset = 0.7
    answer_type: (
        BinaryAnswerType | ContinuousAnswerType | FreeResponseAnswerType | MultipleChoiceAnswerType | None | Unset
    ) = UNSET
    model: ModelConfig | None | Unset = UNSET
    system_instruction: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.binary_answer_type import BinaryAnswerType
        from ..models.continuous_answer_type import ContinuousAnswerType
        from ..models.free_response_answer_type import FreeResponseAnswerType
        from ..models.model_config import ModelConfig
        from ..models.multiple_choice_answer_type import MultipleChoiceAnswerType

        file_set_id = self.file_set_id

        config_type = self.config_type

        temporal_constraint: str | Unset = UNSET
        if not isinstance(self.temporal_constraint, Unset):
            temporal_constraint = self.temporal_constraint.value

        metadata_filter_keys: list[str] | Unset = UNSET
        if not isinstance(self.metadata_filter_keys, Unset):
            metadata_filter_keys = self.metadata_filter_keys

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

        model: dict[str, Any] | None | Unset
        if isinstance(self.model, Unset):
            model = UNSET
        elif isinstance(self.model, ModelConfig):
            model = self.model.to_dict()
        else:
            model = self.model

        system_instruction: None | str | Unset
        if isinstance(self.system_instruction, Unset):
            system_instruction = UNSET
        else:
            system_instruction = self.system_instruction

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "file_set_id": file_set_id,
            }
        )
        if config_type is not UNSET:
            field_dict["config_type"] = config_type
        if temporal_constraint is not UNSET:
            field_dict["temporal_constraint"] = temporal_constraint
        if metadata_filter_keys is not UNSET:
            field_dict["metadata_filter_keys"] = metadata_filter_keys
        if confidence_threshold is not UNSET:
            field_dict["confidence_threshold"] = confidence_threshold
        if answer_type is not UNSET:
            field_dict["answer_type"] = answer_type
        if model is not UNSET:
            field_dict["model"] = model
        if system_instruction is not UNSET:
            field_dict["system_instruction"] = system_instruction

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.binary_answer_type import BinaryAnswerType
        from ..models.continuous_answer_type import ContinuousAnswerType
        from ..models.free_response_answer_type import FreeResponseAnswerType
        from ..models.model_config import ModelConfig
        from ..models.multiple_choice_answer_type import MultipleChoiceAnswerType

        d = dict(src_dict)
        file_set_id = d.pop("file_set_id")

        config_type = cast(Literal["FILESET_DOCUMENT_LABELER"] | Unset, d.pop("config_type", UNSET))
        if config_type != "FILESET_DOCUMENT_LABELER" and not isinstance(config_type, Unset):
            raise ValueError(f"config_type must match const 'FILESET_DOCUMENT_LABELER', got '{config_type}'")

        _temporal_constraint = d.pop("temporal_constraint", UNSET)
        temporal_constraint: TemporalConstraint | Unset
        if isinstance(_temporal_constraint, Unset):
            temporal_constraint = UNSET
        else:
            temporal_constraint = TemporalConstraint(_temporal_constraint)

        metadata_filter_keys = cast(list[str], d.pop("metadata_filter_keys", UNSET))

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

        def _parse_model(data: object) -> ModelConfig | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                model_type_0 = ModelConfig.from_dict(data)

                return model_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(ModelConfig | None | Unset, data)

        model = _parse_model(d.pop("model", UNSET))

        def _parse_system_instruction(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        system_instruction = _parse_system_instruction(d.pop("system_instruction", UNSET))

        file_set_document_labeler = cls(
            file_set_id=file_set_id,
            config_type=config_type,
            temporal_constraint=temporal_constraint,
            metadata_filter_keys=metadata_filter_keys,
            confidence_threshold=confidence_threshold,
            answer_type=answer_type,
            model=model,
            system_instruction=system_instruction,
        )

        file_set_document_labeler.additional_properties = d
        return file_set_document_labeler

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
