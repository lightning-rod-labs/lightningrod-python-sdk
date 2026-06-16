from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Literal, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.aggregate_context_generator import AggregateContextGenerator
    from ..models.big_query_seed_generator import BigQuerySeedGenerator
    from ..models.csv_seed_generator import CsvSeedGenerator
    from ..models.embedding_deduplication import EmbeddingDeduplication
    from ..models.file_set_document_context_generator import FileSetDocumentContextGenerator
    from ..models.file_set_document_labeler import FileSetDocumentLabeler
    from ..models.file_set_seed_generator import FileSetSeedGenerator
    from ..models.forward_looking_question_generator import ForwardLookingQuestionGenerator
    from ..models.fuzzy_deduplication import FuzzyDeduplication
    from ..models.gdelt_seed_generator import GdeltSeedGenerator
    from ..models.news_context_generator import NewsContextGenerator
    from ..models.news_seed_generator import NewsSeedGenerator
    from ..models.open_router_web_search_labeler import OpenRouterWebSearchLabeler
    from ..models.perplexity_context_generator import PerplexityContextGenerator
    from ..models.qdrant_context_generator import QdrantContextGenerator
    from ..models.qdrant_rag_labeler import QdrantRAGLabeler
    from ..models.question_and_label_generator import QuestionAndLabelGenerator
    from ..models.question_generator import QuestionGenerator
    from ..models.question_renderer import QuestionRenderer
    from ..models.rollout_generator import RolloutGenerator
    from ..models.rollout_scorer import RolloutScorer
    from ..models.template_question_generator import TemplateQuestionGenerator
    from ..models.topic_tree_seed_generator import TopicTreeSeedGenerator
    from ..models.web_search_context_generator import WebSearchContextGenerator
    from ..models.web_search_labeler import WebSearchLabeler


T = TypeVar("T", bound="QuestionPipeline")


