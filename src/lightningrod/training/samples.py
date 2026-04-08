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
    """Tracks metrics collected during prepare_for_training.

    Fields are grouped by pipeline stage. Invariants:
      filter_kept  = total - filter_invalid - filter_horizon - filter_context
      dedup_kept   = filter_kept - dedup_removed
      split_train_before + split_test_after + split_no_sort_key = dedup_kept (temporal)
      split_train_excluded = split_train_before - split_train_after (inferred; train leakage only)
    """

    # ── Input ────────────────────────────────────────────────────────────────
    total: int = 0

    # ── Stage 1: filter_samples ───────────────────────────────────────────────
    filter_invalid: int = 0
    filter_horizon: int = 0
    filter_context: int = 0
    filter_missing_resolution_date: int = 0
    filter_missing_prediction_date: int = 0
    filter_kept: int = 0

    # ── Stage 2: deduplicate_samples ─────────────────────────────────────────
    dedup_removed: int = 0
    dedup_kept: int = 0
    dedup_top_collisions: list[tuple[tuple[Any, ...], int]] = field(default_factory=list)

    # ── Stage 3: train_test_split ─────────────────────────────────────────────
    split_no_sort_key: int = 0

    split_train_before: int = 0
    split_train_after: int = 0
    split_test_after: int = 0


@dataclass
class FilterParams:
    """Parameters for :func:`filter_samples`."""
    days_to_resolution_range: DaysToResolutionRange = None
    drop_missing_context: bool = False


@dataclass
class DedupParams:
    """Parameters for :func:`deduplicate_samples`."""
    key_fn: Callable[[Sample], tuple[Any, ...]] | None = None


@dataclass
class SplitParams:
    """Parameters for :func:`train_test_split`."""
    strategy: str = "temporal"
    test_size: float | None = 0.2
    test_start: str | None = None
    random_state: int = 196
    sort_key: Callable[[Sample], str | None] | None = None
    leakage_keys: list[Callable[[Sample], str | None]] | None = None
    filter_leaky_train: bool = True


@dataclass
class PrepareIssue:
    """A single detected problem in the prepared dataset, with actionable tips."""
    message: str
    tips: list[str] = field(default_factory=list)


@dataclass
class PrepareReport:
    """Full report produced by :func:`prepare_for_training`, covering all pipeline stages."""
    stats: PrepareStats
    issues: list[PrepareIssue] = field(default_factory=list)

    @property
    def is_healthy(self) -> bool:
        return not self.issues


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


def _normalize_answer_type(answer_type: Any) -> str:
    if isinstance(answer_type, Unset) or answer_type is None:
        raise ValueError("missing answer_type")
    normalized = str(answer_type).strip().lower()
    if not normalized:
        raise ValueError("missing answer_type")
    _answer_type_from_str(normalized)
    return normalized


def _validate_sample_for_training(sample: Sample, idx: int) -> Optional[str]:
    if sample.label is None or isinstance(sample.label, Unset):
        return None

    label_value = getattr(sample.label, "label", None)
    if label_value is None or not str(label_value).strip():
        return f"Sample {sample.id or idx} has an empty label value."

    try:
        answer_type = _normalize_answer_type(sample.label.answer_type)
    except ValueError:
        return f"Sample {sample.id or idx} has no answer type."
    except Exception as e:
        return f"Sample {sample.id or idx} has invalid answer type: {e}"

    if answer_type == "binary":
        normalized_label = str(label_value).strip().lower()
        if normalized_label not in {"yes", "no", "true", "false", "1", "0"}:
            return (
                f"Sample {sample.id or idx} has binary answer_type but label "
                f"'{label_value}' is not one of yes/no/true/false/1/0."
            )
    elif answer_type == "continuous":
        try:
            float(str(label_value).strip())
        except (TypeError, ValueError):
            return f"Sample {sample.id or idx} has continuous answer_type but non-numeric label '{label_value}'."

    return None


