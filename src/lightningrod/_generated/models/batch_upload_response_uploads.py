from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.file_upload_target import FileUploadTarget


T = TypeVar("T", bound="BatchUploadResponseUploads")


@_attrs_define
class BatchUploadResponseUploads:
    """filename -> upload target (url, method, headers). Provider-agnostic."""

    additional_properties: dict[str, FileUploadTarget] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:

        field_dict: dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            field_dict[prop_name] = prop.to_dict()

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.file_upload_target import FileUploadTarget

        d = dict(src_dict)
        batch_upload_response_uploads = cls()

        additional_properties = {}
        for prop_name, prop_dict in d.items():
            additional_property = FileUploadTarget.from_dict(prop_dict)

            additional_properties[prop_name] = additional_property

        batch_upload_response_uploads.additional_properties = additional_properties
        return batch_upload_response_uploads

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> FileUploadTarget:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: FileUploadTarget) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
