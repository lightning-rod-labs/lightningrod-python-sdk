from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, Literal, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="GdeltSeedGenerator")


@_attrs_define
class GdeltSeedGenerator:
    """
    Attributes:
        start_date (datetime.datetime): Start date for seed search
        end_date (datetime.datetime): End date for seed search
        interval_duration_days (int): Duration of each interval in days
        config_type (Literal['GDELT_SEED_GENERATOR'] | Unset): Type of transform configuration Default:
            'GDELT_SEED_GENERATOR'.
        articles_per_interval (int | Unset): Number of articles to fetch per interval from BigQuery Default: 1000.
    """

    start_date: datetime.datetime
    end_date: datetime.datetime
    interval_duration_days: int
    config_type: Literal["GDELT_SEED_GENERATOR"] | Unset = "GDELT_SEED_GENERATOR"
    articles_per_interval: int | Unset = 1000
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        start_date = self.start_date.isoformat()

        end_date = self.end_date.isoformat()

        interval_duration_days = self.interval_duration_days

        config_type = self.config_type

        articles_per_interval = self.articles_per_interval

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "start_date": start_date,
                "end_date": end_date,
                "interval_duration_days": interval_duration_days,
            }
        )
        if config_type is not UNSET:
            field_dict["config_type"] = config_type
        if articles_per_interval is not UNSET:
            field_dict["articles_per_interval"] = articles_per_interval

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        start_date = isoparse(d.pop("start_date"))

        end_date = isoparse(d.pop("end_date"))

        interval_duration_days = d.pop("interval_duration_days")

        config_type = cast(Literal["GDELT_SEED_GENERATOR"] | Unset, d.pop("config_type", UNSET))
        if config_type != "GDELT_SEED_GENERATOR" and not isinstance(config_type, Unset):
            raise ValueError(f"config_type must match const 'GDELT_SEED_GENERATOR', got '{config_type}'")

        articles_per_interval = d.pop("articles_per_interval", UNSET)

        gdelt_seed_generator = cls(
            start_date=start_date,
            end_date=end_date,
            interval_duration_days=interval_duration_days,
            config_type=config_type,
            articles_per_interval=articles_per_interval,
        )

        gdelt_seed_generator.additional_properties = d
        return gdelt_seed_generator

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
