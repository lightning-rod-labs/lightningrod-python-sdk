from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.metadata_field_type import MetadataFieldType
from ..types import UNSET, Unset

T = TypeVar("T", bound="MetadataFieldDefinition")


@_attrs_define
class MetadataFieldDefinition:
    """Definition of a metadata field for a FileSet.

    Attributes:
        name (str): The name/key of the metadata field
        field_type (MetadataFieldType):
        required (bool | Unset): Whether this field is required for all files Default: False.
        description (None | str | Unset): Human-readable description of this field
        extraction_hint (None | str | Unset): Hint for LLM auto-extraction (e.g., 'the stock ticker symbol mentioned')
    """

    name: str
    field_type: MetadataFieldType
    required: bool | Unset = False
    description: None | str | Unset = UNSET
    extraction_hint: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        field_type = self.field_type.value

        required = self.required

        description: None | str | Unset
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        extraction_hint: None | str | Unset
        if isinstance(self.extraction_hint, Unset):
            extraction_hint = UNSET
        else:
            extraction_hint = self.extraction_hint

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "field_type": field_type,
            }
        )
        if required is not UNSET:
            field_dict["required"] = required
        if description is not UNSET:
            field_dict["description"] = description
        if extraction_hint is not UNSET:
            field_dict["extraction_hint"] = extraction_hint

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        field_type = MetadataFieldType(d.pop("field_type"))

        required = d.pop("required", UNSET)

        def _parse_description(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        description = _parse_description(d.pop("description", UNSET))

        def _parse_extraction_hint(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        extraction_hint = _parse_extraction_hint(d.pop("extraction_hint", UNSET))

        metadata_field_definition = cls(
            name=name,
            field_type=field_type,
            required=required,
            description=description,
            extraction_hint=extraction_hint,
        )

        metadata_field_definition.additional_properties = d
        return metadata_field_definition

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
