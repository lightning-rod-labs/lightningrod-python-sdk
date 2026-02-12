"""Foresight processing utilities. Self-contained prompt rendering for item dicts."""

from datetime import date, datetime
from typing import Any, Callable, Literal, Optional


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


binary_answer_format = """Think carefully in English about your answer and output your final prediction (a float between 0.0 and 1.0) between <answer></answer> tags.

Example Outputs. These are just examples to illustrate the format and should not be considered baselines:
<answer>0.92</answer>
<answer>0.53</answer>
<answer>0.05</answer>"""


DEFAULT_PROMPT_TEMPLATE = """You will make a prediction for the following question.

QUESTION: {question_text}

TODAY'S DATE: {prediction_date}

RESOLUTION CRITERIA: {resolution_criteria}

CONTEXT: {rendered_context}

ANSWER FORMAT: {binary_answer_format}"""


def _render_contexts(contexts: list[dict[str, Any]]) -> str:
    """Render context dicts grouped by context_type with headers."""
    if not contexts:
        return ""

    contexts_by_type: dict[str, list[dict[str, Any]]] = {}
    for ctx in contexts:
        ctx_type = ctx.get("context_type", "CONTEXT")
        if ctx_type not in contexts_by_type:
            contexts_by_type[ctx_type] = []
        contexts_by_type[ctx_type].append(ctx)

    headers: dict[str, str] = {"NEWS_CONTEXT": "NEWS:", "RAG_CONTEXT": "DOCUMENTS:"}
    descriptions: dict[str, str] = {
        "NEWS_CONTEXT": "Recent news articles relevant to this question:",
        "RAG_CONTEXT": "Retrieved documents relevant to this question:",
    }

    rendered_sections: list[str] = []
    for ctx_type, type_contexts in contexts_by_type.items():
        header = headers.get(ctx_type, "CONTEXT:")
        description = descriptions.get(ctx_type, "")
        content = "\n\n".join(ctx.get("rendered_context", "") for ctx in type_contexts)
        rendered_sections.append(f"{header}\n{description}\n\n{content}")

    return "\n\n".join(rendered_sections)


def render_prompt(
    question_text: str,
    contexts: Optional[list[dict[str, Any]]] = None,
    resolution_criteria: str = "",
    prediction_date: str = "",
    template: Optional[str] = None,
) -> str:
    """Build a prompt from question, context, resolution criteria, and prediction date.

    If template is given it may use placeholders: {question_text}, {rendered_context},
    {resolution_criteria}, {prediction_date}. Omitted sections are passed as empty string.
    If template is None, uses DEFAULT_PROMPT_TEMPLATE.
    """
    rendered_context = _render_contexts(contexts) if contexts else ""
    t = template if template is not None else DEFAULT_PROMPT_TEMPLATE
    return t.format(
        question_text=question_text,
        rendered_context=rendered_context,
        resolution_criteria=resolution_criteria,
        prediction_date=prediction_date,
        binary_answer_format=binary_answer_format,
    )


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


def _label_to_correct_answer_binary(item: dict[str, Any]) -> Optional[float]:
    """Label must be 0 or 1 (or "0"/"1"). Return 0.0 or 1.0, else None."""
    raw_label: Any = item.get("label")

    # Support nested SDK format where label is a dict, e.g. {"label": "1"}.
    label_value: Any
    if isinstance(raw_label, dict):
        if "label" in raw_label:
            label_value = raw_label.get("label")
        elif "value" in raw_label:
            label_value = raw_label.get("value")
        else:
            label_value = None
    else:
        label_value = raw_label

    if label_value in (0, 1):
        return float(label_value)
    if label_value is not None and str(label_value).strip() in ("0", "1"):
        return float(str(label_value).strip())
    return None


def filter_records(
    records: list[dict[str, Any]],
    min_horizon: int,
    max_horizon: int,
    drop_missing_context: bool = True,
) -> list[dict[str, Any]]:
    """Filter by prediction horizon (resolution_date - prediction_date in days). Optionally drop records missing context."""
    filtered: list[dict[str, Any]] = []
    for r in records:
        is_valid: bool | None = r.get("is_valid")
        if is_valid is not True:
            continue

        # prediction_date: nested SDK format (question.prediction_date) or flat prediction_date
        pred_raw: Any = (r.get("question") or {}).get("prediction_date") or r.get("prediction_date")
        # resolution_date: nested SDK format (label.resolution_date) or flat resolution_date
        res_raw: Any = (r.get("label") or {}).get("resolution_date") or r.get("resolution_date")

        pred_d = _parse_date(pred_raw)
        res_d = _parse_date(res_raw)
        if pred_d is None or res_d is None:
            continue
        horizon_days: int = (res_d - pred_d).days
        if horizon_days < min_horizon or horizon_days > max_horizon:
            continue
        if drop_missing_context:
            contexts = _extract_contexts(r)
            if not contexts:
                continue
            # Keep only if at least one context block has non-empty rendered_context
            has_nonempty_rendered: bool = any(
                bool(ctx.get("rendered_context")) and len(str(ctx.get("rendered_context"))) > 0
                for ctx in contexts
            )
            if not has_nonempty_rendered:
                continue
        filtered.append(r)
    return filtered


