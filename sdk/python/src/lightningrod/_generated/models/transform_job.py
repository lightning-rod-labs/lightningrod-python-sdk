from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.transform_job_status import TransformJobStatus
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.job_usage import JobUsage


T = TypeVar("T", bound="TransformJob")


@_attrs_define
class TransformJob:
    """
    Attributes:
        id (str):
        organization_id (str):
        status (TransformJobStatus):
        modal_function_call_id (str):
        modal_app_id (str):
        transform_config (str):
        input_dataset_id (None | str):
        output_dataset_id (None | str):
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
        configuration_id (None | str | Unset):
        error_message (None | str | Unset):
        usage (JobUsage | None | Unset):
    """

    id: str
    organization_id: str
    status: TransformJobStatus
    modal_function_call_id: str
    modal_app_id: str
    transform_config: str
    input_dataset_id: None | str
    output_dataset_id: None | str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    configuration_id: None | str | Unset = UNSET
    error_message: None | str | Unset = UNSET
    usage: JobUsage | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.job_usage import JobUsage

        id = self.id

        organization_id = self.organization_id

        status = self.status.value

        modal_function_call_id = self.modal_function_call_id

        modal_app_id = self.modal_app_id

        transform_config = self.transform_config

        input_dataset_id: None | str
        input_dataset_id = self.input_dataset_id

        output_dataset_id: None | str
        output_dataset_id = self.output_dataset_id

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        configuration_id: None | str | Unset
        if isinstance(self.configuration_id, Unset):
            configuration_id = UNSET
        else:
            configuration_id = self.configuration_id

        error_message: None | str | Unset
        if isinstance(self.error_message, Unset):
            error_message = UNSET
        else:
            error_message = self.error_message

        usage: dict[str, Any] | None | Unset
        if isinstance(self.usage, Unset):
            usage = UNSET
        elif isinstance(self.usage, JobUsage):
            usage = self.usage.to_dict()
        else:
            usage = self.usage

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "organization_id": organization_id,
                "status": status,
                "modal_function_call_id": modal_function_call_id,
                "modal_app_id": modal_app_id,
                "transform_config": transform_config,
                "input_dataset_id": input_dataset_id,
                "output_dataset_id": output_dataset_id,
                "created_at": created_at,
                "updated_at": updated_at,
            }
        )
        if configuration_id is not UNSET:
            field_dict["configuration_id"] = configuration_id
        if error_message is not UNSET:
            field_dict["error_message"] = error_message
        if usage is not UNSET:
            field_dict["usage"] = usage

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.job_usage import JobUsage

        d = dict(src_dict)
        id = d.pop("id")

        organization_id = d.pop("organization_id")

        status = TransformJobStatus(d.pop("status"))

        modal_function_call_id = d.pop("modal_function_call_id")

        modal_app_id = d.pop("modal_app_id")

        transform_config = d.pop("transform_config")

        def _parse_input_dataset_id(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        input_dataset_id = _parse_input_dataset_id(d.pop("input_dataset_id"))

        def _parse_output_dataset_id(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        output_dataset_id = _parse_output_dataset_id(d.pop("output_dataset_id"))

        created_at = isoparse(d.pop("created_at"))

        updated_at = isoparse(d.pop("updated_at"))

        def _parse_configuration_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        configuration_id = _parse_configuration_id(d.pop("configuration_id", UNSET))

        def _parse_error_message(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        error_message = _parse_error_message(d.pop("error_message", UNSET))

        def _parse_usage(data: object) -> JobUsage | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                usage_type_0 = JobUsage.from_dict(data)

                return usage_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(JobUsage | None | Unset, data)

        usage = _parse_usage(d.pop("usage", UNSET))

        transform_job = cls(
            id=id,
            organization_id=organization_id,
            status=status,
            modal_function_call_id=modal_function_call_id,
            modal_app_id=modal_app_id,
            transform_config=transform_config,
            input_dataset_id=input_dataset_id,
            output_dataset_id=output_dataset_id,
            created_at=created_at,
            updated_at=updated_at,
            configuration_id=configuration_id,
            error_message=error_message,
            usage=usage,
        )

        transform_job.additional_properties = d
        return transform_job

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
