from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Literal, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="NewsContextGenerator")


@_attrs_define
class NewsContextGenerator:
    """
    Attributes:
        config_type (Literal['NEWS_CONTEXT_GENERATOR'] | Unset): Type of transform configuration Default:
            'NEWS_CONTEXT_GENERATOR'.
        num_search_queries (int | Unset): Number of search queries to generate per question Default: 5.
        articles_per_query (int | Unset): Number of news articles to return per search query Default: 5.
        num_articles (int | Unset): Maximum number of news articles to include in final output Default: 10.
        relevance_threshold (int | Unset): Minimum relevance rating (1-6 scale) to include article Default: 2.
        min_articles (int | Unset): Minimum number of articles to ensure Default: 6.
        time_delta_days (int | Unset): Number of days to look back for news articles Default: 30.
        concurrency_limit (int | Unset): Maximum number of concurrent tasks Default: 50.
        enable_relevance_ranking (bool | Unset): Whether to perform LLM-based relevance ranking Default: True.
    """

    config_type: Literal["NEWS_CONTEXT_GENERATOR"] | Unset = "NEWS_CONTEXT_GENERATOR"
    num_search_queries: int | Unset = 5
    articles_per_query: int | Unset = 5
    num_articles: int | Unset = 10
    relevance_threshold: int | Unset = 2
    min_articles: int | Unset = 6
    time_delta_days: int | Unset = 30
    concurrency_limit: int | Unset = 50
    enable_relevance_ranking: bool | Unset = True
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        config_type = self.config_type

        num_search_queries = self.num_search_queries

        articles_per_query = self.articles_per_query

        num_articles = self.num_articles

        relevance_threshold = self.relevance_threshold

        min_articles = self.min_articles

        time_delta_days = self.time_delta_days

        concurrency_limit = self.concurrency_limit

        enable_relevance_ranking = self.enable_relevance_ranking

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if config_type is not UNSET:
            field_dict["config_type"] = config_type
        if num_search_queries is not UNSET:
            field_dict["num_search_queries"] = num_search_queries
        if articles_per_query is not UNSET:
            field_dict["articles_per_query"] = articles_per_query
        if num_articles is not UNSET:
            field_dict["num_articles"] = num_articles
        if relevance_threshold is not UNSET:
            field_dict["relevance_threshold"] = relevance_threshold
        if min_articles is not UNSET:
            field_dict["min_articles"] = min_articles
        if time_delta_days is not UNSET:
            field_dict["time_delta_days"] = time_delta_days
        if concurrency_limit is not UNSET:
            field_dict["concurrency_limit"] = concurrency_limit
        if enable_relevance_ranking is not UNSET:
            field_dict["enable_relevance_ranking"] = enable_relevance_ranking

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        config_type = cast(Literal["NEWS_CONTEXT_GENERATOR"] | Unset, d.pop("config_type", UNSET))
        if config_type != "NEWS_CONTEXT_GENERATOR" and not isinstance(config_type, Unset):
            raise ValueError(f"config_type must match const 'NEWS_CONTEXT_GENERATOR', got '{config_type}'")

        num_search_queries = d.pop("num_search_queries", UNSET)

        articles_per_query = d.pop("articles_per_query", UNSET)

        num_articles = d.pop("num_articles", UNSET)

        relevance_threshold = d.pop("relevance_threshold", UNSET)

        min_articles = d.pop("min_articles", UNSET)

        time_delta_days = d.pop("time_delta_days", UNSET)

        concurrency_limit = d.pop("concurrency_limit", UNSET)

        enable_relevance_ranking = d.pop("enable_relevance_ranking", UNSET)

        news_context_generator = cls(
            config_type=config_type,
            num_search_queries=num_search_queries,
            articles_per_query=articles_per_query,
            num_articles=num_articles,
            relevance_threshold=relevance_threshold,
            min_articles=min_articles,
            time_delta_days=time_delta_days,
            concurrency_limit=concurrency_limit,
            enable_relevance_ranking=enable_relevance_ranking,
        )

        news_context_generator.additional_properties = d
        return news_context_generator

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
