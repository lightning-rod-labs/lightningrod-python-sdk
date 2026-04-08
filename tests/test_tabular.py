"""Tests for lightningrod.utils.tabular."""

from __future__ import annotations

import json

import pytest
from datetime import datetime

from lightningrod._generated.models.dataset_metadata import DatasetMetadata
from lightningrod._generated.models.eval_config import EvalConfig
from lightningrod._generated.models.eval_job import EvalJob
from lightningrod._generated.models.eval_model import EvalModel
from lightningrod._generated.models.eval_job_list_response import EvalJobListResponse
from lightningrod._generated.models.eval_job_metrics_type_0 import EvalJobMetricsType0
from lightningrod._generated.models.eval_job_status import EvalJobStatus
from lightningrod._generated.models.list_datasets_response import ListDatasetsResponse
from lightningrod._generated.models.paginated_samples_response import PaginatedSamplesResponse
from lightningrod._generated.models.sample import Sample
from lightningrod._generated.models.sample_dataset_config import SampleDatasetConfig
from lightningrod._generated.models.training_config import TrainingConfig
from lightningrod._generated.models.training_job import TrainingJob
from lightningrod._generated.models.training_job_list_response import TrainingJobListResponse
from lightningrod._generated.models.training_job_status import TrainingJobStatus
from lightningrod._generated.types import UNSET, Unset
from lightningrod.utils.tabular import flatten, flatten_dict


def _dt(hour: int = 0) -> datetime:
    return datetime(2025, 1, 1, hour, 0, 0)


def _training_job(
    *,
    base_model_id: str = "Qwen/Qwen3-8B",
    training_steps: int = 10,
) -> TrainingJob:
    cfg = TrainingConfig(
        dataset=SampleDatasetConfig(id="ds1", sample_ids=["s1"]),
        base_model_id=base_model_id,
        training_steps=training_steps,
    )
    return TrainingJob(
        id="job-1",
        organization_id="org-1",
        status=TrainingJobStatus.RUNNING,
        config=cfg,
        created_at=_dt(0),
        updated_at=_dt(1),
    )


def _eval_job_with_metrics() -> EvalJob:
    cfg = EvalConfig(
        organization_id="org",
        models=[EvalModel(model_id="m")],
        dataset=SampleDatasetConfig(id="ds", sample_ids=[]),
    )
    metrics = EvalJobMetricsType0()
    metrics.additional_properties["acc"] = 0.9
    return EvalJob(
        id="e1",
        organization_id="org",
        config=cfg,
        status=EvalJobStatus.COMPLETED,
        created_at=_dt(0),
        updated_at=_dt(1),
        metrics=metrics,
    )


class TestFlattenDict:
    def test_flattens_nested_dict(self) -> None:
        data = {"a": 1, "b": {"c": 2, "d": {"e": 3}}}
        out = flatten_dict(data, max_depth=3, drop_keys=frozenset())
        assert out["a"] == 1
        assert out["b.c"] == 2
        assert out["b.d.e"] == 3

    def test_respects_max_depth(self) -> None:
        data = {"outer": {"inner": {"deep": {"x": 1}}}}
        out = flatten_dict(data, max_depth=2, drop_keys=frozenset())
        assert "outer.inner.deep" in out
        assert isinstance(out["outer.inner.deep"], str)
        parsed = json.loads(out["outer.inner.deep"])
        assert parsed == {"x": 1}

    def test_drops_keys(self) -> None:
        data = {"keep": 1, "config": {"secret": 2}, "nested": {"config": 3, "ok": 4}}
        out = flatten_dict(data, max_depth=4, drop_keys=frozenset({"config"}))
        assert out["keep"] == 1
        assert "config" not in out
        assert out["nested.ok"] == 4
        assert "nested.config" not in out

    def test_skips_unset(self) -> None:
        data = {"a": 1, "b": UNSET, "c": Unset()}
        out = flatten_dict(data, max_depth=2, drop_keys=frozenset())
        assert out == {"a": 1}
        assert "b" not in out
        assert "c" not in out

    def test_list_serializes_to_json_string(self) -> None:
        data = {"items": [1, 2, {"a": "b"}]}
        out = flatten_dict(data, max_depth=2, drop_keys=frozenset())
        assert json.loads(out["items"]) == [1, 2, {"a": "b"}]


class TestTrainingJobList:
    def test_list_response(self) -> None:
        resp = TrainingJobListResponse(
            jobs=[_training_job()],
            total_count=42,
        )
        rows = flatten(resp)
        assert len(rows) == 1
        assert rows[0]["id"] == "job-1"
        assert rows[0]["status"] == "RUNNING"
        assert rows[0]["base_model_id"] == "Qwen/Qwen3-8B"
        assert "config" not in rows[0]


class TestDatasetAndSamples:
    def test_list_datasets_response(self) -> None:
        resp = ListDatasetsResponse(
            datasets=[
                DatasetMetadata(
                    id="ds-1",
                    num_rows=3,
                    created_at=_dt(0),
                    updated_at=_dt(1),
                )
            ],
            has_more=False,
            total=1,
        )
        rows = flatten(resp)
        assert rows[0]["id"] == "ds-1"
        assert rows[0]["num_rows"] == 3

    def test_flatten_list_of_samples(self) -> None:
        s = Sample.from_dict(
            {
                "id": "s-1",
                "question": {"question_type": "QUESTION", "question_text": "Q?"},
                "label": {"label": "x", "label_confidence": 0.5, "answer_type": "binary"},
            }
        )
        rows = flatten([s])
        assert len(rows) == 1
        assert rows[0]["sample_id"] == "s-1"
        assert rows[0]["answer_type"] == "binary"

    def test_paginated_samples_response(self) -> None:
        s = Sample.from_dict({"id": "p-1"})
        resp = PaginatedSamplesResponse(samples=[s], has_more=False, total=1)
        rows = flatten(resp)
        assert len(rows) == 1
        assert rows[0]["sample_id"] == "p-1"


class TestEvalJobList:
    def test_eval_rows_overview_excludes_metrics_blob(self) -> None:
        resp = EvalJobListResponse(
            jobs=[_eval_job_with_metrics()],
            total_count=1,
        )
        rows = flatten(resp)
        assert rows[0]["model_id"] == "m"
        assert "metrics" not in rows[0]
        assert "config" not in rows[0]


class TestFallback:
    def test_unknown_object_with_to_dict(self) -> None:
        class M:
            def to_dict(self) -> dict[str, object]:
                return {"name": "x", "nested": {"y": 2}}

        rows = flatten(M())
        assert len(rows) == 1
        assert rows[0].get("name") == "x"
        assert "nested.y" in rows[0] or rows[0].get("nested") is not None

    def test_no_to_dict_raises(self) -> None:
        class Bad:
            pass

        with pytest.raises(TypeError, match="flatten does not support"):
            flatten(Bad())
