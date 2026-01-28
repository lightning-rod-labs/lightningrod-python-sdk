from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

if TYPE_CHECKING:
    from ..models.file_set_file_metadata_type_0 import FileSetFileMetadataType0


T = TypeVar("T", bound="FileSetFile")


@_attrs_define
class FileSetFile:
    """
    Attributes:
        id (str):
        original_file_name (str):
        cloud_storage_path (str):
        mime_type (None | str):
        size_bytes (int):
        character_count (int | None):
        metadata (FileSetFileMetadataType0 | None):
        gemini_file_id (None | str):
        file_created_date (datetime.datetime | None):
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
    """

    id: str
    original_file_name: str
    cloud_storage_path: str
    mime_type: None | str
    size_bytes: int
    character_count: int | None
    metadata: FileSetFileMetadataType0 | None
    gemini_file_id: None | str
    file_created_date: datetime.datetime | None
    created_at: datetime.datetime
    updated_at: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.file_set_file_metadata_type_0 import FileSetFileMetadataType0

        id = self.id

        original_file_name = self.original_file_name

        cloud_storage_path = self.cloud_storage_path

        mime_type: None | str
        mime_type = self.mime_type

        size_bytes = self.size_bytes

        character_count: int | None
        character_count = self.character_count

        metadata: dict[str, Any] | None
        if isinstance(self.metadata, FileSetFileMetadataType0):
            metadata = self.metadata.to_dict()
        else:
            metadata = self.metadata

        gemini_file_id: None | str
        gemini_file_id = self.gemini_file_id

        file_created_date: None | str
        if isinstance(self.file_created_date, datetime.datetime):
            file_created_date = self.file_created_date.isoformat()
        else:
            file_created_date = self.file_created_date

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "original_file_name": original_file_name,
                "cloud_storage_path": cloud_storage_path,
                "mime_type": mime_type,
                "size_bytes": size_bytes,
                "character_count": character_count,
                "metadata": metadata,
                "gemini_file_id": gemini_file_id,
                "file_created_date": file_created_date,
                "created_at": created_at,
                "updated_at": updated_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.file_set_file_metadata_type_0 import FileSetFileMetadataType0

        d = dict(src_dict)
        id = d.pop("id")

        original_file_name = d.pop("original_file_name")

        cloud_storage_path = d.pop("cloud_storage_path")

        def _parse_mime_type(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        mime_type = _parse_mime_type(d.pop("mime_type"))

        size_bytes = d.pop("size_bytes")

        def _parse_character_count(data: object) -> int | None:
            if data is None:
                return data
            return cast(int | None, data)

        character_count = _parse_character_count(d.pop("character_count"))

        def _parse_metadata(data: object) -> FileSetFileMetadataType0 | None:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                metadata_type_0 = FileSetFileMetadataType0.from_dict(data)

                return metadata_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(FileSetFileMetadataType0 | None, data)

        metadata = _parse_metadata(d.pop("metadata"))

        def _parse_gemini_file_id(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        gemini_file_id = _parse_gemini_file_id(d.pop("gemini_file_id"))

        def _parse_file_created_date(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                file_created_date_type_0 = isoparse(data)

                return file_created_date_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        file_created_date = _parse_file_created_date(d.pop("file_created_date"))

        created_at = isoparse(d.pop("created_at"))

        updated_at = isoparse(d.pop("updated_at"))

        file_set_file = cls(
            id=id,
            original_file_name=original_file_name,
            cloud_storage_path=cloud_storage_path,
            mime_type=mime_type,
            size_bytes=size_bytes,
            character_count=character_count,
            metadata=metadata,
            gemini_file_id=gemini_file_id,
            file_created_date=file_created_date,
            created_at=created_at,
            updated_at=updated_at,
        )

        file_set_file.additional_properties = d
        return file_set_file

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
