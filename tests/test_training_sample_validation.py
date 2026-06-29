from __future__ import annotations

from datetime import datetime

import pytest

from lightningrod._generated.models.binary_answer_type import BinaryAnswerType
from lightningrod._generated.models.label import Label
from lightningrod._generated.models.sample import Sample
from lightningrod._generated.models.seed import Seed
from lightningrod.datasets.dataset import SampleDataset
from lightningrod.training.samples import (
    DedupParams,
    FilterParams,
    PrepareStats,
    SplitParams,
    filter_samples,
    prepare_for_training,
    to_messages,
    to_record,
    to_training_record,
)
from lightningrod._generated.models.forward_looking_question import ForwardLookingQuestion
from lightningrod.training.multi_choice_options import extract_options_from_question_text
from lightningrod.utils.sample import create_sample


class _DummyDatasetsClient:
    def list(self, dataset_id: str) -> list[Sample]:
        return []


def _dataset(samples: list[Sample]) -> SampleDataset:
    return SampleDataset(
        id="ds-test",
        num_rows=len(samples),
        datasets_client=_DummyDatasetsClient(),
        samples=samples,
    )


def test_dataset_exclude_returns_dataset_without_matching_samples() -> None:
    dataset = _dataset([
        Sample(id="keep-1"),
        Sample(id="drop-1"),
        Sample(id="keep-2"),
    ])

    filtered = dataset.exclude(["drop-1", "unknown"])

    assert filtered.id == dataset.id
    assert filtered.num_rows == 2
    assert filtered.sample_ids == ["keep-1", "keep-2"]
    assert [sample.id for sample in filtered.samples()] == ["keep-1", "keep-2"]


def test_create_sample_requires_answer_type_when_label_provided() -> None:
    with pytest.raises(ValueError, match="answer_type is required when label is provided"):
        create_sample("seed", label="yes")


def test_create_sample_accepts_labeled_sample_with_answer_type() -> None:
    sample = create_sample("seed", label="yes", answer_type="BINARY")
    assert sample.label is not None
    assert sample.label.answer_type == "binary"


def test_prepare_for_training_fails_early_when_answer_type_missing() -> None:
    bad = Sample(
        id="s-missing-answer-type",
        is_valid=True,
        seed=Seed(seed_text="seed"),
        label=Label(label="yes", label_confidence=1.0),
    )
    dataset = _dataset([bad])

    with pytest.raises(ValueError, match="has no answer type"):
        prepare_for_training(dataset, verbose=False)


def _mc_sample(question_text: str, sample_id: str = "s-mc") -> Sample:
    return Sample(
        id=sample_id,
        is_valid=True,
        seed=Seed(seed_text="seed"),
        question=ForwardLookingQuestion(
            question_text=question_text,
            date_close=datetime(2030, 1, 1),
            event_date=datetime(2030, 1, 1),
            resolution_criteria="resolves yes if...",
        ),
        label=Label(label="a", label_confidence=1.0, answer_type="multiple_choice"),
    )


def test_prepare_for_training_fails_when_mc_options_too_few() -> None:
    bad = _mc_sample("Q? option_0: a option_1: b")
    dataset = _dataset([bad])

    with pytest.raises(ValueError, match="multiple_choice_options"):
        prepare_for_training(dataset, verbose=False)


def test_prepare_for_training_passes_with_mc_options_from_question_text() -> None:
    good = _mc_sample("Q? option_0: a option_1: b option_2: c")
    dataset = _dataset([good])

    # Resolves 3 options from the question text → no validation error raised.
    prepare_for_training(dataset, split=None, verbose=False)


def test_prepare_for_training_mc_options_override_from_dataset() -> None:
    # Sample text has only 2 options, but the dataset-wide override supplies a valid map.
    sample = _mc_sample("Q? option_0: a option_1: b")
    dataset = SampleDataset(
        id="ds-test",
        num_rows=1,
        datasets_client=_DummyDatasetsClient(),
        samples=[sample],
        multiple_choice_options='{"option_0": "a", "option_1": "b", "option_2": "c"}',
    )

    prepare_for_training(dataset, split=None, verbose=False)


def test_filter_samples_drops_bad_binary_label_and_counts_stat() -> None:
    bad = Sample(
        id="s-bad-binary",
        is_valid=True,
        seed=Seed(seed_text="seed"),
        label=Label(label="maybe", label_confidence=1.0, answer_type="binary"),
    )
    stats = PrepareStats(total=1)
    out = filter_samples([bad], params=FilterParams(), stats=stats)
    assert out == []
    assert stats.filter_missing_or_invalid_label == 1
    assert stats.filter_kept == 0


