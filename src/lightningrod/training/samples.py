"""Sample preparation and conversion for training.

Main entry point: :func:`prepare_for_training` — filters, deduplicates, splits,
and returns train/test SampleDatasets.
"""

import random
from dataclasses import dataclass, field
from datetime import date, datetime
from typing import TYPE_CHECKING, Any, Callable, Optional, Union

if TYPE_CHECKING:
    from lightningrod.datasets.dataset import SampleDataset

from lightningrod._generated.models.binary_answer_type import BinaryAnswerType
from lightningrod._generated.models.continuous_answer_type import ContinuousAnswerType
from lightningrod._generated.models.forward_looking_question import ForwardLookingQuestion
from lightningrod._generated.models.free_response_answer_type import FreeResponseAnswerType
from lightningrod._generated.models.multiple_choice_answer_type import MultipleChoiceAnswerType
from lightningrod._generated.models.news_context import NewsContext
from lightningrod._generated.models.rag_context import RAGContext
from lightningrod._generated.models.sample import Sample
from lightningrod._generated.models.sample_meta import SampleMeta
from lightningrod._generated.types import Unset

AnswerType = Union[BinaryAnswerType, ContinuousAnswerType, MultipleChoiceAnswerType, FreeResponseAnswerType]

DaysToResolutionRange = Optional[tuple[Optional[int], Optional[int]]]

TrainingSample = dict[str, Any]


@dataclass
class PrepareStats:
    """Tracks metrics collected during prepare_for_training."""
    total: int = 0

    filter_invalid: int = 0
    filter_horizon: int = 0
    filter_context: int = 0
    filter_missing_resolution_date: int = 0
    filter_missing_prediction_date: int = 0
    filter_kept: int = 0

    dedup_removed: int = 0
    dedup_kept: int = 0
    dedup_top_collisions: list[tuple[tuple[Any, ...], int]] = field(default_factory=list)

    split_strategy: str = ""
    split_test_size: float | None = None
    split_no_sort_key: int = 0
    split_leaky: int = 0
    split_train: int = 0
    split_test: int = 0

def _validate_days_to_resolution_range(value: Any) -> None:
    if value is None:
        return
    if not isinstance(value, tuple):
        raise ValueError(
            f"days_to_resolution_range must be a tuple of (min_days, max_days), got {type(value).__name__}. "
            "Example: (7, None) or (14, 60)"
        )
    if len(value) != 2:
        raise ValueError(
            f"days_to_resolution_range must be a 2-tuple (min_days, max_days), got tuple of length {len(value)}"
        )
    min_days, max_days = value
    if min_days is not None and max_days is not None and min_days > max_days:
        raise ValueError("min_days must be <= max_days when both are set")


def _parse_date(value: Any) -> Optional[date]:
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


def filter_samples(
    samples: list[Sample],
    days_to_resolution_range: DaysToResolutionRange = None,
    drop_missing_context: bool = True,
    stats: PrepareStats | None = None,
) -> list[Sample]:
    """Filter samples by validity, horizon, and optional context presence."""
    _validate_days_to_resolution_range(days_to_resolution_range)
    min_horizon = days_to_resolution_range[0] if days_to_resolution_range else None
    max_horizon = days_to_resolution_range[1] if days_to_resolution_range else None

    n_invalid = n_horizon = n_context = n_missing_resolution_date = n_missing_prediction_date = 0
    filtered: list[Sample] = []
    for sample in samples:
        if sample.is_valid is not True:
            n_invalid += 1
            continue

        pred_raw: Any = None
        if sample.question:
            try:
                pred_date = sample.question.prediction_date
                if pred_date:
                    pred_raw = pred_date
            except AttributeError:
                pass

        res_raw: Any = None
        if sample.label:
            res_date = sample.label.resolution_date
            if res_date:
                res_raw = res_date

        pred_d = _parse_date(pred_raw)
        res_d = _parse_date(res_raw)
        if min_horizon is not None or max_horizon is not None:
            if pred_d is None or res_d is None:
                if pred_d is None:
                    n_missing_prediction_date += 1
                if res_d is None:
                    n_missing_resolution_date += 1
                n_horizon += 1
                continue
            horizon_days: int = (res_d - pred_d).days
            if min_horizon is not None and horizon_days < min_horizon:
                n_horizon += 1
                continue
            if max_horizon is not None and horizon_days > max_horizon:
                n_horizon += 1
                continue
        if drop_missing_context:
            if not sample.context:
                n_context += 1
                continue
            contexts = [ctx.to_dict() for ctx in sample.context]
            has_nonempty_rendered: bool = any(
                bool(ctx.get("rendered_context")) and len(str(ctx.get("rendered_context"))) > 0
                for ctx in contexts
            )
            if not has_nonempty_rendered:
                n_context += 1
                continue
        filtered.append(sample)

    if stats is not None:
        stats.filter_invalid = n_invalid
        stats.filter_horizon = n_horizon
        stats.filter_context = n_context
        stats.filter_missing_resolution_date = n_missing_resolution_date
        stats.filter_missing_prediction_date = n_missing_prediction_date
        stats.filter_kept = len(filtered)

    return filtered


