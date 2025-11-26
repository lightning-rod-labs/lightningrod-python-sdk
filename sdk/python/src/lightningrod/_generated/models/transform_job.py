from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.transform_job_status import TransformJobStatus

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
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
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

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
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
