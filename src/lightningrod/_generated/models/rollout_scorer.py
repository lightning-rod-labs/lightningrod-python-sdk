from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Literal, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.binary_answer_type import BinaryAnswerType
    from ..models.continuous_answer_type import ContinuousAnswerType
    from ..models.free_response_answer_type import FreeResponseAnswerType
    from ..models.multiple_choice_answer_type import MultipleChoiceAnswerType
    from ..models.rollout_scorer_multiple_choice_options_type_0 import RolloutScorerMultipleChoiceOptionsType0


T = TypeVar("T", bound="RolloutScorer")


@_attrs_define
class RolloutScorer:
    """
    Attributes:
        answer_type (BinaryAnswerType | ContinuousAnswerType | FreeResponseAnswerType | MultipleChoiceAnswerType): the
            answer type of the question
        config_type (Literal['ROLLOUT_SCORER'] | Unset):  Default: 'ROLLOUT_SCORER'.
        multiple_choice_options (None | RolloutScorerMultipleChoiceOptionsType0 | Unset):
        is_mutually_exclusive (bool | Unset):  Default: True.
    """

    answer_type: BinaryAnswerType | ContinuousAnswerType | FreeResponseAnswerType | MultipleChoiceAnswerType
    config_type: Literal["ROLLOUT_SCORER"] | Unset = "ROLLOUT_SCORER"
    multiple_choice_options: None | RolloutScorerMultipleChoiceOptionsType0 | Unset = UNSET
    is_mutually_exclusive: bool | Unset = True
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.binary_answer_type import BinaryAnswerType
        from ..models.continuous_answer_type import ContinuousAnswerType
        from ..models.multiple_choice_answer_type import MultipleChoiceAnswerType
        from ..models.rollout_scorer_multiple_choice_options_type_0 import RolloutScorerMultipleChoiceOptionsType0

        answer_type: dict[str, Any]
        if isinstance(self.answer_type, BinaryAnswerType):
            answer_type = self.answer_type.to_dict()
        elif isinstance(self.answer_type, MultipleChoiceAnswerType):
            answer_type = self.answer_type.to_dict()
        elif isinstance(self.answer_type, ContinuousAnswerType):
            answer_type = self.answer_type.to_dict()
        else:
            answer_type = self.answer_type.to_dict()

        config_type = self.config_type

        multiple_choice_options: dict[str, Any] | None | Unset
        if isinstance(self.multiple_choice_options, Unset):
            multiple_choice_options = UNSET
        elif isinstance(self.multiple_choice_options, RolloutScorerMultipleChoiceOptionsType0):
            multiple_choice_options = self.multiple_choice_options.to_dict()
        else:
            multiple_choice_options = self.multiple_choice_options

        is_mutually_exclusive = self.is_mutually_exclusive

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "answer_type": answer_type,
            }
        )
        if config_type is not UNSET:
            field_dict["config_type"] = config_type
        if multiple_choice_options is not UNSET:
            field_dict["multiple_choice_options"] = multiple_choice_options
        if is_mutually_exclusive is not UNSET:
            field_dict["is_mutually_exclusive"] = is_mutually_exclusive

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.binary_answer_type import BinaryAnswerType
        from ..models.continuous_answer_type import ContinuousAnswerType
        from ..models.free_response_answer_type import FreeResponseAnswerType
        from ..models.multiple_choice_answer_type import MultipleChoiceAnswerType
        from ..models.rollout_scorer_multiple_choice_options_type_0 import RolloutScorerMultipleChoiceOptionsType0

        d = dict(src_dict)

        def _parse_answer_type(
            data: object,
        ) -> BinaryAnswerType | ContinuousAnswerType | FreeResponseAnswerType | MultipleChoiceAnswerType:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                answer_type_type_0 = BinaryAnswerType.from_dict(data)

                return answer_type_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                answer_type_type_1 = MultipleChoiceAnswerType.from_dict(data)

                return answer_type_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                answer_type_type_2 = ContinuousAnswerType.from_dict(data)

                return answer_type_type_2
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()
            answer_type_type_3 = FreeResponseAnswerType.from_dict(data)

            return answer_type_type_3

        answer_type = _parse_answer_type(d.pop("answer_type"))

        config_type = cast(Literal["ROLLOUT_SCORER"] | Unset, d.pop("config_type", UNSET))
        if config_type != "ROLLOUT_SCORER" and not isinstance(config_type, Unset):
            raise ValueError(f"config_type must match const 'ROLLOUT_SCORER', got '{config_type}'")

        def _parse_multiple_choice_options(data: object) -> None | RolloutScorerMultipleChoiceOptionsType0 | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                multiple_choice_options_type_0 = RolloutScorerMultipleChoiceOptionsType0.from_dict(data)

                return multiple_choice_options_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | RolloutScorerMultipleChoiceOptionsType0 | Unset, data)

        multiple_choice_options = _parse_multiple_choice_options(d.pop("multiple_choice_options", UNSET))

        is_mutually_exclusive = d.pop("is_mutually_exclusive", UNSET)

        rollout_scorer = cls(
            answer_type=answer_type,
            config_type=config_type,
            multiple_choice_options=multiple_choice_options,
            is_mutually_exclusive=is_mutually_exclusive,
        )

        rollout_scorer.additional_properties = d
        return rollout_scorer

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
