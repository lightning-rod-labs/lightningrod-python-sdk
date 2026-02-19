from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Literal, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="TemplateQuestionGenerator")


@_attrs_define
class TemplateQuestionGenerator:
    """
    Attributes:
        question_template (str): Template string with {field} placeholders. Supports {seed_text}, {seed}, and any key in
            {meta} (e.g. {meta.label}).
        config_type (Literal['TEMPLATE_QUESTION_GENERATOR'] | Unset): Type of transform configuration Default:
            'TEMPLATE_QUESTION_GENERATOR'.
    """

    question_template: str
    config_type: Literal["TEMPLATE_QUESTION_GENERATOR"] | Unset = "TEMPLATE_QUESTION_GENERATOR"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        question_template = self.question_template

        config_type = self.config_type

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "question_template": question_template,
            }
        )
        if config_type is not UNSET:
            field_dict["config_type"] = config_type

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        question_template = d.pop("question_template")

        config_type = cast(Literal["TEMPLATE_QUESTION_GENERATOR"] | Unset, d.pop("config_type", UNSET))
        if config_type != "TEMPLATE_QUESTION_GENERATOR" and not isinstance(config_type, Unset):
            raise ValueError(f"config_type must match const 'TEMPLATE_QUESTION_GENERATOR', got '{config_type}'")

        template_question_generator = cls(
            question_template=question_template,
            config_type=config_type,
        )

        template_question_generator.additional_properties = d
        return template_question_generator

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
