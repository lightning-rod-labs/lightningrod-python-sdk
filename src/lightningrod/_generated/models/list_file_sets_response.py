from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.file_set import FileSet


T = TypeVar("T", bound="ListFileSetsResponse")


@_attrs_define
class ListFileSetsResponse:
    """
    Attributes:
        file_sets (list[FileSet]):
    """

    file_sets: list[FileSet]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        file_sets = []
        for file_sets_item_data in self.file_sets:
            file_sets_item = file_sets_item_data.to_dict()
            file_sets.append(file_sets_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "file_sets": file_sets,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.file_set import FileSet

        d = dict(src_dict)
        file_sets = []
        _file_sets = d.pop("file_sets")
        for file_sets_item_data in _file_sets:
            file_sets_item = FileSet.from_dict(file_sets_item_data)

            file_sets.append(file_sets_item)

        list_file_sets_response = cls(
            file_sets=file_sets,
        )

        list_file_sets_response.additional_properties = d
        return list_file_sets_response

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
