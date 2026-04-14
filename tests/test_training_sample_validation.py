from __future__ import annotations

from datetime import datetime

import pytest

from lightningrod._generated.models.label import Label
from lightningrod._generated.models.sample import Sample
from lightningrod._generated.models.seed import Seed
from lightningrod.datasets.dataset import SampleDataset
from lightningrod.training.samples import prepare_for_training, to_record
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


def test_prepare_for_training_fails_early_for_bad_binary_label() -> None:
    bad = Sample(
        id="s-bad-binary",
        is_valid=True,
        seed=Seed(seed_text="seed"),
        label=Label(label="maybe", label_confidence=1.0, answer_type="binary"),
    )
    dataset = _dataset([bad])

    with pytest.raises(ValueError, match="binary answer_type"):
        prepare_for_training(dataset, verbose=False)


def test_to_record_raises_clear_error_for_missing_answer_type() -> None:
    sample = Sample(
        id="s-1",
        seed=Seed(seed_text="seed"),
        label=Label(label="yes", label_confidence=1.0),
    )

    with pytest.raises(ValueError, match="invalid label answer_type: missing answer_type"):
        to_record(sample)


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
