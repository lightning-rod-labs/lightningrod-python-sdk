from __future__ import annotations

from collections.abc import Iterable
from typing import TypeGuard, TypeVar

from lightningrod._generated.models import DatasetLinterRunResponse, Severity
from lightningrod._generated.types import Unset

T = TypeVar("T")


def _is_set(value: T | Unset | None) -> TypeGuard[T]:
    return not isinstance(value, Unset) and value is not None

def get_lint_affected_sample_ids(
    run: DatasetLinterRunResponse,
    severities: Iterable[Severity] = (Severity.WARNING, Severity.ERROR),
) -> list[str]:
    """Return unique sample IDs affected by lint issues with matching severities."""
    affected_sample_ids: list[str] = []
    seen: set[str] = set()

    if not _is_set(getattr(run, "rules", None)):
        return affected_sample_ids

    for rule in run.rules:
        if not _is_set(getattr(rule, "issues", None)):
            continue

        for issue in rule.issues:
            if issue.severity not in severities:
                continue
            if not _is_set(getattr(issue, "affected_sample_ids", None)):
                continue

            for sample_id in issue.affected_sample_ids:
                if sample_id in seen:
                    continue
                seen.add(sample_id)
                affected_sample_ids.append(sample_id)

    return affected_sample_ids
