from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, Literal, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="ForwardLookingQuestion")


@_attrs_define
class ForwardLookingQuestion:
    """
    Attributes:
        question_text (str):
        date_close (datetime.datetime):
        event_date (datetime.datetime):
        resolution_criteria (str):
        question_type (Literal['FORWARD_LOOKING_QUESTION'] | Unset):  Default: 'FORWARD_LOOKING_QUESTION'.
        prediction_date (datetime.datetime | None | Unset):
    """

    question_text: str
    date_close: datetime.datetime
    event_date: datetime.datetime
    resolution_criteria: str
    question_type: Literal["FORWARD_LOOKING_QUESTION"] | Unset = "FORWARD_LOOKING_QUESTION"
    prediction_date: datetime.datetime | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        question_text = self.question_text

        date_close = self.date_close.isoformat()

        event_date = self.event_date.isoformat()

        resolution_criteria = self.resolution_criteria

        question_type = self.question_type

        prediction_date: None | str | Unset
        if isinstance(self.prediction_date, Unset):
            prediction_date = UNSET
        elif isinstance(self.prediction_date, datetime.datetime):
            prediction_date = self.prediction_date.isoformat()
        else:
            prediction_date = self.prediction_date

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "question_text": question_text,
                "date_close": date_close,
                "event_date": event_date,
                "resolution_criteria": resolution_criteria,
            }
        )
        if question_type is not UNSET:
            field_dict["question_type"] = question_type
        if prediction_date is not UNSET:
            field_dict["prediction_date"] = prediction_date

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        question_text = d.pop("question_text")

        date_close = isoparse(d.pop("date_close"))

        event_date = isoparse(d.pop("event_date"))

        resolution_criteria = d.pop("resolution_criteria")

        question_type = cast(Literal["FORWARD_LOOKING_QUESTION"] | Unset, d.pop("question_type", UNSET))
        if question_type != "FORWARD_LOOKING_QUESTION" and not isinstance(question_type, Unset):
            raise ValueError(f"question_type must match const 'FORWARD_LOOKING_QUESTION', got '{question_type}'")

        def _parse_prediction_date(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                prediction_date_type_0 = isoparse(data)

                return prediction_date_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        prediction_date = _parse_prediction_date(d.pop("prediction_date", UNSET))

        forward_looking_question = cls(
            question_text=question_text,
            date_close=date_close,
            event_date=event_date,
            resolution_criteria=resolution_criteria,
            question_type=question_type,
            prediction_date=prediction_date,
        )

        forward_looking_question.additional_properties = d
        return forward_looking_question

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
