from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.csv_seed_generator import CsvSeedGenerator
    from ..models.file_set_document_context_generator import FileSetDocumentContextGenerator
    from ..models.file_set_document_labeler import FileSetDocumentLabeler
    from ..models.file_set_seed_generator import FileSetSeedGenerator
    from ..models.forward_looking_question_generator import ForwardLookingQuestionGenerator
    from ..models.gdelt_seed_generator import GdeltSeedGenerator
    from ..models.key_deduplication import KeyDeduplication
    from ..models.news_seed_generator import NewsSeedGenerator
    from ..models.qdrant_context_generator import QdrantContextGenerator
    from ..models.qdrant_rag_labeler import QdrantRAGLabeler
    from ..models.question_and_label_generator import QuestionAndLabelGenerator
    from ..models.question_generator import QuestionGenerator
    from ..models.question_pipeline import QuestionPipeline
    from ..models.question_renderer import QuestionRenderer
    from ..models.topic_tree_seed_generator import TopicTreeSeedGenerator
    from ..models.web_search_labeler import WebSearchLabeler


T = TypeVar("T", bound="EstimateCostRequest")


@_attrs_define
class EstimateCostRequest:
    """
    Attributes:
        config (CsvSeedGenerator | FileSetDocumentContextGenerator | FileSetDocumentLabeler | FileSetSeedGenerator |
            ForwardLookingQuestionGenerator | GdeltSeedGenerator | KeyDeduplication | NewsSeedGenerator |
            QdrantContextGenerator | QdrantRAGLabeler | QuestionAndLabelGenerator | QuestionGenerator | QuestionPipeline |
            QuestionRenderer | TopicTreeSeedGenerator | WebSearchLabeler):
        max_questions (int | None | Unset):
    """

    config: (
        CsvSeedGenerator
        | FileSetDocumentContextGenerator
        | FileSetDocumentLabeler
        | FileSetSeedGenerator
        | ForwardLookingQuestionGenerator
        | GdeltSeedGenerator
        | KeyDeduplication
        | NewsSeedGenerator
        | QdrantContextGenerator
        | QdrantRAGLabeler
        | QuestionAndLabelGenerator
        | QuestionGenerator
        | QuestionPipeline
        | QuestionRenderer
        | TopicTreeSeedGenerator
        | WebSearchLabeler
    )
    max_questions: int | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.csv_seed_generator import CsvSeedGenerator
        from ..models.file_set_document_context_generator import FileSetDocumentContextGenerator
        from ..models.file_set_document_labeler import FileSetDocumentLabeler
        from ..models.file_set_seed_generator import FileSetSeedGenerator
        from ..models.forward_looking_question_generator import ForwardLookingQuestionGenerator
        from ..models.gdelt_seed_generator import GdeltSeedGenerator
        from ..models.key_deduplication import KeyDeduplication
        from ..models.news_seed_generator import NewsSeedGenerator
        from ..models.qdrant_context_generator import QdrantContextGenerator
        from ..models.qdrant_rag_labeler import QdrantRAGLabeler
        from ..models.question_and_label_generator import QuestionAndLabelGenerator
        from ..models.question_generator import QuestionGenerator
        from ..models.question_pipeline import QuestionPipeline
        from ..models.question_renderer import QuestionRenderer
        from ..models.topic_tree_seed_generator import TopicTreeSeedGenerator

        config: dict[str, Any]
        if isinstance(self.config, CsvSeedGenerator):
            config = self.config.to_dict()
        elif isinstance(self.config, FileSetDocumentContextGenerator):
            config = self.config.to_dict()
        elif isinstance(self.config, FileSetDocumentLabeler):
            config = self.config.to_dict()
        elif isinstance(self.config, FileSetSeedGenerator):
            config = self.config.to_dict()
        elif isinstance(self.config, ForwardLookingQuestionGenerator):
            config = self.config.to_dict()
        elif isinstance(self.config, GdeltSeedGenerator):
            config = self.config.to_dict()
        elif isinstance(self.config, KeyDeduplication):
            config = self.config.to_dict()
        elif isinstance(self.config, NewsSeedGenerator):
            config = self.config.to_dict()
        elif isinstance(self.config, QuestionAndLabelGenerator):
            config = self.config.to_dict()
        elif isinstance(self.config, QuestionGenerator):
            config = self.config.to_dict()
        elif isinstance(self.config, QdrantContextGenerator):
            config = self.config.to_dict()
        elif isinstance(self.config, QdrantRAGLabeler):
            config = self.config.to_dict()
        elif isinstance(self.config, QuestionPipeline):
            config = self.config.to_dict()
        elif isinstance(self.config, QuestionRenderer):
            config = self.config.to_dict()
        elif isinstance(self.config, TopicTreeSeedGenerator):
            config = self.config.to_dict()
        else:
            config = self.config.to_dict()

        max_questions: int | None | Unset
        if isinstance(self.max_questions, Unset):
            max_questions = UNSET
        else:
            max_questions = self.max_questions

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "config": config,
            }
        )
        if max_questions is not UNSET:
            field_dict["max_questions"] = max_questions

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.csv_seed_generator import CsvSeedGenerator
        from ..models.file_set_document_context_generator import FileSetDocumentContextGenerator
        from ..models.file_set_document_labeler import FileSetDocumentLabeler
        from ..models.file_set_seed_generator import FileSetSeedGenerator
        from ..models.forward_looking_question_generator import ForwardLookingQuestionGenerator
        from ..models.gdelt_seed_generator import GdeltSeedGenerator
        from ..models.key_deduplication import KeyDeduplication
        from ..models.news_seed_generator import NewsSeedGenerator
        from ..models.qdrant_context_generator import QdrantContextGenerator
        from ..models.qdrant_rag_labeler import QdrantRAGLabeler
        from ..models.question_and_label_generator import QuestionAndLabelGenerator
        from ..models.question_generator import QuestionGenerator
        from ..models.question_pipeline import QuestionPipeline
        from ..models.question_renderer import QuestionRenderer
        from ..models.topic_tree_seed_generator import TopicTreeSeedGenerator
        from ..models.web_search_labeler import WebSearchLabeler

        d = dict(src_dict)

        def _parse_config(
            data: object,
        ) -> (
            CsvSeedGenerator
            | FileSetDocumentContextGenerator
            | FileSetDocumentLabeler
            | FileSetSeedGenerator
            | ForwardLookingQuestionGenerator
            | GdeltSeedGenerator
            | KeyDeduplication
            | NewsSeedGenerator
            | QdrantContextGenerator
            | QdrantRAGLabeler
            | QuestionAndLabelGenerator
            | QuestionGenerator
            | QuestionPipeline
            | QuestionRenderer
            | TopicTreeSeedGenerator
            | WebSearchLabeler
        ):
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_create_transform_config_type_0 = CsvSeedGenerator.from_dict(data)

                return componentsschemas_create_transform_config_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_create_transform_config_type_1 = FileSetDocumentContextGenerator.from_dict(data)

                return componentsschemas_create_transform_config_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_create_transform_config_type_2 = FileSetDocumentLabeler.from_dict(data)

                return componentsschemas_create_transform_config_type_2
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_create_transform_config_type_3 = FileSetSeedGenerator.from_dict(data)

                return componentsschemas_create_transform_config_type_3
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_create_transform_config_type_4 = ForwardLookingQuestionGenerator.from_dict(data)

                return componentsschemas_create_transform_config_type_4
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_create_transform_config_type_5 = GdeltSeedGenerator.from_dict(data)

                return componentsschemas_create_transform_config_type_5
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_create_transform_config_type_6 = KeyDeduplication.from_dict(data)

                return componentsschemas_create_transform_config_type_6
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_create_transform_config_type_7 = NewsSeedGenerator.from_dict(data)

                return componentsschemas_create_transform_config_type_7
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_create_transform_config_type_8 = QuestionAndLabelGenerator.from_dict(data)

                return componentsschemas_create_transform_config_type_8
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_create_transform_config_type_9 = QuestionGenerator.from_dict(data)

                return componentsschemas_create_transform_config_type_9
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_create_transform_config_type_10 = QdrantContextGenerator.from_dict(data)

                return componentsschemas_create_transform_config_type_10
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_create_transform_config_type_11 = QdrantRAGLabeler.from_dict(data)

                return componentsschemas_create_transform_config_type_11
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_create_transform_config_type_12 = QuestionPipeline.from_dict(data)

                return componentsschemas_create_transform_config_type_12
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_create_transform_config_type_13 = QuestionRenderer.from_dict(data)

                return componentsschemas_create_transform_config_type_13
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_create_transform_config_type_14 = TopicTreeSeedGenerator.from_dict(data)

                return componentsschemas_create_transform_config_type_14
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()
            componentsschemas_create_transform_config_type_15 = WebSearchLabeler.from_dict(data)

            return componentsschemas_create_transform_config_type_15

        config = _parse_config(d.pop("config"))

        def _parse_max_questions(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        max_questions = _parse_max_questions(d.pop("max_questions", UNSET))

        estimate_cost_request = cls(
            config=config,
            max_questions=max_questions,
        )

        estimate_cost_request.additional_properties = d
        return estimate_cost_request

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
