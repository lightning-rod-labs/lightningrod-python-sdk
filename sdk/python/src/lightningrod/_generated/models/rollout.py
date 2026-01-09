from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.rollout_parsed_output_type_0 import RolloutParsedOutputType0


T = TypeVar("T", bound="Rollout")


@_attrs_define
class Rollout:
    """A single model rollout/response.

    Attributes:
        model_name (str):
        content (str):
        parsed_output (None | RolloutParsedOutputType0 | Unset):
        reasoning (None | str | Unset):
    """

    model_name: str
    content: str
    parsed_output: None | RolloutParsedOutputType0 | Unset = UNSET
    reasoning: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.rollout_parsed_output_type_0 import RolloutParsedOutputType0

        model_name = self.model_name

        content = self.content

        parsed_output: dict[str, Any] | None | Unset
        if isinstance(self.parsed_output, Unset):
            parsed_output = UNSET
        elif isinstance(self.parsed_output, RolloutParsedOutputType0):
            parsed_output = self.parsed_output.to_dict()
        else:
            parsed_output = self.parsed_output

        reasoning: None | str | Unset
        if isinstance(self.reasoning, Unset):
            reasoning = UNSET
        else:
            reasoning = self.reasoning

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "model_name": model_name,
                "content": content,
            }
        )
        if parsed_output is not UNSET:
            field_dict["parsed_output"] = parsed_output
        if reasoning is not UNSET:
            field_dict["reasoning"] = reasoning

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.rollout_parsed_output_type_0 import RolloutParsedOutputType0

        d = dict(src_dict)
        model_name = d.pop("model_name")

        content = d.pop("content")

        def _parse_parsed_output(data: object) -> None | RolloutParsedOutputType0 | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                parsed_output_type_0 = RolloutParsedOutputType0.from_dict(data)

                return parsed_output_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | RolloutParsedOutputType0 | Unset, data)

        parsed_output = _parse_parsed_output(d.pop("parsed_output", UNSET))

        def _parse_reasoning(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        reasoning = _parse_reasoning(d.pop("reasoning", UNSET))

        rollout = cls(
            model_name=model_name,
            content=content,
            parsed_output=parsed_output,
            reasoning=reasoning,
        )

        rollout.additional_properties = d
        return rollout

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
