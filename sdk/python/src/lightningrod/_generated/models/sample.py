from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.label import Label
    from ..models.question import Question
    from ..models.sample_meta import SampleMeta
    from ..models.seed import Seed


T = TypeVar("T", bound="Sample")


@_attrs_define
class Sample:
    """
    Attributes:
        sample_id (str):
        seed (None | Seed):
        question (None | Question):
        label (Label | None):
        meta (SampleMeta):
    """

    sample_id: str
    seed: None | Seed
    question: None | Question
    label: Label | None
    meta: SampleMeta
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.label import Label
        from ..models.question import Question
        from ..models.seed import Seed

        sample_id = self.sample_id

        seed: dict[str, Any] | None
        if isinstance(self.seed, Seed):
            seed = self.seed.to_dict()
        else:
            seed = self.seed

        question: dict[str, Any] | None
        if isinstance(self.question, Question):
            question = self.question.to_dict()
        else:
            question = self.question

        label: dict[str, Any] | None
        if isinstance(self.label, Label):
            label = self.label.to_dict()
        else:
            label = self.label

        meta = self.meta.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "sample_id": sample_id,
                "seed": seed,
                "question": question,
                "label": label,
                "meta": meta,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.label import Label
        from ..models.question import Question
        from ..models.sample_meta import SampleMeta
        from ..models.seed import Seed

        d = dict(src_dict)
        sample_id = d.pop("sample_id")

        def _parse_seed(data: object) -> None | Seed:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                seed_type_0 = Seed.from_dict(data)

                return seed_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | Seed, data)

        seed = _parse_seed(d.pop("seed"))

        def _parse_question(data: object) -> None | Question:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                question_type_0 = Question.from_dict(data)

                return question_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | Question, data)

        question = _parse_question(d.pop("question"))

        def _parse_label(data: object) -> Label | None:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                label_type_0 = Label.from_dict(data)

                return label_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(Label | None, data)

        label = _parse_label(d.pop("label"))

        meta = SampleMeta.from_dict(d.pop("meta"))

        sample = cls(
            sample_id=sample_id,
            seed=seed,
            question=question,
            label=label,
            meta=meta,
        )

        sample.additional_properties = d
        return sample

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
