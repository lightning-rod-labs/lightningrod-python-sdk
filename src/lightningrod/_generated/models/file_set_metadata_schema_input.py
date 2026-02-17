from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.metadata_field_definition_input import MetadataFieldDefinitionInput


T = TypeVar("T", bound="FileSetMetadataSchemaInput")


@_attrs_define
class FileSetMetadataSchemaInput:
    """Schema definition for file metadata in a FileSet (input/request version).

    Attributes:
        fields (list[MetadataFieldDefinitionInput]): List of metadata field definitions
    """

    fields: list[MetadataFieldDefinitionInput]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        fields = []
        for fields_item_data in self.fields:
            fields_item = fields_item_data.to_dict()
            fields.append(fields_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "fields": fields,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.metadata_field_definition_input import MetadataFieldDefinitionInput

        d = dict(src_dict)
        fields = []
        _fields = d.pop("fields")
        for fields_item_data in _fields:
            fields_item = MetadataFieldDefinitionInput.from_dict(fields_item_data)

            fields.append(fields_item)

        file_set_metadata_schema_input = cls(
            fields=fields,
        )

        file_set_metadata_schema_input.additional_properties = d
        return file_set_metadata_schema_input

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
