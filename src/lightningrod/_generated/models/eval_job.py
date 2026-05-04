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
    from ..models.eval_config import EvalConfig
    from ..models.eval_job_metrics_type_0 import EvalJobMetricsType0
    from ..models.eval_job_reasoning_comparison_report_type_0 import EvalJobReasoningComparisonReportType0


T = TypeVar("T", bound="EvalJob")


@_attrs_define
class EvalJob:
    """
    Attributes:
        id (str):
        organization_id (str):
        config (EvalConfig):
        status (EvalJobStatus):
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
        cost_dollars (float | None | Unset):
        current_step (int | None | Unset):
        total_steps (int | None | Unset):
        metrics (EvalJobMetricsType0 | None | Unset):
        result_model_ids (list[str] | None | Unset):
        reasoning_comparison_report (EvalJobReasoningComparisonReportType0 | None | Unset):
        error_message (None | str | Unset):
    """

    id: str
    organization_id: str
    config: EvalConfig
    status: EvalJobStatus
    created_at: datetime.datetime
    updated_at: datetime.datetime
    cost_dollars: float | None | Unset = UNSET
    current_step: int | None | Unset = UNSET
    total_steps: int | None | Unset = UNSET
    metrics: EvalJobMetricsType0 | None | Unset = UNSET
    result_model_ids: list[str] | None | Unset = UNSET
    reasoning_comparison_report: EvalJobReasoningComparisonReportType0 | None | Unset = UNSET
    error_message: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.eval_job_metrics_type_0 import EvalJobMetricsType0
        from ..models.eval_job_reasoning_comparison_report_type_0 import EvalJobReasoningComparisonReportType0

        id = self.id

        organization_id = self.organization_id

        config = self.config.to_dict()

        status = self.status.value

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        cost_dollars: float | None | Unset
        if isinstance(self.cost_dollars, Unset):
            cost_dollars = UNSET
        else:
            cost_dollars = self.cost_dollars

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

        metrics: dict[str, Any] | None | Unset
        if isinstance(self.metrics, Unset):
            metrics = UNSET
        elif isinstance(self.metrics, EvalJobMetricsType0):
            metrics = self.metrics.to_dict()
        else:
            metrics = self.metrics

        result_model_ids: list[str] | None | Unset
        if isinstance(self.result_model_ids, Unset):
            result_model_ids = UNSET
        elif isinstance(self.result_model_ids, list):
            result_model_ids = self.result_model_ids

        else:
            result_model_ids = self.result_model_ids

        reasoning_comparison_report: dict[str, Any] | None | Unset
        if isinstance(self.reasoning_comparison_report, Unset):
            reasoning_comparison_report = UNSET
        elif isinstance(self.reasoning_comparison_report, EvalJobReasoningComparisonReportType0):
            reasoning_comparison_report = self.reasoning_comparison_report.to_dict()
        else:
            reasoning_comparison_report = self.reasoning_comparison_report

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
                "config": config,
                "status": status,
                "created_at": created_at,
                "updated_at": updated_at,
            }
        )
        if cost_dollars is not UNSET:
            field_dict["cost_dollars"] = cost_dollars
        if current_step is not UNSET:
            field_dict["current_step"] = current_step
        if total_steps is not UNSET:
            field_dict["total_steps"] = total_steps
        if metrics is not UNSET:
            field_dict["metrics"] = metrics
        if result_model_ids is not UNSET:
            field_dict["result_model_ids"] = result_model_ids
        if reasoning_comparison_report is not UNSET:
            field_dict["reasoning_comparison_report"] = reasoning_comparison_report
        if error_message is not UNSET:
            field_dict["error_message"] = error_message

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.eval_config import EvalConfig
        from ..models.eval_job_metrics_type_0 import EvalJobMetricsType0
        from ..models.eval_job_reasoning_comparison_report_type_0 import EvalJobReasoningComparisonReportType0

        d = dict(src_dict)
        id = d.pop("id")

        organization_id = d.pop("organization_id")

        config = EvalConfig.from_dict(d.pop("config"))

        status = EvalJobStatus(d.pop("status"))

        created_at = isoparse(d.pop("created_at"))

        updated_at = isoparse(d.pop("updated_at"))

        def _parse_cost_dollars(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        cost_dollars = _parse_cost_dollars(d.pop("cost_dollars", UNSET))

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

        def _parse_result_model_ids(data: object) -> list[str] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                result_model_ids_type_0 = cast(list[str], data)

                return result_model_ids_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[str] | None | Unset, data)

        result_model_ids = _parse_result_model_ids(d.pop("result_model_ids", UNSET))

        def _parse_reasoning_comparison_report(data: object) -> EvalJobReasoningComparisonReportType0 | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                reasoning_comparison_report_type_0 = EvalJobReasoningComparisonReportType0.from_dict(data)

                return reasoning_comparison_report_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(EvalJobReasoningComparisonReportType0 | None | Unset, data)

        reasoning_comparison_report = _parse_reasoning_comparison_report(d.pop("reasoning_comparison_report", UNSET))

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
            config=config,
            status=status,
            created_at=created_at,
            updated_at=updated_at,
            cost_dollars=cost_dollars,
            current_step=current_step,
            total_steps=total_steps,
            metrics=metrics,
            result_model_ids=result_model_ids,
            reasoning_comparison_report=reasoning_comparison_report,
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
