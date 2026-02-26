from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.training_job_status import TrainingJobStatus
from ..types import UNSET, Unset

T = TypeVar("T", bound="TrainingJob")


@_attrs_define
class TrainingJob:
    """
    Attributes:
        id (str):
        organization_id (str):
        status (TrainingJobStatus):
        modal_function_call_id (str):
        modal_app_id (str):
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
        tinker_checkpoint_path (None | str | Unset):
        reward_history (list[float] | None | Unset):
        current_step (int | None | Unset):
        total_steps (int | None | Unset):
        input_dataset_id (None | str | Unset):
        dataset_path (None | str | Unset):
        name (None | str | Unset):
        error_message (None | str | Unset):
    """

    id: str
    organization_id: str
    status: TrainingJobStatus
    modal_function_call_id: str
    modal_app_id: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    tinker_checkpoint_path: None | str | Unset = UNSET
    reward_history: list[float] | None | Unset = UNSET
    current_step: int | None | Unset = UNSET
    total_steps: int | None | Unset = UNSET
    input_dataset_id: None | str | Unset = UNSET
    dataset_path: None | str | Unset = UNSET
    name: None | str | Unset = UNSET
    error_message: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        organization_id = self.organization_id

        status = self.status.value

        modal_function_call_id = self.modal_function_call_id

        modal_app_id = self.modal_app_id

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        tinker_checkpoint_path: None | str | Unset
        if isinstance(self.tinker_checkpoint_path, Unset):
            tinker_checkpoint_path = UNSET
        else:
            tinker_checkpoint_path = self.tinker_checkpoint_path

        reward_history: list[float] | None | Unset
        if isinstance(self.reward_history, Unset):
            reward_history = UNSET
        elif isinstance(self.reward_history, list):
            reward_history = self.reward_history

        else:
            reward_history = self.reward_history

        current_step: int | None | Unset
        if isinstance(self.current_step, Unset):
            current_step = UNSET
        else:
            current_step = self.current_step

        total_steps: int | None | Unset
        if isinstance(self.total_steps, Unset):
            total_steps = UNSET
        else:
            total_steps = self.total_steps

        input_dataset_id: None | str | Unset
        if isinstance(self.input_dataset_id, Unset):
            input_dataset_id = UNSET
        else:
            input_dataset_id = self.input_dataset_id

        dataset_path: None | str | Unset
        if isinstance(self.dataset_path, Unset):
            dataset_path = UNSET
        else:
            dataset_path = self.dataset_path

        name: None | str | Unset
        if isinstance(self.name, Unset):
            name = UNSET
        else:
            name = self.name

        error_message: None | str | Unset
        if isinstance(self.error_message, Unset):
            error_message = UNSET
        else:
            error_message = self.error_message

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "organization_id": organization_id,
                "status": status,
                "modal_function_call_id": modal_function_call_id,
                "modal_app_id": modal_app_id,
                "created_at": created_at,
                "updated_at": updated_at,
            }
        )
        if tinker_checkpoint_path is not UNSET:
            field_dict["tinker_checkpoint_path"] = tinker_checkpoint_path
        if reward_history is not UNSET:
            field_dict["reward_history"] = reward_history
        if current_step is not UNSET:
            field_dict["current_step"] = current_step
        if total_steps is not UNSET:
            field_dict["total_steps"] = total_steps
        if input_dataset_id is not UNSET:
            field_dict["input_dataset_id"] = input_dataset_id
        if dataset_path is not UNSET:
            field_dict["dataset_path"] = dataset_path
        if name is not UNSET:
            field_dict["name"] = name
        if error_message is not UNSET:
            field_dict["error_message"] = error_message

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        organization_id = d.pop("organization_id")

        status = TrainingJobStatus(d.pop("status"))

        modal_function_call_id = d.pop("modal_function_call_id")

        modal_app_id = d.pop("modal_app_id")

        created_at = isoparse(d.pop("created_at"))

        updated_at = isoparse(d.pop("updated_at"))

        def _parse_tinker_checkpoint_path(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        tinker_checkpoint_path = _parse_tinker_checkpoint_path(d.pop("tinker_checkpoint_path", UNSET))

        def _parse_reward_history(data: object) -> list[float] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                reward_history_type_0 = cast(list[float], data)

                return reward_history_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[float] | None | Unset, data)

        reward_history = _parse_reward_history(d.pop("reward_history", UNSET))

        def _parse_current_step(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        current_step = _parse_current_step(d.pop("current_step", UNSET))

        def _parse_total_steps(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        total_steps = _parse_total_steps(d.pop("total_steps", UNSET))

        def _parse_input_dataset_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        input_dataset_id = _parse_input_dataset_id(d.pop("input_dataset_id", UNSET))

        def _parse_dataset_path(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        dataset_path = _parse_dataset_path(d.pop("dataset_path", UNSET))

        def _parse_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        name = _parse_name(d.pop("name", UNSET))

        def _parse_error_message(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        error_message = _parse_error_message(d.pop("error_message", UNSET))

        training_job = cls(
            id=id,
            organization_id=organization_id,
            status=status,
            modal_function_call_id=modal_function_call_id,
            modal_app_id=modal_app_id,
            created_at=created_at,
            updated_at=updated_at,
            tinker_checkpoint_path=tinker_checkpoint_path,
            reward_history=reward_history,
            current_step=current_step,
            total_steps=total_steps,
            input_dataset_id=input_dataset_id,
            dataset_path=dataset_path,
            name=name,
            error_message=error_message,
        )

        training_job.additional_properties = d
        return training_job

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
