from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Literal, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.perplexity_context_generator_search_context_size import PerplexityContextGeneratorSearchContextSize
from ..types import UNSET, Unset

T = TypeVar("T", bound="PerplexityContextGenerator")


@_attrs_define
class PerplexityContextGenerator:
    """
    Attributes:
        config_type (Literal['PERPLEXITY_CONTEXT_GENERATOR'] | Unset): Type of transform configuration Default:
            'PERPLEXITY_CONTEXT_GENERATOR'.
        model (str | Unset): Perplexity model to query Default: 'sonar-pro'.
        max_tokens (int | Unset): Max tokens for the Perplexity response Default: 2048.
        temperature (float | Unset): Sampling temperature Default: 0.2.
        search_context_size (PerplexityContextGeneratorSearchContextSize | Unset): Perplexity web search context size
            Default: PerplexityContextGeneratorSearchContextSize.HIGH.
        system_prompt (None | str | Unset): Optional override for the research system prompt
    """

    config_type: Literal["PERPLEXITY_CONTEXT_GENERATOR"] | Unset = "PERPLEXITY_CONTEXT_GENERATOR"
    model: str | Unset = "sonar-pro"
    max_tokens: int | Unset = 2048
    temperature: float | Unset = 0.2
    search_context_size: PerplexityContextGeneratorSearchContextSize | Unset = (
        PerplexityContextGeneratorSearchContextSize.HIGH
    )
    system_prompt: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        config_type = self.config_type

        model = self.model

        max_tokens = self.max_tokens

        temperature = self.temperature

        search_context_size: str | Unset = UNSET
        if not isinstance(self.search_context_size, Unset):
            search_context_size = self.search_context_size.value

        system_prompt: None | str | Unset
        if isinstance(self.system_prompt, Unset):
            system_prompt = UNSET
        else:
            system_prompt = self.system_prompt

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if config_type is not UNSET:
            field_dict["config_type"] = config_type
        if model is not UNSET:
            field_dict["model"] = model
        if max_tokens is not UNSET:
            field_dict["max_tokens"] = max_tokens
        if temperature is not UNSET:
            field_dict["temperature"] = temperature
        if search_context_size is not UNSET:
            field_dict["search_context_size"] = search_context_size
        if system_prompt is not UNSET:
            field_dict["system_prompt"] = system_prompt

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        config_type = cast(Literal["PERPLEXITY_CONTEXT_GENERATOR"] | Unset, d.pop("config_type", UNSET))
        if config_type != "PERPLEXITY_CONTEXT_GENERATOR" and not isinstance(config_type, Unset):
            raise ValueError(f"config_type must match const 'PERPLEXITY_CONTEXT_GENERATOR', got '{config_type}'")

        model = d.pop("model", UNSET)

        max_tokens = d.pop("max_tokens", UNSET)

        temperature = d.pop("temperature", UNSET)

        _search_context_size = d.pop("search_context_size", UNSET)
        search_context_size: PerplexityContextGeneratorSearchContextSize | Unset
        if isinstance(_search_context_size, Unset):
            search_context_size = UNSET
        else:
            search_context_size = PerplexityContextGeneratorSearchContextSize(_search_context_size)

        def _parse_system_prompt(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        system_prompt = _parse_system_prompt(d.pop("system_prompt", UNSET))

        perplexity_context_generator = cls(
            config_type=config_type,
            model=model,
            max_tokens=max_tokens,
            temperature=temperature,
            search_context_size=search_context_size,
            system_prompt=system_prompt,
        )

        perplexity_context_generator.additional_properties = d
        return perplexity_context_generator

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
