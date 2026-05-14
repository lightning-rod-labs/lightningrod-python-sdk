"""User-facing display helpers.

These are *display* utilities — convenience converters for inspecting samples
in notebooks or building DataFrames. They are deliberately not primitives on
the dataset class so that agents and users reach for typed `Sample` objects by
default; flattening should be an explicit display choice, not the first thing
auto-complete suggests.
"""
from typing import Any, Iterable, List

from lightningrod._generated.models import Sample


def flatten_samples(samples: Iterable[Sample]) -> List[dict[str, Any]]:
    """Convert an iterable of `Sample` objects into a list of flat dicts.

    Intended for display / quick DataFrame construction. The dict shape is not
    a stable data-access contract — for programmatic field access, use the
    typed `Sample` attributes directly (e.g. `sample.label.label_confidence`).

    Example:
        >>> import pandas as pd
        >>> from lightningrod.display import flatten_samples
        >>> df = pd.DataFrame(flatten_samples(dataset.samples()))
    """
    from lightningrod.training.samples import to_record

    return [to_record(s) for s in samples]


__all__ = ["flatten_samples"]
