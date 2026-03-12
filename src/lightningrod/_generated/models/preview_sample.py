from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="PreviewSample")


@_attrs_define
class PreviewSample:
    """A single sample from a preview run.

    Attributes:
        question (None | str | Unset): The generated question text
        question_type (None | str | Unset): Type of question (e.g., binary)
        label (None | str | Unset): The label/answer if available
        label_confidence (float | None | Unset): Confidence in the label
        prompt_preview (None | str | Unset): Preview of the full prompt
        metadata_keys (list[str] | None | Unset): Keys in sample metadata
    """

    question: None | str | Unset = UNSET
    question_type: None | str | Unset = UNSET
    label: None | str | Unset = UNSET
    label_confidence: float | None | Unset = UNSET
    prompt_preview: None | str | Unset = UNSET
    metadata_keys: list[str] | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        question: None | str | Unset
        if isinstance(self.question, Unset):
            question = UNSET
        else:
            question = self.question

        question_type: None | str | Unset
        if isinstance(self.question_type, Unset):
            question_type = UNSET
        else:
            question_type = self.question_type

        label: None | str | Unset
        if isinstance(self.label, Unset):
            label = UNSET
        else:
            label = self.label

        label_confidence: float | None | Unset
        if isinstance(self.label_confidence, Unset):
            label_confidence = UNSET
        else:
            label_confidence = self.label_confidence

        prompt_preview: None | str | Unset
        if isinstance(self.prompt_preview, Unset):
            prompt_preview = UNSET
        else:
            prompt_preview = self.prompt_preview

        metadata_keys: list[str] | None | Unset
        if isinstance(self.metadata_keys, Unset):
            metadata_keys = UNSET
        elif isinstance(self.metadata_keys, list):
            metadata_keys = self.metadata_keys

        else:
            metadata_keys = self.metadata_keys

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if question is not UNSET:
            field_dict["question"] = question
        if question_type is not UNSET:
            field_dict["question_type"] = question_type
        if label is not UNSET:
            field_dict["label"] = label
        if label_confidence is not UNSET:
            field_dict["label_confidence"] = label_confidence
        if prompt_preview is not UNSET:
            field_dict["prompt_preview"] = prompt_preview
        if metadata_keys is not UNSET:
            field_dict["metadata_keys"] = metadata_keys

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_question(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        question = _parse_question(d.pop("question", UNSET))

        def _parse_question_type(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        question_type = _parse_question_type(d.pop("question_type", UNSET))

        def _parse_label(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        label = _parse_label(d.pop("label", UNSET))

        def _parse_label_confidence(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        label_confidence = _parse_label_confidence(d.pop("label_confidence", UNSET))

        def _parse_prompt_preview(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        prompt_preview = _parse_prompt_preview(d.pop("prompt_preview", UNSET))

        def _parse_metadata_keys(data: object) -> list[str] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                metadata_keys_type_0 = cast(list[str], data)

                return metadata_keys_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[str] | None | Unset, data)

        metadata_keys = _parse_metadata_keys(d.pop("metadata_keys", UNSET))

        preview_sample = cls(
            question=question,
            question_type=question_type,
            label=label,
            label_confidence=label_confidence,
            prompt_preview=prompt_preview,
            metadata_keys=metadata_keys,
        )

        preview_sample.additional_properties = d
        return preview_sample

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
