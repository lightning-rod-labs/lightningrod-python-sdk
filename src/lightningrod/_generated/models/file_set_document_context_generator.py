from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Literal, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.temporal_constraint import TemporalConstraint
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.model_config import ModelConfig


T = TypeVar("T", bound="FileSetDocumentContextGenerator")


@_attrs_define
class FileSetDocumentContextGenerator:
    """Configuration for FileSet Document Context Generator transform.

    Resolves a single document from a FileSet based on temporal ordering,
    downloads the full text, and appends it as context. Optionally processes
    the document through an LLM before injection.

        Attributes:
            file_set_id (str): FileSet ID to resolve documents from
            config_type (Literal['FILESET_DOCUMENT_CONTEXT_GENERATOR'] | Unset): Type of transform configuration Default:
                'FILESET_DOCUMENT_CONTEXT_GENERATOR'.
            temporal_constraint (TemporalConstraint | Unset): Temporal filtering direction relative to a reference (seed)
                timestamp.

                Uses the `file_date` metadata key (unix timestamp int) from the manifest.

                BEFORE: file_date <= seed_timestamp  (context: no lookahead bias, multi-doc)
                AFTER:  file_date >  seed_timestamp  (labels: find resolutions, multi-doc)
                NEXT_DOCUMENT: first file after seed_timestamp (single-doc resolution)
                PREVIOUS_DOCUMENT: most recent file before seed_timestamp (single-doc resolution)
                EQUAL: file_date == seed_timestamp (exact match, single-doc)
            metadata_filter_keys (list[str] | Unset): Optional keys from sample's file_metadata for exact-match filtering
                (e.g., ['district', 'ticker'])
            system_instruction (None | str | Unset): Optional system instruction for LLM processing of the document. When
                provided with model, the document is processed through an LLM before being stored as context.
            model (ModelConfig | None | Unset): Model for optional LLM processing. If None, raw document text is used as
                context.
            max_document_chars (int | None | Unset): Optional character limit for document text. Truncates from the end if
                exceeded.
    """

    file_set_id: str
    config_type: Literal["FILESET_DOCUMENT_CONTEXT_GENERATOR"] | Unset = "FILESET_DOCUMENT_CONTEXT_GENERATOR"
    temporal_constraint: TemporalConstraint | Unset = UNSET
    metadata_filter_keys: list[str] | Unset = UNSET
    system_instruction: None | str | Unset = UNSET
    model: ModelConfig | None | Unset = UNSET
    max_document_chars: int | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.model_config import ModelConfig

        file_set_id = self.file_set_id

        config_type = self.config_type

        temporal_constraint: str | Unset = UNSET
        if not isinstance(self.temporal_constraint, Unset):
            temporal_constraint = self.temporal_constraint.value

        metadata_filter_keys: list[str] | Unset = UNSET
        if not isinstance(self.metadata_filter_keys, Unset):
            metadata_filter_keys = self.metadata_filter_keys

        system_instruction: None | str | Unset
        if isinstance(self.system_instruction, Unset):
            system_instruction = UNSET
        else:
            system_instruction = self.system_instruction

        model: dict[str, Any] | None | Unset
        if isinstance(self.model, Unset):
            model = UNSET
        elif isinstance(self.model, ModelConfig):
            model = self.model.to_dict()
        else:
            model = self.model

        max_document_chars: int | None | Unset
        if isinstance(self.max_document_chars, Unset):
            max_document_chars = UNSET
        else:
            max_document_chars = self.max_document_chars

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
        if system_instruction is not UNSET:
            field_dict["system_instruction"] = system_instruction
        if model is not UNSET:
            field_dict["model"] = model
        if max_document_chars is not UNSET:
            field_dict["max_document_chars"] = max_document_chars

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.model_config import ModelConfig

        d = dict(src_dict)
        file_set_id = d.pop("file_set_id")

        config_type = cast(Literal["FILESET_DOCUMENT_CONTEXT_GENERATOR"] | Unset, d.pop("config_type", UNSET))
        if config_type != "FILESET_DOCUMENT_CONTEXT_GENERATOR" and not isinstance(config_type, Unset):
            raise ValueError(f"config_type must match const 'FILESET_DOCUMENT_CONTEXT_GENERATOR', got '{config_type}'")

        _temporal_constraint = d.pop("temporal_constraint", UNSET)
        temporal_constraint: TemporalConstraint | Unset
        if isinstance(_temporal_constraint, Unset):
            temporal_constraint = UNSET
        else:
            temporal_constraint = TemporalConstraint(_temporal_constraint)

        metadata_filter_keys = cast(list[str], d.pop("metadata_filter_keys", UNSET))

        def _parse_system_instruction(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        system_instruction = _parse_system_instruction(d.pop("system_instruction", UNSET))

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

        def _parse_max_document_chars(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        max_document_chars = _parse_max_document_chars(d.pop("max_document_chars", UNSET))

        file_set_document_context_generator = cls(
            file_set_id=file_set_id,
            config_type=config_type,
            temporal_constraint=temporal_constraint,
            metadata_filter_keys=metadata_filter_keys,
            system_instruction=system_instruction,
            model=model,
            max_document_chars=max_document_chars,
        )

        file_set_document_context_generator.additional_properties = d
        return file_set_document_context_generator

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
