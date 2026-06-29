"""End-to-end inference tests against a real Lightning Rod server.

These hit a live chat-completions endpoint and are skipped unless an API key
is provided, so they never run in plain unit-test/CI contexts.

Run against production (default):

    LIGHTNINGROD_E2E_API_KEY=sk_... pytest tests/test_inference_e2e.py -v

Run against the local server with:

    LIGHTNINGROD_E2E_API_KEY=sk_... \
    LIGHTNINGROD_E2E_BASE_URL=http://localhost:8080/api/public/v1 \
    pytest tests/test_inference_e2e.py -v

`LIGHTNINGROD_E2E_BASE_URL` defaults to production. The model defaults
to `foresight-v4` and can be overridden with `LIGHTNINGROD_E2E_MODEL`.
"""

import os

import pytest

from lightningrod import (
    AnswerType,
    BinaryPrediction,
    ContinuousPrediction,
    FreeResponsePrediction,
    LightningRod,
    MultiChoicePrediction,
    PredictionResult,
    ReasoningEffort,
)

pytest.importorskip("openai")

API_KEY = os.environ.get("LIGHTNINGROD_E2E_API_KEY")
BASE_URL = os.environ.get(
    "LIGHTNINGROD_E2E_BASE_URL", "https://api.lightningrod.ai/v1"
)
MODEL = os.environ.get("LIGHTNINGROD_E2E_MODEL", "foresight-v4")

pytestmark = pytest.mark.skipif(
    not API_KEY,
    reason="Set LIGHTNINGROD_E2E_API_KEY to run live inference tests.",
)


@pytest.fixture(scope="module")
def client() -> LightningRod:
    # Set the credentials/URL directly on the instance so the live server is
    # used regardless of any LIGHTNINGROD_BASE_URL picked up from a local .env.
    lr = LightningRod.__new__(LightningRod)
    lr.api_key = API_KEY
    lr.base_url = BASE_URL.rstrip("/")

    # Connectivity probe — skip the whole module if the server is unreachable.
    try:
        lr.predict("ping", model=MODEL, reasoning_effort="low")
    except Exception as exc:  # noqa: BLE001 - surface as a skip, not a failure
        pytest.skip(f"Live server at {BASE_URL} not reachable: {exc}")
    return lr


def _assert_common(result: PredictionResult) -> None:
    assert isinstance(result, PredictionResult)
    assert isinstance(result.content, str) and result.content
    assert result.model
    assert result.id
    assert result.usage.total_tokens > 0
    # inference_cost_usd and cost_usd are always present per the API contract.
    assert result.usage.inference_cost_usd is not None
    assert result.usage.cost_usd is not None


def test_binary(client: LightningRod) -> None:
    result = client.predict(
        "Will it rain in Seattle tomorrow?",
        model=MODEL,
        answer_type="binary",
        reasoning_effort="low",
    )
    _assert_common(result)
    assert isinstance(result.binary, BinaryPrediction)
    assert 0.0 <= result.binary.probability <= 1.0
    assert "<answer>" in result.content
    # Only the binary field is populated.
    assert result.continuous is None
    assert result.multiple_choice is None
    assert result.free_response is None


def test_binary_with_enums(client: LightningRod) -> None:
    # Enum values should serialize and round-trip just like the string forms.
    result = client.predict(
        "Will the sun rise tomorrow?",
        model=MODEL,
        answer_type=AnswerType.BINARY,
        reasoning_effort=ReasoningEffort.LOW,
    )
    _assert_common(result)
    assert isinstance(result.binary, BinaryPrediction)


def test_free_response(client: LightningRod) -> None:
    result = client.predict(
        "Name one US president.",
        model=MODEL,
        answer_type="free_response",
        reasoning_effort="low",
    )
    _assert_common(result)
    assert isinstance(result.free_response, FreeResponsePrediction)
    assert result.free_response.text.strip()
    assert result.binary is None


def test_continuous(client: LightningRod) -> None:
    result = client.predict(
        "How many moons does Mars have?",
        model=MODEL,
        answer_type="continuous",
        reasoning_effort="low",
    )
    _assert_common(result)
    assert isinstance(result.continuous, ContinuousPrediction)
    assert isinstance(result.continuous.mean, (int, float))
    assert result.continuous.standard_deviation >= 0


def test_multiple_choice(client: LightningRod) -> None:
    result = client.predict(
        "Is the sky blue, green, or red?",
        model=MODEL,
        answer_type="multiple_choice",
        reasoning_effort="low",
    )
    _assert_common(result)
    assert isinstance(result.multiple_choice, MultiChoicePrediction)
    probs = result.multiple_choice.probabilities
    assert probs


def _assert_auto_classified(result: PredictionResult, expected: str) -> None:
    populated = [
        name
        for name in ("binary", "continuous", "multiple_choice", "free_response")
        if getattr(result, name) is not None
    ]
    assert len(populated) == 1, f"expected one populated prediction, got {populated}"
    assert populated[0] == expected, f"expected {expected}, got {populated[0]}"
    assert result.usage.classification_cost_usd is not None

    if expected == "binary":
        assert isinstance(result.binary, BinaryPrediction)
        assert 0.0 <= result.binary.probability <= 1.0
    elif expected == "continuous":
        assert isinstance(result.continuous, ContinuousPrediction)
        assert isinstance(result.continuous.mean, (int, float))
        assert result.continuous.standard_deviation >= 0
    elif expected == "multiple_choice":
        assert isinstance(result.multiple_choice, MultiChoicePrediction)
        assert result.multiple_choice.probabilities
    elif expected == "free_response":
        assert isinstance(result.free_response, FreeResponsePrediction)
        assert result.free_response.text.strip()


@pytest.mark.parametrize(
    ("prompt", "expected"),
    [
        ("Will it rain in Seattle tomorrow?", "binary"),
        ("How many moons does Mars have?", "continuous"),
        ("Is the sky blue, green, or red?", "multiple_choice"),
        ("Name one US president.", "free_response"),
    ],
)
def test_auto_infers_classified_answer_type(
    client: LightningRod, prompt: str, expected: str
) -> None:
    result = client.predict(
        prompt,
        model=MODEL,
        answer_type="auto",
        reasoning_effort="low",
    )
    _assert_common(result)
    _assert_auto_classified(result, expected)


def test_no_answer_type_returns_prose(client: LightningRod) -> None:
    result = client.predict(
        "Say hello in one word.",
        model=MODEL,
        reasoning_effort="low",
    )
    _assert_common(result)
    assert result.binary is None
    assert result.continuous is None
    assert result.multiple_choice is None
    assert result.free_response is None


def test_research_populates_sources(client: LightningRod) -> None:
    result = client.predict(
        "Will the Fed cut interest rates in 2026?",
        model=MODEL,
        answer_type="binary",
        research=True,
        reasoning_effort="low",
    )
    _assert_common(result)
    assert isinstance(result.binary, BinaryPrediction)
    assert result.sources, "expected url_citation sources when research is enabled"
    for source in result.sources:
        assert source.url
    assert result.usage.research_cost_usd is not None
