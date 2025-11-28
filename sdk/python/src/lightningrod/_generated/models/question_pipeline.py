from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Literal, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.gdelt_seed_generator import GdeltSeedGenerator
    from ..models.news_seed_generator import NewsSeedGenerator
    from ..models.question_generator import QuestionGenerator
    from ..models.web_search_labeler import WebSearchLabeler


T = TypeVar("T", bound="QuestionPipeline")


@_attrs_define
class QuestionPipeline:
    """
    Attributes:
        seed_generator (GdeltSeedGenerator | NewsSeedGenerator): Configuration for seed generation
        question_generator (QuestionGenerator):
        labeler (WebSearchLabeler):
        config_type (Literal['QUESTION_PIPELINE'] | Unset): Type of transform configuration Default:
            'QUESTION_PIPELINE'.
    """

    seed_generator: GdeltSeedGenerator | NewsSeedGenerator
    question_generator: QuestionGenerator
    labeler: WebSearchLabeler
    config_type: Literal["QUESTION_PIPELINE"] | Unset = "QUESTION_PIPELINE"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.news_seed_generator import NewsSeedGenerator

        seed_generator: dict[str, Any]
        if isinstance(self.seed_generator, NewsSeedGenerator):
            seed_generator = self.seed_generator.to_dict()
        else:
            seed_generator = self.seed_generator.to_dict()

        question_generator = self.question_generator.to_dict()

        labeler = self.labeler.to_dict()

        config_type = self.config_type

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "seed_generator": seed_generator,
                "question_generator": question_generator,
                "labeler": labeler,
            }
        )
        if config_type is not UNSET:
            field_dict["config_type"] = config_type

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.gdelt_seed_generator import GdeltSeedGenerator
        from ..models.news_seed_generator import NewsSeedGenerator
        from ..models.question_generator import QuestionGenerator
        from ..models.web_search_labeler import WebSearchLabeler

        d = dict(src_dict)

        def _parse_seed_generator(data: object) -> GdeltSeedGenerator | NewsSeedGenerator:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                seed_generator_type_0 = NewsSeedGenerator.from_dict(data)

                return seed_generator_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()
            seed_generator_type_1 = GdeltSeedGenerator.from_dict(data)

            return seed_generator_type_1

        seed_generator = _parse_seed_generator(d.pop("seed_generator"))

        question_generator = QuestionGenerator.from_dict(d.pop("question_generator"))

        labeler = WebSearchLabeler.from_dict(d.pop("labeler"))

        config_type = cast(Literal["QUESTION_PIPELINE"] | Unset, d.pop("config_type", UNSET))
        if config_type != "QUESTION_PIPELINE" and not isinstance(config_type, Unset):
            raise ValueError(f"config_type must match const 'QUESTION_PIPELINE', got '{config_type}'")

        question_pipeline = cls(
            seed_generator=seed_generator,
            question_generator=question_generator,
            labeler=labeler,
            config_type=config_type,
        )

        question_pipeline.additional_properties = d
        return question_pipeline

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