def test_filter_samples_drops_empty_label_value_and_counts_stat() -> None:
    bad = Sample(
        id="s-empty-label",
        is_valid=True,
        seed=Seed(seed_text="seed"),
        label=Label(label="", label_confidence=1.0, answer_type="binary"),
    )
    stats = PrepareStats(total=1)
    out = filter_samples([bad], params=FilterParams(), stats=stats)
    assert out == []
    assert stats.filter_missing_or_invalid_label == 1
    assert stats.filter_kept == 0


def test_prepare_for_training_reports_but_does_not_raise_when_all_samples_dropped_for_bad_labels(
    capsys: pytest.CaptureFixture[str],
) -> None:
    bad = Sample(
        id="s-bad-binary",
        is_valid=True,
        seed=Seed(seed_text="seed"),
        label=Label(label="maybe", label_confidence=1.0, answer_type="binary"),
    )
    dataset = _dataset([bad])

    train, test = prepare_for_training(dataset, verbose=False, report_format="text")

    assert train.num_rows == 0
    assert test.num_rows == 0
    assert "Unhealthy split" in capsys.readouterr().out


def test_prepare_for_training_allows_rich_report_override(monkeypatch: pytest.MonkeyPatch) -> None:
    import lightningrod.training.samples as samples_mod
    import lightningrod._display as display_mod

    called = False

    def fake_display_prepare_report(report: object, verbose: bool = True) -> None:
        nonlocal called
        called = True

    sample = Sample(
        id="s-ok",
        is_valid=True,
        seed=Seed(seed_text="seed"),
        label=Label(label="yes", label_confidence=1.0, answer_type="binary"),
    )
    dataset = _dataset([sample])

    monkeypatch.setattr(samples_mod, "_print_report", lambda report, verbose: None)
    monkeypatch.setattr(display_mod, "display_prepare_report", fake_display_prepare_report)

    prepare_for_training(dataset, split=None, verbose=False, report_format="rich")

    assert called


def test_to_record_raises_clear_error_for_missing_answer_type() -> None:
    sample = Sample(
        id="s-1",
        seed=Seed(seed_text="seed"),
        label=Label(label="yes", label_confidence=1.0),
    )

    with pytest.raises(ValueError, match="invalid label answer_type: missing answer_type"):
        to_record(sample)


@pytest.fixture
def suppress_prepare_report_raise(monkeypatch: pytest.MonkeyPatch) -> None:
    import lightningrod.training.samples as samples_mod

    monkeypatch.setattr(samples_mod, "_print_report", lambda report, verbose: None)


def test_prepare_for_training_explicit_none_skips_stages(
    suppress_prepare_report_raise: None,
) -> None:
    res = datetime(2026, 6, 1)
    dup_a = Sample(
        id="dup-a",
        is_valid=True,
        seed=Seed(seed_text="same"),
        label=Label(label="yes", label_confidence=1.0, answer_type="binary", resolution_date=res),
    )
    dup_b = Sample(
        id="dup-b",
        is_valid=True,
        seed=Seed(seed_text="same"),
        label=Label(label="yes", label_confidence=1.0, answer_type="binary", resolution_date=res),
    )
    invalid = Sample(
        id="inv",
        is_valid=False,
        seed=Seed(seed_text="seed"),
        label=Label(label="yes", label_confidence=1.0, answer_type="binary"),
    )
    dataset = _dataset([dup_a, dup_b, invalid])
    train, test = prepare_for_training(
        dataset,
        filter=None,
        dedup=None,
        split=None,
        verbose=False,
    )
    assert train.num_rows == 3
    assert test.num_rows == 0


def test_prepare_for_training_omitted_params_use_defaults(
    suppress_prepare_report_raise: None,
) -> None:
    def make_sample(sid: str, qtext: str) -> Sample:
        q = ForwardLookingQuestion(
            question_text=qtext,
            date_close=datetime(2026, 3, 1),
            event_date=datetime(2026, 1, 1),
            resolution_criteria="x",
            prediction_date=datetime(2026, 1, 15),
        )
        return Sample(
            id=sid,
            is_valid=True,
            question=q,
            seed=Seed(seed_text="seed"),
            label=Label(
                label="yes",
                label_confidence=1.0,
                answer_type="binary",
                resolution_date=datetime(2026, 6, 1),
            ),
        )

    dataset = _dataset([make_sample("a", "q-a"), make_sample("b", "q-b")])
    train_default, test_default = prepare_for_training(dataset, verbose=False)
    train_explicit, test_explicit = prepare_for_training(
        dataset,
        filter=FilterParams(),
        dedup=DedupParams(),
        split=SplitParams(),
        verbose=False,
    )
    assert train_default.num_rows == train_explicit.num_rows
    assert test_default.num_rows == test_explicit.num_rows


