from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.dataset_plan import DatasetPlan
    from ..models.onboarding_message import OnboardingMessage


T = TypeVar("T", bound="MessageResponse")


@_attrs_define
class MessageResponse:
    """Response from sending a message.

    Attributes:
        message (OnboardingMessage): A message in the onboarding conversation.
        plan (DatasetPlan | None | Unset):
    """

    message: OnboardingMessage
    plan: DatasetPlan | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.dataset_plan import DatasetPlan

        message = self.message.to_dict()

        plan: dict[str, Any] | None | Unset
        if isinstance(self.plan, Unset):
            plan = UNSET
        elif isinstance(self.plan, DatasetPlan):
            plan = self.plan.to_dict()
        else:
            plan = self.plan

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "message": message,
            }
        )
        if plan is not UNSET:
            field_dict["plan"] = plan

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.dataset_plan import DatasetPlan
        from ..models.onboarding_message import OnboardingMessage

        d = dict(src_dict)
        message = OnboardingMessage.from_dict(d.pop("message"))

        def _parse_plan(data: object) -> DatasetPlan | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                plan_type_0 = DatasetPlan.from_dict(data)

                return plan_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(DatasetPlan | None | Unset, data)

        plan = _parse_plan(d.pop("plan", UNSET))

        message_response = cls(
            message=message,
            plan=plan,
        )

        message_response.additional_properties = d
        return message_response

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
