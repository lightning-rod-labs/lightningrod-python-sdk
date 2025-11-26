from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Literal, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="QuestionGenerator")


@_attrs_define
class QuestionGenerator:
    """
    Attributes:
        instructions (str): Instructions for question generation
        config_type (Literal['QUESTION_GENERATOR'] | Unset): Type of transform configuration Default:
            'QUESTION_GENERATOR'.
        examples (list[str] | Unset): Example questions to guide generation
        bad_examples (list[str] | Unset): Examples of questions to avoid
    """

    instructions: str
    config_type: Literal["QUESTION_GENERATOR"] | Unset = "QUESTION_GENERATOR"
    examples: list[str] | Unset = UNSET
    bad_examples: list[str] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        instructions = self.instructions

        config_type = self.config_type

        examples: list[str] | Unset = UNSET
        if not isinstance(self.examples, Unset):
            examples = self.examples

        bad_examples: list[str] | Unset = UNSET
        if not isinstance(self.bad_examples, Unset):
            bad_examples = self.bad_examples

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

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        instructions = d.pop("instructions")

        config_type = cast(Literal["QUESTION_GENERATOR"] | Unset, d.pop("config_type", UNSET))
        if config_type != "QUESTION_GENERATOR" and not isinstance(config_type, Unset):
            raise ValueError(f"config_type must match const 'QUESTION_GENERATOR', got '{config_type}'")

        examples = cast(list[str], d.pop("examples", UNSET))

        bad_examples = cast(list[str], d.pop("bad_examples", UNSET))

        question_generator = cls(
            instructions=instructions,
            config_type=config_type,
            examples=examples,
            bad_examples=bad_examples,
        )

        question_generator.additional_properties = d
        return question_generator

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