def prepare_prompts(
    records: list[dict[str, Any]],
    mode: Literal["user_only", "supervised"] = "user_only",
    template: Optional[str] = None,
    prediction_date: Optional[str] = None,
    include_training_fields: bool = True,
) -> list[dict[str, Any]]:
    """Add messages and training fields to each record.

    - Adds prompt (list of message dicts). user_only: just user message; supervised: user + assistant with correct answer.
    - Sets answer_type, answer_parser_type, reward_function_type (binary only).
    - Sets correct_answer from label: 0 or 1 (or "0"/"1") -> 0.0 or 1.0, else None.
    """
    today_str: str = prediction_date if prediction_date is not None else date.today().isoformat()

    for d in records:
        question = d.get("question") or {}
        question_text: str = str(question.get("question_text") or d.get("question_text") or "")
        contexts = _extract_contexts(d)
        resolution_criteria: str = str(
            question.get("resolution_criteria") or d.get("resolution_criteria") or ""
        )
        prompt_str = render_prompt(
            question_text=question_text,
            contexts=contexts,
            resolution_criteria=resolution_criteria,
            prediction_date=today_str,
            template=template,
        )
        d["prompt"] = [{"role": "user", "content": prompt_str}]

        d["correct_answer"] = _label_to_correct_answer_binary(d)
        if include_training_fields:
            d["answer_type"] = "binary"
            d["answer_parser_type"] = "binary"
            d["reward_function_type"] = "binary_log_score"

        if mode == "supervised" and d["correct_answer"] is not None:
            assistant_content: str = f"<answer>{int(d['correct_answer'])}</answer>"
            d["prompt"] = list(d["prompt"]) + [{"role": "assistant", "content": assistant_content}]

    records.sort(key=lambda d: _parse_date(d.get("prediction_date")) or date.min)
    return records


def _default_leakage_keys() -> list[Callable[[dict], str | None]]:
    """Default leakage keys: date_close and resolution_date."""
    return [
        lambda r: r.get("question", {}).get("date_close"),
        lambda r: r.get("label", {}).get("resolution_date"),
    ]


def temporal_split(
    rows: list[dict],
    *,
    test_start: str | None = None,
    test_fraction: float | None = None,
    sort_key: Callable[[dict], str] = lambda r: r["question"]["prediction_date"],
    leakage_keys: list[Callable[[dict], str | None]] = _default_leakage_keys(),
    filter_leaky_train: bool = True,
) -> tuple[list[dict], list[dict]]:
    """Temporal train/test split with leakage prevention.

    Splits on prediction_date (sort_key). Leakage filter removes train rows where
    ANY of the leakage_keys dates extend past the test set's earliest prediction_date.

    Provide exactly one of test_start or test_fraction.
    """
    if (test_start is None) == (test_fraction is None):
        raise ValueError("Provide exactly one of test_start or test_fraction")

    valid_rows = [r for r in rows if sort_key(r) is not None]
    sorted_rows = sorted(valid_rows, key=sort_key)

    if test_fraction is not None:
        split_idx = int(len(sorted_rows) * (1 - test_fraction))
        train, test = sorted_rows[:split_idx], sorted_rows[split_idx:]
    else:
        assert test_start is not None
        train = [r for r in sorted_rows if sort_key(r) < test_start]
        test = [r for r in sorted_rows if sort_key(r) >= test_start]

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


def _flat_key(parent_key: str, child_key: str, sep: str) -> str:
    """Build flattened key, avoiding duplicate prefixes."""
    # Custom remappings for common foresight schemas.
    # - meta.sample_id -> sample_id
    # - label.label -> label
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


def _flatten_record_dict(d: dict[str, Any], parent_key: str = "", sep: str = "_") -> dict[str, Any]:
    """Recursively flatten nested dicts and lists of dicts."""
    items: list[tuple[str, Any]] = []
    for k, v in d.items():
        new_key = _flat_key(parent_key, k, sep)
        # Keep rich fields like prompt and context unflattened so downstream consumers
        # can still access the original structured values.
        if k in {"prompt", "context"}:
            items.append((new_key, v))
        elif isinstance(v, dict) and v:
            items.extend(_flatten_record_dict(v, new_key, sep).items())
        elif isinstance(v, list) and v and isinstance(v[0], dict):
            for i, item in enumerate(v):
                items.extend(_flatten_record_dict(item, f"{new_key}{sep}{i}", sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


def flatten_records(records: list[dict[str, Any]], sep: str = "_") -> list[dict[str, Any]]:
    """Flatten nested foresight records into a flat list of dicts."""
    return [_flatten_record_dict(r, sep=sep) for r in records]


def deduplicate_rows(
    rows: list[dict[str, Any]],
    key_fn: Callable[[dict[str, Any]], tuple[Any, ...]] | None = None,
) -> list[dict[str, Any]]:
    """Deduplicate rows by key function.

    Default key: (question_text, resolution_date) from SDK format.

    """
    def _default_key_fn(row: dict[str, Any]) -> tuple[Any, ...]:
        question: dict[str, Any] = row.get("question") or {}
        label: dict[str, Any] = row.get("label") or {}
        return question.get("question_text"), label.get("resolution_date")

    key_fn_local: Callable[[dict[str, Any]], tuple[Any, ...]] = key_fn or _default_key_fn
    seen: set[tuple[Any, ...]] = set()
    result: list[dict[str, Any]] = []
    for row in rows:
        key = key_fn_local(row)
        if key not in seen:
            seen.add(key)
            result.append(row)
    return result