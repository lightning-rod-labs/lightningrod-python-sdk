import sys
import types

import pytest

from lightningrod.client import LightningRod, _build_usage
from lightningrod.prediction import (
    DEFAULT_MODEL,
    AnswerType,
    BinaryPrediction,
    ContinuousPrediction,
    FreeResponsePrediction,
    MultiChoicePrediction,
    PredictionResult,
    ReasoningEffort,
    Source,
    Usage,
    _parse_prediction,
)


# --------------------------------------------------------------------------- #
# _parse_prediction
# --------------------------------------------------------------------------- #
class TestParseBinary:
    def test_parses_float(self) -> None:
        result = _parse_prediction("prose\n\n<answer>0.62</answer>", "binary")
        assert result == BinaryPrediction(probability=0.62)

    def test_accepts_enum(self) -> None:
        result = _parse_prediction("<answer>0.0</answer>", AnswerType.BINARY)
        assert result == BinaryPrediction(probability=0.0)

    def test_strips_whitespace(self) -> None:
        result = _parse_prediction("<answer>  0.5  </answer>", "binary")
        assert result == BinaryPrediction(probability=0.5)

    def test_invalid_float_returns_none(self) -> None:
        assert _parse_prediction("<answer>not a number</answer>", "binary") is None


class TestParseContinuous:
    def test_parses_mean_and_std(self) -> None:
        content = '<answer>{"mean": 3.4, "standard_deviation": 0.45}</answer>'
        result = _parse_prediction(content, "continuous")
        assert result == ContinuousPrediction(mean=3.4, standard_deviation=0.45)

    def test_missing_key_returns_none(self) -> None:
        assert _parse_prediction('<answer>{"mean": 3.4}</answer>', "continuous") is None

    def test_invalid_json_returns_none(self) -> None:
        assert _parse_prediction("<answer>{not json}</answer>", "continuous") is None


class TestParseMultipleChoice:
    def test_parses_label_keyed_answer(self) -> None:
        # Current format: human-readable labels are the <answer> keys; no legend.
        content = '<answer>{"Rate cut": 0.28, "Hold": 0.72}</answer>'
        result = _parse_prediction(content, "multiple_choice")
        assert result == MultiChoicePrediction(
            probabilities={"Rate cut": 0.28, "Hold": 0.72},
        )

    def test_parses_legacy_options_and_probabilities(self) -> None:
        # Backward compatibility: legacy two-tag <options>/<answer> with option_N keys.
        content = (
            '<options>{"option_0": "Rate cut", "option_1": "Hold"}</options>'
            '<answer>{"option_0": 0.28, "option_1": 0.72}</answer>'
        )
        result = _parse_prediction(content, "multiple_choice")
        assert result == MultiChoicePrediction(
            probabilities={"Rate cut": 0.28, "Hold": 0.72},
        )

    def test_parses_options_legend_to_label_keys(self) -> None:
        content = (
            '<options>{"A": "No cut", "B": "25bp cut"}</options>'
            '<answer>{"A": 0.30, "B": 0.62}</answer>'
        )
        result = _parse_prediction(content, "multiple_choice")
        assert result == MultiChoicePrediction(
            probabilities={"No cut": 0.30, "25bp cut": 0.62},
        )

    def test_non_dict_answer_returns_none(self) -> None:
        assert _parse_prediction("<answer>0.5</answer>", "multiple_choice") is None

    def test_invalid_json_returns_none(self) -> None:
        content = "<answer>{bad}</answer>"
        assert _parse_prediction(content, "multiple_choice") is None


class TestParseFreeResponse:
    def test_strips_text(self) -> None:
        content = "<answer>  The Fed will likely hold rates steady.  </answer>"
        result = _parse_prediction(content, "free_response")
        assert result == FreeResponsePrediction(text="The Fed will likely hold rates steady.")


