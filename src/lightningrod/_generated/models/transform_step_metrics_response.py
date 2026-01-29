from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="TransformStepMetricsResponse")


@_attrs_define
class TransformStepMetricsResponse:
    """
    Attributes:
        step_index (int):
        transform_name (str):
        input_rows (int):
        output_rows (int):
        rejected_count (int):
        error_count (int):
        duration_seconds (float):
        progress (float):
        summary (None | str):
    """

    step_index: int
    transform_name: str
    input_rows: int
    output_rows: int
    rejected_count: int
    error_count: int
    duration_seconds: float
    progress: float
    summary: None | str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        step_index = self.step_index

        transform_name = self.transform_name

        input_rows = self.input_rows

        output_rows = self.output_rows

        rejected_count = self.rejected_count

        error_count = self.error_count

        duration_seconds = self.duration_seconds

        progress = self.progress

        summary: None | str
        summary = self.summary

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "step_index": step_index,
                "transform_name": transform_name,
                "input_rows": input_rows,
                "output_rows": output_rows,
                "rejected_count": rejected_count,
                "error_count": error_count,
                "duration_seconds": duration_seconds,
                "progress": progress,
                "summary": summary,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        step_index = d.pop("step_index")

        transform_name = d.pop("transform_name")

        input_rows = d.pop("input_rows")

        output_rows = d.pop("output_rows")

        rejected_count = d.pop("rejected_count")

        error_count = d.pop("error_count")

        duration_seconds = d.pop("duration_seconds")

        progress = d.pop("progress")

        def _parse_summary(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        summary = _parse_summary(d.pop("summary"))

        transform_step_metrics_response = cls(
            step_index=step_index,
            transform_name=transform_name,
            input_rows=input_rows,
            output_rows=output_rows,
            rejected_count=rejected_count,
            error_count=error_count,
            duration_seconds=duration_seconds,
            progress=progress,
            summary=summary,
        )

        transform_step_metrics_response.additional_properties = d
        return transform_step_metrics_response

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