def _validate_samples_for_training(samples: list[Sample], max_issues: int = 10) -> None:
    issues: list[str] = []
    for idx, sample in enumerate(samples):
        issue = _validate_sample_for_training(sample, idx)
        if issue:
            issues.append(issue)
            if len(issues) >= max_issues:
                break

    if issues:
        error_lines = ["Invalid samples detected before training preparation:", *issues]
        if len(issues) == max_issues:
            error_lines.append(f"... and more (showing first {max_issues}).")
        raise ValueError("\n".join(error_lines))


def filter_samples(
    samples: list[Sample],
    params: FilterParams | None = None,
    stats: PrepareStats | None = None,
) -> list[Sample]:
    """Filter samples by validity, horizon, and optional context presence."""
    params = params or FilterParams()
    _validate_days_to_resolution_range(params.days_to_resolution_range)
    min_horizon = params.days_to_resolution_range[0] if params.days_to_resolution_range else None
    max_horizon = params.days_to_resolution_range[1] if params.days_to_resolution_range else None

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
        if params.drop_missing_context:
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

def _answer_type_from_str(answer_type: str) -> AnswerType:
    if answer_type == "binary":
        return BinaryAnswerType()
    elif answer_type == "continuous":
        return ContinuousAnswerType()
    elif answer_type == "multiple_choice":
        return MultipleChoiceAnswerType()
    elif answer_type == "free_response":
        return FreeResponseAnswerType()
    raise ValueError(f"Unsupported answer type: {answer_type}")

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
    params: SplitParams | None = None,
    stats: PrepareStats | None = None,
) -> tuple[list[str], list[str]]:
    """Split samples into train/test by temporal order or random shuffle, with optional leakage filtering.
    Returns (train_ids, test_ids) for memory efficiency."""
    params = params or SplitParams()
    temporal_split = params.strategy == "temporal"
    if temporal_split:
        if (params.test_start is None) == (params.test_size is None):
            raise ValueError("Provide exactly one of test_start or test_size when strategy='temporal'")
    else:
        if params.test_size is None:
            raise ValueError("test_size is required when strategy='random'")
        if params.test_start is not None:
            raise ValueError("test_start is only valid when strategy='temporal'")

    sort_key = params.sort_key
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

    leakage_keys = params.leakage_keys or _default_leakage_keys()

    if temporal_split:
        valid_samples = [r for r in samples if sort_key(r) is not None]
        n_no_sort_key = len(samples) - len(valid_samples)
        sorted_samples = sorted(valid_samples, key=sort_key)

        if params.test_size is not None:
            split_idx = int(len(sorted_samples) * (1 - params.test_size))
            train, test = sorted_samples[:split_idx], sorted_samples[split_idx:]
        else:
            assert params.test_start is not None
            train = [r for r in sorted_samples if sort_key(r) is not None and sort_key(r) < params.test_start]
            test = [r for r in sorted_samples if sort_key(r) is not None and sort_key(r) >= params.test_start]

        n_leaky = 0
        if params.filter_leaky_train and test:
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
            stats.split_no_sort_key = n_no_sort_key
            stats.split_train_before = len(train) + n_leaky
            stats.split_train_after = len(train)
            stats.split_test_after = len(test)

        return [s.id for s in train], [s.id for s in test]

    shuffled = list(samples)
    rng = random.Random(params.random_state) if params.random_state is not None else random
    rng.shuffle(shuffled)

    assert params.test_size is not None
    split_idx = int(len(shuffled) * (1 - params.test_size))
    train = shuffled[:split_idx]
    test = shuffled[split_idx:]

    if stats is not None:
        stats.split_train_before = len(train)
        stats.split_train_after = len(train)
        stats.split_test_after = len(test)

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
    params: DedupParams | None = None,
    stats: PrepareStats | None = None,
) -> list[Sample]:
    """Remove duplicate samples by (question_text, resolution_date) or custom key."""
    params = params or DedupParams()
    key_fn_local: Callable[[Sample], tuple[Any, ...]] = params.key_fn or _default_dedup_key
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

