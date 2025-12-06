from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Literal, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.filter_criteria import FilterCriteria


T = TypeVar("T", bound="FilterCriteriaConfig")


@_attrs_define
class FilterCriteriaConfig:
    """Configuration for the FilterCriteria transform.

    Attributes:
        filter_criteria (FilterCriteria): Reusable filter criteria for LLM-based content scoring and filtering.
        config_type (Literal['FILTER_CRITERIA'] | Unset): Type of transform configuration Default: 'FILTER_CRITERIA'.
        input_column (str | Unset): Column name to evaluate for filtering Default: 'question_text'.
    """

    filter_criteria: FilterCriteria
    config_type: Literal["FILTER_CRITERIA"] | Unset = "FILTER_CRITERIA"
    input_column: str | Unset = "question_text"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        filter_criteria = self.filter_criteria.to_dict()

        config_type = self.config_type

        input_column = self.input_column

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "filter_criteria": filter_criteria,
            }
        )
        if config_type is not UNSET:
            field_dict["config_type"] = config_type
        if input_column is not UNSET:
            field_dict["input_column"] = input_column

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.filter_criteria import FilterCriteria

        d = dict(src_dict)
        filter_criteria = FilterCriteria.from_dict(d.pop("filter_criteria"))

        config_type = cast(Literal["FILTER_CRITERIA"] | Unset, d.pop("config_type", UNSET))
        if config_type != "FILTER_CRITERIA" and not isinstance(config_type, Unset):
            raise ValueError(f"config_type must match const 'FILTER_CRITERIA', got '{config_type}'")

        input_column = d.pop("input_column", UNSET)

        filter_criteria_config = cls(
            filter_criteria=filter_criteria,
            config_type=config_type,
            input_column=input_column,
        )

        filter_criteria_config.additional_properties = d
        return filter_criteria_config

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
