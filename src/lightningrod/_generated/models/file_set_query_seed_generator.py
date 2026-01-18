from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Literal, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="FileSetQuerySeedGenerator")


@_attrs_define
class FileSetQuerySeedGenerator:
    """Configuration for FileSet Query Seed Generator transform.

    Attributes:
        file_set_id (str): FileSet ID to query
        prompts (list[str]): List of queries to run against the fileset
        config_type (Literal['FILESET_QUERY_SEED_GENERATOR'] | Unset): Type of transform configuration Default:
            'FILESET_QUERY_SEED_GENERATOR'.
        metadata_filters (list[str] | None | Unset): Optional list of AIP-160 metadata filters to select which documents
            to process. Documents matching ANY filter will be included. (e.g., ["ticker='AAL'", "ticker='MSFT'"])
        system_instruction (None | str | Unset): Optional system instruction for the Gemini model
    """

    file_set_id: str
    prompts: list[str]
    config_type: Literal["FILESET_QUERY_SEED_GENERATOR"] | Unset = "FILESET_QUERY_SEED_GENERATOR"
    metadata_filters: list[str] | None | Unset = UNSET
    system_instruction: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        file_set_id = self.file_set_id

        prompts = self.prompts

        config_type = self.config_type

        metadata_filters: list[str] | None | Unset
        if isinstance(self.metadata_filters, Unset):
            metadata_filters = UNSET
        elif isinstance(self.metadata_filters, list):
            metadata_filters = self.metadata_filters

        else:
            metadata_filters = self.metadata_filters

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
                "prompts": prompts,
            }
        )
        if config_type is not UNSET:
            field_dict["config_type"] = config_type
        if metadata_filters is not UNSET:
            field_dict["metadata_filters"] = metadata_filters
        if system_instruction is not UNSET:
            field_dict["system_instruction"] = system_instruction

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        file_set_id = d.pop("file_set_id")

        prompts = cast(list[str], d.pop("prompts"))

        config_type = cast(Literal["FILESET_QUERY_SEED_GENERATOR"] | Unset, d.pop("config_type", UNSET))
        if config_type != "FILESET_QUERY_SEED_GENERATOR" and not isinstance(config_type, Unset):
            raise ValueError(f"config_type must match const 'FILESET_QUERY_SEED_GENERATOR', got '{config_type}'")

        def _parse_metadata_filters(data: object) -> list[str] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                metadata_filters_type_0 = cast(list[str], data)

                return metadata_filters_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[str] | None | Unset, data)

        metadata_filters = _parse_metadata_filters(d.pop("metadata_filters", UNSET))

        def _parse_system_instruction(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        system_instruction = _parse_system_instruction(d.pop("system_instruction", UNSET))

        file_set_query_seed_generator = cls(
            file_set_id=file_set_id,
            prompts=prompts,
            config_type=config_type,
            metadata_filters=metadata_filters,
            system_instruction=system_instruction,
        )

        file_set_query_seed_generator.additional_properties = d
        return file_set_query_seed_generator

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
