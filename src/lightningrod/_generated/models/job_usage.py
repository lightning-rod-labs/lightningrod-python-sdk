from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.job_usage_by_step_type_0 import JobUsageByStepType0
    from ..models.usage_summary import UsageSummary


T = TypeVar("T", bound="JobUsage")


@_attrs_define
class JobUsage:
    """Aggregated usage statistics for a transform job with step breakdown.

    Attributes:
        total (None | Unset | UsageSummary):
        by_step (JobUsageByStepType0 | None | Unset):
        max_cost_dollars (float | None | Unset):
        current_cost_dollars (float | None | Unset):
        estimated_cost_dollars (float | None | Unset):
    """

    total: None | Unset | UsageSummary = UNSET
    by_step: JobUsageByStepType0 | None | Unset = UNSET
    max_cost_dollars: float | None | Unset = UNSET
    current_cost_dollars: float | None | Unset = UNSET
    estimated_cost_dollars: float | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.job_usage_by_step_type_0 import JobUsageByStepType0
        from ..models.usage_summary import UsageSummary

        total: dict[str, Any] | None | Unset
        if isinstance(self.total, Unset):
            total = UNSET
        elif isinstance(self.total, UsageSummary):
            total = self.total.to_dict()
        else:
            total = self.total

        by_step: dict[str, Any] | None | Unset
        if isinstance(self.by_step, Unset):
            by_step = UNSET
        elif isinstance(self.by_step, JobUsageByStepType0):
            by_step = self.by_step.to_dict()
        else:
            by_step = self.by_step

        max_cost_dollars: float | None | Unset
        if isinstance(self.max_cost_dollars, Unset):
            max_cost_dollars = UNSET
        else:
            max_cost_dollars = self.max_cost_dollars

        current_cost_dollars: float | None | Unset
        if isinstance(self.current_cost_dollars, Unset):
            current_cost_dollars = UNSET
        else:
            current_cost_dollars = self.current_cost_dollars

        estimated_cost_dollars: float | None | Unset
        if isinstance(self.estimated_cost_dollars, Unset):
            estimated_cost_dollars = UNSET
        else:
            estimated_cost_dollars = self.estimated_cost_dollars

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if total is not UNSET:
            field_dict["total"] = total
        if by_step is not UNSET:
            field_dict["by_step"] = by_step
        if max_cost_dollars is not UNSET:
            field_dict["max_cost_dollars"] = max_cost_dollars
        if current_cost_dollars is not UNSET:
            field_dict["current_cost_dollars"] = current_cost_dollars
        if estimated_cost_dollars is not UNSET:
            field_dict["estimated_cost_dollars"] = estimated_cost_dollars

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.job_usage_by_step_type_0 import JobUsageByStepType0
        from ..models.usage_summary import UsageSummary

        d = dict(src_dict)

        def _parse_total(data: object) -> None | Unset | UsageSummary:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                total_type_0 = UsageSummary.from_dict(data)

                return total_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | Unset | UsageSummary, data)

        total = _parse_total(d.pop("total", UNSET))

        def _parse_by_step(data: object) -> JobUsageByStepType0 | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                by_step_type_0 = JobUsageByStepType0.from_dict(data)

                return by_step_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(JobUsageByStepType0 | None | Unset, data)

        by_step = _parse_by_step(d.pop("by_step", UNSET))

        def _parse_max_cost_dollars(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        max_cost_dollars = _parse_max_cost_dollars(d.pop("max_cost_dollars", UNSET))

        def _parse_current_cost_dollars(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        current_cost_dollars = _parse_current_cost_dollars(d.pop("current_cost_dollars", UNSET))

        def _parse_estimated_cost_dollars(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        estimated_cost_dollars = _parse_estimated_cost_dollars(d.pop("estimated_cost_dollars", UNSET))

        job_usage = cls(
            total=total,
            by_step=by_step,
            max_cost_dollars=max_cost_dollars,
            current_cost_dollars=current_cost_dollars,
            estimated_cost_dollars=estimated_cost_dollars,
        )

        job_usage.additional_properties = d
        return job_usage

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