class TestParseAuto:
    def test_auto_falls_back_to_binary(self) -> None:
        assert _parse_prediction("<answer>0.42</answer>", "auto") == BinaryPrediction(0.42)

    def test_auto_continuous(self) -> None:
        content = '<answer>{"mean": 1.0, "standard_deviation": 2.0}</answer>'
        assert _parse_prediction(content, "auto") == ContinuousPrediction(1.0, 2.0)

    def test_auto_multiple_choice(self) -> None:
        content = '<options>{"o": "A"}</options><answer>{"o": 1.0}</answer>'
        assert _parse_prediction(content, "auto") == MultiChoicePrediction(
            probabilities={"A": 1.0}
        )

    def test_auto_label_keyed_multiple_choice(self) -> None:
        # Current format under auto: a dict of label -> probability, no legend.
        content = '<answer>{"Cut": 0.6, "Hold": 0.4}</answer>'
        assert _parse_prediction(content, "auto") == MultiChoicePrediction(
            probabilities={"Cut": 0.6, "Hold": 0.4},
        )

    def test_auto_free_response_fallback(self) -> None:
        result = _parse_prediction("<answer>just plain text</answer>", "auto")
        assert result == FreeResponsePrediction(text="just plain text")


class TestParseEdgeCases:
    def test_no_answer_tag_returns_none(self) -> None:
        assert _parse_prediction("pure prose with no tags", "binary") is None

    def test_omitted_answer_type_returns_none(self) -> None:
        assert _parse_prediction("<answer>0.5</answer>", None) is None

    def test_unknown_answer_type_returns_none(self) -> None:
        assert _parse_prediction("<answer>0.5</answer>", "something_else") is None

    def test_multiline_answer_block(self) -> None:
        content = '<answer>\n{"mean": 1.0,\n "standard_deviation": 2.0}\n</answer>'
        assert _parse_prediction(content, "continuous") == ContinuousPrediction(1.0, 2.0)


# --------------------------------------------------------------------------- #
# _build_usage
# --------------------------------------------------------------------------- #
class TestBuildUsage:
    def test_all_fields(self) -> None:
        usage = _build_usage(
            {
                "prompt_tokens": 1287,
                "completion_tokens": 214,
                "total_tokens": 1501,
                "research_cost_usd": 0.042,
                "classification_cost_usd": 0.0001,
                "inference_cost_usd": 0.0012,
                "cost_usd": 0.0433,
            }
        )
        assert usage == Usage(
            prompt_tokens=1287,
            completion_tokens=214,
            total_tokens=1501,
            research_cost_usd=0.042,
            classification_cost_usd=0.0001,
            inference_cost_usd=0.0012,
            cost_usd=0.0433,
        )

    def test_optional_costs_default_to_none(self) -> None:
        usage = _build_usage(
            {"prompt_tokens": 1, "completion_tokens": 2, "total_tokens": 3}
        )
        assert usage.research_cost_usd is None
        assert usage.classification_cost_usd is None
        assert usage.inference_cost_usd is None
        assert usage.cost_usd is None


# --------------------------------------------------------------------------- #
# _build_prediction_result
# --------------------------------------------------------------------------- #
class _StubResponse:
    """Mimics an OpenAI response object exposing .model_dump()."""

    def __init__(self, payload: dict) -> None:
        self._payload = payload

    def model_dump(self) -> dict:
        return self._payload


def _make_payload(message: dict, usage: dict | None = None, **top) -> dict:
    payload = {
        "id": top.get("id", "chatcmpl-7f3a2b1c"),
        "model": top.get("model", "foresight-v4"),
        "choices": [{"index": 0, "message": message, "finish_reason": "stop"}],
        "usage": usage
        if usage is not None
        else {"prompt_tokens": 1, "completion_tokens": 2, "total_tokens": 3},
    }
    return payload


