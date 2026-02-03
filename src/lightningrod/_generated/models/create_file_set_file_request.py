from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.create_file_set_file_request_metadata_type_0 import CreateFileSetFileRequestMetadataType0


T = TypeVar("T", bound="CreateFileSetFileRequest")


@_attrs_define
class CreateFileSetFileRequest:
    """
    Attributes:
        file_id (str): ID of the file
        file_date (datetime.datetime | None | Unset): The date of the document - ensure this is set for documents to be
            used in forward-looking question generation generation pipelines
        metadata (CreateFileSetFileRequestMetadataType0 | None | Unset): Optional file-level metadata
    """

    file_id: str
    file_date: datetime.datetime | None | Unset = UNSET
    metadata: CreateFileSetFileRequestMetadataType0 | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.create_file_set_file_request_metadata_type_0 import CreateFileSetFileRequestMetadataType0

        file_id = self.file_id

        file_date: None | str | Unset
        if isinstance(self.file_date, Unset):
            file_date = UNSET
        elif isinstance(self.file_date, datetime.datetime):
            file_date = self.file_date.isoformat()
        else:
            file_date = self.file_date

        metadata: dict[str, Any] | None | Unset
        if isinstance(self.metadata, Unset):
            metadata = UNSET
        elif isinstance(self.metadata, CreateFileSetFileRequestMetadataType0):
            metadata = self.metadata.to_dict()
        else:
            metadata = self.metadata

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "file_id": file_id,
            }
        )
        if file_date is not UNSET:
            field_dict["file_date"] = file_date
        if metadata is not UNSET:
            field_dict["metadata"] = metadata

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.create_file_set_file_request_metadata_type_0 import CreateFileSetFileRequestMetadataType0

        d = dict(src_dict)
        file_id = d.pop("file_id")

        def _parse_file_date(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                file_date_type_0 = isoparse(data)

                return file_date_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        file_date = _parse_file_date(d.pop("file_date", UNSET))

        def _parse_metadata(data: object) -> CreateFileSetFileRequestMetadataType0 | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                metadata_type_0 = CreateFileSetFileRequestMetadataType0.from_dict(data)

                return metadata_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(CreateFileSetFileRequestMetadataType0 | None | Unset, data)

        metadata = _parse_metadata(d.pop("metadata", UNSET))

        create_file_set_file_request = cls(
            file_id=file_id,
            file_date=file_date,
            metadata=metadata,
        )

        create_file_set_file_request.additional_properties = d
        return create_file_set_file_request

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
