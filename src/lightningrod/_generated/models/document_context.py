from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Literal, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="DocumentContext")


@_attrs_define
class DocumentContext:
    """
    Attributes:
        rendered_context (str):
        document_id (str):
        source_file_name (str):
        context_type (Literal['DOCUMENT_CONTEXT'] | Unset):  Default: 'DOCUMENT_CONTEXT'.
    """

    rendered_context: str
    document_id: str
    source_file_name: str
    context_type: Literal["DOCUMENT_CONTEXT"] | Unset = "DOCUMENT_CONTEXT"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        rendered_context = self.rendered_context

        document_id = self.document_id

        source_file_name = self.source_file_name

        context_type = self.context_type

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "rendered_context": rendered_context,
                "document_id": document_id,
                "source_file_name": source_file_name,
            }
        )
        if context_type is not UNSET:
            field_dict["context_type"] = context_type

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        rendered_context = d.pop("rendered_context")

        document_id = d.pop("document_id")

        source_file_name = d.pop("source_file_name")

        context_type = cast(Literal["DOCUMENT_CONTEXT"] | Unset, d.pop("context_type", UNSET))
        if context_type != "DOCUMENT_CONTEXT" and not isinstance(context_type, Unset):
            raise ValueError(f"context_type must match const 'DOCUMENT_CONTEXT', got '{context_type}'")

        document_context = cls(
            rendered_context=rendered_context,
            document_id=document_id,
            source_file_name=source_file_name,
            context_type=context_type,
        )

        document_context.additional_properties = d
        return document_context

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
