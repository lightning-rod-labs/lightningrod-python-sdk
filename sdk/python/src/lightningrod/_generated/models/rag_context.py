from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Literal, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="RAGContext")


@_attrs_define
class RAGContext:
    """
    Attributes:
        rendered_context (str):
        document_id (str):
        context_type (Literal['RAG_CONTEXT'] | Unset):  Default: 'RAG_CONTEXT'.
    """

    rendered_context: str
    document_id: str
    context_type: Literal["RAG_CONTEXT"] | Unset = "RAG_CONTEXT"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        rendered_context = self.rendered_context

        document_id = self.document_id

        context_type = self.context_type

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "rendered_context": rendered_context,
                "document_id": document_id,
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

        context_type = cast(Literal["RAG_CONTEXT"] | Unset, d.pop("context_type", UNSET))
        if context_type != "RAG_CONTEXT" and not isinstance(context_type, Unset):
            raise ValueError(f"context_type must match const 'RAG_CONTEXT', got '{context_type}'")

        rag_context = cls(
            rendered_context=rendered_context,
            document_id=document_id,
            context_type=context_type,
        )

        rag_context.additional_properties = d
        return rag_context

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
