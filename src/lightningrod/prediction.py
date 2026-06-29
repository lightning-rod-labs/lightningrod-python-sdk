"""Types and parsing for ``LightningRod.predict()``.

The public chat completions endpoint embeds a structured answer between
``<answer></answer>`` tags at the end of the message content. This module
defines the enums and result dataclasses that ``predict()`` returns, plus the
parser that turns the raw content string into a typed prediction.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from enum import Enum

__all__ = [
    "DEFAULT_MODEL",
    "AnswerType",
    "ReasoningEffort",
    "BinaryPrediction",
    "ContinuousPrediction",
    "MultiChoicePrediction",
    "FreeResponsePrediction",
    "Source",
    "Usage",
    "PredictionResult",
]

# Latest hosted forecasting model, used when ``predict()`` is called without an
# explicit ``model``. Uses the same provider ID as the OpenAI-compatible
# endpoint.
DEFAULT_MODEL = "LightningRodLabs/foresight-v4"


class AnswerType(str, Enum):
    """Structured answer format to request from the model."""

    BINARY = "binary"
    MULTIPLE_CHOICE = "multiple_choice"
    CONTINUOUS = "continuous"
    FREE_RESPONSE = "free_response"
    AUTO = "auto"


class ReasoningEffort(str, Enum):
    """How much reasoning the model should spend before answering."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


@dataclass
class BinaryPrediction:
    """Yes/no forecast parsed from ``<answer>0.62</answer>``."""

    probability: float
    """Affirmative probability in [0, 1], e.g. ``0.62``."""


@dataclass
class ContinuousPrediction:
    """Numeric forecast with uncertainty."""

    mean: float
    """Point estimate, e.g. ``3.4``."""
    standard_deviation: float
    """Uncertainty around ``mean``, e.g. ``0.45``."""


@dataclass
class MultiChoicePrediction:
    """Discrete-option forecast."""

    probabilities: dict[str, float]
    """Per-option probability keyed by human-readable label, e.g. ``{"Rate cut": 0.28, "Hold": 0.72}``."""


@dataclass
class FreeResponsePrediction:
    """Open-ended textual answer."""

    text: str
    """Model answer text, e.g. ``"The Fed will likely hold rates steady."``."""


@dataclass
class Source:
    url: str
    title: str


@dataclass
class Usage:
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    research_cost_usd: float | None = None
    classification_cost_usd: float | None = None
    inference_cost_usd: float | None = None
    cost_usd: float | None = None


@dataclass
class PredictionResult:
    """Result of a :meth:`LightningRod.predict` call.

    ``content`` always carries the full raw model response (prose plus any
    ``<answer>`` tags). At most one of ``binary``, ``continuous``,
    ``multiple_choice`` or ``free_response`` is populated, depending on the
    answer type returned; all are ``None`` when no answer type was requested.
    """

    content: str
    thinking: str | None
    sources: list[Source]
    usage: Usage
    model: str
    id: str
    binary: BinaryPrediction | None = None
    continuous: ContinuousPrediction | None = None
    multiple_choice: MultiChoicePrediction | None = None
    free_response: FreeResponsePrediction | None = None


_ANSWER_RE = re.compile(r"<answer>(.*?)</answer>", re.DOTALL)
_OPTIONS_RE = re.compile(r"<options>(.*?)</options>", re.DOTALL)


def _label_keyed_probabilities(
    probabilities: dict[str, float],
    options: dict[str, str] | None,
) -> dict[str, float]:
    """Map machine keys in ``probabilities`` to human-readable option labels."""
    if options is None:
        return probabilities
    return {options.get(key, key): value for key, value in probabilities.items()}


def _parse_multiple_choice(content: str, raw: str) -> MultiChoicePrediction | None:
    probabilities = json.loads(raw)
    if not isinstance(probabilities, dict):
        return None
    options_match = _OPTIONS_RE.search(content)
    options = json.loads(options_match.group(1)) if options_match is not None else None
    if options is not None and not isinstance(options, dict):
        return None
    return MultiChoicePrediction(
        probabilities=_label_keyed_probabilities(probabilities, options),
    )


def _parse_prediction(
    content: str,
    answer_type: "AnswerType | str | None",
) -> (
    BinaryPrediction
    | ContinuousPrediction
    | MultiChoicePrediction
    | FreeResponsePrediction
    | None
):
    """Parse the structured ``<answer>`` block out of ``content``.

    Returns the typed prediction matching ``answer_type``, or ``None`` when no
    ``<answer>`` tag is present. Never raises: any parse error returns ``None``.
    """
    if answer_type is None:
        return None

    value = answer_type.value if isinstance(answer_type, AnswerType) else str(answer_type)

    match = _ANSWER_RE.search(content)
    if match is None:
        return None
    raw = match.group(1)

    try:
        if value == AnswerType.BINARY.value:
            return BinaryPrediction(probability=float(raw.strip()))

        if value == AnswerType.CONTINUOUS.value:
            data = json.loads(raw)
            return ContinuousPrediction(
                mean=data["mean"],
                standard_deviation=data["standard_deviation"],
            )

        if value == AnswerType.MULTIPLE_CHOICE.value:
            return _parse_multiple_choice(content, raw)

        if value == AnswerType.FREE_RESPONSE.value:
            return FreeResponsePrediction(text=raw.strip())

        if value == AnswerType.AUTO.value:
            return _parse_auto(content, raw)
    except (ValueError, KeyError, TypeError):
        return None

    return None


def _parse_auto(content: str, raw: str):
    """Best-effort parse when the answer type was classified server-side."""
    # binary first
    try:
        return BinaryPrediction(probability=float(raw.strip()))
    except ValueError:
        pass

    try:
        data = json.loads(raw)
    except (ValueError, TypeError):
        return FreeResponsePrediction(text=raw.strip())

    if isinstance(data, dict):
        options_match = _OPTIONS_RE.search(content)
        if options_match is not None:
            try:
                options = json.loads(options_match.group(1))
                if isinstance(options, dict):
                    return MultiChoicePrediction(
                        probabilities=_label_keyed_probabilities(data, options),
                    )
            except (ValueError, TypeError):
                pass
        if "mean" in data and "standard_deviation" in data:
            return ContinuousPrediction(
                mean=data["mean"],
                standard_deviation=data["standard_deviation"],
            )
        if data and all(
            isinstance(v, (int, float)) and not isinstance(v, bool)
            for v in data.values()
        ):
            return MultiChoicePrediction(probabilities=data)

    return FreeResponsePrediction(text=raw.strip())
