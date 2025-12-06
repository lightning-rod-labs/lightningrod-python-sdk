from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Literal, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="NewsContextGenerator")


@_attrs_define
class NewsContextGenerator:
    r"""
    Attributes:
        config_type (Literal['NEWS_CONTEXT_GENERATOR'] | Unset): Type of transform configuration Default:
            'NEWS_CONTEXT_GENERATOR'.
        search_query_generation_instructions (str | Unset): Instructions for LLM to generate search query from question
            Default: "You are helping generate a search query for Google News to find relevant information for answering a
            question.\n\nGiven the question, generate:\n1. A concise search query that will find relevant news articles\n2.
            A goal describing what information you're looking for\n\nThe search query should be specific enough to find
            relevant articles but not so narrow that it misses important context. Focus on the key entities, events, or
            topics mentioned in the question.".
        num_articles (int | Unset): Number of news articles to fetch per question Default: 5.
        time_delta_days (int | Unset): Number of days to look back for news articles Default: 30.
        concurrency_limit (int | Unset): Maximum number of concurrent news search tasks Default: 10.
    """

    config_type: Literal["NEWS_CONTEXT_GENERATOR"] | Unset = "NEWS_CONTEXT_GENERATOR"
    search_query_generation_instructions: str | Unset = (
        "You are helping generate a search query for Google News to find relevant information for answering a question.\n\nGiven the question, generate:\n1. A concise search query that will find relevant news articles\n2. A goal describing what information you're looking for\n\nThe search query should be specific enough to find relevant articles but not so narrow that it misses important context. Focus on the key entities, events, or topics mentioned in the question."
    )
    num_articles: int | Unset = 5
    time_delta_days: int | Unset = 30
    concurrency_limit: int | Unset = 10
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        config_type = self.config_type

        search_query_generation_instructions = self.search_query_generation_instructions

        num_articles = self.num_articles

        time_delta_days = self.time_delta_days

        concurrency_limit = self.concurrency_limit

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if config_type is not UNSET:
            field_dict["config_type"] = config_type
        if search_query_generation_instructions is not UNSET:
            field_dict["search_query_generation_instructions"] = search_query_generation_instructions
        if num_articles is not UNSET:
            field_dict["num_articles"] = num_articles
        if time_delta_days is not UNSET:
            field_dict["time_delta_days"] = time_delta_days
        if concurrency_limit is not UNSET:
            field_dict["concurrency_limit"] = concurrency_limit

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        config_type = cast(Literal["NEWS_CONTEXT_GENERATOR"] | Unset, d.pop("config_type", UNSET))
        if config_type != "NEWS_CONTEXT_GENERATOR" and not isinstance(config_type, Unset):
            raise ValueError(f"config_type must match const 'NEWS_CONTEXT_GENERATOR', got '{config_type}'")

        search_query_generation_instructions = d.pop("search_query_generation_instructions", UNSET)

        num_articles = d.pop("num_articles", UNSET)

        time_delta_days = d.pop("time_delta_days", UNSET)

        concurrency_limit = d.pop("concurrency_limit", UNSET)

        news_context_generator = cls(
            config_type=config_type,
            search_query_generation_instructions=search_query_generation_instructions,
            num_articles=num_articles,
            time_delta_days=time_delta_days,
            concurrency_limit=concurrency_limit,
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
