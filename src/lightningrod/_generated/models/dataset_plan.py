from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.plan_step import PlanStep


T = TypeVar("T", bound="DatasetPlan")


@_attrs_define
class DatasetPlan:
    """A generated dataset generation plan.

    Attributes:
        domain (str):
        data_sources (list[str]):
        goal (str):
        plan_title (str):
        steps (list[PlanStep]):
        estimated_total_samples (int):
        estimated_time (str):
    """

    domain: str
    data_sources: list[str]
    goal: str
    plan_title: str
    steps: list[PlanStep]
    estimated_total_samples: int
    estimated_time: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        domain = self.domain

        data_sources = self.data_sources

        goal = self.goal

        plan_title = self.plan_title

        steps = []
        for steps_item_data in self.steps:
            steps_item = steps_item_data.to_dict()
            steps.append(steps_item)

        estimated_total_samples = self.estimated_total_samples

        estimated_time = self.estimated_time

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "domain": domain,
                "data_sources": data_sources,
                "goal": goal,
                "plan_title": plan_title,
                "steps": steps,
                "estimated_total_samples": estimated_total_samples,
                "estimated_time": estimated_time,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.plan_step import PlanStep

        d = dict(src_dict)
        domain = d.pop("domain")

        data_sources = cast(list[str], d.pop("data_sources"))

        goal = d.pop("goal")

        plan_title = d.pop("plan_title")

        steps = []
        _steps = d.pop("steps")
        for steps_item_data in _steps:
            steps_item = PlanStep.from_dict(steps_item_data)

            steps.append(steps_item)

        estimated_total_samples = d.pop("estimated_total_samples")

        estimated_time = d.pop("estimated_time")

        dataset_plan = cls(
            domain=domain,
            data_sources=data_sources,
            goal=goal,
            plan_title=plan_title,
            steps=steps,
            estimated_total_samples=estimated_total_samples,
            estimated_time=estimated_time,
        )

        dataset_plan.additional_properties = d
        return dataset_plan

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