def _label_to_numeric(sample: Sample) -> Optional[float]:
    if not sample.label:
        return None
    value = sample.label.label
    if not value:
        return None
    try:
        s = str(value).strip()
        if not s:
            return None
        return float(s)
    except (TypeError, ValueError):
        return None

def _label_to_boolean(sample: Sample) -> Optional[int]:
    if not sample.label:
        return None
    value = sample.label.label
    if value.lower() in ["yes", "true", "1"]:
        return 1
    elif value.lower() in ["no", "false", "0"]:
        return 0
    return None

def _label_to_text(sample: Sample) -> Optional[str]:
    if not sample.label:
        return None
    value = sample.label.label
    if not value:
        return None
    s = str(value).strip()
    return s or None

def sample_label(sample: Sample, answer_type: AnswerType) -> str:
    """Extract the label value from a sample as numeric (float) or text (str) based on answer type."""
    if isinstance(answer_type, BinaryAnswerType):
        return _label_to_boolean(sample)
    elif isinstance(answer_type, ContinuousAnswerType):
        return _label_to_numeric(sample)
    elif isinstance(answer_type, MultipleChoiceAnswerType):
        return _label_to_text(sample)
    elif isinstance(answer_type, FreeResponseAnswerType):
        return _label_to_text(sample)
    raise ValueError(f"Unsupported answer type: {type(answer_type).__name__}")

def _default_leakage_keys() -> list[Callable[[Sample], str | None]]:
    def get_date_close(sample: Sample) -> str | None:
        if not sample.question:
            return None
        try:
            return sample.question.date_close.isoformat()
        except AttributeError:
            return None

    def get_resolution_date(sample: Sample) -> str | None:
        if not sample.label:
            return None
        res_date = sample.label.resolution_date
        if not res_date:
            return None
        return res_date.isoformat()

    return [get_date_close, get_resolution_date]


