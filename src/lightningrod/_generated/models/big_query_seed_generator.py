from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Literal, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="BigQuerySeedGenerator")


@_attrs_define
class BigQuerySeedGenerator:
    """
    Attributes:
        query (str): BigQuery SQL query to execute
        config_type (Literal['BIGQUERY_SEED_GENERATOR'] | Unset): Type of transform configuration Default:
            'BIGQUERY_SEED_GENERATOR'.
        seed_text_column (str | Unset): Column name for Seed.seed_text Default: 'text'.
        date_column (None | str | Unset): Column name for Seed.seed_creation_date
        max_rows (int | Unset): Total rows to fetch across all batches Default: 10000.
        batch_size (int | Unset): Rows per batch; each batch becomes one seed interval Default: 250.
    """

    query: str
    config_type: Literal["BIGQUERY_SEED_GENERATOR"] | Unset = "BIGQUERY_SEED_GENERATOR"
    seed_text_column: str | Unset = "text"
    date_column: None | str | Unset = UNSET
    max_rows: int | Unset = 10000
    batch_size: int | Unset = 250
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        query = self.query

        config_type = self.config_type

        seed_text_column = self.seed_text_column

        date_column: None | str | Unset
        if isinstance(self.date_column, Unset):
            date_column = UNSET
        else:
            date_column = self.date_column

        max_rows = self.max_rows

        batch_size = self.batch_size

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "query": query,
            }
        )
        if config_type is not UNSET:
            field_dict["config_type"] = config_type
        if seed_text_column is not UNSET:
            field_dict["seed_text_column"] = seed_text_column
        if date_column is not UNSET:
            field_dict["date_column"] = date_column
        if max_rows is not UNSET:
            field_dict["max_rows"] = max_rows
        if batch_size is not UNSET:
            field_dict["batch_size"] = batch_size

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        query = d.pop("query")

        config_type = cast(Literal["BIGQUERY_SEED_GENERATOR"] | Unset, d.pop("config_type", UNSET))
        if config_type != "BIGQUERY_SEED_GENERATOR" and not isinstance(config_type, Unset):
            raise ValueError(f"config_type must match const 'BIGQUERY_SEED_GENERATOR', got '{config_type}'")

        seed_text_column = d.pop("seed_text_column", UNSET)

        def _parse_date_column(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        date_column = _parse_date_column(d.pop("date_column", UNSET))

        max_rows = d.pop("max_rows", UNSET)

        batch_size = d.pop("batch_size", UNSET)

        big_query_seed_generator = cls(
            query=query,
            config_type=config_type,
            seed_text_column=seed_text_column,
            date_column=date_column,
            max_rows=max_rows,
            batch_size=batch_size,
        )

        big_query_seed_generator.additional_properties = d
        return big_query_seed_generator

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
