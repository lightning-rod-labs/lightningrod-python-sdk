from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.severity import Severity
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.linter_issue_meta import LinterIssueMeta


T = TypeVar("T", bound="LinterIssue")


@_attrs_define
class LinterIssue:
    """
    Attributes:
        rule (str):
        severity (Severity):
        message (str):
        tip (None | str | Unset):
        affected_sample_ids (list[str] | Unset):
        meta (LinterIssueMeta | Unset):
    """

    rule: str
    severity: Severity
    message: str
    tip: None | str | Unset = UNSET
    affected_sample_ids: list[str] | Unset = UNSET
    meta: LinterIssueMeta | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        rule = self.rule

        severity = self.severity.value

        message = self.message

        tip: None | str | Unset
        if isinstance(self.tip, Unset):
            tip = UNSET
        else:
            tip = self.tip

        affected_sample_ids: list[str] | Unset = UNSET
        if not isinstance(self.affected_sample_ids, Unset):
            affected_sample_ids = self.affected_sample_ids

        meta: dict[str, Any] | Unset = UNSET
        if not isinstance(self.meta, Unset):
            meta = self.meta.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "rule": rule,
                "severity": severity,
                "message": message,
            }
        )
        if tip is not UNSET:
            field_dict["tip"] = tip
        if affected_sample_ids is not UNSET:
            field_dict["affected_sample_ids"] = affected_sample_ids
        if meta is not UNSET:
            field_dict["meta"] = meta

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.linter_issue_meta import LinterIssueMeta

        d = dict(src_dict)
        rule = d.pop("rule")

        severity = Severity(d.pop("severity"))

        message = d.pop("message")

        def _parse_tip(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        tip = _parse_tip(d.pop("tip", UNSET))

        affected_sample_ids = cast(list[str], d.pop("affected_sample_ids", UNSET))

        _meta = d.pop("meta", UNSET)
        meta: LinterIssueMeta | Unset
        if isinstance(_meta, Unset):
            meta = UNSET
        else:
            meta = LinterIssueMeta.from_dict(_meta)

        linter_issue = cls(
            rule=rule,
            severity=severity,
            message=message,
            tip=tip,
            affected_sample_ids=affected_sample_ids,
            meta=meta,
        )

        linter_issue.additional_properties = d
        return linter_issue

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
