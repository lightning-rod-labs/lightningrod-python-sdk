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
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
        metadata_schema (FileSetMetadataSchema | None | Unset):
        is_public (bool | Unset):  Default: False.
        cloud_storage_folder (None | str | Unset):
        qdrant_snapshot_path (None | str | Unset):
        qdrant_collection_name (None | str | Unset):
    """

    id: str
    name: str
    description: None | str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    metadata_schema: FileSetMetadataSchema | None | Unset = UNSET
    is_public: bool | Unset = False
    cloud_storage_folder: None | str | Unset = UNSET
    qdrant_snapshot_path: None | str | Unset = UNSET
    qdrant_collection_name: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.file_set_metadata_schema import FileSetMetadataSchema

        id = self.id

        name = self.name

        description: None | str
        description = self.description

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        metadata_schema: dict[str, Any] | None | Unset
        if isinstance(self.metadata_schema, Unset):
            metadata_schema = UNSET
        elif isinstance(self.metadata_schema, FileSetMetadataSchema):
            metadata_schema = self.metadata_schema.to_dict()
        else:
            metadata_schema = self.metadata_schema

        is_public = self.is_public

        cloud_storage_folder: None | str | Unset
        if isinstance(self.cloud_storage_folder, Unset):
            cloud_storage_folder = UNSET
        else:
            cloud_storage_folder = self.cloud_storage_folder

        qdrant_snapshot_path: None | str | Unset
        if isinstance(self.qdrant_snapshot_path, Unset):
            qdrant_snapshot_path = UNSET
        else:
            qdrant_snapshot_path = self.qdrant_snapshot_path

        qdrant_collection_name: None | str | Unset
        if isinstance(self.qdrant_collection_name, Unset):
            qdrant_collection_name = UNSET
        else:
            qdrant_collection_name = self.qdrant_collection_name

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
                "description": description,
                "created_at": created_at,
                "updated_at": updated_at,
            }
        )
        if metadata_schema is not UNSET:
            field_dict["metadata_schema"] = metadata_schema
        if is_public is not UNSET:
            field_dict["is_public"] = is_public
        if cloud_storage_folder is not UNSET:
            field_dict["cloud_storage_folder"] = cloud_storage_folder
        if qdrant_snapshot_path is not UNSET:
            field_dict["qdrant_snapshot_path"] = qdrant_snapshot_path
        if qdrant_collection_name is not UNSET:
            field_dict["qdrant_collection_name"] = qdrant_collection_name

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

        is_public = d.pop("is_public", UNSET)

        def _parse_cloud_storage_folder(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        cloud_storage_folder = _parse_cloud_storage_folder(d.pop("cloud_storage_folder", UNSET))

        def _parse_qdrant_snapshot_path(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        qdrant_snapshot_path = _parse_qdrant_snapshot_path(d.pop("qdrant_snapshot_path", UNSET))

        def _parse_qdrant_collection_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        qdrant_collection_name = _parse_qdrant_collection_name(d.pop("qdrant_collection_name", UNSET))

        file_set = cls(
            id=id,
            name=name,
            description=description,
            created_at=created_at,
            updated_at=updated_at,
            metadata_schema=metadata_schema,
            is_public=is_public,
            cloud_storage_folder=cloud_storage_folder,
            qdrant_snapshot_path=qdrant_snapshot_path,
            qdrant_collection_name=qdrant_collection_name,
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
