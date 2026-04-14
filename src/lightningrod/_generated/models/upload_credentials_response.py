from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="UploadCredentialsResponse")


@_attrs_define
class UploadCredentialsResponse:
    """
    Attributes:
        token (str): Short-lived OAuth2 access token for GCS uploads
        expiry (str): Token expiry time (ISO 8601)
        bucket (str): GCS bucket name
        folder (str): GCS folder prefix (include trailing slash)
    """

    token: str
    expiry: str
    bucket: str
    folder: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        token = self.token

        expiry = self.expiry

        bucket = self.bucket

        folder = self.folder

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "token": token,
                "expiry": expiry,
                "bucket": bucket,
                "folder": folder,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        token = d.pop("token")

        expiry = d.pop("expiry")

        bucket = d.pop("bucket")

        folder = d.pop("folder")

        upload_credentials_response = cls(
            token=token,
            expiry=expiry,
            bucket=bucket,
            folder=folder,
        )

        upload_credentials_response.additional_properties = d
        return upload_credentials_response

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
