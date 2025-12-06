from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

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
        seed (None | Seed | Unset):
        question (None | Question | Unset):
        label (Label | None | Unset):
        prompt (None | str | Unset):
        meta (SampleMeta | Unset):
    """

    seed: None | Seed | Unset = UNSET
    question: None | Question | Unset = UNSET
    label: Label | None | Unset = UNSET
    prompt: None | str | Unset = UNSET
    meta: SampleMeta | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.label import Label
        from ..models.question import Question
        from ..models.seed import Seed

        seed: dict[str, Any] | None | Unset
        if isinstance(self.seed, Unset):
            seed = UNSET
        elif isinstance(self.seed, Seed):
            seed = self.seed.to_dict()
        else:
            seed = self.seed

        question: dict[str, Any] | None | Unset
        if isinstance(self.question, Unset):
            question = UNSET
        elif isinstance(self.question, Question):
            question = self.question.to_dict()
        else:
            question = self.question

        label: dict[str, Any] | None | Unset
        if isinstance(self.label, Unset):
            label = UNSET
        elif isinstance(self.label, Label):
            label = self.label.to_dict()
        else:
            label = self.label

        prompt: None | str | Unset
        if isinstance(self.prompt, Unset):
            prompt = UNSET
        else:
            prompt = self.prompt

        meta: dict[str, Any] | Unset = UNSET
        if not isinstance(self.meta, Unset):
            meta = self.meta.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if seed is not UNSET:
            field_dict["seed"] = seed
        if question is not UNSET:
            field_dict["question"] = question
        if label is not UNSET:
            field_dict["label"] = label
        if prompt is not UNSET:
            field_dict["prompt"] = prompt
        if meta is not UNSET:
            field_dict["meta"] = meta

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.label import Label
        from ..models.question import Question
        from ..models.sample_meta import SampleMeta
        from ..models.seed import Seed

        d = dict(src_dict)

        def _parse_seed(data: object) -> None | Seed | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                seed_type_0 = Seed.from_dict(data)

                return seed_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | Seed | Unset, data)

        seed = _parse_seed(d.pop("seed", UNSET))

        def _parse_question(data: object) -> None | Question | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                question_type_0 = Question.from_dict(data)

                return question_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | Question | Unset, data)

        question = _parse_question(d.pop("question", UNSET))

        def _parse_label(data: object) -> Label | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                label_type_0 = Label.from_dict(data)

                return label_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(Label | None | Unset, data)

        label = _parse_label(d.pop("label", UNSET))

        def _parse_prompt(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        prompt = _parse_prompt(d.pop("prompt", UNSET))

        _meta = d.pop("meta", UNSET)
        meta: SampleMeta | Unset
        if isinstance(_meta, Unset):
            meta = UNSET
        else:
            meta = SampleMeta.from_dict(_meta)

        sample = cls(
            seed=seed,
            question=question,
            label=label,
            prompt=prompt,
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
