from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.run_summary_by_rule import RunSummaryByRule
    from ..models.run_summary_by_severity import RunSummaryBySeverity


T = TypeVar("T", bound="RunSummary")


@_attrs_define
class RunSummary:
    """
    Attributes:
        total_issues (int):
        by_severity (RunSummaryBySeverity):
        by_rule (RunSummaryByRule):
    """

    total_issues: int
    by_severity: RunSummaryBySeverity
    by_rule: RunSummaryByRule
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        total_issues = self.total_issues

        by_severity = self.by_severity.to_dict()

        by_rule = self.by_rule.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "total_issues": total_issues,
                "by_severity": by_severity,
                "by_rule": by_rule,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.run_summary_by_rule import RunSummaryByRule
        from ..models.run_summary_by_severity import RunSummaryBySeverity

        d = dict(src_dict)
        total_issues = d.pop("total_issues")

        by_severity = RunSummaryBySeverity.from_dict(d.pop("by_severity"))

        by_rule = RunSummaryByRule.from_dict(d.pop("by_rule"))

        run_summary = cls(
            total_issues=total_issues,
            by_severity=by_severity,
            by_rule=by_rule,
        )

        run_summary.additional_properties = d
        return run_summary

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
