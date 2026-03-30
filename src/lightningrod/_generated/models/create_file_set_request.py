from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.file_set_metadata_schema_input import FileSetMetadataSchemaInput


T = TypeVar("T", bound="CreateFileSetRequest")


@_attrs_define
class CreateFileSetRequest:
    """
    Attributes:
        name (str): Human-readable name for the FileSet
        description (None | str | Unset): Optional description of the FileSet's purpose
        metadata_schema (FileSetMetadataSchemaInput | None | Unset): Optional schema for validating file metadata
        rag_enabled (bool | Unset): Whether files should be indexed in Gemini File Search for RAG. When False, files can
            only be used with document-level transforms. This setting is immutable after creation. Default: True.
    """

    name: str
    description: None | str | Unset = UNSET
    metadata_schema: FileSetMetadataSchemaInput | None | Unset = UNSET
    rag_enabled: bool | Unset = True
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.file_set_metadata_schema_input import FileSetMetadataSchemaInput

        name = self.name

        description: None | str | Unset
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        metadata_schema: dict[str, Any] | None | Unset
        if isinstance(self.metadata_schema, Unset):
            metadata_schema = UNSET
        elif isinstance(self.metadata_schema, FileSetMetadataSchemaInput):
            metadata_schema = self.metadata_schema.to_dict()
        else:
            metadata_schema = self.metadata_schema

        rag_enabled = self.rag_enabled

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if metadata_schema is not UNSET:
            field_dict["metadata_schema"] = metadata_schema
        if rag_enabled is not UNSET:
            field_dict["rag_enabled"] = rag_enabled

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.file_set_metadata_schema_input import FileSetMetadataSchemaInput

        d = dict(src_dict)
        name = d.pop("name")

        def _parse_description(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        description = _parse_description(d.pop("description", UNSET))

        def _parse_metadata_schema(data: object) -> FileSetMetadataSchemaInput | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                metadata_schema_type_0 = FileSetMetadataSchemaInput.from_dict(data)

                return metadata_schema_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(FileSetMetadataSchemaInput | None | Unset, data)

        metadata_schema = _parse_metadata_schema(d.pop("metadata_schema", UNSET))

        rag_enabled = d.pop("rag_enabled", UNSET)

        create_file_set_request = cls(
            name=name,
            description=description,
            metadata_schema=metadata_schema,
            rag_enabled=rag_enabled,
        )

        create_file_set_request.additional_properties = d
        return create_file_set_request

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
