from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Literal, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.temporal_constraint import TemporalConstraint
from ..types import UNSET, Unset

T = TypeVar("T", bound="FileSetContextGenerator")


@_attrs_define
class FileSetContextGenerator:
    """Configuration for FileSet Context Generator transform.

    Attributes:
        file_set_id (str): FileSet ID to query for context
        config_type (Literal['FILESET_CONTEXT_GENERATOR'] | Unset): Type of transform configuration Default:
            'FILESET_CONTEXT_GENERATOR'.
        metadata_filter_keys (list[str] | Unset): Keys from seed's file_metadata for dynamic filtering (e.g.,
            ['ticker'])
        metadata_filter (None | str | Unset): Static AIP-160 metadata filter (combined with dynamic via AND)
        system_instruction (None | str | Unset): Optional system instruction for the Gemini model
        query_template (None | str | Unset): Template with {question} placeholder; default: raw question text
        temporal_constraint (None | TemporalConstraint | Unset): Filter documents by date relative to seed date. BEFORE
            (<=) for context without lookahead, AFTER (>) for future docs.
        model (str | Unset): Gemini model to use for file search Default: 'gemini-2.5-flash'.
    """

    file_set_id: str
    config_type: Literal["FILESET_CONTEXT_GENERATOR"] | Unset = "FILESET_CONTEXT_GENERATOR"
    metadata_filter_keys: list[str] | Unset = UNSET
    metadata_filter: None | str | Unset = UNSET
    system_instruction: None | str | Unset = UNSET
    query_template: None | str | Unset = UNSET
    temporal_constraint: None | TemporalConstraint | Unset = UNSET
    model: str | Unset = "gemini-2.5-flash"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
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

        query_template: None | str | Unset
        if isinstance(self.query_template, Unset):
            query_template = UNSET
        else:
            query_template = self.query_template

        temporal_constraint: None | str | Unset
        if isinstance(self.temporal_constraint, Unset):
            temporal_constraint = UNSET
        elif isinstance(self.temporal_constraint, TemporalConstraint):
            temporal_constraint = self.temporal_constraint.value
        else:
            temporal_constraint = self.temporal_constraint

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
        if query_template is not UNSET:
            field_dict["query_template"] = query_template
        if temporal_constraint is not UNSET:
            field_dict["temporal_constraint"] = temporal_constraint
        if model is not UNSET:
            field_dict["model"] = model

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        file_set_id = d.pop("file_set_id")

        config_type = cast(Literal["FILESET_CONTEXT_GENERATOR"] | Unset, d.pop("config_type", UNSET))
        if config_type != "FILESET_CONTEXT_GENERATOR" and not isinstance(config_type, Unset):
            raise ValueError(f"config_type must match const 'FILESET_CONTEXT_GENERATOR', got '{config_type}'")

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

        def _parse_query_template(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        query_template = _parse_query_template(d.pop("query_template", UNSET))

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

        model = d.pop("model", UNSET)

        file_set_context_generator = cls(
            file_set_id=file_set_id,
            config_type=config_type,
            metadata_filter_keys=metadata_filter_keys,
            metadata_filter=metadata_filter,
            system_instruction=system_instruction,
            query_template=query_template,
            temporal_constraint=temporal_constraint,
            model=model,
        )

        file_set_context_generator.additional_properties = d
        return file_set_context_generator

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
