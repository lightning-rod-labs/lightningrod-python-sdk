from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.seed_passthrough_data import SeedPassthroughData


T = TypeVar("T", bound="Seed")


@_attrs_define
class Seed:
    """
    Attributes:
        seed_text (str):
        passthrough_data (SeedPassthroughData | Unset):
        url (None | str | Unset):
        seed_creation_date (datetime.datetime | None | Unset):
    """

    seed_text: str
    passthrough_data: SeedPassthroughData | Unset = UNSET
    url: None | str | Unset = UNSET
    seed_creation_date: datetime.datetime | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        seed_text = self.seed_text

        passthrough_data: dict[str, Any] | Unset = UNSET
        if not isinstance(self.passthrough_data, Unset):
            passthrough_data = self.passthrough_data.to_dict()

        url: None | str | Unset
        if isinstance(self.url, Unset):
            url = UNSET
        else:
            url = self.url

        seed_creation_date: None | str | Unset
        if isinstance(self.seed_creation_date, Unset):
            seed_creation_date = UNSET
        elif isinstance(self.seed_creation_date, datetime.datetime):
            seed_creation_date = self.seed_creation_date.isoformat()
        else:
            seed_creation_date = self.seed_creation_date

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "seed_text": seed_text,
            }
        )
        if passthrough_data is not UNSET:
            field_dict["passthrough_data"] = passthrough_data
        if url is not UNSET:
            field_dict["url"] = url
        if seed_creation_date is not UNSET:
            field_dict["seed_creation_date"] = seed_creation_date

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.seed_passthrough_data import SeedPassthroughData

        d = dict(src_dict)
        seed_text = d.pop("seed_text")

        _passthrough_data = d.pop("passthrough_data", UNSET)
        passthrough_data: SeedPassthroughData | Unset
        if isinstance(_passthrough_data, Unset):
            passthrough_data = UNSET
        else:
            passthrough_data = SeedPassthroughData.from_dict(_passthrough_data)

        def _parse_url(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        url = _parse_url(d.pop("url", UNSET))

        def _parse_seed_creation_date(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                seed_creation_date_type_0 = isoparse(data)

                return seed_creation_date_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        seed_creation_date = _parse_seed_creation_date(d.pop("seed_creation_date", UNSET))

        seed = cls(
            seed_text=seed_text,
            passthrough_data=passthrough_data,
            url=url,
            seed_creation_date=seed_creation_date,
        )

        seed.additional_properties = d
        return seed

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
