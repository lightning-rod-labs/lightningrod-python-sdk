from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Literal, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.answer_type_enum import AnswerTypeEnum
from ..models.completion_request_reasoning_effort_type_0 import CompletionRequestReasoningEffortType0
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.research_options import ResearchOptions


T = TypeVar("T", bound="CompletionRequest")


@_attrs_define
class CompletionRequest:
    """
    Attributes:
        model (str): ID of the model to use
        prompt (list[str] | str): The prompt(s) to generate completions for
        temperature (float | None | Unset): Sampling temperature between 0 and 2 Default: 0.6.
        max_tokens (int | None | Unset): Maximum number of tokens to generate
        top_p (float | None | Unset): Nucleus sampling parameter
        top_k (int | None | Unset): Number of top tokens to consider
        min_p (float | None | Unset): Minimum probability for a token to be considered
        stream (bool | None | Unset): Whether to stream back partial progress Default: False.
        n (int | None | Unset): Number of completions to generate Default: 1.
        stop (list[str] | None | str | Unset): Up to 4 sequences where the API will stop generating
        seed (int | None | Unset): Deterministic sampling seed
        reasoning_effort (CompletionRequestReasoningEffortType0 | None | Unset): Reasoning effort for hosted Foresight
            models. Defaults to medium; pass low to reduce reasoning budget. High is accepted for OpenAI compatibility and
            treated as medium.
        research (bool | None | ResearchOptions | Unset): Opt-in: enrich the request with web research before
            forecasting. Pass `true` for default sources or an object to select sources. Each successful source is billed as
            a separate RESEARCH event.
        answer_type (AnswerTypeEnum | Literal['auto'] | None | Unset): Optional Lightning Rod extension that injects
            output-format guidance. Use one of: binary, multiple_choice, continuous, free_response, auto. `auto` classifies
            the prompt before running inference.
    """

    model: str
    prompt: list[str] | str
    temperature: float | None | Unset = 0.6
    max_tokens: int | None | Unset = UNSET
    top_p: float | None | Unset = UNSET
    top_k: int | None | Unset = UNSET
    min_p: float | None | Unset = UNSET
    stream: bool | None | Unset = False
    n: int | None | Unset = 1
    stop: list[str] | None | str | Unset = UNSET
    seed: int | None | Unset = UNSET
    reasoning_effort: CompletionRequestReasoningEffortType0 | None | Unset = UNSET
    research: bool | None | ResearchOptions | Unset = UNSET
    answer_type: AnswerTypeEnum | Literal["auto"] | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.research_options import ResearchOptions

        model = self.model

        prompt: list[str] | str
        if isinstance(self.prompt, list):
            prompt = self.prompt

        else:
            prompt = self.prompt

        temperature: float | None | Unset
        if isinstance(self.temperature, Unset):
            temperature = UNSET
        else:
            temperature = self.temperature

        max_tokens: int | None | Unset
        if isinstance(self.max_tokens, Unset):
            max_tokens = UNSET
        else:
            max_tokens = self.max_tokens

        top_p: float | None | Unset
        if isinstance(self.top_p, Unset):
            top_p = UNSET
        else:
            top_p = self.top_p

        top_k: int | None | Unset
        if isinstance(self.top_k, Unset):
            top_k = UNSET
        else:
            top_k = self.top_k

        min_p: float | None | Unset
        if isinstance(self.min_p, Unset):
            min_p = UNSET
        else:
            min_p = self.min_p

        stream: bool | None | Unset
        if isinstance(self.stream, Unset):
            stream = UNSET
        else:
            stream = self.stream

        n: int | None | Unset
        if isinstance(self.n, Unset):
            n = UNSET
        else:
            n = self.n

        stop: list[str] | None | str | Unset
        if isinstance(self.stop, Unset):
            stop = UNSET
        elif isinstance(self.stop, list):
            stop = self.stop

        else:
            stop = self.stop

        seed: int | None | Unset
        if isinstance(self.seed, Unset):
            seed = UNSET
        else:
            seed = self.seed

        reasoning_effort: None | str | Unset
        if isinstance(self.reasoning_effort, Unset):
            reasoning_effort = UNSET
        elif isinstance(self.reasoning_effort, CompletionRequestReasoningEffortType0):
            reasoning_effort = self.reasoning_effort.value
        else:
            reasoning_effort = self.reasoning_effort

        research: bool | dict[str, Any] | None | Unset
        if isinstance(self.research, Unset):
            research = UNSET
        elif isinstance(self.research, ResearchOptions):
            research = self.research.to_dict()
        else:
            research = self.research

        answer_type: Literal["auto"] | None | str | Unset
        if isinstance(self.answer_type, Unset):
            answer_type = UNSET
        elif isinstance(self.answer_type, AnswerTypeEnum):
            answer_type = self.answer_type.value
        else:
            answer_type = self.answer_type

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "model": model,
                "prompt": prompt,
            }
        )
        if temperature is not UNSET:
            field_dict["temperature"] = temperature
        if max_tokens is not UNSET:
            field_dict["max_tokens"] = max_tokens
        if top_p is not UNSET:
            field_dict["top_p"] = top_p
        if top_k is not UNSET:
            field_dict["top_k"] = top_k
        if min_p is not UNSET:
            field_dict["min_p"] = min_p
        if stream is not UNSET:
            field_dict["stream"] = stream
        if n is not UNSET:
            field_dict["n"] = n
        if stop is not UNSET:
            field_dict["stop"] = stop
        if seed is not UNSET:
            field_dict["seed"] = seed
        if reasoning_effort is not UNSET:
            field_dict["reasoning_effort"] = reasoning_effort
        if research is not UNSET:
            field_dict["research"] = research
        if answer_type is not UNSET:
            field_dict["answer_type"] = answer_type

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.research_options import ResearchOptions

        d = dict(src_dict)
        model = d.pop("model")

        def _parse_prompt(data: object) -> list[str] | str:
            try:
                if not isinstance(data, list):
                    raise TypeError()
                prompt_type_1 = cast(list[str], data)

                return prompt_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[str] | str, data)

        prompt = _parse_prompt(d.pop("prompt"))

        def _parse_temperature(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        temperature = _parse_temperature(d.pop("temperature", UNSET))

        def _parse_max_tokens(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        max_tokens = _parse_max_tokens(d.pop("max_tokens", UNSET))

        def _parse_top_p(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        top_p = _parse_top_p(d.pop("top_p", UNSET))

        def _parse_top_k(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        top_k = _parse_top_k(d.pop("top_k", UNSET))

        def _parse_min_p(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        min_p = _parse_min_p(d.pop("min_p", UNSET))

        def _parse_stream(data: object) -> bool | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(bool | None | Unset, data)

        stream = _parse_stream(d.pop("stream", UNSET))

        def _parse_n(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        n = _parse_n(d.pop("n", UNSET))

        def _parse_stop(data: object) -> list[str] | None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                stop_type_1 = cast(list[str], data)

                return stop_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[str] | None | str | Unset, data)

        stop = _parse_stop(d.pop("stop", UNSET))

        def _parse_seed(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        seed = _parse_seed(d.pop("seed", UNSET))

        def _parse_reasoning_effort(data: object) -> CompletionRequestReasoningEffortType0 | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                reasoning_effort_type_0 = CompletionRequestReasoningEffortType0(data)

                return reasoning_effort_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(CompletionRequestReasoningEffortType0 | None | Unset, data)

        reasoning_effort = _parse_reasoning_effort(d.pop("reasoning_effort", UNSET))

        def _parse_research(data: object) -> bool | None | ResearchOptions | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                research_type_1 = ResearchOptions.from_dict(data)

                return research_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(bool | None | ResearchOptions | Unset, data)

        research = _parse_research(d.pop("research", UNSET))

        def _parse_answer_type(data: object) -> AnswerTypeEnum | Literal["auto"] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                answer_type_type_0 = AnswerTypeEnum(data)

                return answer_type_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            answer_type_type_1 = cast(Literal["auto"], data)
            if answer_type_type_1 != "auto":
                raise ValueError(f"answer_type_type_1 must match const 'auto', got '{answer_type_type_1}'")
            return answer_type_type_1
            return cast(AnswerTypeEnum | Literal["auto"] | None | Unset, data)

        answer_type = _parse_answer_type(d.pop("answer_type", UNSET))

        completion_request = cls(
            model=model,
            prompt=prompt,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
            top_k=top_k,
            min_p=min_p,
            stream=stream,
            n=n,
            stop=stop,
            seed=seed,
            reasoning_effort=reasoning_effort,
            research=research,
            answer_type=answer_type,
        )

        completion_request.additional_properties = d
        return completion_request

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
