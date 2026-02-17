"""LightningRod SDK processing utilities."""

import random
from datetime import date, datetime
from typing import Any, Callable, Optional

from lightningrod._generated.models.answer_type import AnswerType
from lightningrod._generated.models.answer_type_enum import AnswerTypeEnum


def _parse_date(value: Any) -> Optional[date]:
    """Parse a date value (date, datetime, or ISO-8601 string) into a date."""
    if value is None:
        return None
    if isinstance(value, date):
        return value if not isinstance(value, datetime) else value.date()
    if isinstance(value, str) and value.strip():
        try:
            return datetime.fromisoformat(value.replace("Z", "+00:00")).date()
        except ValueError:
            return None
    return None


def _extract_contexts(item: dict[str, Any]) -> Optional[list[dict[str, Any]]]:
    """Get context list from an item. If missing/empty and seed.seed_text exists, use that as one context block."""
    context = item.get("context")
    if context:
        return context
    seed = item.get("seed")
    if seed:
        seed_text = seed.get("seed_text")
        if seed_text and str(seed_text).strip():
            return [{"context_type": "CONTEXT", "rendered_context": str(seed_text).strip()}]
    return None


def filter_samples(
    samples: list[dict[str, Any]],
    min_horizon: Optional[int] = None,
    max_horizon: Optional[int] = None,
    drop_missing_context: bool = True,
) -> list[dict[str, Any]]:
    """Filter samples by time horizon and optional context.

    Args:
        samples: List of sample dicts to filter.
        min_horizon: Minimum allowed days between prediction and resolution; omit to skip filter.
        max_horizon: Maximum allowed days between prediction and resolution; omit to skip filter.
        drop_missing_context: If True, drop samples with no non-empty context.

    Returns:
        Filtered list of samples.
    """
    filtered: list[dict[str, Any]] = []
    for sample in samples:
        is_valid: bool | None = sample.get("is_valid")
        if is_valid is not True:
            continue

        # prediction_date: nested SDK format (question.prediction_date) or flat prediction_date
        pred_raw: Any = (sample.get("question") or {}).get("prediction_date") or sample.get(
            "prediction_date"
        )
        # resolution_date: nested SDK format (label.resolution_date) or flat resolution_date
        res_raw: Any = (sample.get("label") or {}).get("resolution_date") or sample.get(
            "resolution_date"
        )

        pred_d = _parse_date(pred_raw)
        res_d = _parse_date(res_raw)
        if min_horizon is not None or max_horizon is not None:
            if pred_d is None or res_d is None:
                continue
            horizon_days: int = (res_d - pred_d).days
            if min_horizon is not None and horizon_days < min_horizon:
                continue
            if max_horizon is not None and horizon_days > max_horizon:
                continue
        if drop_missing_context:
            contexts = _extract_contexts(sample)
            if not contexts:
                continue
            # Keep only if at least one context block has non-empty rendered_context
            has_nonempty_rendered: bool = any(
                bool(ctx.get("rendered_context")) and len(str(ctx.get("rendered_context"))) > 0
                for ctx in contexts
            )
            if not has_nonempty_rendered:
                continue
        filtered.append(sample)
    return filtered


def _label_to_numeric(sample: dict[str, Any]) -> Optional[float]:
    """Extract a numeric label (for BINARY or CONTINUOUS)."""
    raw_label: Any = sample.get("label")

    if isinstance(raw_label, dict):
        # Prefer "value" when present, fall back to "label".
        if "value" in raw_label:
            value = raw_label.get("value")
        elif "label" in raw_label:
            value = raw_label.get("label")
        else:
            value = None
    else:
        value = raw_label

    if value is None:
        return None

    try:
        s = str(value).strip()
        if not s:
            return None
        return float(s)
    except (TypeError, ValueError):
        return None


def _label_to_text(sample: dict[str, Any]) -> Optional[str]:
    """Extract a text label (for FREE_RESPONSE or MULTIPLE_CHOICE)."""
    raw_label: Any = sample.get("label")

    if isinstance(raw_label, dict):
        if "label" in raw_label:
            value = raw_label.get("label")
        elif "value" in raw_label:
            value = raw_label.get("value")
        else:
            value = None
    else:
        value = raw_label

    if value is None:
        return None

    s = str(value).strip()
    return s or None