def train_test_split(
    samples: list[Sample],
    *,
    split_strategy: str = "temporal",
    test_start: str | None = None,
    test_size: float | None = None,
    random_state: int = 196,
    sort_key: Callable[[Sample], str | None] | None = None,
    leakage_keys: list[Callable[[Sample], str | None]] | None = None,
    filter_leaky_train: bool = True,
    stats: PrepareStats | None = None,
) -> tuple[list[str], list[str]]:
    """Split samples into train/test by temporal order or random shuffle, with optional leakage filtering.
    Returns (train_ids, test_ids) for memory efficiency."""
    temporal_split = split_strategy == "temporal"
    if temporal_split:
        if (test_start is None) == (test_size is None):
            raise ValueError("Provide exactly one of test_start or test_size when split_strategy='temporal'")
    else:
        if test_size is None:
            raise ValueError("test_size is required when split_strategy='random'")
        if test_start is not None:
            raise ValueError("test_start is only valid when split_strategy='temporal'")

    if sort_key is None:
        def default_sort_key(sample: Sample) -> str | None:
            if not sample.question:
                return None
            try:
                pred_date = sample.question.prediction_date
                if not pred_date:
                    return None
                return pred_date.isoformat()
            except AttributeError:
                return None
        sort_key = default_sort_key

    if leakage_keys is None:
        leakage_keys = _default_leakage_keys()

    if temporal_split:
        valid_samples = [r for r in samples if sort_key(r) is not None]
        n_no_sort_key = len(samples) - len(valid_samples)
        sorted_samples = sorted(valid_samples, key=sort_key)

        if test_size is not None:
            split_idx = int(len(sorted_samples) * (1 - test_size))
            train, test = sorted_samples[:split_idx], sorted_samples[split_idx:]
        else:
            assert test_start is not None
            train = [r for r in sorted_samples if sort_key(r) is not None and sort_key(r) < test_start]
            test = [r for r in sorted_samples if sort_key(r) is not None and sort_key(r) >= test_start]

        n_leaky = 0
        if filter_leaky_train and test:
            test_cutoff = sort_key(test[0])
            if test_cutoff is not None:
                def is_safe(row: Sample) -> bool:
                    for key_fn in leakage_keys:
                        date_val = key_fn(row)
                        if date_val is not None and date_val >= test_cutoff:
                            return False
                    return True

                train_before = len(train)
                train = [r for r in train if is_safe(r)]
                n_leaky = train_before - len(train)

        if stats is not None:
            stats.split_strategy = "temporal"
            stats.split_no_sort_key = n_no_sort_key
            stats.split_leaky = n_leaky
            stats.split_train = len(train)
            stats.split_test = len(test)

        return [s.id for s in train], [s.id for s in test]

    shuffled = list(samples)
    rng = random.Random(random_state) if random_state is not None else random
    rng.shuffle(shuffled)

    assert test_size is not None
    split_idx = int(len(shuffled) * (1 - test_size))
    train = shuffled[:split_idx]
    test = shuffled[split_idx:]

    if stats is not None:
        stats.split_strategy = "random"
        stats.split_test_size = test_size
        stats.split_train = len(train)
        stats.split_test = len(test)

    return [s.id for s in train], [s.id for s in test]


def _default_dedup_key(sample: Sample) -> tuple[Any, ...]:
    question_text: Any = None
    if sample.question:
        question_text = sample.question.question_text
    resolution_date: Any = None
    if sample.label:
        res_date = sample.label.resolution_date
        if res_date:
            resolution_date = res_date.isoformat()
    return question_text, resolution_date


def deduplicate_samples(
    samples: list[Sample],
    key_fn: Callable[[Sample], tuple[Any, ...]] | None = None,
    stats: PrepareStats | None = None,
) -> list[Sample]:
    """Remove duplicate samples by (question_text, resolution_date) or custom key."""
    key_fn_local: Callable[[Sample], tuple[Any, ...]] = key_fn or _default_dedup_key
    seen: set[tuple[Any, ...]] = set()
    key_counts: dict[tuple[Any, ...], int] = {}
    result: list[Sample] = []
    for sample in samples:
        key = key_fn_local(sample)
        key_counts[key] = key_counts.get(key, 0) + 1
        if key not in seen:
            seen.add(key)
            result.append(sample)

    if stats is not None:
        removed = len(samples) - len(result)
        stats.dedup_removed = removed
        stats.dedup_kept = len(result)
        stats.dedup_top_collisions = sorted(
            ((k, c) for k, c in key_counts.items() if c > 1),
            key=lambda x: -x[1],
        )[:3]

    return result