class TestBuildPredictionResult:
    def test_full_binary_response(self) -> None:
        payload = _make_payload(
            {
                "role": "assistant",
                "content": "Recent signals...\n\n<answer>0.62</answer>",
                "thinking": "Weighed base rates...",
                "annotations": [
                    {
                        "type": "url_citation",
                        "url_citation": {
                            "url": "https://example.com/analysis",
                            "title": "Latest analysis",
                            "start_index": 0,
                            "end_index": 0,
                        },
                    }
                ],
            },
            usage={
                "prompt_tokens": 1287,
                "completion_tokens": 214,
                "total_tokens": 1501,
                "research_cost_usd": 0.042,
                "inference_cost_usd": 0.0012,
                "cost_usd": 0.0433,
            },
        )
        result = LightningRod._build_prediction_result(_StubResponse(payload), "binary")

        assert isinstance(result, PredictionResult)
        assert result.content.endswith("<answer>0.62</answer>")
        assert result.thinking == "Weighed base rates..."
        assert result.sources == [
            Source(url="https://example.com/analysis", title="Latest analysis")
        ]
        assert result.model == "foresight-v4"
        assert result.id == "chatcmpl-7f3a2b1c"
        assert result.binary == BinaryPrediction(probability=0.62)
        assert result.continuous is None
        assert result.multiple_choice is None
        assert result.free_response is None
        assert result.usage.research_cost_usd == 0.042
        assert result.usage.classification_cost_usd is None

    def test_continuous_field_populated(self) -> None:
        payload = _make_payload(
            {"content": '<answer>{"mean": 3.4, "standard_deviation": 0.45}</answer>'}
        )
        result = LightningRod._build_prediction_result(_StubResponse(payload), "continuous")
        assert result.continuous == ContinuousPrediction(mean=3.4, standard_deviation=0.45)
        assert result.binary is None

    @pytest.mark.parametrize(
        ("content", "expected"),
        [
            (
                (
                    '<options>{"option_0": "Cut", "option_1": "Hold"}</options>'
                    '<answer>{"option_0": 0.3, "option_1": 0.7}</answer>'
                ),
                MultiChoicePrediction(
                    probabilities={"Cut": 0.3, "Hold": 0.7},
                ),
            ),
            (
                '<answer>{"Rate cut": 0.28, "Hold": 0.72}</answer>',
                MultiChoicePrediction(
                    probabilities={"Rate cut": 0.28, "Hold": 0.72},
                ),
            ),
        ],
        ids=["options_and_answer", "label_keyed_answer_only"],
    )
    def test_multiple_choice_both_formats(
        self, content: str, expected: MultiChoicePrediction
    ) -> None:
        result = LightningRod._build_prediction_result(
            _StubResponse(_make_payload({"content": content})), "multiple_choice"
        )
        assert result.multiple_choice == expected
        assert result.binary is None
        assert result.continuous is None
        assert result.free_response is None

    def test_free_response_field_populated(self) -> None:
        payload = _make_payload({"content": "<answer>Rates hold steady.</answer>"})
        result = LightningRod._build_prediction_result(
            _StubResponse(payload), "free_response"
        )
        assert result.free_response == FreeResponsePrediction(text="Rates hold steady.")

    @pytest.mark.parametrize(
        ("content", "expected"),
        [
            (
                "prose\n\n<answer>0.62</answer>",
                ("binary", BinaryPrediction(probability=0.62)),
            ),
            (
                '<answer>{"mean": 3.4, "standard_deviation": 0.45}</answer>',
                ("continuous", ContinuousPrediction(mean=3.4, standard_deviation=0.45)),
            ),
            (
                (
                    '<options>{"option_0": "Cut", "option_1": "Hold"}</options>'
                    '<answer>{"option_0": 0.3, "option_1": 0.7}</answer>'
                ),
                (
                    "multiple_choice",
                    MultiChoicePrediction(
                        probabilities={"Cut": 0.3, "Hold": 0.7},
                    ),
                ),
            ),
            (
                '<answer>{"Rate cut": 0.28, "Hold": 0.72}</answer>',
                (
                    "multiple_choice",
                    MultiChoicePrediction(
                        probabilities={"Rate cut": 0.28, "Hold": 0.72},
                    ),
                ),
            ),
            (
                "<answer>Rates hold steady.</answer>",
                ("free_response", FreeResponsePrediction(text="Rates hold steady.")),
            ),
        ],
        ids=[
            "binary",
            "continuous",
            "multiple_choice_options_and_answer",
            "multiple_choice_label_keyed",
            "free_response",
        ],
    )
    def test_auto_infers_answer_field(self, content: str, expected: tuple) -> None:
        field_name, expected_prediction = expected
        result = LightningRod._build_prediction_result(
            _StubResponse(_make_payload({"content": content})), "auto"
        )
        assert getattr(result, field_name) == expected_prediction
        for other in ("binary", "continuous", "multiple_choice", "free_response"):
            if other != field_name:
                assert getattr(result, other) is None

    def test_no_answer_type_leaves_all_predictions_none(self) -> None:
        payload = _make_payload({"content": "Just some prose, no answer tags."})
        result = LightningRod._build_prediction_result(_StubResponse(payload), None)
        assert result.content == "Just some prose, no answer tags."
        assert result.binary is None
        assert result.continuous is None
        assert result.multiple_choice is None
        assert result.free_response is None

    def test_missing_thinking_and_annotations(self) -> None:
        payload = _make_payload({"content": "<answer>0.5</answer>"})
        result = LightningRod._build_prediction_result(_StubResponse(payload), "binary")
        assert result.thinking is None
        assert result.sources == []

    def test_null_content_handled(self) -> None:
        payload = _make_payload({"content": None})
        result = LightningRod._build_prediction_result(_StubResponse(payload), "binary")
        assert result.content == ""
        assert result.binary is None

    def test_non_url_citation_annotations_filtered(self) -> None:
        payload = _make_payload(
            {
                "content": "<answer>0.5</answer>",
                "annotations": [
                    {"type": "file_citation", "file_citation": {"file_id": "f1"}},
                    {
                        "type": "url_citation",
                        "url_citation": {"url": "https://a.com", "title": "A"},
                    },
                ],
            }
        )
        result = LightningRod._build_prediction_result(_StubResponse(payload), "binary")
        assert result.sources == [Source(url="https://a.com", title="A")]


