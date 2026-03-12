from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.create_session_request_autonomy_level_type_0 import CreateSessionRequestAutonomyLevelType0
from ..types import UNSET, Unset

T = TypeVar("T", bound="CreateSessionRequest")


@_attrs_define
class CreateSessionRequest:
    """Request to create a new assistant session.

    Attributes:
        goal (str): What the user wants to accomplish
        autonomy_level (CreateSessionRequestAutonomyLevelType0 | None | Unset): Deprecated. Kept for backward
            compatibility. Default: CreateSessionRequestAutonomyLevelType0.SEMI_AUTO.
        model_name (None | str | Unset): Model to use (e.g., 'anthropic/claude-sonnet-4'). Defaults to configured model.
    """

    goal: str
    autonomy_level: CreateSessionRequestAutonomyLevelType0 | None | Unset = (
        CreateSessionRequestAutonomyLevelType0.SEMI_AUTO
    )
    model_name: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        goal = self.goal

        autonomy_level: None | str | Unset
        if isinstance(self.autonomy_level, Unset):
            autonomy_level = UNSET
        elif isinstance(self.autonomy_level, CreateSessionRequestAutonomyLevelType0):
            autonomy_level = self.autonomy_level.value
        else:
            autonomy_level = self.autonomy_level

        model_name: None | str | Unset
        if isinstance(self.model_name, Unset):
            model_name = UNSET
        else:
            model_name = self.model_name

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "goal": goal,
            }
        )
        if autonomy_level is not UNSET:
            field_dict["autonomy_level"] = autonomy_level
        if model_name is not UNSET:
            field_dict["model_name"] = model_name

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        goal = d.pop("goal")

        def _parse_autonomy_level(data: object) -> CreateSessionRequestAutonomyLevelType0 | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                autonomy_level_type_0 = CreateSessionRequestAutonomyLevelType0(data)

                return autonomy_level_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(CreateSessionRequestAutonomyLevelType0 | None | Unset, data)

        autonomy_level = _parse_autonomy_level(d.pop("autonomy_level", UNSET))

        def _parse_model_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        model_name = _parse_model_name(d.pop("model_name", UNSET))

        create_session_request = cls(
            goal=goal,
            autonomy_level=autonomy_level,
            model_name=model_name,
        )

        create_session_request.additional_properties = d
        return create_session_request

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
