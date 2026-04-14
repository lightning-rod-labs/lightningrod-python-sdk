from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Literal, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="WebSearchContextGenerator")


@_attrs_define
class WebSearchContextGenerator:
    """
    Attributes:
        config_type (Literal['WEB_SEARCH_CONTEXT_GENERATOR'] | Unset): Type of transform configuration Default:
            'WEB_SEARCH_CONTEXT_GENERATOR'.
        num_search_queries (int | Unset): Number of search queries to generate per question Default: 5.
        results_per_query (int | Unset): Number of search results to return per query Default: 3.
        num_results (int | Unset): Maximum number of search results to include in final output Default: 10.
        relevance_threshold (int | Unset): Minimum relevance rating (1-6 scale) to include result Default: 2.
        min_results (int | Unset): Minimum number of results to ensure Default: 6.
        time_delta_days (int | Unset): Number of days to look back for search results Default: 30.
        enable_relevance_ranking (bool | Unset): Whether to perform LLM-based relevance ranking Default: True.
        search_queries_column (None | str | Unset): Column name in sample.meta containing pre-generated search queries
            (list of strings). If provided, skips LLM query generation.
        search_query_instructions (None | str | Unset): Optional guidance for the LLM step that generates multiple
            search queries, replaces the default instructions.
    """

    config_type: Literal["WEB_SEARCH_CONTEXT_GENERATOR"] | Unset = "WEB_SEARCH_CONTEXT_GENERATOR"
    num_search_queries: int | Unset = 5
    results_per_query: int | Unset = 3
    num_results: int | Unset = 10
    relevance_threshold: int | Unset = 2
    min_results: int | Unset = 6
    time_delta_days: int | Unset = 30
    enable_relevance_ranking: bool | Unset = True
    search_queries_column: None | str | Unset = UNSET
    search_query_instructions: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        config_type = self.config_type

        num_search_queries = self.num_search_queries

        results_per_query = self.results_per_query

        num_results = self.num_results

        relevance_threshold = self.relevance_threshold

        min_results = self.min_results

        time_delta_days = self.time_delta_days

        enable_relevance_ranking = self.enable_relevance_ranking

        search_queries_column: None | str | Unset
        if isinstance(self.search_queries_column, Unset):
            search_queries_column = UNSET
        else:
            search_queries_column = self.search_queries_column

        search_query_instructions: None | str | Unset
        if isinstance(self.search_query_instructions, Unset):
            search_query_instructions = UNSET
        else:
            search_query_instructions = self.search_query_instructions

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if config_type is not UNSET:
            field_dict["config_type"] = config_type
        if num_search_queries is not UNSET:
            field_dict["num_search_queries"] = num_search_queries
        if results_per_query is not UNSET:
            field_dict["results_per_query"] = results_per_query
        if num_results is not UNSET:
            field_dict["num_results"] = num_results
        if relevance_threshold is not UNSET:
            field_dict["relevance_threshold"] = relevance_threshold
        if min_results is not UNSET:
            field_dict["min_results"] = min_results
        if time_delta_days is not UNSET:
            field_dict["time_delta_days"] = time_delta_days
        if enable_relevance_ranking is not UNSET:
            field_dict["enable_relevance_ranking"] = enable_relevance_ranking
        if search_queries_column is not UNSET:
            field_dict["search_queries_column"] = search_queries_column
        if search_query_instructions is not UNSET:
            field_dict["search_query_instructions"] = search_query_instructions

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        config_type = cast(Literal["WEB_SEARCH_CONTEXT_GENERATOR"] | Unset, d.pop("config_type", UNSET))
        if config_type != "WEB_SEARCH_CONTEXT_GENERATOR" and not isinstance(config_type, Unset):
            raise ValueError(f"config_type must match const 'WEB_SEARCH_CONTEXT_GENERATOR', got '{config_type}'")

        num_search_queries = d.pop("num_search_queries", UNSET)

        results_per_query = d.pop("results_per_query", UNSET)

        num_results = d.pop("num_results", UNSET)

        relevance_threshold = d.pop("relevance_threshold", UNSET)

        min_results = d.pop("min_results", UNSET)

        time_delta_days = d.pop("time_delta_days", UNSET)

        enable_relevance_ranking = d.pop("enable_relevance_ranking", UNSET)

        def _parse_search_queries_column(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        search_queries_column = _parse_search_queries_column(d.pop("search_queries_column", UNSET))

        def _parse_search_query_instructions(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        search_query_instructions = _parse_search_query_instructions(d.pop("search_query_instructions", UNSET))

        web_search_context_generator = cls(
            config_type=config_type,
            num_search_queries=num_search_queries,
            results_per_query=results_per_query,
            num_results=num_results,
            relevance_threshold=relevance_threshold,
            min_results=min_results,
            time_delta_days=time_delta_days,
            enable_relevance_ranking=enable_relevance_ranking,
            search_queries_column=search_queries_column,
            search_query_instructions=search_query_instructions,
        )

        web_search_context_generator.additional_properties = d
        return web_search_context_generator

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
