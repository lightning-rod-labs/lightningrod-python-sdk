from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.file_upload_target_headers import FileUploadTargetHeaders


T = TypeVar("T", bound="FileUploadTarget")


@_attrs_define
class FileUploadTarget:
    """Provider-agnostic upload instruction. The client issues `method` to `url`
    with exactly these `headers` (the Content-Type must match the signature).

        Attributes:
            url (str): Pre-signed upload URL (GCS or S3)
            method (str | Unset): HTTP method to use for the upload Default: 'PUT'.
            headers (FileUploadTargetHeaders | Unset): Headers that must accompany the upload request
    """

    url: str
    method: str | Unset = "PUT"
    headers: FileUploadTargetHeaders | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        url = self.url

        method = self.method

        headers: dict[str, Any] | Unset = UNSET
        if not isinstance(self.headers, Unset):
            headers = self.headers.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "url": url,
            }
        )
        if method is not UNSET:
            field_dict["method"] = method
        if headers is not UNSET:
            field_dict["headers"] = headers

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.file_upload_target_headers import FileUploadTargetHeaders

        d = dict(src_dict)
        url = d.pop("url")

        method = d.pop("method", UNSET)

        _headers = d.pop("headers", UNSET)
        headers: FileUploadTargetHeaders | Unset
        if isinstance(_headers, Unset):
            headers = UNSET
        else:
            headers = FileUploadTargetHeaders.from_dict(_headers)

        file_upload_target = cls(
            url=url,
            method=method,
            headers=headers,
        )

        file_upload_target.additional_properties = d
        return file_upload_target

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
