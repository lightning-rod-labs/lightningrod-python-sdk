from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Literal, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="QuestionFilter")


@_attrs_define
class QuestionFilter:
    r"""
    Attributes:
        config_type (Literal['QUESTION_FILTER'] | Unset): Type of transform configuration Default: 'QUESTION_FILTER'.
        rubric (str | Unset): Rubric for evaluating question quality Default: 'Score the question from 0 to 1 based on
            these criteria:\n- Clear resolution criteria: The question must have an unambiguous way to determine yes/no\n-
            Specific and measurable: Avoids vague terms, includes concrete details\n- Appropriate timeframe: Has a clear
            resolution date or event trigger\n- Not self-referential: Does not reference the prediction itself\n-
            Grammatically correct: Well-formed, readable English'.
        threshold (float | Unset): Minimum score to keep a question Default: 0.7.
    """

    config_type: Literal["QUESTION_FILTER"] | Unset = "QUESTION_FILTER"
    rubric: str | Unset = (
        "Score the question from 0 to 1 based on these criteria:\n- Clear resolution criteria: The question must have an unambiguous way to determine yes/no\n- Specific and measurable: Avoids vague terms, includes concrete details\n- Appropriate timeframe: Has a clear resolution date or event trigger\n- Not self-referential: Does not reference the prediction itself\n- Grammatically correct: Well-formed, readable English"
    )
    threshold: float | Unset = 0.7
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        config_type = self.config_type

        rubric = self.rubric

        threshold = self.threshold

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if config_type is not UNSET:
            field_dict["config_type"] = config_type
        if rubric is not UNSET:
            field_dict["rubric"] = rubric
        if threshold is not UNSET:
            field_dict["threshold"] = threshold

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        config_type = cast(Literal["QUESTION_FILTER"] | Unset, d.pop("config_type", UNSET))
        if config_type != "QUESTION_FILTER" and not isinstance(config_type, Unset):
            raise ValueError(f"config_type must match const 'QUESTION_FILTER', got '{config_type}'")

        rubric = d.pop("rubric", UNSET)

        threshold = d.pop("threshold", UNSET)

        question_filter = cls(
            config_type=config_type,
            rubric=rubric,
            threshold=threshold,
        )

        question_filter.additional_properties = d
        return question_filter

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
