from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

T = TypeVar("T", bound="DatasetDownloadUrlResponse")


@_attrs_define
class DatasetDownloadUrlResponse:
    """
    Attributes:
        url (str):
        expires_at (datetime.datetime):
        dataset_id (str):
        filename (str):
    """

    url: str
    expires_at: datetime.datetime
    dataset_id: str
    filename: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        url = self.url

        expires_at = self.expires_at.isoformat()

        dataset_id = self.dataset_id

        filename = self.filename

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "url": url,
                "expires_at": expires_at,
                "dataset_id": dataset_id,
                "filename": filename,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        url = d.pop("url")

        expires_at = isoparse(d.pop("expires_at"))

        dataset_id = d.pop("dataset_id")

        filename = d.pop("filename")

        dataset_download_url_response = cls(
            url=url,
            expires_at=expires_at,
            dataset_id=dataset_id,
            filename=filename,
        )

        dataset_download_url_response.additional_properties = d
        return dataset_download_url_response

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
