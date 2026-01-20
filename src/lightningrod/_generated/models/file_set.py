from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="FileSet")


@_attrs_define
class FileSet:
    """
    Attributes:
        id (str):
        name (str):
        description (None | str):
        file_count (int):
        indexed_file_count (int):
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
        is_public (bool | Unset):  Default: False.
    """

    id: str
    name: str
    description: None | str
    file_count: int
    indexed_file_count: int
    created_at: datetime.datetime
    updated_at: datetime.datetime
    is_public: bool | Unset = False
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        name = self.name

        description: None | str
        description = self.description

        file_count = self.file_count

        indexed_file_count = self.indexed_file_count

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        is_public = self.is_public

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
                "description": description,
                "file_count": file_count,
                "indexed_file_count": indexed_file_count,
                "created_at": created_at,
                "updated_at": updated_at,
            }
        )
        if is_public is not UNSET:
            field_dict["is_public"] = is_public

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        name = d.pop("name")

        def _parse_description(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        description = _parse_description(d.pop("description"))

        file_count = d.pop("file_count")

        indexed_file_count = d.pop("indexed_file_count")

        created_at = isoparse(d.pop("created_at"))

        updated_at = isoparse(d.pop("updated_at"))

        is_public = d.pop("is_public", UNSET)

        file_set = cls(
            id=id,
            name=name,
            description=description,
            file_count=file_count,
            indexed_file_count=indexed_file_count,
            created_at=created_at,
            updated_at=updated_at,
            is_public=is_public,
        )

        file_set.additional_properties = d
        return file_set

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