@_attrs_define
class QuestionPipeline:
    """Serializable config for a question-generation pipeline.

    QuestionPipeline configs are expanded into ordered stage configs at run time.
    They are not executable Transform wrappers.

        Attributes:
            config_type (Literal['QUESTION_PIPELINE'] | Unset): Type of transform configuration Default:
                'QUESTION_PIPELINE'.
            seed_generator (BigQuerySeedGenerator | CsvSeedGenerator | FileSetSeedGenerator | GdeltSeedGenerator |
                NewsSeedGenerator | None | TopicTreeSeedGenerator | Unset): Configuration for seed generation
            question_generator (ForwardLookingQuestionGenerator | None | QuestionAndLabelGenerator | QuestionGenerator |
                TemplateQuestionGenerator | Unset): Configuration for question generation
            deduplication (EmbeddingDeduplication | FuzzyDeduplication | None | Unset): Optional sample deduplication
                config. Deduplication is applied at the earliest stage possible, depending on the config used.
            labeler (FileSetDocumentLabeler | None | OpenRouterWebSearchLabeler | QdrantRAGLabeler | Unset |
                WebSearchLabeler): Configuration for labeling. Not needed when using QuestionAndLabelGenerator.
            context_generators (list[AggregateContextGenerator | FileSetDocumentContextGenerator | NewsContextGenerator |
                PerplexityContextGenerator | QdrantContextGenerator | WebSearchContextGenerator] | None | Unset): Optional list
                of context generators to run before rendering
            renderer (None | QuestionRenderer | Unset): Optional configuration for rendering the final prompt
            rollout_generator (None | RolloutGenerator | Unset): Optional configuration for generating rollouts from
                multiple models
            scorer (None | RolloutScorer | Unset): Optional configuration for scoring rollouts against ground truth
    """

    config_type: Literal["QUESTION_PIPELINE"] | Unset = "QUESTION_PIPELINE"
    seed_generator: (
        BigQuerySeedGenerator
        | CsvSeedGenerator
        | FileSetSeedGenerator
        | GdeltSeedGenerator
        | NewsSeedGenerator
        | None
        | TopicTreeSeedGenerator
        | Unset
    ) = UNSET
    question_generator: (
        ForwardLookingQuestionGenerator
        | None
        | QuestionAndLabelGenerator
        | QuestionGenerator
        | TemplateQuestionGenerator
        | Unset
    ) = UNSET
    deduplication: EmbeddingDeduplication | FuzzyDeduplication | None | Unset = UNSET
    labeler: (
        FileSetDocumentLabeler | None | OpenRouterWebSearchLabeler | QdrantRAGLabeler | Unset | WebSearchLabeler
    ) = UNSET
    context_generators: (
        list[
            AggregateContextGenerator
            | FileSetDocumentContextGenerator
            | NewsContextGenerator
            | PerplexityContextGenerator
            | QdrantContextGenerator
            | WebSearchContextGenerator
        ]
        | None
        | Unset
    ) = UNSET
    renderer: None | QuestionRenderer | Unset = UNSET
    rollout_generator: None | RolloutGenerator | Unset = UNSET
    scorer: None | RolloutScorer | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.big_query_seed_generator import BigQuerySeedGenerator
        from ..models.csv_seed_generator import CsvSeedGenerator
        from ..models.embedding_deduplication import EmbeddingDeduplication
        from ..models.file_set_document_context_generator import FileSetDocumentContextGenerator
        from ..models.file_set_document_labeler import FileSetDocumentLabeler
        from ..models.file_set_seed_generator import FileSetSeedGenerator
        from ..models.forward_looking_question_generator import ForwardLookingQuestionGenerator
        from ..models.fuzzy_deduplication import FuzzyDeduplication
        from ..models.gdelt_seed_generator import GdeltSeedGenerator
        from ..models.news_context_generator import NewsContextGenerator
        from ..models.news_seed_generator import NewsSeedGenerator
        from ..models.open_router_web_search_labeler import OpenRouterWebSearchLabeler
        from ..models.perplexity_context_generator import PerplexityContextGenerator
        from ..models.qdrant_context_generator import QdrantContextGenerator
        from ..models.qdrant_rag_labeler import QdrantRAGLabeler
        from ..models.question_and_label_generator import QuestionAndLabelGenerator
        from ..models.question_generator import QuestionGenerator
        from ..models.question_renderer import QuestionRenderer
        from ..models.rollout_generator import RolloutGenerator
        from ..models.rollout_scorer import RolloutScorer
        from ..models.template_question_generator import TemplateQuestionGenerator
        from ..models.topic_tree_seed_generator import TopicTreeSeedGenerator
        from ..models.web_search_context_generator import WebSearchContextGenerator
        from ..models.web_search_labeler import WebSearchLabeler

        config_type = self.config_type

        seed_generator: dict[str, Any] | None | Unset
        if isinstance(self.seed_generator, Unset):
            seed_generator = UNSET
        elif isinstance(self.seed_generator, BigQuerySeedGenerator):
            seed_generator = self.seed_generator.to_dict()
        elif isinstance(self.seed_generator, NewsSeedGenerator):
            seed_generator = self.seed_generator.to_dict()
        elif isinstance(self.seed_generator, GdeltSeedGenerator):
            seed_generator = self.seed_generator.to_dict()
        elif isinstance(self.seed_generator, FileSetSeedGenerator):
            seed_generator = self.seed_generator.to_dict()
        elif isinstance(self.seed_generator, TopicTreeSeedGenerator):
            seed_generator = self.seed_generator.to_dict()
        elif isinstance(self.seed_generator, CsvSeedGenerator):
            seed_generator = self.seed_generator.to_dict()
        else:
            seed_generator = self.seed_generator

        question_generator: dict[str, Any] | None | Unset
        if isinstance(self.question_generator, Unset):
            question_generator = UNSET
        elif isinstance(self.question_generator, QuestionGenerator):
            question_generator = self.question_generator.to_dict()
        elif isinstance(self.question_generator, ForwardLookingQuestionGenerator):
            question_generator = self.question_generator.to_dict()
        elif isinstance(self.question_generator, QuestionAndLabelGenerator):
            question_generator = self.question_generator.to_dict()
        elif isinstance(self.question_generator, TemplateQuestionGenerator):
            question_generator = self.question_generator.to_dict()
        else:
            question_generator = self.question_generator

        deduplication: dict[str, Any] | None | Unset
        if isinstance(self.deduplication, Unset):
            deduplication = UNSET
        elif isinstance(self.deduplication, FuzzyDeduplication):
            deduplication = self.deduplication.to_dict()
        elif isinstance(self.deduplication, EmbeddingDeduplication):
            deduplication = self.deduplication.to_dict()
        else:
            deduplication = self.deduplication

        labeler: dict[str, Any] | None | Unset
        if isinstance(self.labeler, Unset):
            labeler = UNSET
        elif isinstance(self.labeler, WebSearchLabeler):
            labeler = self.labeler.to_dict()
        elif isinstance(self.labeler, OpenRouterWebSearchLabeler):
            labeler = self.labeler.to_dict()
        elif isinstance(self.labeler, QdrantRAGLabeler):
            labeler = self.labeler.to_dict()
        elif isinstance(self.labeler, FileSetDocumentLabeler):
            labeler = self.labeler.to_dict()
        else:
            labeler = self.labeler

        context_generators: list[dict[str, Any]] | None | Unset
        if isinstance(self.context_generators, Unset):
            context_generators = UNSET
        elif isinstance(self.context_generators, list):
            context_generators = []
            for context_generators_type_0_item_data in self.context_generators:
                context_generators_type_0_item: dict[str, Any]
                if isinstance(context_generators_type_0_item_data, NewsContextGenerator):
                    context_generators_type_0_item = context_generators_type_0_item_data.to_dict()
                elif isinstance(context_generators_type_0_item_data, QdrantContextGenerator):
                    context_generators_type_0_item = context_generators_type_0_item_data.to_dict()
                elif isinstance(context_generators_type_0_item_data, FileSetDocumentContextGenerator):
                    context_generators_type_0_item = context_generators_type_0_item_data.to_dict()
                elif isinstance(context_generators_type_0_item_data, WebSearchContextGenerator):
                    context_generators_type_0_item = context_generators_type_0_item_data.to_dict()
                elif isinstance(context_generators_type_0_item_data, PerplexityContextGenerator):
                    context_generators_type_0_item = context_generators_type_0_item_data.to_dict()
                else:
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

        rollout_generator: dict[str, Any] | None | Unset
        if isinstance(self.rollout_generator, Unset):
            rollout_generator = UNSET
        elif isinstance(self.rollout_generator, RolloutGenerator):
            rollout_generator = self.rollout_generator.to_dict()
        else:
            rollout_generator = self.rollout_generator

        scorer: dict[str, Any] | None | Unset
        if isinstance(self.scorer, Unset):
            scorer = UNSET
        elif isinstance(self.scorer, RolloutScorer):
            scorer = self.scorer.to_dict()
        else:
            scorer = self.scorer

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if config_type is not UNSET:
            field_dict["config_type"] = config_type
        if seed_generator is not UNSET:
            field_dict["seed_generator"] = seed_generator
        if question_generator is not UNSET:
            field_dict["question_generator"] = question_generator
        if deduplication is not UNSET:
            field_dict["deduplication"] = deduplication
        if labeler is not UNSET:
            field_dict["labeler"] = labeler
        if context_generators is not UNSET:
            field_dict["context_generators"] = context_generators
        if renderer is not UNSET:
            field_dict["renderer"] = renderer
        if rollout_generator is not UNSET:
            field_dict["rollout_generator"] = rollout_generator
        if scorer is not UNSET:
            field_dict["scorer"] = scorer

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.aggregate_context_generator import AggregateContextGenerator
        from ..models.big_query_seed_generator import BigQuerySeedGenerator
        from ..models.csv_seed_generator import CsvSeedGenerator
        from ..models.embedding_deduplication import EmbeddingDeduplication
        from ..models.file_set_document_context_generator import FileSetDocumentContextGenerator
        from ..models.file_set_document_labeler import FileSetDocumentLabeler
        from ..models.file_set_seed_generator import FileSetSeedGenerator
        from ..models.forward_looking_question_generator import ForwardLookingQuestionGenerator
        from ..models.fuzzy_deduplication import FuzzyDeduplication
        from ..models.gdelt_seed_generator import GdeltSeedGenerator
        from ..models.news_context_generator import NewsContextGenerator
        from ..models.news_seed_generator import NewsSeedGenerator
        from ..models.open_router_web_search_labeler import OpenRouterWebSearchLabeler
        from ..models.perplexity_context_generator import PerplexityContextGenerator
        from ..models.qdrant_context_generator import QdrantContextGenerator
        from ..models.qdrant_rag_labeler import QdrantRAGLabeler
        from ..models.question_and_label_generator import QuestionAndLabelGenerator
        from ..models.question_generator import QuestionGenerator
        from ..models.question_renderer import QuestionRenderer
        from ..models.rollout_generator import RolloutGenerator
        from ..models.rollout_scorer import RolloutScorer
        from ..models.template_question_generator import TemplateQuestionGenerator
        from ..models.topic_tree_seed_generator import TopicTreeSeedGenerator
        from ..models.web_search_context_generator import WebSearchContextGenerator
        from ..models.web_search_labeler import WebSearchLabeler

        d = dict(src_dict)
        config_type = cast(Literal["QUESTION_PIPELINE"] | Unset, d.pop("config_type", UNSET))
        if config_type != "QUESTION_PIPELINE" and not isinstance(config_type, Unset):
            raise ValueError(f"config_type must match const 'QUESTION_PIPELINE', got '{config_type}'")

        def _parse_seed_generator(
            data: object,
        ) -> (
            BigQuerySeedGenerator
            | CsvSeedGenerator
            | FileSetSeedGenerator
            | GdeltSeedGenerator
            | NewsSeedGenerator
            | None
            | TopicTreeSeedGenerator
            | Unset
        ):
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                seed_generator_type_0_type_0 = BigQuerySeedGenerator.from_dict(data)

                return seed_generator_type_0_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                seed_generator_type_0_type_1 = NewsSeedGenerator.from_dict(data)

                return seed_generator_type_0_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                seed_generator_type_0_type_2 = GdeltSeedGenerator.from_dict(data)

                return seed_generator_type_0_type_2
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                seed_generator_type_0_type_3 = FileSetSeedGenerator.from_dict(data)

                return seed_generator_type_0_type_3
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                seed_generator_type_0_type_4 = TopicTreeSeedGenerator.from_dict(data)

                return seed_generator_type_0_type_4
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                seed_generator_type_0_type_5 = CsvSeedGenerator.from_dict(data)

                return seed_generator_type_0_type_5
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(
                BigQuerySeedGenerator
                | CsvSeedGenerator
                | FileSetSeedGenerator
                | GdeltSeedGenerator
                | NewsSeedGenerator
                | None
                | TopicTreeSeedGenerator
                | Unset,
                data,
            )

        seed_generator = _parse_seed_generator(d.pop("seed_generator", UNSET))

        def _parse_question_generator(
            data: object,
        ) -> (
            ForwardLookingQuestionGenerator
            | None
            | QuestionAndLabelGenerator
            | QuestionGenerator
            | TemplateQuestionGenerator
            | Unset
        ):
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                question_generator_type_0_type_0 = QuestionGenerator.from_dict(data)

                return question_generator_type_0_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                question_generator_type_0_type_1 = ForwardLookingQuestionGenerator.from_dict(data)

                return question_generator_type_0_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                question_generator_type_0_type_2 = QuestionAndLabelGenerator.from_dict(data)

                return question_generator_type_0_type_2
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                question_generator_type_0_type_3 = TemplateQuestionGenerator.from_dict(data)

                return question_generator_type_0_type_3
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(
                ForwardLookingQuestionGenerator
                | None
                | QuestionAndLabelGenerator
                | QuestionGenerator
                | TemplateQuestionGenerator
                | Unset,
                data,
            )

        question_generator = _parse_question_generator(d.pop("question_generator", UNSET))

        def _parse_deduplication(data: object) -> EmbeddingDeduplication | FuzzyDeduplication | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                deduplication_type_0 = FuzzyDeduplication.from_dict(data)

                return deduplication_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                deduplication_type_1 = EmbeddingDeduplication.from_dict(data)

                return deduplication_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(EmbeddingDeduplication | FuzzyDeduplication | None | Unset, data)

        deduplication = _parse_deduplication(d.pop("deduplication", UNSET))

        def _parse_labeler(
            data: object,
        ) -> FileSetDocumentLabeler | None | OpenRouterWebSearchLabeler | QdrantRAGLabeler | Unset | WebSearchLabeler:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                labeler_type_0_type_0 = WebSearchLabeler.from_dict(data)

                return labeler_type_0_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                labeler_type_0_type_1 = OpenRouterWebSearchLabeler.from_dict(data)

                return labeler_type_0_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                labeler_type_0_type_2 = QdrantRAGLabeler.from_dict(data)

                return labeler_type_0_type_2
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                labeler_type_0_type_3 = FileSetDocumentLabeler.from_dict(data)

                return labeler_type_0_type_3
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(
                FileSetDocumentLabeler
                | None
                | OpenRouterWebSearchLabeler
                | QdrantRAGLabeler
                | Unset
                | WebSearchLabeler,
                data,
            )

        labeler = _parse_labeler(d.pop("labeler", UNSET))

        def _parse_context_generators(
            data: object,
        ) -> (
            list[
                AggregateContextGenerator
                | FileSetDocumentContextGenerator
                | NewsContextGenerator
                | PerplexityContextGenerator
                | QdrantContextGenerator
                | WebSearchContextGenerator
            ]
            | None
            | Unset
        ):
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

                    def _parse_context_generators_type_0_item(
                        data: object,
                    ) -> (
                        AggregateContextGenerator
                        | FileSetDocumentContextGenerator
                        | NewsContextGenerator
                        | PerplexityContextGenerator
                        | QdrantContextGenerator
                        | WebSearchContextGenerator
                    ):
                        try:
                            if not isinstance(data, dict):
                                raise TypeError()
                            context_generators_type_0_item_type_0 = NewsContextGenerator.from_dict(data)

                            return context_generators_type_0_item_type_0
                        except (TypeError, ValueError, AttributeError, KeyError):
                            pass
                        try:
                            if not isinstance(data, dict):
                                raise TypeError()
                            context_generators_type_0_item_type_1 = QdrantContextGenerator.from_dict(data)

                            return context_generators_type_0_item_type_1
                        except (TypeError, ValueError, AttributeError, KeyError):
                            pass
                        try:
                            if not isinstance(data, dict):
                                raise TypeError()
                            context_generators_type_0_item_type_2 = FileSetDocumentContextGenerator.from_dict(data)

                            return context_generators_type_0_item_type_2
                        except (TypeError, ValueError, AttributeError, KeyError):
                            pass
                        try:
                            if not isinstance(data, dict):
                                raise TypeError()
                            context_generators_type_0_item_type_3 = WebSearchContextGenerator.from_dict(data)

                            return context_generators_type_0_item_type_3
                        except (TypeError, ValueError, AttributeError, KeyError):
                            pass
                        try:
                            if not isinstance(data, dict):
                                raise TypeError()
                            context_generators_type_0_item_type_4 = PerplexityContextGenerator.from_dict(data)

                            return context_generators_type_0_item_type_4
                        except (TypeError, ValueError, AttributeError, KeyError):
                            pass
                        if not isinstance(data, dict):
                            raise TypeError()
                        context_generators_type_0_item_type_5 = AggregateContextGenerator.from_dict(data)

                        return context_generators_type_0_item_type_5

                    context_generators_type_0_item = _parse_context_generators_type_0_item(
                        context_generators_type_0_item_data
                    )

                    context_generators_type_0.append(context_generators_type_0_item)

                return context_generators_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(
                list[
                    AggregateContextGenerator
                    | FileSetDocumentContextGenerator
                    | NewsContextGenerator
                    | PerplexityContextGenerator
                    | QdrantContextGenerator
                    | WebSearchContextGenerator
                ]
                | None
                | Unset,
                data,
            )

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

        def _parse_rollout_generator(data: object) -> None | RolloutGenerator | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                rollout_generator_type_0 = RolloutGenerator.from_dict(data)

                return rollout_generator_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | RolloutGenerator | Unset, data)

        rollout_generator = _parse_rollout_generator(d.pop("rollout_generator", UNSET))

        def _parse_scorer(data: object) -> None | RolloutScorer | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                scorer_type_0 = RolloutScorer.from_dict(data)

                return scorer_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | RolloutScorer | Unset, data)

        scorer = _parse_scorer(d.pop("scorer", UNSET))

        question_pipeline = cls(
            config_type=config_type,
            seed_generator=seed_generator,
            question_generator=question_generator,
            deduplication=deduplication,
            labeler=labeler,
            context_generators=context_generators,
            renderer=renderer,
            rollout_generator=rollout_generator,
            scorer=scorer,
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