def to_record(
    sample: Sample,
    answer_type: AnswerType,
) -> dict[str, Any]:
    """Convert a sample to a flat dict for DataFrame inspection or training.

    Uses short, stable field names (question_text, label, prompt, context, etc.).
    When training=True, includes prompt as chat messages; otherwise includes raw fields.

    Args:
        sample: A LightningRod sample.
        answer_type: Answer type for label formatting and answer instructions.
        training: If True, add prompt as chat messages; if False, include raw prompt.
        include_assistant: When training=True, if True append assistant message with
            the correct answer (for SFT). Set False for GRPO or when label is used separately.

    Returns:
        Flat dict suitable for pd.DataFrame([to_record(s, ...) for s in samples]).
    """
    row: TrainingSample = {
        "sample_id": sample.id,
    }
    question = sample.question if not isinstance(sample.question, Unset) else None

    if question:
        if isinstance(question, ForwardLookingQuestion):
            row["question_text"] = question.question_text
            row["date_close"] = question.date_close.isoformat()
            row["event_date"] = question.event_date.isoformat()
            row["resolution_criteria"] = question.resolution_criteria
            if question.prediction_date is not None and not isinstance(question.prediction_date, Unset):
                row["prediction_date"] = question.prediction_date.isoformat()
        else:
            question_text = getattr(question, "question_text", None)
            if question_text is not None:
                row["question_text"] = question_text

    if sample.label and not isinstance(sample.label, Unset):
        row["label"] = sample_label(sample, answer_type)
        row["answer_type"] = answer_type.answer_type.lower()
        row["label_confidence"] = sample.label.label_confidence
        if sample.label.resolution_date is not None and not isinstance(sample.label.resolution_date, Unset):
            row["resolution_date"] = sample.label.resolution_date.isoformat()
        if sample.label.reasoning is not None and not isinstance(sample.label.reasoning, Unset):
            row["reasoning"] = sample.label.reasoning
        if sample.label.answer_sources is not None and not isinstance(sample.label.answer_sources, Unset):
            row["answer_sources"] = sample.label.answer_sources

    if sample.prompt and not isinstance(sample.prompt, Unset):
        row["prompt"] = sample.prompt

    if sample.seed and not isinstance(sample.seed, Unset):
        row["seed_text"] = sample.seed.seed_text
        if sample.seed.url is not None and not isinstance(sample.seed.url, Unset):
            row["seed_url"] = sample.seed.url
        if sample.seed.seed_creation_date is not None and not isinstance(sample.seed.seed_creation_date, Unset):
            row["seed_creation_date"] = sample.seed.seed_creation_date.isoformat()
        if sample.seed.search_query is not None and not isinstance(sample.seed.search_query, Unset):
            row["seed_search_query"] = sample.seed.search_query

    if sample.context is not None and not isinstance(sample.context, Unset):
        # Serialize context objects to dicts to ensure compatibility with DataFrame/from_dict() operations
        row["context"] = [ctx.to_dict() if hasattr(ctx, "to_dict") else ctx for ctx in sample.context]

    meta_key_map = {"filter_reason": "invalid_reason"}
    if sample.meta is not None and not isinstance(sample.meta, Unset):
        if isinstance(sample.meta, SampleMeta):
            for key, value in sample.meta.additional_properties.items():
                row[meta_key_map.get(key, f"meta_{key}")] = value

    if sample.additional_properties:
        for key, value in sample.additional_properties.items():
            row[key] = value

    return row

# to_training_record is used to convert a sample to a record with minimum required fields for training (expected by the training API).
def to_training_record(
    sample: Sample,
    answer_type: AnswerType,
    prompt_template: str | None = None,
    include_assistant: bool = False,
) -> TrainingSample:
    row: TrainingSample = {
        "sample_id": sample.id,
        "prompt": to_messages(sample, answer_type=answer_type, include_assistant=include_assistant, template=prompt_template),
        "correct_answer": sample_label(sample, answer_type),
    }

    if isinstance(answer_type, BinaryAnswerType):
        row["answer_type"] = "binary"
        row["reward_function_type"] = "binary_log_score"
    elif isinstance(answer_type, ContinuousAnswerType):
        row["answer_type"] = "continuous"
        row["reward_function_type"] = "continuous_log_score"
    elif isinstance(answer_type, MultipleChoiceAnswerType):
        row["answer_type"] = "multiple_choice"
        row["reward_function_type"] = "multi_choice_log_score"
    elif isinstance(answer_type, FreeResponseAnswerType):
        row["answer_type"] = "free_response"
        row["reward_function_type"] = ""

    row["answer_parser_type"] = row["answer_type"]

    return row
    

