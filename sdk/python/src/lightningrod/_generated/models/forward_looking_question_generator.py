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
        config_type (Literal['FORWARD_LOOKING_QUESTION_GENERATOR'] | Unset): Type of transform configuration Default:
            'FORWARD_LOOKING_QUESTION_GENERATOR'.
        instructions (None | str | Unset): Additional instructions for question generation. If not provided, uses
            sensible defaults.
        examples (list[str] | Unset): Example questions to guide generation
        bad_examples (list[str] | Unset): Examples of questions to avoid
        filter_ (FilterCriteria | list[FilterCriteria] | None | Unset): Optional filter criteria to apply after question
            generation
        include_default_filter (bool | Unset): Whether to include the default filter for generated questions Default:
            True.
        questions_per_seed (int | Unset): Number of questions to generate per seed Default: 1.
    """

    config_type: Literal["FORWARD_LOOKING_QUESTION_GENERATOR"] | Unset = "FORWARD_LOOKING_QUESTION_GENERATOR"
    instructions: None | str | Unset = UNSET
    examples: list[str] | Unset = UNSET
    bad_examples: list[str] | Unset = UNSET
    filter_: FilterCriteria | list[FilterCriteria] | None | Unset = UNSET
    include_default_filter: bool | Unset = True
    questions_per_seed: int | Unset = 1
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.filter_criteria import FilterCriteria

        config_type = self.config_type

        instructions: None | str | Unset
        if isinstance(self.instructions, Unset):
            instructions = UNSET
        else:
            instructions = self.instructions

        examples: list[str] | Unset = UNSET
        if not isinstance(self.examples, Unset):
            examples = self.examples

        bad_examples: list[str] | Unset = UNSET
        if not isinstance(self.bad_examples, Unset):
            bad_examples = self.bad_examples

        filter_: dict[str, Any] | list[dict[str, Any]] | None | Unset
        if isinstance(self.filter_, Unset):
            filter_ = UNSET
        elif isinstance(self.filter_, FilterCriteria):
            filter_ = self.filter_.to_dict()
        elif isinstance(self.filter_, list):
            filter_ = []
            for filter_type_1_item_data in self.filter_:
                filter_type_1_item = filter_type_1_item_data.to_dict()
                filter_.append(filter_type_1_item)

        else:
            filter_ = self.filter_

        include_default_filter = self.include_default_filter

        questions_per_seed = self.questions_per_seed

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if config_type is not UNSET:
            field_dict["config_type"] = config_type
        if instructions is not UNSET:
            field_dict["instructions"] = instructions
        if examples is not UNSET:
            field_dict["examples"] = examples
        if bad_examples is not UNSET:
            field_dict["bad_examples"] = bad_examples
        if filter_ is not UNSET:
            field_dict["filter"] = filter_
        if include_default_filter is not UNSET:
            field_dict["include_default_filter"] = include_default_filter
        if questions_per_seed is not UNSET:
            field_dict["questions_per_seed"] = questions_per_seed

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.filter_criteria import FilterCriteria

        d = dict(src_dict)
        config_type = cast(Literal["FORWARD_LOOKING_QUESTION_GENERATOR"] | Unset, d.pop("config_type", UNSET))
        if config_type != "FORWARD_LOOKING_QUESTION_GENERATOR" and not isinstance(config_type, Unset):
            raise ValueError(f"config_type must match const 'FORWARD_LOOKING_QUESTION_GENERATOR', got '{config_type}'")

        def _parse_instructions(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        instructions = _parse_instructions(d.pop("instructions", UNSET))

        examples = cast(list[str], d.pop("examples", UNSET))

        bad_examples = cast(list[str], d.pop("bad_examples", UNSET))

        def _parse_filter_(data: object) -> FilterCriteria | list[FilterCriteria] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                filter_type_0 = FilterCriteria.from_dict(data)

                return filter_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, list):
                    raise TypeError()
                filter_type_1 = []
                _filter_type_1 = data
                for filter_type_1_item_data in _filter_type_1:
                    filter_type_1_item = FilterCriteria.from_dict(filter_type_1_item_data)

                    filter_type_1.append(filter_type_1_item)

                return filter_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(FilterCriteria | list[FilterCriteria] | None | Unset, data)

        filter_ = _parse_filter_(d.pop("filter", UNSET))

        include_default_filter = d.pop("include_default_filter", UNSET)

        questions_per_seed = d.pop("questions_per_seed", UNSET)

        forward_looking_question_generator = cls(
            config_type=config_type,
            instructions=instructions,
            examples=examples,
            bad_examples=bad_examples,
            filter_=filter_,
            include_default_filter=include_default_filter,
            questions_per_seed=questions_per_seed,
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
