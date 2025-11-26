from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, Literal, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="NewsSeedGenerator")


@_attrs_define
class NewsSeedGenerator:
    """
    Attributes:
        start_date (datetime.datetime): Start date for news search
        end_date (datetime.datetime): End date for news search
        interval_duration_days (int): Duration of each interval in days
        search_query (str): Search query for news articles
        config_type (Literal['NEWS_SEED_GENERATOR'] | Unset): Type of transform configuration Default:
            'NEWS_SEED_GENERATOR'.
        max_count (int | None | Unset): Maximum number of seeds to generate. If None, process all intervals concurrently
        articles_per_interval (int | Unset): Number of articles to fetch per interval (max 100) Default: 10.
        concurrency_limit (int | Unset): Maximum number of concurrent intervals when max_count is None Default: 5.
    """

    start_date: datetime.datetime
    end_date: datetime.datetime
    interval_duration_days: int
    search_query: str
    config_type: Literal["NEWS_SEED_GENERATOR"] | Unset = "NEWS_SEED_GENERATOR"
    max_count: int | None | Unset = UNSET
    articles_per_interval: int | Unset = 10
    concurrency_limit: int | Unset = 5
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        start_date = self.start_date.isoformat()

        end_date = self.end_date.isoformat()

        interval_duration_days = self.interval_duration_days

        search_query = self.search_query

        config_type = self.config_type

        max_count: int | None | Unset
        if isinstance(self.max_count, Unset):
            max_count = UNSET
        else:
            max_count = self.max_count

        articles_per_interval = self.articles_per_interval

        concurrency_limit = self.concurrency_limit

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "start_date": start_date,
                "end_date": end_date,
                "interval_duration_days": interval_duration_days,
                "search_query": search_query,
            }
        )
        if config_type is not UNSET:
            field_dict["config_type"] = config_type
        if max_count is not UNSET:
            field_dict["max_count"] = max_count
        if articles_per_interval is not UNSET:
            field_dict["articles_per_interval"] = articles_per_interval
        if concurrency_limit is not UNSET:
            field_dict["concurrency_limit"] = concurrency_limit

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        start_date = isoparse(d.pop("start_date"))

        end_date = isoparse(d.pop("end_date"))

        interval_duration_days = d.pop("interval_duration_days")

        search_query = d.pop("search_query")

        config_type = cast(Literal["NEWS_SEED_GENERATOR"] | Unset, d.pop("config_type", UNSET))
        if config_type != "NEWS_SEED_GENERATOR" and not isinstance(config_type, Unset):
            raise ValueError(f"config_type must match const 'NEWS_SEED_GENERATOR', got '{config_type}'")

        def _parse_max_count(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        max_count = _parse_max_count(d.pop("max_count", UNSET))

        articles_per_interval = d.pop("articles_per_interval", UNSET)

        concurrency_limit = d.pop("concurrency_limit", UNSET)

        news_seed_generator = cls(
            start_date=start_date,
            end_date=end_date,
            interval_duration_days=interval_duration_days,
            search_query=search_query,
            config_type=config_type,
            max_count=max_count,
            articles_per_interval=articles_per_interval,
            concurrency_limit=concurrency_limit,
        )

        news_seed_generator.additional_properties = d
        return news_seed_generator

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