def to_messages(
    sample: Sample,
    template: Optional[str] = None,
    answer_type: Optional[AnswerType] = None,
    include_assistant: bool = False,
) -> list[dict[str, str]]:
    """Convert a sample to LLM chat messages for training or inference.

    Args:
        sample: A LightningRod sample.
        template: Optional format string with placeholders (question_text, context,
            answer_instructions, date_close, etc.). If None, uses default sections.
        answer_type: Optional answer type for answer_format_instruction in the prompt.
        include_assistant: If True and sample has a label, append an assistant message
            with the correct answer. Use for SFT; omit for GRPO, inference, or when
            label is used separately.

    Returns:
        List of chat dicts, e.g. [{"role": "user", "content": "..."}] or
        [{"role": "user", ...}, {"role": "assistant", "content": "..."}] when include_assistant.
    """
    template_values: dict[str, Any] = {}
    question = sample.question if not isinstance(sample.question, Unset) else None
    question_text = question.question_text if question else ""
    template_values["question_text"] = question_text

    context_list = sample.context if not isinstance(sample.context, Unset) else None
    rendered_context = _render_context(context_list) if context_list else ""
    template_values["context"] = rendered_context

    answer_instructions = answer_type.answer_format_instruction if answer_type else ""
    if isinstance(answer_instructions, Unset) or answer_instructions is None:
        answer_instructions = ""
    template_values["answer_instructions"] = answer_instructions

    date_close: Optional[str] = None
    todays_date: Optional[str] = None
    resolution_criteria: Optional[str] = None
    if question and isinstance(question, ForwardLookingQuestion):
        date_close = question.date_close.strftime("%Y-%m-%d")
        todays_date = question.event_date.strftime("%Y-%m-%d")
        resolution_criteria = question.resolution_criteria
    template_values["date_close"] = date_close or ""
    template_values["question_date"] = todays_date or ""
    template_values["resolution_criteria"] = resolution_criteria or ""

    if not isinstance(sample.seed, Unset):
        template_values["seed"] = sample.seed
        template_values["seed_text"] = sample.seed.seed_text
    else:
        template_values["seed_text"] = ""
    if not isinstance(sample.question, Unset):
        template_values["question"] = sample.question
    if not isinstance(sample.label, Unset):
        template_values["label"] = sample.label
    if not isinstance(sample.meta, Unset):
        template_values["meta"] = sample.meta

    if template is not None:
        messages = [{"role": "user", "content": template.format(**template_values)}]
    else:
        sections: list[str] = ["QUESTION:\n{question_text}"]
        if todays_date:
            sections.append("TODAY'S DATE:\n{question_date}")
        if resolution_criteria:
            sections.append("RESOLUTION CRITERIA:\n{resolution_criteria}")
        if date_close:
            sections.append("CLOSE DATE:\n{date_close}")
        if rendered_context.strip():
            sections.append("CONTEXT:\n{context}")
        if answer_instructions.strip():
            sections.append("ANSWER FORMAT:\n{answer_instructions}")
        messages = [{"role": "user", "content": "\n\n".join(sections).format(**template_values)}]

    if include_assistant and answer_type:
        label = sample_label(sample, answer_type)
        if label is not None:
            messages.append({"role": "assistant", "content": f"<answer>{str(label)}</answer>"})

    return messages


def _render_context(context: list[Union[NewsContext, RAGContext]]) -> str:
    if not context:
        return ""
    contexts_by_type: dict[str, list[Union[NewsContext, RAGContext]]] = {}
    for ctx in context:
        ct = "NEWS_CONTEXT" if isinstance(ctx, NewsContext) else "RAG_CONTEXT"
        if ct not in contexts_by_type:
            contexts_by_type[ct] = []
        contexts_by_type[ct].append(ctx)

    headers = {"NEWS_CONTEXT": "NEWS:", "RAG_CONTEXT": "DOCUMENTS:"}
    descriptions = {
        "NEWS_CONTEXT": "Recent news articles relevant to this question:",
        "RAG_CONTEXT": "Retrieved documents relevant to this question:",
    }
    rendered_sections: list[str] = []
    for context_type, type_contexts in contexts_by_type.items():
        header = headers.get(context_type, "CONTEXT:")
        description = descriptions.get(context_type, "")
        content = "\n\n".join(ctx.rendered_context for ctx in type_contexts)
        rendered_sections.append(f"{header}\n{description}\n\n{content}")
    return "\n\n".join(rendered_sections)


