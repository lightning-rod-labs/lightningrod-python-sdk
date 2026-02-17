from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.metadata_field_definition import MetadataFieldDefinition


T = TypeVar("T", bound="FileSetMetadataSchema")


@_attrs_define
class FileSetMetadataSchema:
    """Schema definition for file metadata in a FileSet.

    Attributes:
        fields (list[MetadataFieldDefinition] | Unset): List of metadata field definitions
    """

    fields: list[MetadataFieldDefinition] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        fields: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.fields, Unset):
            fields = []
            for fields_item_data in self.fields:
                fields_item = fields_item_data.to_dict()
                fields.append(fields_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if fields is not UNSET:
            field_dict["fields"] = fields

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.metadata_field_definition import MetadataFieldDefinition

        d = dict(src_dict)
        _fields = d.pop("fields", UNSET)
        fields: list[MetadataFieldDefinition] | Unset = UNSET
        if _fields is not UNSET:
            fields = []
            for fields_item_data in _fields:
                fields_item = MetadataFieldDefinition.from_dict(fields_item_data)

                fields.append(fields_item)

        file_set_metadata_schema = cls(
            fields=fields,
        )

        file_set_metadata_schema.additional_properties = d
        return file_set_metadata_schema

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
