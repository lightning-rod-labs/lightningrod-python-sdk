from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.create_file_upload_response_metadata_type_0 import CreateFileUploadResponseMetadataType0


T = TypeVar("T", bound="CreateFileUploadResponse")


@_attrs_define
class CreateFileUploadResponse:
    """
    Attributes:
        id (str):
        original_file_name (str):
        cloud_storage_path (str):
        upload_url (str): Signed GCS upload URL for direct upload
        mime_type (None | str):
        size_bytes (int):
        created_at (datetime.datetime):
        expires_at (datetime.datetime): When the upload URL expires
        metadata (CreateFileUploadResponseMetadataType0 | None | Unset): File-level metadata
    """

    id: str
    original_file_name: str
    cloud_storage_path: str
    upload_url: str
    mime_type: None | str
    size_bytes: int
    created_at: datetime.datetime
    expires_at: datetime.datetime
    metadata: CreateFileUploadResponseMetadataType0 | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.create_file_upload_response_metadata_type_0 import CreateFileUploadResponseMetadataType0

        id = self.id

        original_file_name = self.original_file_name

        cloud_storage_path = self.cloud_storage_path

        upload_url = self.upload_url

        mime_type: None | str
        mime_type = self.mime_type

        size_bytes = self.size_bytes

        created_at = self.created_at.isoformat()

        expires_at = self.expires_at.isoformat()

        metadata: dict[str, Any] | None | Unset
        if isinstance(self.metadata, Unset):
            metadata = UNSET
        elif isinstance(self.metadata, CreateFileUploadResponseMetadataType0):
            metadata = self.metadata.to_dict()
        else:
            metadata = self.metadata

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "original_file_name": original_file_name,
                "cloud_storage_path": cloud_storage_path,
                "upload_url": upload_url,
                "mime_type": mime_type,
                "size_bytes": size_bytes,
                "created_at": created_at,
                "expires_at": expires_at,
            }
        )
        if metadata is not UNSET:
            field_dict["metadata"] = metadata

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.create_file_upload_response_metadata_type_0 import CreateFileUploadResponseMetadataType0

        d = dict(src_dict)
        id = d.pop("id")

        original_file_name = d.pop("original_file_name")

        cloud_storage_path = d.pop("cloud_storage_path")

        upload_url = d.pop("upload_url")

        def _parse_mime_type(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        mime_type = _parse_mime_type(d.pop("mime_type"))

        size_bytes = d.pop("size_bytes")

        created_at = isoparse(d.pop("created_at"))

        expires_at = isoparse(d.pop("expires_at"))

        def _parse_metadata(data: object) -> CreateFileUploadResponseMetadataType0 | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                metadata_type_0 = CreateFileUploadResponseMetadataType0.from_dict(data)

                return metadata_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(CreateFileUploadResponseMetadataType0 | None | Unset, data)

        metadata = _parse_metadata(d.pop("metadata", UNSET))

        create_file_upload_response = cls(
            id=id,
            original_file_name=original_file_name,
            cloud_storage_path=cloud_storage_path,
            upload_url=upload_url,
            mime_type=mime_type,
            size_bytes=size_bytes,
            created_at=created_at,
            expires_at=expires_at,
            metadata=metadata,
        )

        create_file_upload_response.additional_properties = d
        return create_file_upload_response

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
