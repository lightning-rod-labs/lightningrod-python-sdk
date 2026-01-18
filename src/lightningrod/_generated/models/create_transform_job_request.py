from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.file_set_query_seed_generator import FileSetQuerySeedGenerator
    from ..models.file_set_seed_generator import FileSetSeedGenerator
    from ..models.forward_looking_question_generator import ForwardLookingQuestionGenerator
    from ..models.gdelt_seed_generator import GdeltSeedGenerator
    from ..models.news_seed_generator import NewsSeedGenerator
    from ..models.question_and_label_generator import QuestionAndLabelGenerator
    from ..models.question_generator import QuestionGenerator
    from ..models.question_pipeline import QuestionPipeline
    from ..models.question_renderer import QuestionRenderer
    from ..models.web_search_labeler import WebSearchLabeler


T = TypeVar("T", bound="CreateTransformJobRequest")


@_attrs_define
class CreateTransformJobRequest:
    """
    Attributes:
        config (FileSetQuerySeedGenerator | FileSetSeedGenerator | ForwardLookingQuestionGenerator | GdeltSeedGenerator
            | NewsSeedGenerator | QuestionAndLabelGenerator | QuestionGenerator | QuestionPipeline | QuestionRenderer |
            WebSearchLabeler):
        input_dataset_id (None | str | Unset):
        max_questions (int | None | Unset):
        configuration_id (None | str | Unset):
    """

    config: (
        FileSetQuerySeedGenerator
        | FileSetSeedGenerator
        | ForwardLookingQuestionGenerator
        | GdeltSeedGenerator
        | NewsSeedGenerator
        | QuestionAndLabelGenerator
        | QuestionGenerator
        | QuestionPipeline
        | QuestionRenderer
        | WebSearchLabeler
    )
    input_dataset_id: None | str | Unset = UNSET
    max_questions: int | None | Unset = UNSET
    configuration_id: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.file_set_query_seed_generator import FileSetQuerySeedGenerator
        from ..models.file_set_seed_generator import FileSetSeedGenerator
        from ..models.forward_looking_question_generator import ForwardLookingQuestionGenerator
        from ..models.gdelt_seed_generator import GdeltSeedGenerator
        from ..models.news_seed_generator import NewsSeedGenerator
        from ..models.question_and_label_generator import QuestionAndLabelGenerator
        from ..models.question_generator import QuestionGenerator
        from ..models.question_pipeline import QuestionPipeline
        from ..models.question_renderer import QuestionRenderer

        config: dict[str, Any]
        if isinstance(self.config, ForwardLookingQuestionGenerator):
            config = self.config.to_dict()
        elif isinstance(self.config, FileSetQuerySeedGenerator):
            config = self.config.to_dict()
        elif isinstance(self.config, FileSetSeedGenerator):
            config = self.config.to_dict()
        elif isinstance(self.config, GdeltSeedGenerator):
            config = self.config.to_dict()
        elif isinstance(self.config, NewsSeedGenerator):
            config = self.config.to_dict()
        elif isinstance(self.config, QuestionAndLabelGenerator):
            config = self.config.to_dict()
        elif isinstance(self.config, QuestionGenerator):
            config = self.config.to_dict()
        elif isinstance(self.config, QuestionPipeline):
            config = self.config.to_dict()
        elif isinstance(self.config, QuestionRenderer):
            config = self.config.to_dict()
        else:
            config = self.config.to_dict()

        input_dataset_id: None | str | Unset
        if isinstance(self.input_dataset_id, Unset):
            input_dataset_id = UNSET
        else:
            input_dataset_id = self.input_dataset_id

        max_questions: int | None | Unset
        if isinstance(self.max_questions, Unset):
            max_questions = UNSET
        else:
            max_questions = self.max_questions

        configuration_id: None | str | Unset
        if isinstance(self.configuration_id, Unset):
            configuration_id = UNSET
        else:
            configuration_id = self.configuration_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "config": config,
            }
        )
        if input_dataset_id is not UNSET:
            field_dict["input_dataset_id"] = input_dataset_id
        if max_questions is not UNSET:
            field_dict["max_questions"] = max_questions
        if configuration_id is not UNSET:
            field_dict["configuration_id"] = configuration_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.file_set_query_seed_generator import FileSetQuerySeedGenerator
        from ..models.file_set_seed_generator import FileSetSeedGenerator
        from ..models.forward_looking_question_generator import ForwardLookingQuestionGenerator
        from ..models.gdelt_seed_generator import GdeltSeedGenerator
        from ..models.news_seed_generator import NewsSeedGenerator
        from ..models.question_and_label_generator import QuestionAndLabelGenerator
        from ..models.question_generator import QuestionGenerator
        from ..models.question_pipeline import QuestionPipeline
        from ..models.question_renderer import QuestionRenderer
        from ..models.web_search_labeler import WebSearchLabeler

        d = dict(src_dict)

        def _parse_config(
            data: object,
        ) -> (
            FileSetQuerySeedGenerator
            | FileSetSeedGenerator
            | ForwardLookingQuestionGenerator
            | GdeltSeedGenerator
            | NewsSeedGenerator
            | QuestionAndLabelGenerator
            | QuestionGenerator
            | QuestionPipeline
            | QuestionRenderer
            | WebSearchLabeler
        ):
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_create_transform_config_type_0 = ForwardLookingQuestionGenerator.from_dict(data)

                return componentsschemas_create_transform_config_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_create_transform_config_type_1 = FileSetQuerySeedGenerator.from_dict(data)

                return componentsschemas_create_transform_config_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_create_transform_config_type_2 = FileSetSeedGenerator.from_dict(data)

                return componentsschemas_create_transform_config_type_2
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_create_transform_config_type_3 = GdeltSeedGenerator.from_dict(data)

                return componentsschemas_create_transform_config_type_3
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_create_transform_config_type_4 = NewsSeedGenerator.from_dict(data)

                return componentsschemas_create_transform_config_type_4
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_create_transform_config_type_5 = QuestionAndLabelGenerator.from_dict(data)

                return componentsschemas_create_transform_config_type_5
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_create_transform_config_type_6 = QuestionGenerator.from_dict(data)

                return componentsschemas_create_transform_config_type_6
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_create_transform_config_type_7 = QuestionPipeline.from_dict(data)

                return componentsschemas_create_transform_config_type_7
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_create_transform_config_type_8 = QuestionRenderer.from_dict(data)

                return componentsschemas_create_transform_config_type_8
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()
            componentsschemas_create_transform_config_type_9 = WebSearchLabeler.from_dict(data)

            return componentsschemas_create_transform_config_type_9

        config = _parse_config(d.pop("config"))

        def _parse_input_dataset_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        input_dataset_id = _parse_input_dataset_id(d.pop("input_dataset_id", UNSET))

        def _parse_max_questions(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        max_questions = _parse_max_questions(d.pop("max_questions", UNSET))

        def _parse_configuration_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        configuration_id = _parse_configuration_id(d.pop("configuration_id", UNSET))

        create_transform_job_request = cls(
            config=config,
            input_dataset_id=input_dataset_id,
            max_questions=max_questions,
            configuration_id=configuration_id,
        )

        create_transform_job_request.additional_properties = d
        return create_transform_job_request

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
