from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Literal, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.filter_criteria import FilterCriteria


T = TypeVar("T", bound="NewsSeedGenerator")


@_attrs_define
class NewsSeedGenerator:
    """
    Attributes:
        start_date (datetime.datetime): Start date for seed search
        end_date (datetime.datetime): End date for seed search
        search_query (list[str] | str): Search query for news articles. If multiple queries are provided, a separate
            search will be done for each query.
        config_type (Literal['NEWS_SEED_GENERATOR'] | Unset): Type of transform configuration Default:
            'NEWS_SEED_GENERATOR'.
        interval_step_days (int | Unset): Duration of each interval step in days Default: 7.
        articles_per_search (int | Unset): Number of articles to fetch per search (max 100). Each query/domain
            combination is a separate search. Default: 10.
        filter_criteria (FilterCriteria | list[FilterCriteria] | None | Unset): Optional criteria for filtering news
            snippets before scraping
        source_domain (list[str] | None | str | Unset): Optional URL source of the news articles, e.g.
            'https://reuters.com/business', if multiple sources are provided, multiple searchers will be done for each
            interval
    """

    start_date: datetime.datetime
    end_date: datetime.datetime
    search_query: list[str] | str
    config_type: Literal["NEWS_SEED_GENERATOR"] | Unset = "NEWS_SEED_GENERATOR"
    interval_step_days: int | Unset = 7
    articles_per_search: int | Unset = 10
    filter_criteria: FilterCriteria | list[FilterCriteria] | None | Unset = UNSET
    source_domain: list[str] | None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.filter_criteria import FilterCriteria

        start_date = self.start_date.isoformat()

        end_date = self.end_date.isoformat()

        search_query: list[str] | str
        if isinstance(self.search_query, list):
            search_query = self.search_query

        else:
            search_query = self.search_query

        config_type = self.config_type

        interval_step_days = self.interval_step_days

        articles_per_search = self.articles_per_search

        filter_criteria: dict[str, Any] | list[dict[str, Any]] | None | Unset
        if isinstance(self.filter_criteria, Unset):
            filter_criteria = UNSET
        elif isinstance(self.filter_criteria, FilterCriteria):
            filter_criteria = self.filter_criteria.to_dict()
        elif isinstance(self.filter_criteria, list):
            filter_criteria = []
            for filter_criteria_type_1_item_data in self.filter_criteria:
                filter_criteria_type_1_item = filter_criteria_type_1_item_data.to_dict()
                filter_criteria.append(filter_criteria_type_1_item)

        else:
            filter_criteria = self.filter_criteria

        source_domain: list[str] | None | str | Unset
        if isinstance(self.source_domain, Unset):
            source_domain = UNSET
        elif isinstance(self.source_domain, list):
            source_domain = self.source_domain

        else:
            source_domain = self.source_domain

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "start_date": start_date,
                "end_date": end_date,
                "search_query": search_query,
            }
        )
        if config_type is not UNSET:
            field_dict["config_type"] = config_type
        if interval_step_days is not UNSET:
            field_dict["interval_step_days"] = interval_step_days
        if articles_per_search is not UNSET:
            field_dict["articles_per_search"] = articles_per_search
        if filter_criteria is not UNSET:
            field_dict["filter_criteria"] = filter_criteria
        if source_domain is not UNSET:
            field_dict["source_domain"] = source_domain

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.filter_criteria import FilterCriteria

        d = dict(src_dict)
        start_date = isoparse(d.pop("start_date"))

        end_date = isoparse(d.pop("end_date"))

        def _parse_search_query(data: object) -> list[str] | str:
            try:
                if not isinstance(data, list):
                    raise TypeError()
                search_query_type_1 = cast(list[str], data)

                return search_query_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[str] | str, data)

        search_query = _parse_search_query(d.pop("search_query"))

        config_type = cast(Literal["NEWS_SEED_GENERATOR"] | Unset, d.pop("config_type", UNSET))
        if config_type != "NEWS_SEED_GENERATOR" and not isinstance(config_type, Unset):
            raise ValueError(f"config_type must match const 'NEWS_SEED_GENERATOR', got '{config_type}'")

        interval_step_days = d.pop("interval_step_days", UNSET)

        articles_per_search = d.pop("articles_per_search", UNSET)

        def _parse_filter_criteria(data: object) -> FilterCriteria | list[FilterCriteria] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                filter_criteria_type_0 = FilterCriteria.from_dict(data)

                return filter_criteria_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, list):
                    raise TypeError()
                filter_criteria_type_1 = []
                _filter_criteria_type_1 = data
                for filter_criteria_type_1_item_data in _filter_criteria_type_1:
                    filter_criteria_type_1_item = FilterCriteria.from_dict(filter_criteria_type_1_item_data)

                    filter_criteria_type_1.append(filter_criteria_type_1_item)

                return filter_criteria_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(FilterCriteria | list[FilterCriteria] | None | Unset, data)

        filter_criteria = _parse_filter_criteria(d.pop("filter_criteria", UNSET))

        def _parse_source_domain(data: object) -> list[str] | None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                source_domain_type_1 = cast(list[str], data)

                return source_domain_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[str] | None | str | Unset, data)

        source_domain = _parse_source_domain(d.pop("source_domain", UNSET))

        news_seed_generator = cls(
            start_date=start_date,
            end_date=end_date,
            search_query=search_query,
            config_type=config_type,
            interval_step_days=interval_step_days,
            articles_per_search=articles_per_search,
            filter_criteria=filter_criteria,
            source_domain=source_domain,
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
