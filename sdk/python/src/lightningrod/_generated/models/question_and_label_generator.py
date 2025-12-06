from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Literal, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.filter_criteria_config import FilterCriteriaConfig


T = TypeVar("T", bound="QuestionAndLabelGenerator")


@_attrs_define
class QuestionAndLabelGenerator:
    """
    Attributes:
        instructions (str): Instructions for question and label generation
        config_type (Literal['QUESTION_AND_LABEL_GENERATOR'] | Unset): Type of transform configuration Default:
            'QUESTION_AND_LABEL_GENERATOR'.
        examples (list[str] | Unset): Example questions with labels to guide generation
        bad_examples (list[str] | Unset): Examples of questions/labels to avoid
        filter_ (FilterCriteriaConfig | None | Unset): Optional filter to apply after question generation
        questions_per_seed (int | Unset): Number of question/label pairs to generate per seed Default: 1.
    """

    instructions: str
    config_type: Literal["QUESTION_AND_LABEL_GENERATOR"] | Unset = "QUESTION_AND_LABEL_GENERATOR"
    examples: list[str] | Unset = UNSET
    bad_examples: list[str] | Unset = UNSET
    filter_: FilterCriteriaConfig | None | Unset = UNSET
    questions_per_seed: int | Unset = 1
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.filter_criteria_config import FilterCriteriaConfig

        instructions = self.instructions

        config_type = self.config_type

        examples: list[str] | Unset = UNSET
        if not isinstance(self.examples, Unset):
            examples = self.examples

        bad_examples: list[str] | Unset = UNSET
        if not isinstance(self.bad_examples, Unset):
            bad_examples = self.bad_examples

        filter_: dict[str, Any] | None | Unset
        if isinstance(self.filter_, Unset):
            filter_ = UNSET
        elif isinstance(self.filter_, FilterCriteriaConfig):
            filter_ = self.filter_.to_dict()
        else:
            filter_ = self.filter_

        questions_per_seed = self.questions_per_seed

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "instructions": instructions,
            }
        )
        if config_type is not UNSET:
            field_dict["config_type"] = config_type
        if examples is not UNSET:
            field_dict["examples"] = examples
        if bad_examples is not UNSET:
            field_dict["bad_examples"] = bad_examples
        if filter_ is not UNSET:
            field_dict["filter"] = filter_
        if questions_per_seed is not UNSET:
            field_dict["questions_per_seed"] = questions_per_seed

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.filter_criteria_config import FilterCriteriaConfig

        d = dict(src_dict)
        instructions = d.pop("instructions")

        config_type = cast(Literal["QUESTION_AND_LABEL_GENERATOR"] | Unset, d.pop("config_type", UNSET))
        if config_type != "QUESTION_AND_LABEL_GENERATOR" and not isinstance(config_type, Unset):
            raise ValueError(f"config_type must match const 'QUESTION_AND_LABEL_GENERATOR', got '{config_type}'")

        examples = cast(list[str], d.pop("examples", UNSET))

        bad_examples = cast(list[str], d.pop("bad_examples", UNSET))

        def _parse_filter_(data: object) -> FilterCriteriaConfig | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                filter_type_0 = FilterCriteriaConfig.from_dict(data)

                return filter_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(FilterCriteriaConfig | None | Unset, data)

        filter_ = _parse_filter_(d.pop("filter", UNSET))

        questions_per_seed = d.pop("questions_per_seed", UNSET)

        question_and_label_generator = cls(
            instructions=instructions,
            config_type=config_type,
            examples=examples,
            bad_examples=bad_examples,
            filter_=filter_,
            questions_per_seed=questions_per_seed,
        )

        question_and_label_generator.additional_properties = d
        return question_and_label_generator

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