def test_to_record_normalizes_answer_type() -> None:
    sample = Sample(
        id="s-2",
        seed=Seed(seed_text="seed"),
        label=Label(
            label="1",
            label_confidence=1.0,
            answer_type="BINARY",
            resolution_date=datetime(2026, 1, 1),
        ),
    )

    record = to_record(sample)
    assert record["answer_type"] == "binary"
    assert record["label"] == 1


def _binary_rendered_prompt_sample(prompt: str | None = "PRE-RENDERED PROMPT") -> Sample:
    return Sample(
        id="s-rendered",
        prompt=prompt,
        question=ForwardLookingQuestion(
            question_text="This question should only appear when rendering is needed.",
            date_close=datetime(2030, 1, 1),
            event_date=datetime(2030, 1, 1),
            resolution_criteria="resolves yes if...",
        ),
        label=Label(label="1", label_confidence=1.0, answer_type="binary"),
    )


def test_to_messages_preserves_existing_sample_prompt() -> None:
    sample = _binary_rendered_prompt_sample()

    messages = to_messages(
        sample,
        answer_type=BinaryAnswerType(),
        template="TEMPLATE: {question_text}",
    )

    assert messages == [{"role": "user", "content": "PRE-RENDERED PROMPT"}]


def test_to_training_record_preserves_existing_sample_prompt_for_sft() -> None:
    sample = _binary_rendered_prompt_sample()

    row = to_training_record(sample, BinaryAnswerType(), include_assistant=True)

    assert row["prompt"] == [
        {"role": "user", "content": "PRE-RENDERED PROMPT"},
        {"role": "assistant", "content": "<answer>1</answer>"},
    ]


def test_to_messages_renders_when_sample_prompt_is_missing_or_blank() -> None:
    for prompt in (None, "   "):
        sample = _binary_rendered_prompt_sample(prompt=prompt)

        messages = to_messages(sample, answer_type=BinaryAnswerType())

        assert messages[0]["role"] == "user"
        assert (
            "QUESTION:\nThis question should only appear when rendering is needed."
            in messages[0]["content"]
        )
        assert "ANSWER FORMAT:" in messages[0]["content"]


# --- extract_options_from_question_text: cases derived from real production MC question text.
# Keep in sync with tests/unit/v2/test_multi_choice_options.py in the backend repo. ---

def test_extract_space_separated() -> None:
    q = ("What will the approval rating be? option_0: 45% or lower option_1: 46% to 50% "
         "option_2: 51% to 55% option_3: 56% or higher")
    assert extract_options_from_question_text(q) == {
        "option_0": "45% or lower",
        "option_1": "46% to 50%",
        "option_2": "51% to 55%",
        "option_3": "56% or higher",
    }


def test_extract_semicolon_separated_strips_trailing_separator() -> None:
    q = ("Who wins? option_0: Kamala Harris; option_1: Donald Trump; "
         "option_2: Neither or a statistical tie (within +/- 3 points).")
    assert extract_options_from_question_text(q) == {
        "option_0": "Kamala Harris",
        "option_1": "Donald Trump",
        "option_2": "Neither or a statistical tie (within +/- 3 points).",
    }


def test_extract_comma_separated_keeps_internal_commas() -> None:
    q = ("How many? option_0: Fewer than 1,000 structures, option_1: 1,000 to 5,000 structures, "
         "option_2: More than 5,000 structures")
    assert extract_options_from_question_text(q) == {
        "option_0": "Fewer than 1,000 structures",
        "option_1": "1,000 to 5,000 structures",
        "option_2": "More than 5,000 structures",
    }


def test_extract_newline_separated() -> None:
    q = "Range?\noption_0: Below $3,800.00\noption_1: $3,800.00 to $4,200.00\noption_2: $4,200.00 or higher"
    assert extract_options_from_question_text(q) == {
        "option_0": "Below $3,800.00",
        "option_1": "$3,800.00 to $4,200.00",
        "option_2": "$4,200.00 or higher",
    }


def test_extract_ignores_trailing_answer_format_block() -> None:
    # Regression: the last option must NOT swallow the appended format instruction / JSON example.
    q = ('Rate the risk. option_0: low option_1: medium option_2: high\n\n'
         'Example: <answer>{"option_0": 0.25, "option_1": 0.50, "option_2": 0.25}</answer>')
    assert extract_options_from_question_text(q) == {
        "option_0": "low",
        "option_1": "medium",
        "option_2": "high",
    }


def test_extract_returns_empty_when_no_options() -> None:
    assert extract_options_from_question_text("A plain question with no options.") == {}