# --------------------------------------------------------------------------- #
# predict() — request body construction (mocked OpenAI client)
# --------------------------------------------------------------------------- #
@pytest.fixture
def lr_with_fake_openai(monkeypatch):
    """Yields a factory: ``make_client(content) -> (client, captured)``."""

    def make_client(content: str = "p <answer>0.4</answer>"):
        captured: dict = {}

        class _FakeCompletions:
            def create(self, **kwargs):
                captured.clear()
                captured.update(kwargs)
                return _StubResponse(_make_payload({"content": content}))

        class _FakeChat:
            completions = _FakeCompletions()

        class _FakeOpenAI:
            def __init__(self, **kwargs):
                captured["_init"] = kwargs

            chat = _FakeChat()

        fake_module = types.ModuleType("openai")
        fake_module.OpenAI = _FakeOpenAI
        monkeypatch.setitem(sys.modules, "openai", fake_module)

        client = LightningRod.__new__(LightningRod)
        client.api_key = "test-key"
        client.base_url = "https://api.lightningrod.ai/v1"
        return client, captured

    return make_client


class TestPredictRequestBody:
    def test_research_true(self, lr_with_fake_openai) -> None:
        client, captured = lr_with_fake_openai()
        client.predict("q", model="m", research=True, answer_type="binary")
        assert captured["extra_body"] == {
            "reasoning_effort": "medium",
            "research": True,
            "answer_type": "binary",
        }

    def test_research_list(self, lr_with_fake_openai) -> None:
        client, captured = lr_with_fake_openai()
        client.predict("q", model="m", research=["perplexity", "google_news"])
        assert captured["extra_body"]["research"] == {"sources": ["perplexity", "google_news"]}
        assert "answer_type" not in captured["extra_body"]

    def test_research_false_omitted(self, lr_with_fake_openai) -> None:
        client, captured = lr_with_fake_openai()
        client.predict("q", model="m", research=False)
        assert "research" not in captured["extra_body"]

    def test_research_none_omitted(self, lr_with_fake_openai) -> None:
        client, captured = lr_with_fake_openai()
        client.predict("q", model="m")
        assert "research" not in captured["extra_body"]

    def test_reasoning_effort_enum_serialized(self, lr_with_fake_openai) -> None:
        client, captured = lr_with_fake_openai()
        client.predict("q", model="m", reasoning_effort=ReasoningEffort.HIGH)
        assert captured["extra_body"]["reasoning_effort"] == "high"

    def test_reasoning_effort_string(self, lr_with_fake_openai) -> None:
        client, captured = lr_with_fake_openai()
        client.predict("q", model="m", reasoning_effort="low")
        assert captured["extra_body"]["reasoning_effort"] == "low"

    def test_answer_type_enum_serialized(self, lr_with_fake_openai) -> None:
        client, captured = lr_with_fake_openai()
        client.predict("q", model="m", answer_type=AnswerType.AUTO)
        assert captured["extra_body"]["answer_type"] == "auto"

    @pytest.mark.parametrize(
        ("content", "expected"),
        [
            (
                (
                    'p <options>{"option_0": "Cut", "option_1": "Hold"}</options>'
                    '<answer>{"option_0": 0.3, "option_1": 0.7}</answer>'
                ),
                MultiChoicePrediction(
                    probabilities={"Cut": 0.3, "Hold": 0.7},
                ),
            ),
            (
                'p <answer>{"Rate cut": 0.28, "Hold": 0.72}</answer>',
                MultiChoicePrediction(
                    probabilities={"Rate cut": 0.28, "Hold": 0.72},
                ),
            ),
        ],
        ids=["options_and_answer", "label_keyed_answer_only"],
    )
    def test_multiple_choice_parses_both_formats(
        self, lr_with_fake_openai, content: str, expected: MultiChoicePrediction
    ) -> None:
        client, _ = lr_with_fake_openai(content)
        result = client.predict("q", model="m", answer_type="multiple_choice")
        assert result.multiple_choice == expected
        assert result.binary is None
        assert result.continuous is None
        assert result.free_response is None

    @pytest.mark.parametrize(
        ("content", "field_name", "expected"),
        [
            ("p <answer>0.4</answer>", "binary", BinaryPrediction(probability=0.4)),
            (
                'p <answer>{"mean": 3.4, "standard_deviation": 0.45}</answer>',
                "continuous",
                ContinuousPrediction(mean=3.4, standard_deviation=0.45),
            ),
            (
                (
                    'p <options>{"option_0": "Cut", "option_1": "Hold"}</options>'
                    '<answer>{"option_0": 0.3, "option_1": 0.7}</answer>'
                ),
                "multiple_choice",
                MultiChoicePrediction(
                    probabilities={"Cut": 0.3, "Hold": 0.7},
                ),
            ),
            (
                'p <answer>{"Rate cut": 0.28, "Hold": 0.72}</answer>',
                "multiple_choice",
                MultiChoicePrediction(
                    probabilities={"Rate cut": 0.28, "Hold": 0.72},
                ),
            ),
            (
                "p <answer>Rates hold steady.</answer>",
                "free_response",
                FreeResponsePrediction(text="Rates hold steady."),
            ),
        ],
        ids=[
            "binary",
            "continuous",
            "multiple_choice_options_and_answer",
            "multiple_choice_label_keyed",
            "free_response",
        ],
    )
    def test_auto_parses_all_answer_formats(
        self,
        lr_with_fake_openai,
        content: str,
        field_name: str,
        expected: object,
    ) -> None:
        client, captured = lr_with_fake_openai(content)
        result = client.predict("q", model="m", answer_type="auto")
        assert captured["extra_body"]["answer_type"] == "auto"
        assert getattr(result, field_name) == expected
        for other in ("binary", "continuous", "multiple_choice", "free_response"):
            if other != field_name:
                assert getattr(result, other) is None

    def test_default_reasoning_effort_is_medium(self, lr_with_fake_openai) -> None:
        client, captured = lr_with_fake_openai()
        client.predict("q", model="m")
        assert captured["extra_body"]["reasoning_effort"] == "medium"

    def test_system_prompt_prepended(self, lr_with_fake_openai) -> None:
        client, captured = lr_with_fake_openai()
        client.predict("the question", model="m", system_prompt="be terse")
        assert captured["messages"] == [
            {"role": "system", "content": "be terse"},
            {"role": "user", "content": "the question"},
        ]

    def test_no_system_prompt(self, lr_with_fake_openai) -> None:
        client, captured = lr_with_fake_openai()
        client.predict("the question", model="m")
        assert captured["messages"] == [{"role": "user", "content": "the question"}]

    def test_returns_prediction_result(self, lr_with_fake_openai) -> None:
        client, _ = lr_with_fake_openai()
        result = client.predict("q", model="m", answer_type="binary")
        assert isinstance(result, PredictionResult)
        assert result.binary == BinaryPrediction(probability=0.4)

    def test_caller_extra_body_merged(self, lr_with_fake_openai) -> None:
        client, captured = lr_with_fake_openai()
        client.predict("q", model="m", extra_body={"custom_flag": True})
        assert captured["extra_body"]["custom_flag"] is True
        assert captured["extra_body"]["reasoning_effort"] == "medium"

    def test_model_defaults_to_latest(self, lr_with_fake_openai) -> None:
        client, captured = lr_with_fake_openai()
        client.predict("q")
        assert captured["model"] == DEFAULT_MODEL

    def test_model_override(self, lr_with_fake_openai) -> None:
        client, captured = lr_with_fake_openai()
        client.predict("q", model="LightningRodLabs/foresight-v4")
        assert captured["model"] == "LightningRodLabs/foresight-v4"
