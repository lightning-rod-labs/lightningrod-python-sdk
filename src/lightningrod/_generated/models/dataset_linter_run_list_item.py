from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.dataset_linter_run_status import DatasetLinterRunStatus
from ..types import UNSET, Unset

T = TypeVar("T", bound="DatasetLinterRunListItem")


@_attrs_define
class DatasetLinterRunListItem:
    """
    Attributes:
        id (str):
        dataset_id (str):
        status (DatasetLinterRunStatus):
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
        error_message (None | str | Unset):
        total_issues (int | None | Unset):
    """

    id: str
    dataset_id: str
    status: DatasetLinterRunStatus
    created_at: datetime.datetime
    updated_at: datetime.datetime
    error_message: None | str | Unset = UNSET
    total_issues: int | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        dataset_id = self.dataset_id

        status = self.status.value

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        error_message: None | str | Unset
        if isinstance(self.error_message, Unset):
            error_message = UNSET
        else:
            error_message = self.error_message

        total_issues: int | None | Unset
        if isinstance(self.total_issues, Unset):
            total_issues = UNSET
        else:
            total_issues = self.total_issues

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "dataset_id": dataset_id,
                "status": status,
                "created_at": created_at,
                "updated_at": updated_at,
            }
        )
        if error_message is not UNSET:
            field_dict["error_message"] = error_message
        if total_issues is not UNSET:
            field_dict["total_issues"] = total_issues

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        dataset_id = d.pop("dataset_id")

        status = DatasetLinterRunStatus(d.pop("status"))

        created_at = isoparse(d.pop("created_at"))

        updated_at = isoparse(d.pop("updated_at"))

        def _parse_error_message(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        error_message = _parse_error_message(d.pop("error_message", UNSET))

        def _parse_total_issues(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        total_issues = _parse_total_issues(d.pop("total_issues", UNSET))

        dataset_linter_run_list_item = cls(
            id=id,
            dataset_id=dataset_id,
            status=status,
            created_at=created_at,
            updated_at=updated_at,
            error_message=error_message,
            total_issues=total_issues,
        )

        dataset_linter_run_list_item.additional_properties = d
        return dataset_linter_run_list_item

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
