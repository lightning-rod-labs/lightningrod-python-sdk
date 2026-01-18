from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Literal, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.answer_type import AnswerType


T = TypeVar("T", bound="QuestionRenderer")


@_attrs_define
class QuestionRenderer:
    """
    Attributes:
        config_type (Literal['QUESTION_RENDERER'] | Unset): Type of transform configuration Default:
            'QUESTION_RENDERER'.
        template (None | str | Unset): Custom template for rendering the prompt. If not provided, dynamically builds
            based on available content. Supports placeholders like {question_text}, {context}, {answer_instructions}.
        answer_type (AnswerType | None | Unset): The type of answer expected, used to render answer instructions
    """

    config_type: Literal["QUESTION_RENDERER"] | Unset = "QUESTION_RENDERER"
    template: None | str | Unset = UNSET
    answer_type: AnswerType | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.answer_type import AnswerType

        config_type = self.config_type

        template: None | str | Unset
        if isinstance(self.template, Unset):
            template = UNSET
        else:
            template = self.template

        answer_type: dict[str, Any] | None | Unset
        if isinstance(self.answer_type, Unset):
            answer_type = UNSET
        elif isinstance(self.answer_type, AnswerType):
            answer_type = self.answer_type.to_dict()
        else:
            answer_type = self.answer_type

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if config_type is not UNSET:
            field_dict["config_type"] = config_type
        if template is not UNSET:
            field_dict["template"] = template
        if answer_type is not UNSET:
            field_dict["answer_type"] = answer_type

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.answer_type import AnswerType

        d = dict(src_dict)
        config_type = cast(Literal["QUESTION_RENDERER"] | Unset, d.pop("config_type", UNSET))
        if config_type != "QUESTION_RENDERER" and not isinstance(config_type, Unset):
            raise ValueError(f"config_type must match const 'QUESTION_RENDERER', got '{config_type}'")

        def _parse_template(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        template = _parse_template(d.pop("template", UNSET))

        def _parse_answer_type(data: object) -> AnswerType | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                answer_type_type_0 = AnswerType.from_dict(data)

                return answer_type_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(AnswerType | None | Unset, data)

        answer_type = _parse_answer_type(d.pop("answer_type", UNSET))

        question_renderer = cls(
            config_type=config_type,
            template=template,
            answer_type=answer_type,
        )

        question_renderer.additional_properties = d
        return question_renderer

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
