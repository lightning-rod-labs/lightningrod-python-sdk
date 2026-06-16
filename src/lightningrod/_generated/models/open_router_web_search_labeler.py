from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Literal, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.open_router_web_search_labeler_engine import OpenRouterWebSearchLabelerEngine
from ..models.open_router_web_search_labeler_search_context_size import OpenRouterWebSearchLabelerSearchContextSize
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.binary_answer_type import BinaryAnswerType
    from ..models.continuous_answer_type import ContinuousAnswerType
    from ..models.continuous_value_only_answer_type import ContinuousValueOnlyAnswerType
    from ..models.free_response_answer_type import FreeResponseAnswerType
    from ..models.multiple_choice_answer_type import MultipleChoiceAnswerType


T = TypeVar("T", bound="OpenRouterWebSearchLabeler")


@_attrs_define
class OpenRouterWebSearchLabeler:
    """Configuration for labeling with OpenRouter's web-search server tool.

    Uses OpenRouter's current `openrouter:web_search` server tool rather than
    Gemini web-search grounding. The default model is Grok, but `model` can be
    any OpenRouter model that supports tool calling.

        Attributes:
            config_type (Literal['OPENROUTER_WEB_SEARCH_LABELER'] | Unset): Type of transform configuration Default:
                'OPENROUTER_WEB_SEARCH_LABELER'.
            confidence_threshold (float | Unset): Minimum confidence threshold for including questions Default: 0.9.
            answer_type (BinaryAnswerType | ContinuousAnswerType | ContinuousValueOnlyAnswerType | FreeResponseAnswerType |
                MultipleChoiceAnswerType | None | Unset): The type of answer expected, used to guide the labeler
            model (str | Unset): OpenRouter model slug to use for labeling. Defaults to Grok. Default: 'x-ai/grok-4.20'.
            engine (OpenRouterWebSearchLabelerEngine | Unset): OpenRouter web-search engine: auto, native, exa, firecrawl,
                or parallel. Default: OpenRouterWebSearchLabelerEngine.AUTO.
            max_results (int | Unset): Maximum results per web-search call for supported engines. Default: 5.
            max_total_results (int | None | Unset): Maximum total results across all web-search calls in one model request.
                Default: 15.
            search_context_size (OpenRouterWebSearchLabelerSearchContextSize | Unset): Amount of context to retrieve for
                engines that support it: low, medium, or high. Default: OpenRouterWebSearchLabelerSearchContextSize.MEDIUM.
            allowed_domains (list[str] | None | Unset): Optional domains to restrict web-search results to.
            excluded_domains (list[str] | None | Unset): Optional domains to exclude from web-search results.
    """

    config_type: Literal["OPENROUTER_WEB_SEARCH_LABELER"] | Unset = "OPENROUTER_WEB_SEARCH_LABELER"
    confidence_threshold: float | Unset = 0.9
    answer_type: (
        BinaryAnswerType
        | ContinuousAnswerType
        | ContinuousValueOnlyAnswerType
        | FreeResponseAnswerType
        | MultipleChoiceAnswerType
        | None
        | Unset
    ) = UNSET
    model: str | Unset = "x-ai/grok-4.20"
    engine: OpenRouterWebSearchLabelerEngine | Unset = OpenRouterWebSearchLabelerEngine.AUTO
    max_results: int | Unset = 5
    max_total_results: int | None | Unset = 15
    search_context_size: OpenRouterWebSearchLabelerSearchContextSize | Unset = (
        OpenRouterWebSearchLabelerSearchContextSize.MEDIUM
    )
    allowed_domains: list[str] | None | Unset = UNSET
    excluded_domains: list[str] | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.binary_answer_type import BinaryAnswerType
        from ..models.continuous_answer_type import ContinuousAnswerType
        from ..models.continuous_value_only_answer_type import ContinuousValueOnlyAnswerType
        from ..models.free_response_answer_type import FreeResponseAnswerType
        from ..models.multiple_choice_answer_type import MultipleChoiceAnswerType

        config_type = self.config_type

        confidence_threshold = self.confidence_threshold

        answer_type: dict[str, Any] | None | Unset
        if isinstance(self.answer_type, Unset):
            answer_type = UNSET
        elif isinstance(self.answer_type, BinaryAnswerType):
            answer_type = self.answer_type.to_dict()
        elif isinstance(self.answer_type, MultipleChoiceAnswerType):
            answer_type = self.answer_type.to_dict()
        elif isinstance(self.answer_type, ContinuousAnswerType):
            answer_type = self.answer_type.to_dict()
        elif isinstance(self.answer_type, ContinuousValueOnlyAnswerType):
            answer_type = self.answer_type.to_dict()
        elif isinstance(self.answer_type, FreeResponseAnswerType):
            answer_type = self.answer_type.to_dict()
        else:
            answer_type = self.answer_type

        model = self.model

        engine: str | Unset = UNSET
        if not isinstance(self.engine, Unset):
            engine = self.engine.value

        max_results = self.max_results

        max_total_results: int | None | Unset
        if isinstance(self.max_total_results, Unset):
            max_total_results = UNSET
        else:
            max_total_results = self.max_total_results

        search_context_size: str | Unset = UNSET
        if not isinstance(self.search_context_size, Unset):
            search_context_size = self.search_context_size.value

        allowed_domains: list[str] | None | Unset
        if isinstance(self.allowed_domains, Unset):
            allowed_domains = UNSET
        elif isinstance(self.allowed_domains, list):
            allowed_domains = self.allowed_domains

        else:
            allowed_domains = self.allowed_domains

        excluded_domains: list[str] | None | Unset
        if isinstance(self.excluded_domains, Unset):
            excluded_domains = UNSET
        elif isinstance(self.excluded_domains, list):
            excluded_domains = self.excluded_domains

        else:
            excluded_domains = self.excluded_domains

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if config_type is not UNSET:
            field_dict["config_type"] = config_type
        if confidence_threshold is not UNSET:
            field_dict["confidence_threshold"] = confidence_threshold
        if answer_type is not UNSET:
            field_dict["answer_type"] = answer_type
        if model is not UNSET:
            field_dict["model"] = model
        if engine is not UNSET:
            field_dict["engine"] = engine
        if max_results is not UNSET:
            field_dict["max_results"] = max_results
        if max_total_results is not UNSET:
            field_dict["max_total_results"] = max_total_results
        if search_context_size is not UNSET:
            field_dict["search_context_size"] = search_context_size
        if allowed_domains is not UNSET:
            field_dict["allowed_domains"] = allowed_domains
        if excluded_domains is not UNSET:
            field_dict["excluded_domains"] = excluded_domains

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.binary_answer_type import BinaryAnswerType
        from ..models.continuous_answer_type import ContinuousAnswerType
        from ..models.continuous_value_only_answer_type import ContinuousValueOnlyAnswerType
        from ..models.free_response_answer_type import FreeResponseAnswerType
        from ..models.multiple_choice_answer_type import MultipleChoiceAnswerType

        d = dict(src_dict)
        config_type = cast(Literal["OPENROUTER_WEB_SEARCH_LABELER"] | Unset, d.pop("config_type", UNSET))
        if config_type != "OPENROUTER_WEB_SEARCH_LABELER" and not isinstance(config_type, Unset):
            raise ValueError(f"config_type must match const 'OPENROUTER_WEB_SEARCH_LABELER', got '{config_type}'")

        confidence_threshold = d.pop("confidence_threshold", UNSET)

        def _parse_answer_type(
            data: object,
        ) -> (
            BinaryAnswerType
            | ContinuousAnswerType
            | ContinuousValueOnlyAnswerType
            | FreeResponseAnswerType
            | MultipleChoiceAnswerType
            | None
            | Unset
        ):
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                answer_type_type_0_type_0 = BinaryAnswerType.from_dict(data)

                return answer_type_type_0_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                answer_type_type_0_type_1 = MultipleChoiceAnswerType.from_dict(data)

                return answer_type_type_0_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                answer_type_type_0_type_2 = ContinuousAnswerType.from_dict(data)

                return answer_type_type_0_type_2
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                answer_type_type_0_type_3 = ContinuousValueOnlyAnswerType.from_dict(data)

                return answer_type_type_0_type_3
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                answer_type_type_0_type_4 = FreeResponseAnswerType.from_dict(data)

                return answer_type_type_0_type_4
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(
                BinaryAnswerType
                | ContinuousAnswerType
                | ContinuousValueOnlyAnswerType
                | FreeResponseAnswerType
                | MultipleChoiceAnswerType
                | None
                | Unset,
                data,
            )

        answer_type = _parse_answer_type(d.pop("answer_type", UNSET))

        model = d.pop("model", UNSET)

        _engine = d.pop("engine", UNSET)
        engine: OpenRouterWebSearchLabelerEngine | Unset
        if isinstance(_engine, Unset):
            engine = UNSET
        else:
            engine = OpenRouterWebSearchLabelerEngine(_engine)

        max_results = d.pop("max_results", UNSET)

        def _parse_max_total_results(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        max_total_results = _parse_max_total_results(d.pop("max_total_results", UNSET))

        _search_context_size = d.pop("search_context_size", UNSET)
        search_context_size: OpenRouterWebSearchLabelerSearchContextSize | Unset
        if isinstance(_search_context_size, Unset):
            search_context_size = UNSET
        else:
            search_context_size = OpenRouterWebSearchLabelerSearchContextSize(_search_context_size)

        def _parse_allowed_domains(data: object) -> list[str] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                allowed_domains_type_0 = cast(list[str], data)

                return allowed_domains_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[str] | None | Unset, data)

        allowed_domains = _parse_allowed_domains(d.pop("allowed_domains", UNSET))

        def _parse_excluded_domains(data: object) -> list[str] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                excluded_domains_type_0 = cast(list[str], data)

                return excluded_domains_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[str] | None | Unset, data)

        excluded_domains = _parse_excluded_domains(d.pop("excluded_domains", UNSET))

        open_router_web_search_labeler = cls(
            config_type=config_type,
            confidence_threshold=confidence_threshold,
            answer_type=answer_type,
            model=model,
            engine=engine,
            max_results=max_results,
            max_total_results=max_total_results,
            search_context_size=search_context_size,
            allowed_domains=allowed_domains,
            excluded_domains=excluded_domains,
        )

        open_router_web_search_labeler.additional_properties = d
        return open_router_web_search_labeler

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