def add_rl_training_fields(
    samples: list[dict[str, Any]],
    answer_type: AnswerType,
) -> list[dict[str, Any]]:
    """Add RL training fields and ``correct_answer`` to each sample in-place.

    Args:
        samples: List of sample dicts to enrich in-place.
        answer_type: An ``AnswerType`` object whose ``answer_type`` attribute is one of
            ``BINARY``, ``CONTINUOUS``, ``FREE_RESPONSE``, ``MULTIPLE_CHOICE``.

    Returns:
        The same list of samples, updated with ``correct_answer`` and RL fields.
    """
    at = answer_type.answer_type
    answer_type_str = at.value.lower()

    if at is AnswerTypeEnum.BINARY:
        reward_type = "binary_log_score"
        extract_fn: Callable[[dict[str, Any]], Any] = _label_to_numeric
    elif at is AnswerTypeEnum.CONTINUOUS:
        reward_type = "continuous_log_score"
        extract_fn = _label_to_numeric
    elif at is AnswerTypeEnum.MULTIPLE_CHOICE:
        reward_type = "multi_choice_log_score"
        extract_fn = _label_to_text
    elif at is AnswerTypeEnum.FREE_RESPONSE:
        reward_type = ""
        extract_fn = _label_to_text
    else:
        # Fallback: treat as free-response-like text.
        reward_type = ""
        extract_fn = _label_to_text

    for sample in samples:
        sample["correct_answer"] = extract_fn(sample)
        sample["answer_type"] = answer_type_str
        sample["answer_parser_type"] = answer_type_str
        sample["reward_function_type"] = reward_type.lower() if reward_type else reward_type

    return samples


def _default_leakage_keys() -> list[Callable[[dict], str | None]]:
    """Default leakage keys: date_close and resolution_date."""
    return [
        lambda r: r.get("question", {}).get("date_close"),
        lambda r: r.get("label", {}).get("resolution_date"),
    ]


def test_train_split(
    samples: list[dict],
    *,
    temporal_split: bool = True,
    test_start: str | None = None,
    test_fraction: float | None = None,
    seed: int | None = None,
    sort_key: Callable[[dict], str] = lambda r: r["question"]["prediction_date"],
    leakage_keys: list[Callable[[dict], str | None]] = _default_leakage_keys(),
    filter_leaky_train: bool = True,
) -> tuple[list[dict], list[dict]]:
    """Split samples into train/test sets. Temporal (time-ordered) or random.

    Args:
        samples: List of row dicts to split.
        temporal_split: If True, split by time (test = latest fraction or after test_start).
            If False, shuffle and split by test_fraction (random split).
        test_start: Earliest prediction date (as a string) to include in the test
            set; everything earlier goes to train. Only used when temporal_split=True.
            Mutually exclusive with test_fraction.
        test_fraction: Fraction of the data to put into the test set. When temporal_split=True,
            applied by time order; when temporal_split=False, applied after shuffling.
            Required when temporal_split=False.
        seed: Random seed for reproducible split when temporal_split=False; ignored when
            temporal_split=True.
        sort_key: Function that returns the prediction date string for each row.
            Only used when temporal_split=True.
        leakage_keys: List of functions that extract date strings used to detect
            information leakage. Only used when temporal_split=True.
        filter_leaky_train: If True (and temporal_split=True), drop train samples whose
            leakage dates extend into the test period.

    Returns:
        A `(train, test)` tuple of row lists.
    """
    if temporal_split:
        if (test_start is None) == (test_fraction is None):
            raise ValueError("Provide exactly one of test_start or test_fraction")
    else:
        if test_fraction is None:
            raise ValueError("test_fraction is required when temporal_split=False")
        if test_start is not None:
            raise ValueError("test_start is only valid when temporal_split=True")

    if temporal_split:
        valid_samples = [r for r in samples if sort_key(r) is not None]
        sorted_samples = sorted(valid_samples, key=sort_key)

        if test_fraction is not None:
            split_idx = int(len(sorted_samples) * (1 - test_fraction))
            train, test = sorted_samples[:split_idx], sorted_samples[split_idx:]
        else:
            assert test_start is not None
            train = [r for r in sorted_samples if sort_key(r) < test_start]
            test = [r for r in sorted_samples if sort_key(r) >= test_start]

        if filter_leaky_train and test:
            test_cutoff = sort_key(test[0])

            def is_safe(row: dict) -> bool:
                for key_fn in leakage_keys:
                    date_val = key_fn(row)
                    if date_val is not None and date_val >= test_cutoff:
                        return False
                return True

            train = [r for r in train if is_safe(r)]

        return train, test

    # Random split (temporal_split=False)
    shuffled = list(samples)
    rng = random.Random(seed) if seed is not None else random
    rng.shuffle(shuffled)

    # At this point, test_fraction is guaranteed non-None by the validation above,
    # but we assert here to satisfy static type checkers.
    assert test_fraction is not None
    split_idx = int(len(shuffled) * (1 - test_fraction))
    
    train = shuffled[:split_idx]
    test = shuffled[split_idx:]
    return train, test


