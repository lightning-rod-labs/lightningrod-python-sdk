from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.model_source_type import ModelSourceType
from ..types import UNSET, Unset

T = TypeVar("T", bound="ModelConfig")


@_attrs_define
class ModelConfig:
    """
    Attributes:
        model_name (str | Unset):  Default: 'meta-llama/llama-3.3-70b-instruct'.
        model_source (ModelSourceType | Unset):
        temperature (float | Unset):  Default: 1.0.
        max_tokens (int | None | Unset):
        ip_address (None | str | Unset):
        lora_base_model_name (None | str | Unset):
        lora_repo_path (None | str | Unset):
        lora_checkpoint_path (None | str | Unset):
        runpod_endpoint_id (None | str | Unset):
        is_lightningrod_model (bool | None | Unset):
        openrouter_provider (list[str] | None | Unset):
        reasoning_effort (None | str | Unset):
        is_reasoning_model (bool | None | Unset):
        disable_reasoning (bool | Unset):  Default: False.
        use_pipeline_key (bool | Unset):  Default: False.
    """

    model_name: str | Unset = "meta-llama/llama-3.3-70b-instruct"
    model_source: ModelSourceType | Unset = UNSET
    temperature: float | Unset = 1.0
    max_tokens: int | None | Unset = UNSET
    ip_address: None | str | Unset = UNSET
    lora_base_model_name: None | str | Unset = UNSET
    lora_repo_path: None | str | Unset = UNSET
    lora_checkpoint_path: None | str | Unset = UNSET
    runpod_endpoint_id: None | str | Unset = UNSET
    is_lightningrod_model: bool | None | Unset = UNSET
    openrouter_provider: list[str] | None | Unset = UNSET
    reasoning_effort: None | str | Unset = UNSET
    is_reasoning_model: bool | None | Unset = UNSET
    disable_reasoning: bool | Unset = False
    use_pipeline_key: bool | Unset = False
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        model_name = self.model_name

        model_source: str | Unset = UNSET
        if not isinstance(self.model_source, Unset):
            model_source = self.model_source.value

        temperature = self.temperature

        max_tokens: int | None | Unset
        if isinstance(self.max_tokens, Unset):
            max_tokens = UNSET
        else:
            max_tokens = self.max_tokens

        ip_address: None | str | Unset
        if isinstance(self.ip_address, Unset):
            ip_address = UNSET
        else:
            ip_address = self.ip_address

        lora_base_model_name: None | str | Unset
        if isinstance(self.lora_base_model_name, Unset):
            lora_base_model_name = UNSET
        else:
            lora_base_model_name = self.lora_base_model_name

        lora_repo_path: None | str | Unset
        if isinstance(self.lora_repo_path, Unset):
            lora_repo_path = UNSET
        else:
            lora_repo_path = self.lora_repo_path

        lora_checkpoint_path: None | str | Unset
        if isinstance(self.lora_checkpoint_path, Unset):
            lora_checkpoint_path = UNSET
        else:
            lora_checkpoint_path = self.lora_checkpoint_path

        runpod_endpoint_id: None | str | Unset
        if isinstance(self.runpod_endpoint_id, Unset):
            runpod_endpoint_id = UNSET
        else:
            runpod_endpoint_id = self.runpod_endpoint_id

        is_lightningrod_model: bool | None | Unset
        if isinstance(self.is_lightningrod_model, Unset):
            is_lightningrod_model = UNSET
        else:
            is_lightningrod_model = self.is_lightningrod_model

        openrouter_provider: list[str] | None | Unset
        if isinstance(self.openrouter_provider, Unset):
            openrouter_provider = UNSET
        elif isinstance(self.openrouter_provider, list):
            openrouter_provider = self.openrouter_provider

        else:
            openrouter_provider = self.openrouter_provider

        reasoning_effort: None | str | Unset
        if isinstance(self.reasoning_effort, Unset):
            reasoning_effort = UNSET
        else:
            reasoning_effort = self.reasoning_effort

        is_reasoning_model: bool | None | Unset
        if isinstance(self.is_reasoning_model, Unset):
            is_reasoning_model = UNSET
        else:
            is_reasoning_model = self.is_reasoning_model

        disable_reasoning = self.disable_reasoning

        use_pipeline_key = self.use_pipeline_key

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if model_name is not UNSET:
            field_dict["model_name"] = model_name
        if model_source is not UNSET:
            field_dict["model_source"] = model_source
        if temperature is not UNSET:
            field_dict["temperature"] = temperature
        if max_tokens is not UNSET:
            field_dict["max_tokens"] = max_tokens
        if ip_address is not UNSET:
            field_dict["ip_address"] = ip_address
        if lora_base_model_name is not UNSET:
            field_dict["lora_base_model_name"] = lora_base_model_name
        if lora_repo_path is not UNSET:
            field_dict["lora_repo_path"] = lora_repo_path
        if lora_checkpoint_path is not UNSET:
            field_dict["lora_checkpoint_path"] = lora_checkpoint_path
        if runpod_endpoint_id is not UNSET:
            field_dict["runpod_endpoint_id"] = runpod_endpoint_id
        if is_lightningrod_model is not UNSET:
            field_dict["is_lightningrod_model"] = is_lightningrod_model
        if openrouter_provider is not UNSET:
            field_dict["openrouter_provider"] = openrouter_provider
        if reasoning_effort is not UNSET:
            field_dict["reasoning_effort"] = reasoning_effort
        if is_reasoning_model is not UNSET:
            field_dict["is_reasoning_model"] = is_reasoning_model
        if disable_reasoning is not UNSET:
            field_dict["disable_reasoning"] = disable_reasoning
        if use_pipeline_key is not UNSET:
            field_dict["use_pipeline_key"] = use_pipeline_key

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        model_name = d.pop("model_name", UNSET)

        _model_source = d.pop("model_source", UNSET)
        model_source: ModelSourceType | Unset
        if isinstance(_model_source, Unset):
            model_source = UNSET
        else:
            model_source = ModelSourceType(_model_source)

        temperature = d.pop("temperature", UNSET)

        def _parse_max_tokens(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        max_tokens = _parse_max_tokens(d.pop("max_tokens", UNSET))

        def _parse_ip_address(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        ip_address = _parse_ip_address(d.pop("ip_address", UNSET))

        def _parse_lora_base_model_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        lora_base_model_name = _parse_lora_base_model_name(d.pop("lora_base_model_name", UNSET))

        def _parse_lora_repo_path(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        lora_repo_path = _parse_lora_repo_path(d.pop("lora_repo_path", UNSET))

        def _parse_lora_checkpoint_path(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        lora_checkpoint_path = _parse_lora_checkpoint_path(d.pop("lora_checkpoint_path", UNSET))

        def _parse_runpod_endpoint_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        runpod_endpoint_id = _parse_runpod_endpoint_id(d.pop("runpod_endpoint_id", UNSET))

        def _parse_is_lightningrod_model(data: object) -> bool | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(bool | None | Unset, data)

        is_lightningrod_model = _parse_is_lightningrod_model(d.pop("is_lightningrod_model", UNSET))

        def _parse_openrouter_provider(data: object) -> list[str] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                openrouter_provider_type_0 = cast(list[str], data)

                return openrouter_provider_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[str] | None | Unset, data)

        openrouter_provider = _parse_openrouter_provider(d.pop("openrouter_provider", UNSET))

        def _parse_reasoning_effort(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        reasoning_effort = _parse_reasoning_effort(d.pop("reasoning_effort", UNSET))

        def _parse_is_reasoning_model(data: object) -> bool | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(bool | None | Unset, data)

        is_reasoning_model = _parse_is_reasoning_model(d.pop("is_reasoning_model", UNSET))

        disable_reasoning = d.pop("disable_reasoning", UNSET)

        use_pipeline_key = d.pop("use_pipeline_key", UNSET)

        model_config = cls(
            model_name=model_name,
            model_source=model_source,
            temperature=temperature,
            max_tokens=max_tokens,
            ip_address=ip_address,
            lora_base_model_name=lora_base_model_name,
            lora_repo_path=lora_repo_path,
            lora_checkpoint_path=lora_checkpoint_path,
            runpod_endpoint_id=runpod_endpoint_id,
            is_lightningrod_model=is_lightningrod_model,
            openrouter_provider=openrouter_provider,
            reasoning_effort=reasoning_effort,
            is_reasoning_model=is_reasoning_model,
            disable_reasoning=disable_reasoning,
            use_pipeline_key=use_pipeline_key,
        )

        model_config.additional_properties = d
        return model_config

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
