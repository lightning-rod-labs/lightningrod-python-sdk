from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.batch_upload_response_upload_urls import BatchUploadResponseUploadUrls
    from ..models.batch_upload_response_uploads import BatchUploadResponseUploads


T = TypeVar("T", bound="BatchUploadResponse")


@_attrs_define
class BatchUploadResponse:
    """
    Attributes:
        folder_path (str): Cloud storage folder where files will be stored
        upload_urls (BatchUploadResponseUploadUrls): Deprecated: filename -> signed URL. Use `uploads` instead.
        uploads (BatchUploadResponseUploads | Unset): filename -> upload target (url, method, headers). Provider-
            agnostic.
    """

    folder_path: str
    upload_urls: BatchUploadResponseUploadUrls
    uploads: BatchUploadResponseUploads | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        folder_path = self.folder_path

        upload_urls = self.upload_urls.to_dict()

        uploads: dict[str, Any] | Unset = UNSET
        if not isinstance(self.uploads, Unset):
            uploads = self.uploads.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "folder_path": folder_path,
                "upload_urls": upload_urls,
            }
        )
        if uploads is not UNSET:
            field_dict["uploads"] = uploads

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.batch_upload_response_upload_urls import BatchUploadResponseUploadUrls
        from ..models.batch_upload_response_uploads import BatchUploadResponseUploads

        d = dict(src_dict)
        folder_path = d.pop("folder_path")

        upload_urls = BatchUploadResponseUploadUrls.from_dict(d.pop("upload_urls"))

        _uploads = d.pop("uploads", UNSET)
        uploads: BatchUploadResponseUploads | Unset
        if isinstance(_uploads, Unset):
            uploads = UNSET
        else:
            uploads = BatchUploadResponseUploads.from_dict(_uploads)

        batch_upload_response = cls(
            folder_path=folder_path,
            upload_urls=upload_urls,
            uploads=uploads,
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
