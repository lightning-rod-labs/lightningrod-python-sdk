"""Resolution and validation of multiple_choice_options.

HAND-MIRRORED COPY of the backend helper. The SDK cannot import backend internals, so
this file is a deliberate duplicate of:

    lightningrodlabs/v2/answer_parsers/multi_choice_options.py
    (resolve_multiple_choice_options, validate_multiple_choice_options)

plus the option-extraction regex from:

    lightningrodlabs/v2/answer_parsers/multi_choice_answer_parser.py
    (extract_options_from_question_text)

KEEP IN SYNC: the resolution priority, the minimum option count, and the error messages
below must match the backend exactly, otherwise prepare_for_training will accept datasets
the training API later rejects (or vice versa).
"""

import json
import re
from typing import TYPE_CHECKING, Any, Dict, Optional, Union

from lightningrod._generated.models.sample_meta import SampleMeta
from lightningrod._generated.types import Unset

if TYPE_CHECKING:
    from lightningrod._generated.models.sample import Sample

MIN_MULTIPLE_CHOICE_OPTIONS: int = 3

# Matches "option_N: <text>" patterns embedded in question text (options end at next option_ or end of string)
_OPTION_PATTERN = re.compile(r"option_(\d+):\s*(.+?)(?=\s*option_\d+:|$)", re.DOTALL)


class MultipleChoiceOptionsError(ValueError):
    """Raised when a multiple_choice_options value is missing, malformed, or too small."""


def extract_options_from_question_text(question_text: str) -> Dict[str, str]:
    """Parse ``option_N: <text>`` patterns embedded in a question's text.

    Returns a dict mapping option labels to option texts, e.g.
    ``{"option_0": "Rate increase", "option_1": "No change", "option_2": "Rate cut"}``.
    Returns an empty dict if no options are found.
    """
    return {f"option_{n}": text.strip() for n, text in _OPTION_PATTERN.findall(question_text)}


def resolve_multiple_choice_options(
    sample: "Sample",
    *,
    explicit_options: Optional[Union[Dict[str, str], str]] = None,
    answer_type_options: Optional[Dict[str, str]] = None,
) -> Optional[Union[Dict[str, str], str]]:
    """Resolve the option map for a sample, in priority order:

    1. ``explicit_options`` — an override (e.g. dataset-wide ``multiple_choice_options``).
    2. ``answer_type_options`` — ``MultipleChoiceAnswerType.multiple_choice_options``.
    3. ``sample.meta["multiple_choice_options"]`` — per-sample options.
    4. Options parsed out of ``sample.question.question_text``.

    Returns ``None`` when no options can be resolved.
    """
    if isinstance(explicit_options, Unset):
        explicit_options = None
    if explicit_options is not None:
        return explicit_options
    if answer_type_options:
        return answer_type_options
    meta = sample.meta
    if isinstance(meta, SampleMeta) and "multiple_choice_options" in meta:
        meta_options: Any = meta["multiple_choice_options"]
        if meta_options:
            if isinstance(meta_options, str):
                try:
                    meta_options = json.loads(meta_options)
                except json.JSONDecodeError:
                    pass
            return meta_options
    question = sample.question
    if question is not None and not isinstance(question, Unset):
        question_text = getattr(question, "question_text", None)
        if question_text and not isinstance(question_text, Unset):
            extracted = extract_options_from_question_text(question_text)
            if extracted:
                return extracted
    return None


def validate_multiple_choice_options(options: object) -> Dict[str, str]:
    """Normalize and validate a multiple_choice_options value.

    Accepts a dict or a JSON string. Raises ``MultipleChoiceOptionsError`` if the value
    is missing, not valid JSON, not a dict, or has fewer than
    ``MIN_MULTIPLE_CHOICE_OPTIONS`` options. Returns the parsed dict on success.
    """
    if not options:
        raise MultipleChoiceOptionsError(
            "missing 'multiple_choice_options' (required for multi_choice questions)"
        )
    if isinstance(options, str):
        try:
            options = json.loads(options)
        except json.JSONDecodeError:
            raise MultipleChoiceOptionsError("'multiple_choice_options' is not valid JSON")
    if not isinstance(options, dict):
        raise MultipleChoiceOptionsError(
            f"'multiple_choice_options' must be a dict, got {type(options).__name__}"
        )
    if len(options) < MIN_MULTIPLE_CHOICE_OPTIONS:
        raise MultipleChoiceOptionsError(
            f"'multiple_choice_options' has {len(options)} option(s); "
            f"need at least {MIN_MULTIPLE_CHOICE_OPTIONS} (2-option questions should use BinaryAnswerType)"
        )
    return options
