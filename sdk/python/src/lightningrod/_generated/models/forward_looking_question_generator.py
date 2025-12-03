from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Literal, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.filter_criteria import FilterCriteria


T = TypeVar("T", bound="ForwardLookingQuestionGenerator")


@_attrs_define
class ForwardLookingQuestionGenerator:
    """
    Attributes:
        instructions (str): Instructions for question generation
        config_type (Literal['FORWARD_LOOKING_QUESTION_GENERATOR'] | Unset): Type of transform configuration Default:
            'FORWARD_LOOKING_QUESTION_GENERATOR'.
        examples (list[str] | Unset): Example questions to guide generation
        bad_examples (list[str] | Unset): Examples of questions to avoid
        quality_filter (FilterCriteria | None | Unset): Optional quality filter to apply after question generation
    """

    instructions: str
    config_type: Literal["FORWARD_LOOKING_QUESTION_GENERATOR"] | Unset = "FORWARD_LOOKING_QUESTION_GENERATOR"
    examples: list[str] | Unset = UNSET
    bad_examples: list[str] | Unset = UNSET
    quality_filter: FilterCriteria | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.filter_criteria import FilterCriteria

        instructions = self.instructions

        config_type = self.config_type

        examples: list[str] | Unset = UNSET
        if not isinstance(self.examples, Unset):
            examples = self.examples

        bad_examples: list[str] | Unset = UNSET
        if not isinstance(self.bad_examples, Unset):
            bad_examples = self.bad_examples

        quality_filter: dict[str, Any] | None | Unset
        if isinstance(self.quality_filter, Unset):
            quality_filter = UNSET
        elif isinstance(self.quality_filter, FilterCriteria):
            quality_filter = self.quality_filter.to_dict()
        else:
            quality_filter = self.quality_filter

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
        if quality_filter is not UNSET:
            field_dict["quality_filter"] = quality_filter

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.filter_criteria import FilterCriteria

        d = dict(src_dict)
        instructions = d.pop("instructions")

        config_type = cast(Literal["FORWARD_LOOKING_QUESTION_GENERATOR"] | Unset, d.pop("config_type", UNSET))
        if config_type != "FORWARD_LOOKING_QUESTION_GENERATOR" and not isinstance(config_type, Unset):
            raise ValueError(f"config_type must match const 'FORWARD_LOOKING_QUESTION_GENERATOR', got '{config_type}'")

        examples = cast(list[str], d.pop("examples", UNSET))

        bad_examples = cast(list[str], d.pop("bad_examples", UNSET))

        def _parse_quality_filter(data: object) -> FilterCriteria | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                quality_filter_type_0 = FilterCriteria.from_dict(data)

                return quality_filter_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(FilterCriteria | None | Unset, data)

        quality_filter = _parse_quality_filter(d.pop("quality_filter", UNSET))

        forward_looking_question_generator = cls(
            instructions=instructions,
            config_type=config_type,
            examples=examples,
            bad_examples=bad_examples,
            quality_filter=quality_filter,
        )

        forward_looking_question_generator.additional_properties = d
        return forward_looking_question_generator

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
