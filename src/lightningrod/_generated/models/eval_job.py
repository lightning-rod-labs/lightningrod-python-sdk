from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.eval_job_status import EvalJobStatus
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.eval_job_metrics_type_0 import EvalJobMetricsType0


T = TypeVar("T", bound="EvalJob")


@_attrs_define
class EvalJob:
    """
    Attributes:
        id (str):
        organization_id (str):
        model_id (str):
        status (EvalJobStatus):
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
        test_dataset_id (None | str | Unset):
        dataset_hf_repo (None | str | Unset):
        benchmark_model_id (None | str | Unset):
        metrics (EvalJobMetricsType0 | None | Unset):
        error_message (None | str | Unset):
    """

    id: str
    organization_id: str
    model_id: str
    status: EvalJobStatus
    created_at: datetime.datetime
    updated_at: datetime.datetime
    test_dataset_id: None | str | Unset = UNSET
    dataset_hf_repo: None | str | Unset = UNSET
    benchmark_model_id: None | str | Unset = UNSET
    metrics: EvalJobMetricsType0 | None | Unset = UNSET
    error_message: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.eval_job_metrics_type_0 import EvalJobMetricsType0

        id = self.id

        organization_id = self.organization_id

        model_id = self.model_id

        status = self.status.value

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        test_dataset_id: None | str | Unset
        if isinstance(self.test_dataset_id, Unset):
            test_dataset_id = UNSET
        else:
            test_dataset_id = self.test_dataset_id

        dataset_hf_repo: None | str | Unset
        if isinstance(self.dataset_hf_repo, Unset):
            dataset_hf_repo = UNSET
        else:
            dataset_hf_repo = self.dataset_hf_repo

        benchmark_model_id: None | str | Unset
        if isinstance(self.benchmark_model_id, Unset):
            benchmark_model_id = UNSET
        else:
            benchmark_model_id = self.benchmark_model_id

        metrics: dict[str, Any] | None | Unset
        if isinstance(self.metrics, Unset):
            metrics = UNSET
        elif isinstance(self.metrics, EvalJobMetricsType0):
            metrics = self.metrics.to_dict()
        else:
            metrics = self.metrics

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
                "model_id": model_id,
                "status": status,
                "created_at": created_at,
                "updated_at": updated_at,
            }
        )
        if test_dataset_id is not UNSET:
            field_dict["test_dataset_id"] = test_dataset_id
        if dataset_hf_repo is not UNSET:
            field_dict["dataset_hf_repo"] = dataset_hf_repo
        if benchmark_model_id is not UNSET:
            field_dict["benchmark_model_id"] = benchmark_model_id
        if metrics is not UNSET:
            field_dict["metrics"] = metrics
        if error_message is not UNSET:
            field_dict["error_message"] = error_message

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.eval_job_metrics_type_0 import EvalJobMetricsType0

        d = dict(src_dict)
        id = d.pop("id")

        organization_id = d.pop("organization_id")

        model_id = d.pop("model_id")

        status = EvalJobStatus(d.pop("status"))

        created_at = isoparse(d.pop("created_at"))

        updated_at = isoparse(d.pop("updated_at"))

        def _parse_test_dataset_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        test_dataset_id = _parse_test_dataset_id(d.pop("test_dataset_id", UNSET))

        def _parse_dataset_hf_repo(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        dataset_hf_repo = _parse_dataset_hf_repo(d.pop("dataset_hf_repo", UNSET))

        def _parse_benchmark_model_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        benchmark_model_id = _parse_benchmark_model_id(d.pop("benchmark_model_id", UNSET))

        def _parse_metrics(data: object) -> EvalJobMetricsType0 | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                metrics_type_0 = EvalJobMetricsType0.from_dict(data)

                return metrics_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(EvalJobMetricsType0 | None | Unset, data)

        metrics = _parse_metrics(d.pop("metrics", UNSET))

        def _parse_error_message(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        error_message = _parse_error_message(d.pop("error_message", UNSET))

        eval_job = cls(
            id=id,
            organization_id=organization_id,
            model_id=model_id,
            status=status,
            created_at=created_at,
            updated_at=updated_at,
            test_dataset_id=test_dataset_id,
            dataset_hf_repo=dataset_hf_repo,
            benchmark_model_id=benchmark_model_id,
            metrics=metrics,
            error_message=error_message,
        )

        eval_job.additional_properties = d
        return eval_job

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
