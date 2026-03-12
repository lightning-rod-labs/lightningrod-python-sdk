from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.dataset_plan import DatasetPlan
    from ..models.onboarding_message import OnboardingMessage


T = TypeVar("T", bound="SessionResponse")


@_attrs_define
class SessionResponse:
    """Response containing onboarding session state.

    Attributes:
        session_id (str):
        created_at (datetime.datetime):
        messages (list[OnboardingMessage] | Unset):
        plan (DatasetPlan | None | Unset):
        fulfillment_type (None | str | Unset):
    """

    session_id: str
    created_at: datetime.datetime
    messages: list[OnboardingMessage] | Unset = UNSET
    plan: DatasetPlan | None | Unset = UNSET
    fulfillment_type: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.dataset_plan import DatasetPlan

        session_id = self.session_id

        created_at = self.created_at.isoformat()

        messages: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.messages, Unset):
            messages = []
            for messages_item_data in self.messages:
                messages_item = messages_item_data.to_dict()
                messages.append(messages_item)

        plan: dict[str, Any] | None | Unset
        if isinstance(self.plan, Unset):
            plan = UNSET
        elif isinstance(self.plan, DatasetPlan):
            plan = self.plan.to_dict()
        else:
            plan = self.plan

        fulfillment_type: None | str | Unset
        if isinstance(self.fulfillment_type, Unset):
            fulfillment_type = UNSET
        else:
            fulfillment_type = self.fulfillment_type

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "session_id": session_id,
                "created_at": created_at,
            }
        )
        if messages is not UNSET:
            field_dict["messages"] = messages
        if plan is not UNSET:
            field_dict["plan"] = plan
        if fulfillment_type is not UNSET:
            field_dict["fulfillment_type"] = fulfillment_type

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.dataset_plan import DatasetPlan
        from ..models.onboarding_message import OnboardingMessage

        d = dict(src_dict)
        session_id = d.pop("session_id")

        created_at = isoparse(d.pop("created_at"))

        _messages = d.pop("messages", UNSET)
        messages: list[OnboardingMessage] | Unset = UNSET
        if _messages is not UNSET:
            messages = []
            for messages_item_data in _messages:
                messages_item = OnboardingMessage.from_dict(messages_item_data)

                messages.append(messages_item)

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

        def _parse_fulfillment_type(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        fulfillment_type = _parse_fulfillment_type(d.pop("fulfillment_type", UNSET))

        session_response = cls(
            session_id=session_id,
            created_at=created_at,
            messages=messages,
            plan=plan,
            fulfillment_type=fulfillment_type,
        )

        session_response.additional_properties = d
        return session_response

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
