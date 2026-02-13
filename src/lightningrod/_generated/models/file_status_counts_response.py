from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="FileStatusCountsResponse")


@_attrs_define
class FileStatusCountsResponse:
    """
    Attributes:
        pending (int | Unset): Files awaiting processing Default: 0.
        processing (int | Unset): Files currently being processed Default: 0.
        active (int | Unset): Successfully processed files Default: 0.
        failed (int | Unset): Files that failed processing Default: 0.
    """

    pending: int | Unset = 0
    processing: int | Unset = 0
    active: int | Unset = 0
    failed: int | Unset = 0
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        pending = self.pending

        processing = self.processing

        active = self.active

        failed = self.failed

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if pending is not UNSET:
            field_dict["pending"] = pending
        if processing is not UNSET:
            field_dict["processing"] = processing
        if active is not UNSET:
            field_dict["active"] = active
        if failed is not UNSET:
            field_dict["failed"] = failed

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        pending = d.pop("pending", UNSET)

        processing = d.pop("processing", UNSET)

        active = d.pop("active", UNSET)

        failed = d.pop("failed", UNSET)

        file_status_counts_response = cls(
            pending=pending,
            processing=processing,
            active=active,
            failed=failed,
        )

        file_status_counts_response.additional_properties = d
        return file_status_counts_response

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
