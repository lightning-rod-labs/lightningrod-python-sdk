from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.linter_issue import LinterIssue
    from ..models.rule_result_stats import RuleResultStats


T = TypeVar("T", bound="RuleResult")


@_attrs_define
class RuleResult:
    """
    Attributes:
        name (str):
        stats (RuleResultStats | Unset):
        issues (list[LinterIssue] | Unset):
        duration_ms (int | Unset):  Default: 0.
    """

    name: str
    stats: RuleResultStats | Unset = UNSET
    issues: list[LinterIssue] | Unset = UNSET
    duration_ms: int | Unset = 0
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        stats: dict[str, Any] | Unset = UNSET
        if not isinstance(self.stats, Unset):
            stats = self.stats.to_dict()

        issues: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.issues, Unset):
            issues = []
            for issues_item_data in self.issues:
                issues_item = issues_item_data.to_dict()
                issues.append(issues_item)

        duration_ms = self.duration_ms

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
            }
        )
        if stats is not UNSET:
            field_dict["stats"] = stats
        if issues is not UNSET:
            field_dict["issues"] = issues
        if duration_ms is not UNSET:
            field_dict["duration_ms"] = duration_ms

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.linter_issue import LinterIssue
        from ..models.rule_result_stats import RuleResultStats

        d = dict(src_dict)
        name = d.pop("name")

        _stats = d.pop("stats", UNSET)
        stats: RuleResultStats | Unset
        if isinstance(_stats, Unset):
            stats = UNSET
        else:
            stats = RuleResultStats.from_dict(_stats)

        _issues = d.pop("issues", UNSET)
        issues: list[LinterIssue] | Unset = UNSET
        if _issues is not UNSET:
            issues = []
            for issues_item_data in _issues:
                issues_item = LinterIssue.from_dict(issues_item_data)

                issues.append(issues_item)

        duration_ms = d.pop("duration_ms", UNSET)

        rule_result = cls(
            name=name,
            stats=stats,
            issues=issues,
            duration_ms=duration_ms,
        )

        rule_result.additional_properties = d
        return rule_result

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
