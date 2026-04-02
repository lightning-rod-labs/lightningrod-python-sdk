from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.file_set_metadata_schema import FileSetMetadataSchema


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
        metadata_schema (FileSetMetadataSchema | None | Unset):
        rag_enabled (bool | Unset):  Default: True.
        is_public (bool | Unset):  Default: False.
    """

    id: str
    name: str
    description: None | str
    file_count: int
    indexed_file_count: int
    created_at: datetime.datetime
    updated_at: datetime.datetime
    metadata_schema: FileSetMetadataSchema | None | Unset = UNSET
    rag_enabled: bool | Unset = True
    is_public: bool | Unset = False
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.file_set_metadata_schema import FileSetMetadataSchema

        id = self.id

        name = self.name

        description: None | str
        description = self.description

        file_count = self.file_count

        indexed_file_count = self.indexed_file_count

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        metadata_schema: dict[str, Any] | None | Unset
        if isinstance(self.metadata_schema, Unset):
            metadata_schema = UNSET
        elif isinstance(self.metadata_schema, FileSetMetadataSchema):
            metadata_schema = self.metadata_schema.to_dict()
        else:
            metadata_schema = self.metadata_schema

        rag_enabled = self.rag_enabled

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
        if metadata_schema is not UNSET:
            field_dict["metadata_schema"] = metadata_schema
        if rag_enabled is not UNSET:
            field_dict["rag_enabled"] = rag_enabled
        if is_public is not UNSET:
            field_dict["is_public"] = is_public

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.file_set_metadata_schema import FileSetMetadataSchema

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

        def _parse_metadata_schema(data: object) -> FileSetMetadataSchema | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                metadata_schema_type_0 = FileSetMetadataSchema.from_dict(data)

                return metadata_schema_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(FileSetMetadataSchema | None | Unset, data)

        metadata_schema = _parse_metadata_schema(d.pop("metadata_schema", UNSET))

        rag_enabled = d.pop("rag_enabled", UNSET)

        is_public = d.pop("is_public", UNSET)

        file_set = cls(
            id=id,
            name=name,
            description=description,
            file_count=file_count,
            indexed_file_count=indexed_file_count,
            created_at=created_at,
            updated_at=updated_at,
            metadata_schema=metadata_schema,
            rag_enabled=rag_enabled,
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
