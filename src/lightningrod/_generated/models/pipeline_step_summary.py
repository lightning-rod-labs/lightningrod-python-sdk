from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.pipeline_step_summary_rejection_reasons import PipelineStepSummaryRejectionReasons


T = TypeVar("T", bound="PipelineStepSummary")


@_attrs_define
class PipelineStepSummary:
    """Summary of a single pipeline step including rejection reasons.

    Attributes:
        step_index (int):
        transform_name (str):
        input_count (int | Unset):  Default: 0.
        output_count (int | Unset):  Default: 0.
        rejected_count (int | Unset):  Default: 0.
        error_count (int | Unset):  Default: 0.
        rejection_reasons (PipelineStepSummaryRejectionReasons | Unset):
    """

    step_index: int
    transform_name: str
    input_count: int | Unset = 0
    output_count: int | Unset = 0
    rejected_count: int | Unset = 0
    error_count: int | Unset = 0
    rejection_reasons: PipelineStepSummaryRejectionReasons | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        step_index = self.step_index

        transform_name = self.transform_name

        input_count = self.input_count

        output_count = self.output_count

        rejected_count = self.rejected_count

        error_count = self.error_count

        rejection_reasons: dict[str, Any] | Unset = UNSET
        if not isinstance(self.rejection_reasons, Unset):
            rejection_reasons = self.rejection_reasons.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "step_index": step_index,
                "transform_name": transform_name,
            }
        )
        if input_count is not UNSET:
            field_dict["input_count"] = input_count
        if output_count is not UNSET:
            field_dict["output_count"] = output_count
        if rejected_count is not UNSET:
            field_dict["rejected_count"] = rejected_count
        if error_count is not UNSET:
            field_dict["error_count"] = error_count
        if rejection_reasons is not UNSET:
            field_dict["rejection_reasons"] = rejection_reasons

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.pipeline_step_summary_rejection_reasons import PipelineStepSummaryRejectionReasons

        d = dict(src_dict)
        step_index = d.pop("step_index")

        transform_name = d.pop("transform_name")

        input_count = d.pop("input_count", UNSET)

        output_count = d.pop("output_count", UNSET)

        rejected_count = d.pop("rejected_count", UNSET)

        error_count = d.pop("error_count", UNSET)

        _rejection_reasons = d.pop("rejection_reasons", UNSET)
        rejection_reasons: PipelineStepSummaryRejectionReasons | Unset
        if isinstance(_rejection_reasons, Unset):
            rejection_reasons = UNSET
        else:
            rejection_reasons = PipelineStepSummaryRejectionReasons.from_dict(_rejection_reasons)

        pipeline_step_summary = cls(
            step_index=step_index,
            transform_name=transform_name,
            input_count=input_count,
            output_count=output_count,
            rejected_count=rejected_count,
            error_count=error_count,
            rejection_reasons=rejection_reasons,
        )

        pipeline_step_summary.additional_properties = d
        return pipeline_step_summary

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
