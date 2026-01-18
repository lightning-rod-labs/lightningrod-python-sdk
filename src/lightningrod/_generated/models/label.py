from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="Label")


@_attrs_define
class Label:
    """
    Attributes:
        label (str):
        label_confidence (float):
        resolution_date (datetime.datetime | None | Unset):
        reasoning (None | str | Unset):
        answer_sources (None | str | Unset):
    """

    label: str
    label_confidence: float
    resolution_date: datetime.datetime | None | Unset = UNSET
    reasoning: None | str | Unset = UNSET
    answer_sources: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        label = self.label

        label_confidence = self.label_confidence

        resolution_date: None | str | Unset
        if isinstance(self.resolution_date, Unset):
            resolution_date = UNSET
        elif isinstance(self.resolution_date, datetime.datetime):
            resolution_date = self.resolution_date.isoformat()
        else:
            resolution_date = self.resolution_date

        reasoning: None | str | Unset
        if isinstance(self.reasoning, Unset):
            reasoning = UNSET
        else:
            reasoning = self.reasoning

        answer_sources: None | str | Unset
        if isinstance(self.answer_sources, Unset):
            answer_sources = UNSET
        else:
            answer_sources = self.answer_sources

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "label": label,
                "label_confidence": label_confidence,
            }
        )
        if resolution_date is not UNSET:
            field_dict["resolution_date"] = resolution_date
        if reasoning is not UNSET:
            field_dict["reasoning"] = reasoning
        if answer_sources is not UNSET:
            field_dict["answer_sources"] = answer_sources

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        label = d.pop("label")

        label_confidence = d.pop("label_confidence")

        def _parse_resolution_date(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                resolution_date_type_0 = isoparse(data)

                return resolution_date_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        resolution_date = _parse_resolution_date(d.pop("resolution_date", UNSET))

        def _parse_reasoning(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        reasoning = _parse_reasoning(d.pop("reasoning", UNSET))

        def _parse_answer_sources(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        answer_sources = _parse_answer_sources(d.pop("answer_sources", UNSET))

        label = cls(
            label=label,
            label_confidence=label_confidence,
            resolution_date=resolution_date,
            reasoning=reasoning,
            answer_sources=answer_sources,
        )

        label.additional_properties = d
        return label

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
