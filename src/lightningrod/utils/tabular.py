from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime
from functools import singledispatch
from typing import Any, Mapping

from lightningrod._generated.models.dataset_metadata import DatasetMetadata
from lightningrod._generated.models.eval_job import EvalJob
from lightningrod._generated.models.eval_job_list_response import EvalJobListResponse
from lightningrod._generated.models.file_set import FileSet
from lightningrod._generated.models.list_datasets_response import ListDatasetsResponse
from lightningrod._generated.models.list_file_sets_response import ListFileSetsResponse
from lightningrod._generated.models.list_transform_jobs_response import ListTransformJobsResponse
from lightningrod._generated.models.model_list_response import ModelListResponse
from lightningrod._generated.models.model_object import ModelObject
from lightningrod._generated.models.paginated_samples_response import PaginatedSamplesResponse
from lightningrod._generated.models.sample import Sample
from lightningrod._generated.models.training_job import TrainingJob
from lightningrod._generated.models.training_job_list_response import TrainingJobListResponse
from lightningrod._generated.models.transform_job import TransformJob
from lightningrod._generated.types import UNSET, Unset
from lightningrod.training.samples import to_record

_DEFAULT_DROP_KEYS = frozenset(
    {"config", "metrics", "usage", "additional_properties", "transform_config"}
)


def _is_sample_instance(x: Any) -> bool:
    """True if x is a generated Sample, including when a second copy of the class is loaded."""
    if isinstance(x, Sample):
        return True
    cls = getattr(x, "__class__", None)
    if cls is None:
        return False
    return cls.__name__ == "Sample" and cls.__module__ == Sample.__module__


@dataclass(frozen=True)
class TabularOptions:
    max_depth: int | None = 2
    drop_keys: frozenset[str] = _DEFAULT_DROP_KEYS


def flatten(
    obj: Any,
    *,
    max_depth: int | None = 2,
    drop_keys: frozenset[str] | None = None,
) -> list[dict[str, Any]]:
    """Turn a domain object or API list response into flat row dicts for notebooks and pandas.

    Returns a list of rows so callers can use ``pd.DataFrame(flatten(x))``. List responses
    expand to one row per item (totals and cursors stay on the response object).

    A plain ``list`` of :class:`~lightningrod._generated.models.sample.Sample` (e.g. from
    ``dataset.samples()``) is flattened to one row per sample via
    :func:`lightningrod.training.samples.to_record`.

    Registered API types use a **compact overview**: a small set of columns (id, status, key
    names, timestamps, costs, errors). For full field dumps, call ``obj.to_dict()`` or use the
    generic fallback with custom ``max_depth`` / ``drop_keys``.

    For types without a dedicated handler, falls back to :func:`flatten_dict` on
    ``obj.to_dict()`` when available.

    Args:
        obj: A generated model instance (e.g. ``TrainingJobListResponse``, ``TrainingJob``).
        max_depth: Maximum dict nesting depth for the generic fallback path (see :func:`flatten_dict`).
        drop_keys: Top-level and nested keys to omit in the fallback path. Curated handlers
            ignore this except where noted.
    """
    if isinstance(obj, list):
        if not obj:
            return []
        if all(_is_sample_instance(x) for x in obj):
            return [_sample_row(s) for s in obj]
    dk = drop_keys if drop_keys is not None else _DEFAULT_DROP_KEYS
    opts = TabularOptions(
        max_depth=max_depth,
        drop_keys=dk,
    )
    return _records_impl(obj, opts)


def flatten_dict(
    data: Mapping[str, Any],
    *,
    sep: str = ".",
    max_depth: int | None = 2,
    drop_keys: frozenset[str] | None = None,
) -> dict[str, Any]:
    """Flatten a nested mapping into single-level keys (e.g. ``config.model.name``).

    Nested dicts at depth ``>= max_depth`` (root depth is 0) are JSON-serialized to
    strings instead of flattened further. List values are always JSON-serialized.
    Keys in ``drop_keys`` are omitted at every level. ``Unset`` / ``UNSET`` values are skipped.
    """
    drop = drop_keys or frozenset()

    def walk(d: Mapping[str, Any], prefix: str, depth: int) -> dict[str, Any]:
        out: dict[str, Any] = {}
        for k, v in d.items():
            if k in drop:
                continue
            if isinstance(v, Unset) or v is UNSET:
                continue
            path = f"{prefix}{sep}{k}" if prefix else k
            if isinstance(v, dict):
                if max_depth is not None and depth >= max_depth:
                    out[path] = json.dumps(v, default=str)
                else:
                    out.update(walk(v, path, depth + 1))
            elif isinstance(v, list):
                out[path] = json.dumps(v, default=str)
            else:
                out[path] = v
        return out

    return walk(data, "", 0)


def _iso(dt: datetime) -> str:
    return dt.isoformat()


def _training_progress(job: TrainingJob) -> str | None:
    if isinstance(job.current_step, Unset) or isinstance(job.total_steps, Unset):
        return None
    if job.current_step is None or job.total_steps is None:
        return None
    return f"{job.current_step}/{job.total_steps}"


def _training_job_row(job: TrainingJob) -> dict[str, Any]:
    row: dict[str, Any] = {
        "id": job.id,
        "status": job.status.value,
        "base_model": job.config.base_model,
        "updated_at": _iso(job.updated_at),
    }
    if not isinstance(job.name, Unset) and job.name is not None:
        row["name"] = job.name
    if not isinstance(job.model_id, Unset) and job.model_id is not None:
        row["model_id"] = job.model_id
    if not isinstance(job.cost_dollars, Unset) and job.cost_dollars is not None:
        row["cost_dollars"] = job.cost_dollars
    prog = _training_progress(job)
    if prog is not None:
        row["progress"] = prog
    if not isinstance(job.error_message, Unset) and job.error_message:
        row["error_message"] = job.error_message
    return row


