from __future__ import annotations

from datetime import datetime

import pytest

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
    to_record,
)
from lightningrod._generated.models.forward_looking_question import ForwardLookingQuestion
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
