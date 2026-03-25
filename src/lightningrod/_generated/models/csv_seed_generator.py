from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Literal, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="CsvSeedGenerator")


@_attrs_define
class CsvSeedGenerator:
    """
    Attributes:
        file_id (list[str] | str): OrgFile ID(s) from POST /files/ upload response
        config_type (Literal['CSV_SEED_GENERATOR'] | Unset): Type of transform configuration Default:
            'CSV_SEED_GENERATOR'.
        seed_text_column (None | str | Unset): Column name for Seed.seed_text; if None, serialize entire row as JSON
        label_column (None | str | Unset): Column name for pre-existing labels (populates Sample.label)
        date_column (None | str | Unset): Column name for Seed.seed_creation_date
    """

    file_id: list[str] | str
    config_type: Literal["CSV_SEED_GENERATOR"] | Unset = "CSV_SEED_GENERATOR"
    seed_text_column: None | str | Unset = UNSET
    label_column: None | str | Unset = UNSET
    date_column: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        file_id: list[str] | str
        if isinstance(self.file_id, list):
            file_id = self.file_id

        else:
            file_id = self.file_id

        config_type = self.config_type

        seed_text_column: None | str | Unset
        if isinstance(self.seed_text_column, Unset):
            seed_text_column = UNSET
        else:
            seed_text_column = self.seed_text_column

        label_column: None | str | Unset
        if isinstance(self.label_column, Unset):
            label_column = UNSET
        else:
            label_column = self.label_column

        date_column: None | str | Unset
        if isinstance(self.date_column, Unset):
            date_column = UNSET
        else:
            date_column = self.date_column

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "file_id": file_id,
            }
        )
        if config_type is not UNSET:
            field_dict["config_type"] = config_type
        if seed_text_column is not UNSET:
            field_dict["seed_text_column"] = seed_text_column
        if label_column is not UNSET:
            field_dict["label_column"] = label_column
        if date_column is not UNSET:
            field_dict["date_column"] = date_column

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_file_id(data: object) -> list[str] | str:
            try:
                if not isinstance(data, list):
                    raise TypeError()
                file_id_type_1 = cast(list[str], data)

                return file_id_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[str] | str, data)

        file_id = _parse_file_id(d.pop("file_id"))

        config_type = cast(Literal["CSV_SEED_GENERATOR"] | Unset, d.pop("config_type", UNSET))
        if config_type != "CSV_SEED_GENERATOR" and not isinstance(config_type, Unset):
            raise ValueError(f"config_type must match const 'CSV_SEED_GENERATOR', got '{config_type}'")

        def _parse_seed_text_column(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        seed_text_column = _parse_seed_text_column(d.pop("seed_text_column", UNSET))

        def _parse_label_column(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        label_column = _parse_label_column(d.pop("label_column", UNSET))

        def _parse_date_column(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        date_column = _parse_date_column(d.pop("date_column", UNSET))

        csv_seed_generator = cls(
            file_id=file_id,
            config_type=config_type,
            seed_text_column=seed_text_column,
            label_column=label_column,
            date_column=date_column,
        )

        csv_seed_generator.additional_properties = d
        return csv_seed_generator

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
