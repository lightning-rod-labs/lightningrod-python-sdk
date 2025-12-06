from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Literal, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.forward_looking_question_generator import ForwardLookingQuestionGenerator
    from ..models.gdelt_seed_generator import GdeltSeedGenerator
    from ..models.news_context_generator import NewsContextGenerator
    from ..models.news_seed_generator import NewsSeedGenerator
    from ..models.question_and_label_generator import QuestionAndLabelGenerator
    from ..models.question_generator import QuestionGenerator
    from ..models.question_renderer import QuestionRenderer
    from ..models.web_search_labeler import WebSearchLabeler


T = TypeVar("T", bound="QuestionPipeline")


@_attrs_define
class QuestionPipeline:
    """
    Attributes:
        seed_generator (GdeltSeedGenerator | NewsSeedGenerator): Configuration for seed generation
        question_generator (ForwardLookingQuestionGenerator | QuestionAndLabelGenerator | QuestionGenerator):
            Configuration for question generation
        config_type (Literal['QUESTION_PIPELINE'] | Unset): Type of transform configuration Default:
            'QUESTION_PIPELINE'.
        labeler (None | Unset | WebSearchLabeler): Configuration for labeling. Not needed when using
            QuestionAndLabelGenerator.
        context_generators (list[NewsContextGenerator] | None | Unset): Optional list of context generators to run
            before rendering
        renderer (None | QuestionRenderer | Unset): Optional configuration for rendering the final prompt
    """

    seed_generator: GdeltSeedGenerator | NewsSeedGenerator
    question_generator: ForwardLookingQuestionGenerator | QuestionAndLabelGenerator | QuestionGenerator
    config_type: Literal["QUESTION_PIPELINE"] | Unset = "QUESTION_PIPELINE"
    labeler: None | Unset | WebSearchLabeler = UNSET
    context_generators: list[NewsContextGenerator] | None | Unset = UNSET
    renderer: None | QuestionRenderer | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.forward_looking_question_generator import ForwardLookingQuestionGenerator
        from ..models.news_seed_generator import NewsSeedGenerator
        from ..models.question_generator import QuestionGenerator
        from ..models.question_renderer import QuestionRenderer
        from ..models.web_search_labeler import WebSearchLabeler

        seed_generator: dict[str, Any]
        if isinstance(self.seed_generator, NewsSeedGenerator):
            seed_generator = self.seed_generator.to_dict()
        else:
            seed_generator = self.seed_generator.to_dict()

        question_generator: dict[str, Any]
        if isinstance(self.question_generator, QuestionGenerator):
            question_generator = self.question_generator.to_dict()
        elif isinstance(self.question_generator, ForwardLookingQuestionGenerator):
            question_generator = self.question_generator.to_dict()
        else:
            question_generator = self.question_generator.to_dict()

        config_type = self.config_type

        labeler: dict[str, Any] | None | Unset
        if isinstance(self.labeler, Unset):
            labeler = UNSET
        elif isinstance(self.labeler, WebSearchLabeler):
            labeler = self.labeler.to_dict()
        else:
            labeler = self.labeler

        context_generators: list[dict[str, Any]] | None | Unset
        if isinstance(self.context_generators, Unset):
            context_generators = UNSET
        elif isinstance(self.context_generators, list):
            context_generators = []
            for context_generators_type_0_item_data in self.context_generators:
                context_generators_type_0_item = context_generators_type_0_item_data.to_dict()
                context_generators.append(context_generators_type_0_item)

        else:
            context_generators = self.context_generators

        renderer: dict[str, Any] | None | Unset
        if isinstance(self.renderer, Unset):
            renderer = UNSET
        elif isinstance(self.renderer, QuestionRenderer):
            renderer = self.renderer.to_dict()
        else:
            renderer = self.renderer

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "seed_generator": seed_generator,
                "question_generator": question_generator,
            }
        )
        if config_type is not UNSET:
            field_dict["config_type"] = config_type
        if labeler is not UNSET:
            field_dict["labeler"] = labeler
        if context_generators is not UNSET:
            field_dict["context_generators"] = context_generators
        if renderer is not UNSET:
            field_dict["renderer"] = renderer

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.forward_looking_question_generator import ForwardLookingQuestionGenerator
        from ..models.gdelt_seed_generator import GdeltSeedGenerator
        from ..models.news_context_generator import NewsContextGenerator
        from ..models.news_seed_generator import NewsSeedGenerator
        from ..models.question_and_label_generator import QuestionAndLabelGenerator
        from ..models.question_generator import QuestionGenerator
        from ..models.question_renderer import QuestionRenderer
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

        def _parse_question_generator(
            data: object,
        ) -> ForwardLookingQuestionGenerator | QuestionAndLabelGenerator | QuestionGenerator:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                question_generator_type_0 = QuestionGenerator.from_dict(data)

                return question_generator_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                question_generator_type_1 = ForwardLookingQuestionGenerator.from_dict(data)

                return question_generator_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()
            question_generator_type_2 = QuestionAndLabelGenerator.from_dict(data)

            return question_generator_type_2

        question_generator = _parse_question_generator(d.pop("question_generator"))

        config_type = cast(Literal["QUESTION_PIPELINE"] | Unset, d.pop("config_type", UNSET))
        if config_type != "QUESTION_PIPELINE" and not isinstance(config_type, Unset):
            raise ValueError(f"config_type must match const 'QUESTION_PIPELINE', got '{config_type}'")

        def _parse_labeler(data: object) -> None | Unset | WebSearchLabeler:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                labeler_type_0 = WebSearchLabeler.from_dict(data)

                return labeler_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | Unset | WebSearchLabeler, data)

        labeler = _parse_labeler(d.pop("labeler", UNSET))

        def _parse_context_generators(data: object) -> list[NewsContextGenerator] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                context_generators_type_0 = []
                _context_generators_type_0 = data
                for context_generators_type_0_item_data in _context_generators_type_0:
                    context_generators_type_0_item = NewsContextGenerator.from_dict(context_generators_type_0_item_data)

                    context_generators_type_0.append(context_generators_type_0_item)

                return context_generators_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[NewsContextGenerator] | None | Unset, data)

        context_generators = _parse_context_generators(d.pop("context_generators", UNSET))

        def _parse_renderer(data: object) -> None | QuestionRenderer | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                renderer_type_0 = QuestionRenderer.from_dict(data)

                return renderer_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | QuestionRenderer | Unset, data)

        renderer = _parse_renderer(d.pop("renderer", UNSET))

        question_pipeline = cls(
            seed_generator=seed_generator,
            question_generator=question_generator,
            config_type=config_type,
            labeler=labeler,
            context_generators=context_generators,
            renderer=renderer,
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
