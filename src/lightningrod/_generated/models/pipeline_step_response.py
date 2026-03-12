from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.pipeline_step_response_config_type_0 import PipelineStepResponseConfigType0
    from ..models.pipeline_step_response_parameters_type_0 import PipelineStepResponseParametersType0


T = TypeVar("T", bound="PipelineStepResponse")


@_attrs_define
class PipelineStepResponse:
    """A single step in the progressive plan outline.

    Attributes:
        step_id (str): Unique step identifier
        name (str): Display name
        status (str): 'partial' or 'configured'
        description (None | str | Unset):
        parameters (None | PipelineStepResponseParametersType0 | Unset): Key-value pairs
        config (None | PipelineStepResponseConfigType0 | Unset): Actual transform config dict
        instructions (None | str | Unset): Full config text
        example_input (None | str | Unset):
        example_output (None | str | Unset):
    """

    step_id: str
    name: str
    status: str
    description: None | str | Unset = UNSET
    parameters: None | PipelineStepResponseParametersType0 | Unset = UNSET
    config: None | PipelineStepResponseConfigType0 | Unset = UNSET
    instructions: None | str | Unset = UNSET
    example_input: None | str | Unset = UNSET
    example_output: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.pipeline_step_response_config_type_0 import PipelineStepResponseConfigType0
        from ..models.pipeline_step_response_parameters_type_0 import PipelineStepResponseParametersType0

        step_id = self.step_id

        name = self.name

        status = self.status

        description: None | str | Unset
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        parameters: dict[str, Any] | None | Unset
        if isinstance(self.parameters, Unset):
            parameters = UNSET
        elif isinstance(self.parameters, PipelineStepResponseParametersType0):
            parameters = self.parameters.to_dict()
        else:
            parameters = self.parameters

        config: dict[str, Any] | None | Unset
        if isinstance(self.config, Unset):
            config = UNSET
        elif isinstance(self.config, PipelineStepResponseConfigType0):
            config = self.config.to_dict()
        else:
            config = self.config

        instructions: None | str | Unset
        if isinstance(self.instructions, Unset):
            instructions = UNSET
        else:
            instructions = self.instructions

        example_input: None | str | Unset
        if isinstance(self.example_input, Unset):
            example_input = UNSET
        else:
            example_input = self.example_input

        example_output: None | str | Unset
        if isinstance(self.example_output, Unset):
            example_output = UNSET
        else:
            example_output = self.example_output

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "step_id": step_id,
                "name": name,
                "status": status,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if parameters is not UNSET:
            field_dict["parameters"] = parameters
        if config is not UNSET:
            field_dict["config"] = config
        if instructions is not UNSET:
            field_dict["instructions"] = instructions
        if example_input is not UNSET:
            field_dict["example_input"] = example_input
        if example_output is not UNSET:
            field_dict["example_output"] = example_output

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.pipeline_step_response_config_type_0 import PipelineStepResponseConfigType0
        from ..models.pipeline_step_response_parameters_type_0 import PipelineStepResponseParametersType0

        d = dict(src_dict)
        step_id = d.pop("step_id")

        name = d.pop("name")

        status = d.pop("status")

        def _parse_description(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        description = _parse_description(d.pop("description", UNSET))

        def _parse_parameters(data: object) -> None | PipelineStepResponseParametersType0 | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                parameters_type_0 = PipelineStepResponseParametersType0.from_dict(data)

                return parameters_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | PipelineStepResponseParametersType0 | Unset, data)

        parameters = _parse_parameters(d.pop("parameters", UNSET))

        def _parse_config(data: object) -> None | PipelineStepResponseConfigType0 | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                config_type_0 = PipelineStepResponseConfigType0.from_dict(data)

                return config_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | PipelineStepResponseConfigType0 | Unset, data)

        config = _parse_config(d.pop("config", UNSET))

        def _parse_instructions(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        instructions = _parse_instructions(d.pop("instructions", UNSET))

        def _parse_example_input(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        example_input = _parse_example_input(d.pop("example_input", UNSET))

        def _parse_example_output(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        example_output = _parse_example_output(d.pop("example_output", UNSET))

        pipeline_step_response = cls(
            step_id=step_id,
            name=name,
            status=status,
            description=description,
            parameters=parameters,
            config=config,
            instructions=instructions,
            example_input=example_input,
            example_output=example_output,
        )

        pipeline_step_response.additional_properties = d
        return pipeline_step_response

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