def _transform_job_row(job: TransformJob) -> dict[str, Any]:
    row: dict[str, Any] = {
        "id": job.id,
        "status": job.status.value,
        "updated_at": _iso(job.updated_at),
    }
    if not isinstance(job.name, Unset) and job.name is not None:
        row["name"] = job.name
    if job.input_dataset_id is not None:
        row["input_dataset_id"] = job.input_dataset_id
    if job.output_dataset_id is not None:
        row["output_dataset_id"] = job.output_dataset_id
    if not isinstance(job.estimated_cost_dollars, Unset) and job.estimated_cost_dollars is not None:
        row["estimated_cost_dollars"] = job.estimated_cost_dollars
    elif not isinstance(job.usage, Unset) and job.usage is not None:
        u = job.usage
        if not isinstance(u.current_cost_dollars, Unset) and u.current_cost_dollars is not None:
            row["current_cost_dollars"] = u.current_cost_dollars
    if not isinstance(job.error_message, Unset) and job.error_message:
        row["error_message"] = job.error_message
    return row


def _eval_job_row(job: EvalJob) -> dict[str, Any]:
    row: dict[str, Any] = {
        "id": job.id,
        "status": job.status.value,
        "model_id": job.config.model_id,
        "updated_at": _iso(job.updated_at),
    }
    if not isinstance(job.cost_dollars, Unset) and job.cost_dollars is not None:
        row["cost_dollars"] = job.cost_dollars
    if not isinstance(job.error_message, Unset) and job.error_message:
        row["error_message"] = job.error_message
    return row


def _dataset_metadata_row(ds: DatasetMetadata) -> dict[str, Any]:
    return {
        "id": ds.id,
        "num_rows": ds.num_rows,
        "updated_at": _iso(ds.updated_at),
    }


def _sample_row(sample: Sample) -> dict[str, Any]:
    return to_record(sample)


def _file_set_row(fs: FileSet) -> dict[str, Any]:
    return {
        "id": fs.id,
        "name": fs.name,
        "file_count": fs.file_count,
        "updated_at": _iso(fs.updated_at),
    }


def _model_object_row(mo: ModelObject) -> dict[str, Any]:
    row: dict[str, Any] = {"id": mo.id}
    if not isinstance(mo.name, Unset) and mo.name:
        row["name"] = mo.name
    if not isinstance(mo.context_length, Unset) and mo.context_length is not None:
        row["context_length"] = mo.context_length
    return row


def _fallback_records(obj: Any, opts: TabularOptions) -> list[dict[str, Any]]:
    to_dict = getattr(obj, "to_dict", None)
    if not callable(to_dict):
        raise TypeError(
            f"flatten does not support {type(obj)!r}; "
            "expected a known API model or an object with a to_dict() method."
        )
    raw = to_dict()
    if not isinstance(raw, dict):
        raise TypeError(f"to_dict() for {type(obj)!r} did not return a dict.")
    flat = flatten_dict(raw, max_depth=opts.max_depth, drop_keys=opts.drop_keys)
    return [flat]


@singledispatch
def _records_impl(obj: Any, opts: TabularOptions) -> list[dict[str, Any]]:
    return _fallback_records(obj, opts)


@_records_impl.register
def _(obj: TrainingJobListResponse, _opts: TabularOptions) -> list[dict[str, Any]]:
    return [_training_job_row(j) for j in obj.jobs]


@_records_impl.register
def _(obj: TrainingJob, _opts: TabularOptions) -> list[dict[str, Any]]:
    return [_training_job_row(obj)]


@_records_impl.register
def _(obj: ListTransformJobsResponse, _opts: TabularOptions) -> list[dict[str, Any]]:
    return [_transform_job_row(j) for j in obj.jobs]


@_records_impl.register
def _(obj: TransformJob, _opts: TabularOptions) -> list[dict[str, Any]]:
    return [_transform_job_row(obj)]


@_records_impl.register
def _(obj: ListDatasetsResponse, _opts: TabularOptions) -> list[dict[str, Any]]:
    return [_dataset_metadata_row(d) for d in obj.datasets]


@_records_impl.register
def _(obj: DatasetMetadata, _opts: TabularOptions) -> list[dict[str, Any]]:
    return [_dataset_metadata_row(obj)]


@_records_impl.register
def _(obj: EvalJobListResponse, _opts: TabularOptions) -> list[dict[str, Any]]:
    return [_eval_job_row(j) for j in obj.jobs]


@_records_impl.register
def _(obj: EvalJob, _opts: TabularOptions) -> list[dict[str, Any]]:
    return [_eval_job_row(obj)]


@_records_impl.register
def _(obj: ListFileSetsResponse, _opts: TabularOptions) -> list[dict[str, Any]]:
    return [_file_set_row(fs) for fs in obj.file_sets]


@_records_impl.register
def _(obj: PaginatedSamplesResponse, _opts: TabularOptions) -> list[dict[str, Any]]:
    return [_sample_row(s) for s in obj.samples]


@_records_impl.register
def _(obj: Sample, _opts: TabularOptions) -> list[dict[str, Any]]:
    return [_sample_row(obj)]


@_records_impl.register
def _(obj: FileSet, _opts: TabularOptions) -> list[dict[str, Any]]:
    return [_file_set_row(obj)]


@_records_impl.register
def _(obj: ModelListResponse, _opts: TabularOptions) -> list[dict[str, Any]]:
    return [_model_object_row(m) for m in obj.data]


@_records_impl.register
def _(obj: ModelObject, _opts: TabularOptions) -> list[dict[str, Any]]:
    return [_model_object_row(obj)]
