from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.dataset_linter_run_status import DatasetLinterRunStatus
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.rule_result import RuleResult
    from ..models.run_summary import RunSummary


T = TypeVar("T", bound="DatasetLinterRunResponse")


@_attrs_define
class DatasetLinterRunResponse:
    """
    Attributes:
        id (str):
        dataset_id (str):
        status (DatasetLinterRunStatus):
        rules_requested (list[str]):
        sample_size (int | None):
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
        error_message (None | str | Unset):
        summary (None | RunSummary | Unset):
        rules (list[RuleResult] | Unset):
    """

    id: str
    dataset_id: str
    status: DatasetLinterRunStatus
    rules_requested: list[str]
    sample_size: int | None
    created_at: datetime.datetime
    updated_at: datetime.datetime
    error_message: None | str | Unset = UNSET
    summary: None | RunSummary | Unset = UNSET
    rules: list[RuleResult] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.run_summary import RunSummary

        id = self.id

        dataset_id = self.dataset_id

        status = self.status.value

        rules_requested = self.rules_requested

        sample_size: int | None
        sample_size = self.sample_size

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        error_message: None | str | Unset
        if isinstance(self.error_message, Unset):
            error_message = UNSET
        else:
            error_message = self.error_message

        summary: dict[str, Any] | None | Unset
        if isinstance(self.summary, Unset):
            summary = UNSET
        elif isinstance(self.summary, RunSummary):
            summary = self.summary.to_dict()
        else:
            summary = self.summary

        rules: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.rules, Unset):
            rules = []
            for rules_item_data in self.rules:
                rules_item = rules_item_data.to_dict()
                rules.append(rules_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "dataset_id": dataset_id,
                "status": status,
                "rules_requested": rules_requested,
                "sample_size": sample_size,
                "created_at": created_at,
                "updated_at": updated_at,
            }
        )
        if error_message is not UNSET:
            field_dict["error_message"] = error_message
        if summary is not UNSET:
            field_dict["summary"] = summary
        if rules is not UNSET:
            field_dict["rules"] = rules

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.rule_result import RuleResult
        from ..models.run_summary import RunSummary

        d = dict(src_dict)
        id = d.pop("id")

        dataset_id = d.pop("dataset_id")

        status = DatasetLinterRunStatus(d.pop("status"))

        rules_requested = cast(list[str], d.pop("rules_requested"))

        def _parse_sample_size(data: object) -> int | None:
            if data is None:
                return data
            return cast(int | None, data)

        sample_size = _parse_sample_size(d.pop("sample_size"))

        created_at = isoparse(d.pop("created_at"))

        updated_at = isoparse(d.pop("updated_at"))

        def _parse_error_message(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        error_message = _parse_error_message(d.pop("error_message", UNSET))

        def _parse_summary(data: object) -> None | RunSummary | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                summary_type_0 = RunSummary.from_dict(data)

                return summary_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | RunSummary | Unset, data)

        summary = _parse_summary(d.pop("summary", UNSET))

        _rules = d.pop("rules", UNSET)
        rules: list[RuleResult] | Unset = UNSET
        if _rules is not UNSET:
            rules = []
            for rules_item_data in _rules:
                rules_item = RuleResult.from_dict(rules_item_data)

                rules.append(rules_item)

        dataset_linter_run_response = cls(
            id=id,
            dataset_id=dataset_id,
            status=status,
            rules_requested=rules_requested,
            sample_size=sample_size,
            created_at=created_at,
            updated_at=updated_at,
            error_message=error_message,
            summary=summary,
            rules=rules,
        )

        dataset_linter_run_response.additional_properties = d
        return dataset_linter_run_response

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