def to_record(sample: Sample) -> dict[str, Any]:
    """Convert a sample to a flat dict for DataFrame inspection or training.

    Uses short, stable field names (question_text, label, prompt, context, etc.).
    When training=True, includes prompt as chat messages; otherwise includes raw fields.

    Args:
        sample: A LightningRod sample.
        training: If True, add prompt as chat messages; if False, include raw prompt.

    Returns:
        Flat dict suitable for pd.DataFrame([to_record(s) for s in samples]).
    """
    row: TrainingSample = {
        "sample_id": sample.id,
        "is_valid": sample.is_valid,
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
        sample_id = sample.id or "<unknown>"
        try:
            normalized_answer_type = _normalize_answer_type(sample.label.answer_type)
        except ValueError as e:
            raise ValueError(f"Sample {sample_id} has invalid label answer_type: {e}") from e
        answer_type = _answer_type_from_str(normalized_answer_type)
        row["label"] = sample_label(sample, answer_type)
        row["answer_type"] = normalized_answer_type
        row["label_confidence"] = sample.label.label_confidence
        if sample.label.resolution_date is not None and not isinstance(sample.label.resolution_date, Unset):
            row["resolution_date"] = sample.label.resolution_date.isoformat()
        if sample.label.reasoning is not None and not isinstance(sample.label.reasoning, Unset):
            row["reasoning"] = sample.label.reasoning
        if sample.label.answer_sources is not None and not isinstance(sample.label.answer_sources, Unset):
            row["answer_sources"] = sample.label.answer_sources
        else:
            row["answer_sources"] = None
    elif sample.label is None or isinstance(sample.label, Unset):
        row["answer_sources"] = None

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


def _build_report(stats: PrepareStats, split: SplitParams, filter: FilterParams) -> PrepareReport:
    """Build a structured PrepareReport from pipeline stats and params. Pure — no side effects."""
    issues: list[PrepareIssue] = []
    split_train_excluded = stats.split_train_before - stats.split_train_after

    # Issue: majority of train samples leaked into test period
    majority_train_leaked = (
        split.filter_leaky_train
        and split.strategy == "temporal"
        and stats.split_train_before > 0
        and split_train_excluded > stats.split_train_before // 2
    )
    if majority_train_leaked:
        pct = int(100 * split_train_excluded / stats.split_train_before)
        tips: list[str] = []
        max_horizon = filter.days_to_resolution_range[1] if filter.days_to_resolution_range else None
        if max_horizon is not None:
            tips.append(
                f"Extend the seed generator date range to start earlier — the range should span at least "
                f"{max_horizon * 2} days so questions generated near the start resolve well before the test window."
            )
        else:
            tips.append(
                "Extend the seed generator (date) filter range to start earlier — questions generated near the start "
                "will resolve well before the test window. Aim for at least 2× your max resolution horizon."
            )
        tips.append(
            "Generate more samples by increasing max_questions in lr.transforms.run() or removing the limit, "
            "or increase questions_per_seed in your question generator config. "
            "A larger, temporally well-spread dataset naturally pushes the split cutoff far enough back."
        )
        tips.append(
            "If very few seeds were returned by the pipeline (check the run summary table), the search queries "
            "may not surface results across the full date range. Try more diverse search queries, increase "
            "articles_per_search, or shorten interval_duration_days."
        )
        issues.append(PrepareIssue(
            message=(
                f"{split_train_excluded}/{stats.split_train_before} train samples ({pct}%) were removed "
                "for temporal leakage — the date_close or resolution_date of train questions extends into the test period."
            ),
            tips=tips,
        ))

    # Issue: all samples dropped because prediction_date was missing
    if stats.split_no_sort_key > 0 and stats.split_train_after == 0 and stats.split_test_after == 0:
        issues.append(PrepareIssue(
            message=(
                f"All {stats.split_no_sort_key} samples were dropped because prediction_date was missing. "
                "No train or test samples remain."
            ),
            tips=[
                "Ensure your question generator sets prediction_date on every sample.",
                "Check that the sort_key passed to SplitParams can extract a valid date from each sample.",
                "Inspect a few samples with dataset.flattened() to confirm prediction_date is populated.",
            ],
        ))

    # Issue: too few train samples for effective training
    MIN_TRAIN_SAMPLES = 1000
    if stats.split_train_after < MIN_TRAIN_SAMPLES and stats.split_train_after > 0:
        issues.append(PrepareIssue(
            message=(
                f"Only {stats.split_train_after} train samples remain after preparation. "
                f"This is below the recommended minimum of +{MIN_TRAIN_SAMPLES} for effective training."
            ),
            tips=[
                "Increase max_questions in lr.transforms.run() to generate more samples.",
                "Increase questions_per_seed in your question generator (ForwardLookingQuestionGenerator or QuestionGenerator) to produce more questions from each seed article."
                "Add more search queries to your seed generator to diversify seed sources.",
                "Widen the seed generator date range (start_date to end_date) to capture more events.",
            ],
        ))

    # Issue: too few test samples for reliable evaluation
    MIN_TEST_SAMPLES = 200
    if stats.split_test_after < MIN_TEST_SAMPLES and stats.split_test_after > 0:
        issues.append(PrepareIssue(
            message=(
                f"Only {stats.split_test_after} test samples remain after preparation. "
                f"This is below the recommended minimum of +{MIN_TEST_SAMPLES} for reliable evaluation."
            ),
            tips=[
                "Generate more samples overall — test samples come from the most recent portion of your date range.",
                "Ensure your seed generator date range extends close to the present so recent events appear in the test set.",
            ],
        ))

    # Issue: high invalid rate (>30% of samples were invalid)
    HIGH_INVALID_THRESHOLD = 0.30
    if stats.total > 0 and stats.filter_invalid / stats.total > HIGH_INVALID_THRESHOLD:
        pct = int(100 * stats.filter_invalid / stats.total)
        issues.append(PrepareIssue(
            message=(
                f"{stats.filter_invalid}/{stats.total} samples ({pct}%) were marked invalid. "
                "This suggests issues with dataset generation configuration."
            ),
            tips=[
                "Add more examples and bad_examples to guide the question generator toward more sensible questions.",
                "Check the labeler configuration — if WebSearchLabeler can't find resolution info, samples are marked invalid.",
                "Inspect a few invalid samples with dataset.flattened() to identify patterns.",
            ],
        ))

    # Issue: high dedup rate (>40% removed as duplicates)
    HIGH_DEDUP_THRESHOLD = 0.40
    if stats.filter_kept > 0 and stats.dedup_removed / stats.filter_kept > HIGH_DEDUP_THRESHOLD:
        pct = int(100 * stats.dedup_removed / stats.filter_kept)
        issues.append(PrepareIssue(
            message=(
                f"{stats.dedup_removed}/{stats.filter_kept} samples ({pct}%) were duplicates. "
                "The pipeline is generating repetitive or similar questions."
            ),
            tips=[
                "Add more diverse search queries to your seed generator to surface different source articles.",
                "Increase interval_duration_days to spread seeds across more time periods.",
                "Add bad_examples to your question generator showing the repetitive patterns to avoid.",
                "Use more specific instructions in your question generator to encourage variety.",
            ],
        ))

    # Issue: high horizon filter rate (>50% filtered out by horizon)
    HIGH_HORIZON_THRESHOLD = 0.50
    if stats.total > 0 and stats.filter_horizon / stats.total > HIGH_HORIZON_THRESHOLD:
        pct = int(100 * stats.filter_horizon / stats.total)
        horizon_desc = ""
        if filter.days_to_resolution_range:
            min_h, max_h = filter.days_to_resolution_range
            if min_h is not None and max_h is not None:
                horizon_desc = f" (required: {min_h}-{max_h} days)"
            elif min_h is not None:
                horizon_desc = f" (required: ≥{min_h} days)"
            elif max_h is not None:
                horizon_desc = f" (required: ≤{max_h} days)"
        issues.append(PrepareIssue(
            message=(
                f"{stats.filter_horizon}/{stats.total} samples ({pct}%) fell outside the resolution horizon{horizon_desc}. "
            ),
            tips=[
                "Widen your days_to_resolution_range in FilterParams if your use case allows longer/shorter horizons.",
                "Adjust your seed generator date range — questions from very recent seeds may not have resolved yet, "
                "while questions from old seeds may exceed your max horizon.",
                "Check that your question generator is producing questions with appropriate resolution timelines for your target horizon."
            ],
        ))

    return PrepareReport(stats=stats, issues=issues)


def _print_report(report: PrepareReport, verbose: bool) -> None:
    """Print the report to stdout and raise if unhealthy (non-notebook path)."""
    stats = report.stats
    if verbose:
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
        print(f"[filter] Dropped {', '.join(parts)} → {stats.filter_kept} remain" if parts else f"[filter] {stats.filter_kept} remain (0 dropped)")

        if stats.dedup_removed > 0:
            print(f"[dedup] Removed {stats.dedup_removed} duplicates ({stats.dedup_kept + stats.dedup_removed} → {stats.dedup_kept}). Top colliding keys:")
            for k, c in stats.dedup_top_collisions:
                q = repr(k[0])[:60] + ("..." if len(repr(k[0])) > 60 else "")
                print(f"  ({q}, {k[1]}): {c} samples → 1")
        else:
            print(f"[dedup] {stats.dedup_kept} remain (0 duplicates)")

        if stats.split_no_sort_key:
            print(f"[split] {stats.split_no_sort_key} samples had no prediction_date (dropped)")
        n_leaked = stats.split_train_before - stats.split_train_after
        if n_leaked:
            print(f"[split] {n_leaked} train samples removed for leakage")
        print(f"[split] Temporal split: {stats.split_train_after} train, {stats.split_test_after} test")

    if not report.is_healthy:
        lines = ["[prepare_for_training] Unhealthy split detected."]
        for issue in report.issues:
            lines.append(issue.message)
            if issue.tips:
                lines.append("Tips:\n" + "\n".join(f"  - {t}" for t in issue.tips))
        raise ValueError("\n\n".join(lines))


def prepare_for_training(
    dataset: "SampleDataset",
    *,
    filter: FilterParams | None = None,
    dedup: DedupParams | None = None,
    split: SplitParams | None = None,
    verbose: bool = True,
) -> tuple["SampleDataset", "SampleDataset"]:
    """Prepare a dataset for model training: filter, deduplicate, split into train/test.

    Returns train and test SampleDatasets that can be passed to lr.training.run() or
    EvalsClient. Use dataset.preview_prompts() or to_messages() to iterate on
    prompt templates before training.

    Args:
        dataset: SampleDataset to prepare (samples are fetched via dataset.samples()).
        filter: Controls validity filtering and horizon range. See :class:`FilterParams`.
        dedup: Controls deduplication key. See :class:`DedupParams`.
        split: Controls train/test split strategy, size, and leakage filtering. See :class:`SplitParams`.
        verbose: When True, print step-by-step stats.

    Returns:
        (train_dataset, test_dataset): SampleDatasets ready for training/eval.
    """
    filter = filter or FilterParams()
    dedup = dedup or DedupParams()
    split = split or SplitParams()

    samples = dataset.samples()
    _validate_samples_for_training(samples)
    stats = PrepareStats(total=len(samples))

    filtered = filter_samples(samples, filter, stats=stats)
    deduped = deduplicate_samples(filtered, dedup, stats=stats)
    train_ids, test_ids = train_test_split(deduped, split, stats=stats)

    report = _build_report(stats, split=split, filter=filter)
    from lightningrod._display import _is_notebook, display_prepare_report
    if _is_notebook():
        display_prepare_report(report, verbose=verbose)
    else:
        _print_report(report, verbose=verbose)

    return dataset.subset(train_ids), dataset.subset(test_ids)