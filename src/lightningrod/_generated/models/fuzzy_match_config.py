from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="FuzzyMatchConfig")


@_attrs_define
class FuzzyMatchConfig:
    """
    Attributes:
        field (str): Field to match on. Options: ['question_text', 'seed_text', 'seed_url', 'date_close', 'event_date',
            'prediction_date', 'resolution_criteria', 'resolution_date', 'label']
        similarity_threshold (float | None | Unset): If set, perform approximate (fuzzy) matching where the similarity
            between field values must meet or exceed this threshold (from 0.0 to 1.0, with 1.0 being identical and 0.0
            completely dissimilar). If None, only exact matches are considered duplicates.
    """

    field: str
    similarity_threshold: float | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        field = self.field

        similarity_threshold: float | None | Unset
        if isinstance(self.similarity_threshold, Unset):
            similarity_threshold = UNSET
        else:
            similarity_threshold = self.similarity_threshold

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "field": field,
            }
        )
        if similarity_threshold is not UNSET:
            field_dict["similarity_threshold"] = similarity_threshold

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        field = d.pop("field")

        def _parse_similarity_threshold(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        similarity_threshold = _parse_similarity_threshold(d.pop("similarity_threshold", UNSET))

        fuzzy_match_config = cls(
            field=field,
            similarity_threshold=similarity_threshold,
        )

        fuzzy_match_config.additional_properties = d
        return fuzzy_match_config

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
