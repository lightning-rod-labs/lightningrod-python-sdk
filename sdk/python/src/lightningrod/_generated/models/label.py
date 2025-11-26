from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

T = TypeVar("T", bound="Label")


@_attrs_define
class Label:
    """
    Attributes:
        label (str):
        label_confidence (float):
        resolution_date (datetime.datetime | None):
    """

    label: str
    label_confidence: float
    resolution_date: datetime.datetime | None
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        label = self.label

        label_confidence = self.label_confidence

        resolution_date: None | str
        if isinstance(self.resolution_date, datetime.datetime):
            resolution_date = self.resolution_date.isoformat()
        else:
            resolution_date = self.resolution_date

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "label": label,
                "label_confidence": label_confidence,
                "resolution_date": resolution_date,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        label = d.pop("label")

        label_confidence = d.pop("label_confidence")

        def _parse_resolution_date(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                resolution_date_type_0 = isoparse(data)

                return resolution_date_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        resolution_date = _parse_resolution_date(d.pop("resolution_date"))

        label = cls(
            label=label,
            label_confidence=label_confidence,
            resolution_date=resolution_date,
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
