from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.transform_step_metrics_response import TransformStepMetricsResponse


T = TypeVar("T", bound="PipelineMetricsResponse")


@_attrs_define
class PipelineMetricsResponse:
    """
    Attributes:
        total_input_rows (int):
        total_output_rows (int):
        total_duration_seconds (float):
        steps (list[TransformStepMetricsResponse]):
    """

    total_input_rows: int
    total_output_rows: int
    total_duration_seconds: float
    steps: list[TransformStepMetricsResponse]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        total_input_rows = self.total_input_rows

        total_output_rows = self.total_output_rows

        total_duration_seconds = self.total_duration_seconds

        steps = []
        for steps_item_data in self.steps:
            steps_item = steps_item_data.to_dict()
            steps.append(steps_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "total_input_rows": total_input_rows,
                "total_output_rows": total_output_rows,
                "total_duration_seconds": total_duration_seconds,
                "steps": steps,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.transform_step_metrics_response import TransformStepMetricsResponse

        d = dict(src_dict)
        total_input_rows = d.pop("total_input_rows")

        total_output_rows = d.pop("total_output_rows")

        total_duration_seconds = d.pop("total_duration_seconds")

        steps = []
        _steps = d.pop("steps")
        for steps_item_data in _steps:
            steps_item = TransformStepMetricsResponse.from_dict(steps_item_data)

            steps.append(steps_item)

        pipeline_metrics_response = cls(
            total_input_rows=total_input_rows,
            total_output_rows=total_output_rows,
            total_duration_seconds=total_duration_seconds,
            steps=steps,
        )

        pipeline_metrics_response.additional_properties = d
        return pipeline_metrics_response

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
