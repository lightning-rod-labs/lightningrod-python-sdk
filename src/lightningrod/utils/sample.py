"""Convenience helpers for creating Sample objects."""

from datetime import datetime
from typing import Optional, Any

from lightningrod._generated.models.label import Label
from lightningrod._generated.models.sample import Sample
from lightningrod._generated.models.seed import Seed
from lightningrod._generated.models.sample_meta import SampleMeta


def create_sample(
    seed_text: str,
    label: Optional[str] = None,
    seed_date: Optional[datetime] = None,
    meta: Optional[dict[str, Any]] = None,
    *,
    answer_type: Optional[str] = None,
) -> Sample:
    """Create a Sample with less boilerplate.

    Args:
        seed_text: The text content for the seed.
        label: Optional label value. If provided, wraps in a Label object.
        answer_type: Required when label is provided (e.g. "binary", "continuous").
        seed_date: Optional creation date for the seed.

    Returns:
        A Sample object.
    """
    seed = Seed(seed_text=seed_text, seed_creation_date=seed_date)

    label_obj = None
    if label is not None:
        normalized_answer_type = (answer_type or "").strip().lower()
        if not normalized_answer_type:
            raise ValueError("answer_type is required when label is provided.")
        label_obj = Label(label=label, label_confidence=1.0, answer_type=normalized_answer_type)
    
    meta_obj = SampleMeta()
    if meta is not None:
        for k, v in meta.items():
            meta_obj[k] = v

    return Sample(seed=seed, label=label_obj, meta=meta_obj)
