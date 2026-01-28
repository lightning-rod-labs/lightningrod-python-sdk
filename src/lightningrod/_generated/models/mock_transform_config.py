from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Literal, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.mock_transform_config_metadata_additions import MockTransformConfigMetadataAdditions


T = TypeVar("T", bound="MockTransformConfig")


@_attrs_define
class MockTransformConfig:
    """
    Attributes:
        config_type (Literal['MOCK'] | Unset):  Default: 'MOCK'.
        num_seeds (int | Unset): Number of mock seeds to generate (0 = not a seed generator) Default: 0.
        seed_text_template (str | Unset): Template for seed text Default: 'Mock seed content {index}'.
        delay_seconds (float | Unset): Simulated processing time per item Default: 0.1.
        delay_variance (float | Unset): Random variance (+/- seconds) Default: 0.05.
        error_rate (float | Unset): Probability of error (0.0-1.0) Default: 0.01.
        error_message (str | Unset): Error message when error_rate triggers Default: 'Mock error'.
        expansion_factor (int | Unset): Outputs per input (1:N expansion) Default: 1.
        filter_rate (float | Unset): Probability of marking invalid Default: 0.0.
        add_question (bool | Unset): Add a mock question to samples Default: False.
        question_template (str | Unset): Template for question text Default: 'Mock question {index}?'.
        metadata_additions (MockTransformConfigMetadataAdditions | Unset): Added to sample.meta
        estimated_input_tokens (int | Unset): Estimated input tokens per call Default: 0.
        estimated_output_tokens (int | Unset): Estimated output tokens per call Default: 0.
        estimated_model_name (None | str | Unset): Model name for cost estimation
        simulated_cost_per_call (float | Unset): Simulated cost per call in dollars (records usage event when > 0)
            Default: 0.0.
        random_seed (int | None | Unset): Seed for deterministic behavior
    """

    config_type: Literal["MOCK"] | Unset = "MOCK"
    num_seeds: int | Unset = 0
    seed_text_template: str | Unset = "Mock seed content {index}"
    delay_seconds: float | Unset = 0.1
    delay_variance: float | Unset = 0.05
    error_rate: float | Unset = 0.01
    error_message: str | Unset = "Mock error"
    expansion_factor: int | Unset = 1
    filter_rate: float | Unset = 0.0
    add_question: bool | Unset = False
    question_template: str | Unset = "Mock question {index}?"
    metadata_additions: MockTransformConfigMetadataAdditions | Unset = UNSET
    estimated_input_tokens: int | Unset = 0
    estimated_output_tokens: int | Unset = 0
    estimated_model_name: None | str | Unset = UNSET
    simulated_cost_per_call: float | Unset = 0.0
    random_seed: int | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        config_type = self.config_type

        num_seeds = self.num_seeds

        seed_text_template = self.seed_text_template

        delay_seconds = self.delay_seconds

        delay_variance = self.delay_variance

        error_rate = self.error_rate

        error_message = self.error_message

        expansion_factor = self.expansion_factor

        filter_rate = self.filter_rate

        add_question = self.add_question

        question_template = self.question_template

        metadata_additions: dict[str, Any] | Unset = UNSET
        if not isinstance(self.metadata_additions, Unset):
            metadata_additions = self.metadata_additions.to_dict()

        estimated_input_tokens = self.estimated_input_tokens

        estimated_output_tokens = self.estimated_output_tokens

        estimated_model_name: None | str | Unset
        if isinstance(self.estimated_model_name, Unset):
            estimated_model_name = UNSET
        else:
            estimated_model_name = self.estimated_model_name

        simulated_cost_per_call = self.simulated_cost_per_call

        random_seed: int | None | Unset
        if isinstance(self.random_seed, Unset):
            random_seed = UNSET
        else:
            random_seed = self.random_seed

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if config_type is not UNSET:
            field_dict["config_type"] = config_type
        if num_seeds is not UNSET:
            field_dict["num_seeds"] = num_seeds
        if seed_text_template is not UNSET:
            field_dict["seed_text_template"] = seed_text_template
        if delay_seconds is not UNSET:
            field_dict["delay_seconds"] = delay_seconds
        if delay_variance is not UNSET:
            field_dict["delay_variance"] = delay_variance
        if error_rate is not UNSET:
            field_dict["error_rate"] = error_rate
        if error_message is not UNSET:
            field_dict["error_message"] = error_message
        if expansion_factor is not UNSET:
            field_dict["expansion_factor"] = expansion_factor
        if filter_rate is not UNSET:
            field_dict["filter_rate"] = filter_rate
        if add_question is not UNSET:
            field_dict["add_question"] = add_question
        if question_template is not UNSET:
            field_dict["question_template"] = question_template
        if metadata_additions is not UNSET:
            field_dict["metadata_additions"] = metadata_additions
        if estimated_input_tokens is not UNSET:
            field_dict["estimated_input_tokens"] = estimated_input_tokens
        if estimated_output_tokens is not UNSET:
            field_dict["estimated_output_tokens"] = estimated_output_tokens
        if estimated_model_name is not UNSET:
            field_dict["estimated_model_name"] = estimated_model_name
        if simulated_cost_per_call is not UNSET:
            field_dict["simulated_cost_per_call"] = simulated_cost_per_call
        if random_seed is not UNSET:
            field_dict["random_seed"] = random_seed

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.mock_transform_config_metadata_additions import MockTransformConfigMetadataAdditions

        d = dict(src_dict)
        config_type = cast(Literal["MOCK"] | Unset, d.pop("config_type", UNSET))
        if config_type != "MOCK" and not isinstance(config_type, Unset):
            raise ValueError(f"config_type must match const 'MOCK', got '{config_type}'")

        num_seeds = d.pop("num_seeds", UNSET)

        seed_text_template = d.pop("seed_text_template", UNSET)

        delay_seconds = d.pop("delay_seconds", UNSET)

        delay_variance = d.pop("delay_variance", UNSET)

        error_rate = d.pop("error_rate", UNSET)

        error_message = d.pop("error_message", UNSET)

        expansion_factor = d.pop("expansion_factor", UNSET)

        filter_rate = d.pop("filter_rate", UNSET)

        add_question = d.pop("add_question", UNSET)

        question_template = d.pop("question_template", UNSET)

        _metadata_additions = d.pop("metadata_additions", UNSET)
        metadata_additions: MockTransformConfigMetadataAdditions | Unset
        if isinstance(_metadata_additions, Unset):
            metadata_additions = UNSET
        else:
            metadata_additions = MockTransformConfigMetadataAdditions.from_dict(_metadata_additions)

        estimated_input_tokens = d.pop("estimated_input_tokens", UNSET)

        estimated_output_tokens = d.pop("estimated_output_tokens", UNSET)

        def _parse_estimated_model_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        estimated_model_name = _parse_estimated_model_name(d.pop("estimated_model_name", UNSET))

        simulated_cost_per_call = d.pop("simulated_cost_per_call", UNSET)

        def _parse_random_seed(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        random_seed = _parse_random_seed(d.pop("random_seed", UNSET))

        mock_transform_config = cls(
            config_type=config_type,
            num_seeds=num_seeds,
            seed_text_template=seed_text_template,
            delay_seconds=delay_seconds,
            delay_variance=delay_variance,
            error_rate=error_rate,
            error_message=error_message,
            expansion_factor=expansion_factor,
            filter_rate=filter_rate,
            add_question=add_question,
            question_template=question_template,
            metadata_additions=metadata_additions,
            estimated_input_tokens=estimated_input_tokens,
            estimated_output_tokens=estimated_output_tokens,
            estimated_model_name=estimated_model_name,
            simulated_cost_per_call=simulated_cost_per_call,
            random_seed=random_seed,
        )

        mock_transform_config.additional_properties = d
        return mock_transform_config

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
