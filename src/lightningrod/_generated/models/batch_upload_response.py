from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.batch_upload_response_upload_urls import BatchUploadResponseUploadUrls


T = TypeVar("T", bound="BatchUploadResponse")


@_attrs_define
class BatchUploadResponse:
    """
    Attributes:
        folder_path (str): GCS folder path where files will be stored
        upload_urls (BatchUploadResponseUploadUrls): Mapping of filename -> signed upload URL
    """

    folder_path: str
    upload_urls: BatchUploadResponseUploadUrls
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        folder_path = self.folder_path

        upload_urls = self.upload_urls.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "folder_path": folder_path,
                "upload_urls": upload_urls,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.batch_upload_response_upload_urls import BatchUploadResponseUploadUrls

        d = dict(src_dict)
        folder_path = d.pop("folder_path")

        upload_urls = BatchUploadResponseUploadUrls.from_dict(d.pop("upload_urls"))

        batch_upload_response = cls(
            folder_path=folder_path,
            upload_urls=upload_urls,
        )

        batch_upload_response.additional_properties = d
        return batch_upload_response

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
