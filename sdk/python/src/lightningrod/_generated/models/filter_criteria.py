from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.model_config import ModelConfig


T = TypeVar("T", bound="FilterCriteria")


@_attrs_define
class FilterCriteria:
    """Reusable filter criteria for LLM-based content scoring and filtering.

    Attributes:
        rubric (str): Scoring rubric/prompt for evaluating content
        min_score (float | Unset): Minimum score threshold Default: 0.5.
        llm_config (ModelConfig | Unset):
    """

    rubric: str
    min_score: float | Unset = 0.5
    llm_config: ModelConfig | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        rubric = self.rubric

        min_score = self.min_score

        llm_config: dict[str, Any] | Unset = UNSET
        if not isinstance(self.llm_config, Unset):
            llm_config = self.llm_config.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "rubric": rubric,
            }
        )
        if min_score is not UNSET:
            field_dict["min_score"] = min_score
        if llm_config is not UNSET:
            field_dict["llm_config"] = llm_config

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.model_config import ModelConfig

        d = dict(src_dict)
        rubric = d.pop("rubric")

        min_score = d.pop("min_score", UNSET)

        _llm_config = d.pop("llm_config", UNSET)
        llm_config: ModelConfig | Unset
        if isinstance(_llm_config, Unset):
            llm_config = UNSET
        else:
            llm_config = ModelConfig.from_dict(_llm_config)

        filter_criteria = cls(
            rubric=rubric,
            min_score=min_score,
            llm_config=llm_config,
        )

        filter_criteria.additional_properties = d
        return filter_criteria

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