def _print_stats(stats: PrepareStats) -> None:
    print(f"[prepare_for_training] Starting with {stats.total} samples")

    parts = []
    if stats.filter_invalid:
        parts.append(f"{stats.filter_invalid} invalid")
    if stats.filter_horizon:
        part = f"{stats.filter_horizon} horizon"
        if stats.filter_missing_resolution_date or stats.filter_missing_prediction_date:
            sub = []
            if stats.filter_missing_resolution_date:
                sub.append(f"{stats.filter_missing_resolution_date} missing resolution date")
            if stats.filter_missing_prediction_date:
                sub.append(f"{stats.filter_missing_prediction_date} missing prediction date")
            part += f" ({', '.join(sub)})"
        parts.append(part)
    if stats.filter_context:
        parts.append(f"{stats.filter_context} missing context")
    if parts:
        print(f"[filter] Dropped {', '.join(parts)} → {stats.filter_kept} remain")
    else:
        print(f"[filter] {stats.filter_kept} remain (0 dropped)")

    if stats.dedup_removed > 0:
        print(f"[dedup] Removed {stats.dedup_removed} duplicates ({stats.dedup_kept + stats.dedup_removed} → {stats.dedup_kept}). Top colliding keys:")
        for k, c in stats.dedup_top_collisions:
            q = repr(k[0])[:60] + ("..." if len(repr(k[0])) > 60 else "")
            print(f"  ({q}, {k[1]}): {c} samples → 1")
    else:
        print(f"[dedup] {stats.dedup_kept} remain (0 duplicates)")

    if stats.split_strategy == "temporal":
        if stats.split_no_sort_key:
            print(f"[split] {stats.split_no_sort_key} samples had no prediction_date (dropped)")
        if stats.split_leaky:
            print(f"[split] {stats.split_leaky} train samples removed for leakage")
        print(f"[split] Temporal split: {stats.split_train} train, {stats.split_test} test")
    else:
        print(f"[split] Random split (test_size={stats.split_test_size}): {stats.split_train} train, {stats.split_test} test")


def prepare_for_training(
    dataset: "SampleDataset",
    answer_type: AnswerType,
    *,
    test_size: float = 0.2,
    split_strategy: str = "temporal",
    test_start: str | None = None,
    drop_missing_context: bool = False,
    days_to_resolution_range: DaysToResolutionRange = None,
    random_state: int = 196,
    filter_leaky_train: bool = True,
    deduplicate_key_fn: Callable[[Sample], tuple[Any, ...]] | None = None,
    verbose: bool = False,
) -> tuple["SampleDataset", "SampleDataset"]:
    """Prepare a dataset for model training: filter, deduplicate, split into train/test.

    Returns train and test SampleDatasets that can be passed to lr.training.run() or
    EvalsClient. Use dataset.preview_prompts() or to_messages() to iterate on
    prompt templates before training.

    Args:
        dataset: SampleDataset to prepare (samples are fetched via dataset.samples()).
        answer_type: The answer type used for filtering and validation.
        test_size: Fraction of samples for the test set (0.0–1.0). Default 0.2.
        split_strategy: 'temporal' (default) or 'random'.
        test_start: ISO date string for temporal splits. Provide exactly one of
            test_start or test_size for temporal splits.
        drop_missing_context: If True, exclude samples with no context.
        days_to_resolution_range: Optional (min_days, max_days) tuple.
        random_state: Seed for reproducible random splits.
        filter_leaky_train: When True and temporal, remove temporal leakage.
        deduplicate_key_fn: Optional function to customize deduplication key.
        verbose: When True, print step-by-step stats.

    Returns:
        (train_dataset, test_dataset): SampleDatasets ready for training/eval.
    """
    samples = dataset.samples()
    stats = PrepareStats(total=len(samples))

    filtered = filter_samples(
        samples,
        days_to_resolution_range=days_to_resolution_range,
        drop_missing_context=drop_missing_context,
        stats=stats,
    )
    deduped = deduplicate_samples(filtered, key_fn=deduplicate_key_fn, stats=stats)

    train_ids, test_ids = train_test_split(
        deduped,
        split_strategy=split_strategy,
        test_start=test_start,
        filter_leaky_train=filter_leaky_train,
        test_size=test_size,
        random_state=random_state,
        stats=stats,
    )

    if verbose:
        _print_stats(stats)

    return dataset.subset(train_ids), dataset.subset(test_ids)