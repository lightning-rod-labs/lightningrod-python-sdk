from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Literal, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="TopicTreeSeedGenerator")


@_attrs_define
class TopicTreeSeedGenerator:
    """Generates diverse seeds by recursively decomposing broad topics into specific subtopics.

    Given one or more root topics, uses an LLM to break each into `tree_degree` subtopics,
    then repeats `tree_depth` levels deep. The leaf paths become seeds for downstream transforms.
    This produces tree_degree^tree_depth seeds per root topic, each more specific than the root.

    Example:
        TopicTreeSeedGenerator(topic="AI Regulation", tree_depth=2, tree_degree=4)
        # Produces 16 specific seeds like "AI Regulation → Healthcare → FDA approval of
        # diagnostic algorithms" that feed into QuestionGenerator or other downstream transforms.

        Attributes:
            topic (list[str] | str): Root topic(s) to decompose into subtopic trees
            config_type (Literal['TOPIC_TREE_SEED_GENERATOR'] | Unset): Type of transform configuration Default:
                'TOPIC_TREE_SEED_GENERATOR'.
            tree_depth (int | Unset): Levels of recursive expansion Default: 2.
            tree_degree (int | Unset): Subtopics generated per node Default: 5.
            model_name (str | Unset): LLM model for subtopic generation Default: 'google/gemini-3-flash-preview'.
            model_system_prompt (None | str | Unset): Optional system prompt for the LLM
    """

    topic: list[str] | str
    config_type: Literal["TOPIC_TREE_SEED_GENERATOR"] | Unset = "TOPIC_TREE_SEED_GENERATOR"
    tree_depth: int | Unset = 2
    tree_degree: int | Unset = 5
    model_name: str | Unset = "google/gemini-3-flash-preview"
    model_system_prompt: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        topic: list[str] | str
        if isinstance(self.topic, list):
            topic = self.topic

        else:
            topic = self.topic

        config_type = self.config_type

        tree_depth = self.tree_depth

        tree_degree = self.tree_degree

        model_name = self.model_name

        model_system_prompt: None | str | Unset
        if isinstance(self.model_system_prompt, Unset):
            model_system_prompt = UNSET
        else:
            model_system_prompt = self.model_system_prompt

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "topic": topic,
            }
        )
        if config_type is not UNSET:
            field_dict["config_type"] = config_type
        if tree_depth is not UNSET:
            field_dict["tree_depth"] = tree_depth
        if tree_degree is not UNSET:
            field_dict["tree_degree"] = tree_degree
        if model_name is not UNSET:
            field_dict["model_name"] = model_name
        if model_system_prompt is not UNSET:
            field_dict["model_system_prompt"] = model_system_prompt

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_topic(data: object) -> list[str] | str:
            try:
                if not isinstance(data, list):
                    raise TypeError()
                topic_type_1 = cast(list[str], data)

                return topic_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[str] | str, data)

        topic = _parse_topic(d.pop("topic"))

        config_type = cast(Literal["TOPIC_TREE_SEED_GENERATOR"] | Unset, d.pop("config_type", UNSET))
        if config_type != "TOPIC_TREE_SEED_GENERATOR" and not isinstance(config_type, Unset):
            raise ValueError(f"config_type must match const 'TOPIC_TREE_SEED_GENERATOR', got '{config_type}'")

        tree_depth = d.pop("tree_depth", UNSET)

        tree_degree = d.pop("tree_degree", UNSET)

        model_name = d.pop("model_name", UNSET)

        def _parse_model_system_prompt(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        model_system_prompt = _parse_model_system_prompt(d.pop("model_system_prompt", UNSET))

        topic_tree_seed_generator = cls(
            topic=topic,
            config_type=config_type,
            tree_depth=tree_depth,
            tree_degree=tree_degree,
            model_name=model_name,
            model_system_prompt=model_system_prompt,
        )

        topic_tree_seed_generator.additional_properties = d
        return topic_tree_seed_generator

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
