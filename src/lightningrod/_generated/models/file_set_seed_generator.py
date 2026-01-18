from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Literal, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="FileSetSeedGenerator")


@_attrs_define
class FileSetSeedGenerator:
    """Configuration for FileSet Seed Generator transform.

    Attributes:
        file_set_id (str): FileSet ID to read files from
        config_type (Literal['FILESET_SEED_GENERATOR'] | Unset): Type of transform configuration Default:
            'FILESET_SEED_GENERATOR'.
        chunk_size (int | Unset): Number of characters per chunk Default: 4000.
        chunk_overlap (int | Unset): Number of overlapping characters between consecutive chunks Default: 200.
    """

    file_set_id: str
    config_type: Literal["FILESET_SEED_GENERATOR"] | Unset = "FILESET_SEED_GENERATOR"
    chunk_size: int | Unset = 4000
    chunk_overlap: int | Unset = 200
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        file_set_id = self.file_set_id

        config_type = self.config_type

        chunk_size = self.chunk_size

        chunk_overlap = self.chunk_overlap

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "file_set_id": file_set_id,
            }
        )
        if config_type is not UNSET:
            field_dict["config_type"] = config_type
        if chunk_size is not UNSET:
            field_dict["chunk_size"] = chunk_size
        if chunk_overlap is not UNSET:
            field_dict["chunk_overlap"] = chunk_overlap

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        file_set_id = d.pop("file_set_id")

        config_type = cast(Literal["FILESET_SEED_GENERATOR"] | Unset, d.pop("config_type", UNSET))
        if config_type != "FILESET_SEED_GENERATOR" and not isinstance(config_type, Unset):
            raise ValueError(f"config_type must match const 'FILESET_SEED_GENERATOR', got '{config_type}'")

        chunk_size = d.pop("chunk_size", UNSET)

        chunk_overlap = d.pop("chunk_overlap", UNSET)

        file_set_seed_generator = cls(
            file_set_id=file_set_id,
            config_type=config_type,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )

        file_set_seed_generator.additional_properties = d
        return file_set_seed_generator

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
