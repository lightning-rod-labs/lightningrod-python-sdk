from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.file_set_file import FileSetFile


T = TypeVar("T", bound="ListFileSetFilesResponse")


@_attrs_define
class ListFileSetFilesResponse:
    """
    Attributes:
        files (list[FileSetFile]):
        has_more (bool):
        total (int):
        next_cursor (None | str | Unset):
    """

    files: list[FileSetFile]
    has_more: bool
    total: int
    next_cursor: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        files = []
        for files_item_data in self.files:
            files_item = files_item_data.to_dict()
            files.append(files_item)

        has_more = self.has_more

        total = self.total

        next_cursor: None | str | Unset
        if isinstance(self.next_cursor, Unset):
            next_cursor = UNSET
        else:
            next_cursor = self.next_cursor

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "files": files,
                "has_more": has_more,
                "total": total,
            }
        )
        if next_cursor is not UNSET:
            field_dict["next_cursor"] = next_cursor

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.file_set_file import FileSetFile

        d = dict(src_dict)
        files = []
        _files = d.pop("files")
        for files_item_data in _files:
            files_item = FileSetFile.from_dict(files_item_data)

            files.append(files_item)

        has_more = d.pop("has_more")

        total = d.pop("total")

        def _parse_next_cursor(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        next_cursor = _parse_next_cursor(d.pop("next_cursor", UNSET))

        list_file_set_files_response = cls(
            files=files,
            has_more=has_more,
            total=total,
            next_cursor=next_cursor,
        )

        list_file_set_files_response.additional_properties = d
        return list_file_set_files_response

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
