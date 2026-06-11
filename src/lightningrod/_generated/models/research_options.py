from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.research_options_sources_item import ResearchOptionsSourcesItem
from ..types import UNSET, Unset

T = TypeVar("T", bound="ResearchOptions")


@_attrs_define
class ResearchOptions:
    """Opt-in research enrichment for forecasting requests.

    When set, the API fetches web-grounded context from the requested sources
    and injects it into the prompt before calling the model. Each successful
    source produces a billable RESEARCH event.

        Attributes:
            sources (list[ResearchOptionsSourcesItem] | Unset): Which research providers to query in parallel.
    """

    sources: list[ResearchOptionsSourcesItem] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        sources: list[str] | Unset = UNSET
        if not isinstance(self.sources, Unset):
            sources = []
            for sources_item_data in self.sources:
                sources_item = sources_item_data.value
                sources.append(sources_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if sources is not UNSET:
            field_dict["sources"] = sources

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _sources = d.pop("sources", UNSET)
        sources: list[ResearchOptionsSourcesItem] | Unset = UNSET
        if _sources is not UNSET:
            sources = []
            for sources_item_data in _sources:
                sources_item = ResearchOptionsSourcesItem(sources_item_data)

                sources.append(sources_item)

        research_options = cls(
            sources=sources,
        )

        research_options.additional_properties = d
        return research_options

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