def _flat_key(parent_key: str, child_key: str, sep: str) -> str:
    """Build flattened key, avoiding duplicate prefixes."""
    if parent_key == "meta" and child_key == "sample_id":
        return "sample_id"
    if parent_key == "label" and child_key == "label":
        return "label"

    if parent_key and child_key == parent_key:
        return f"{parent_key}{sep}{child_key}"
    if parent_key and child_key.startswith(parent_key + sep):
        return child_key
    if parent_key:
        return parent_key + sep + child_key
    return child_key


def _flatten_sample_dict(d: dict[str, Any], parent_key: str = "", sep: str = "_") -> dict[str, Any]:
    """Recursively flatten nested dicts and lists of dicts."""
    items: list[tuple[str, Any]] = []
    for k, v in d.items():
        new_key = _flat_key(parent_key, k, sep)
        # Keep rich fields like prompt and context unflattened so downstream consumers
        # can still access the original structured values.
        if k in {"prompt", "context"}:
            items.append((new_key, v))
        elif isinstance(v, dict) and v:
            items.extend(_flatten_sample_dict(v, new_key, sep).items())
        elif isinstance(v, list) and v and isinstance(v[0], dict):
            for i, item in enumerate(v):
                items.extend(_flatten_sample_dict(item, f"{new_key}{sep}{i}", sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


def flatten_samples(samples: list[dict[str, Any]], sep: str = "_") -> list[dict[str, Any]]:
    """Flatten nested samples into flat dicts.

    Args:
        samples: List of nested sample dicts.
        sep: String used to join nested field names in the flattened keys.

    Returns:
        List of flattened sample dicts.
    """
    return [_flatten_sample_dict(sample, sep=sep) for sample in samples]


def deduplicate_samples(
    samples: list[dict[str, Any]],
    key_fn: Callable[[dict[str, Any]], tuple[Any, ...]] | None = None,
) -> list[dict[str, Any]]:
    """Remove duplicate samples based on a key function.

    Args:
        samples: List of row dicts to deduplicate.
        key_fn: Optional function that turns a row into a hashable key; by default
            uses `(question_text, resolution_date)` from the SDK-style schema.

    Returns:
        List of samples with duplicates removed (first occurrence kept).
    """
    def _default_key_fn(row: dict[str, Any]) -> tuple[Any, ...]:
        question: dict[str, Any] = row.get("question") or {}
        label: dict[str, Any] = row.get("label") or {}
        return question.get("question_text"), label.get("resolution_date")

    key_fn_local: Callable[[dict[str, Any]], tuple[Any, ...]] = key_fn or _default_key_fn
    seen: set[tuple[Any, ...]] = set()
    result: list[dict[str, Any]] = []
    for row in samples:
        key = key_fn_local(row)
        if key not in seen:
            seen.add(key)
            result.append(row)
    return result