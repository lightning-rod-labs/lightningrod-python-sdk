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


T = TypeVar("T", bound="WebSearchLabeler")


@_attrs_define
class WebSearchLabeler:
    """
    Attributes:
        config_type (Literal['WEB_SEARCH_LABELER'] | Unset): Type of transform configuration Default:
            'WEB_SEARCH_LABELER'.
        confidence_threshold (float | Unset): Minimum confidence threshold for including questions Default: 0.9.
        answer_type (BinaryAnswerType | ContinuousAnswerType | FreeResponseAnswerType | MultipleChoiceAnswerType | None
            | Unset): The type of answer expected, used to guide the labeler
        resolve_redirects (bool | Unset): Resolve redirect URLs to actual destinations Default: False.
    """

    config_type: Literal["WEB_SEARCH_LABELER"] | Unset = "WEB_SEARCH_LABELER"
    confidence_threshold: float | Unset = 0.9
    answer_type: (
        BinaryAnswerType | ContinuousAnswerType | FreeResponseAnswerType | MultipleChoiceAnswerType | None | Unset
    ) = UNSET
    resolve_redirects: bool | Unset = False
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.binary_answer_type import BinaryAnswerType
        from ..models.continuous_answer_type import ContinuousAnswerType
        from ..models.free_response_answer_type import FreeResponseAnswerType
        from ..models.multiple_choice_answer_type import MultipleChoiceAnswerType

        config_type = self.config_type

        confidence_threshold = self.confidence_threshold

        answer_type: dict[str, Any] | None | Unset
        if isinstance(self.answer_type, Unset):
            answer_type = UNSET
        elif isinstance(self.answer_type, BinaryAnswerType):
            answer_type = self.answer_type.to_dict()
        elif isinstance(self.answer_type, MultipleChoiceAnswerType):
            answer_type = self.answer_type.to_dict()
        elif isinstance(self.answer_type, ContinuousAnswerType):
            answer_type = self.answer_type.to_dict()
        elif isinstance(self.answer_type, FreeResponseAnswerType):
            answer_type = self.answer_type.to_dict()
        else:
            answer_type = self.answer_type

        resolve_redirects = self.resolve_redirects

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if config_type is not UNSET:
            field_dict["config_type"] = config_type
        if confidence_threshold is not UNSET:
            field_dict["confidence_threshold"] = confidence_threshold
        if answer_type is not UNSET:
            field_dict["answer_type"] = answer_type
        if resolve_redirects is not UNSET:
            field_dict["resolve_redirects"] = resolve_redirects

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.binary_answer_type import BinaryAnswerType
        from ..models.continuous_answer_type import ContinuousAnswerType
        from ..models.free_response_answer_type import FreeResponseAnswerType
        from ..models.multiple_choice_answer_type import MultipleChoiceAnswerType

        d = dict(src_dict)
        config_type = cast(Literal["WEB_SEARCH_LABELER"] | Unset, d.pop("config_type", UNSET))
        if config_type != "WEB_SEARCH_LABELER" and not isinstance(config_type, Unset):
            raise ValueError(f"config_type must match const 'WEB_SEARCH_LABELER', got '{config_type}'")

        confidence_threshold = d.pop("confidence_threshold", UNSET)

        def _parse_answer_type(
            data: object,
        ) -> BinaryAnswerType | ContinuousAnswerType | FreeResponseAnswerType | MultipleChoiceAnswerType | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                answer_type_type_0_type_0 = BinaryAnswerType.from_dict(data)

                return answer_type_type_0_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                answer_type_type_0_type_1 = MultipleChoiceAnswerType.from_dict(data)

                return answer_type_type_0_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                answer_type_type_0_type_2 = ContinuousAnswerType.from_dict(data)

                return answer_type_type_0_type_2
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                answer_type_type_0_type_3 = FreeResponseAnswerType.from_dict(data)

                return answer_type_type_0_type_3
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(
                BinaryAnswerType
                | ContinuousAnswerType
                | FreeResponseAnswerType
                | MultipleChoiceAnswerType
                | None
                | Unset,
                data,
            )

        answer_type = _parse_answer_type(d.pop("answer_type", UNSET))

        resolve_redirects = d.pop("resolve_redirects", UNSET)

        web_search_labeler = cls(
            config_type=config_type,
            confidence_threshold=confidence_threshold,
            answer_type=answer_type,
            resolve_redirects=resolve_redirects,
        )

        web_search_labeler.additional_properties = d
        return web_search_labeler

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
