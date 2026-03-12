from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.onboarding_message_role import OnboardingMessageRole
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.dataset_plan import DatasetPlan
    from ..models.structured_question import StructuredQuestion


T = TypeVar("T", bound="OnboardingMessage")


@_attrs_define
class OnboardingMessage:
    """A message in the onboarding conversation.

    Attributes:
        role (OnboardingMessageRole): Who sent the message
        content (str):
        timestamp (datetime.datetime):
        structured_question (None | StructuredQuestion | Unset):
        dataset_plan (DatasetPlan | None | Unset):
    """

    role: OnboardingMessageRole
    content: str
    timestamp: datetime.datetime
    structured_question: None | StructuredQuestion | Unset = UNSET
    dataset_plan: DatasetPlan | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.dataset_plan import DatasetPlan
        from ..models.structured_question import StructuredQuestion

        role = self.role.value

        content = self.content

        timestamp = self.timestamp.isoformat()

        structured_question: dict[str, Any] | None | Unset
        if isinstance(self.structured_question, Unset):
            structured_question = UNSET
        elif isinstance(self.structured_question, StructuredQuestion):
            structured_question = self.structured_question.to_dict()
        else:
            structured_question = self.structured_question

        dataset_plan: dict[str, Any] | None | Unset
        if isinstance(self.dataset_plan, Unset):
            dataset_plan = UNSET
        elif isinstance(self.dataset_plan, DatasetPlan):
            dataset_plan = self.dataset_plan.to_dict()
        else:
            dataset_plan = self.dataset_plan

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "role": role,
                "content": content,
                "timestamp": timestamp,
            }
        )
        if structured_question is not UNSET:
            field_dict["structured_question"] = structured_question
        if dataset_plan is not UNSET:
            field_dict["dataset_plan"] = dataset_plan

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.dataset_plan import DatasetPlan
        from ..models.structured_question import StructuredQuestion

        d = dict(src_dict)
        role = OnboardingMessageRole(d.pop("role"))

        content = d.pop("content")

        timestamp = isoparse(d.pop("timestamp"))

        def _parse_structured_question(data: object) -> None | StructuredQuestion | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                structured_question_type_0 = StructuredQuestion.from_dict(data)

                return structured_question_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | StructuredQuestion | Unset, data)

        structured_question = _parse_structured_question(d.pop("structured_question", UNSET))

        def _parse_dataset_plan(data: object) -> DatasetPlan | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                dataset_plan_type_0 = DatasetPlan.from_dict(data)

                return dataset_plan_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(DatasetPlan | None | Unset, data)

        dataset_plan = _parse_dataset_plan(d.pop("dataset_plan", UNSET))

        onboarding_message = cls(
            role=role,
            content=content,
            timestamp=timestamp,
            structured_question=structured_question,
            dataset_plan=dataset_plan,
        )

        onboarding_message.additional_properties = d
        return onboarding_message

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
