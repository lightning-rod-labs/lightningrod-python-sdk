from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="DatasetLinterRunRequest")


@_attrs_define
class DatasetLinterRunRequest:
    """
    Attributes:
        rules (list[str] | None | Unset): Subset of rule names to run. Defaults to all registered rules.
        random_sample_size (int | None | Unset): How many randomly-selected samples to lint for probabilistic rules.
            Defaults to an internal constant.
    """

    rules: list[str] | None | Unset = UNSET
    random_sample_size: int | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        rules: list[str] | None | Unset
        if isinstance(self.rules, Unset):
            rules = UNSET
        elif isinstance(self.rules, list):
            rules = self.rules

        else:
            rules = self.rules

        random_sample_size: int | None | Unset
        if isinstance(self.random_sample_size, Unset):
            random_sample_size = UNSET
        else:
            random_sample_size = self.random_sample_size

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if rules is not UNSET:
            field_dict["rules"] = rules
        if random_sample_size is not UNSET:
            field_dict["random_sample_size"] = random_sample_size

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_rules(data: object) -> list[str] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                rules_type_0 = cast(list[str], data)

                return rules_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[str] | None | Unset, data)

        rules = _parse_rules(d.pop("rules", UNSET))

        def _parse_random_sample_size(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        random_sample_size = _parse_random_sample_size(d.pop("random_sample_size", UNSET))

        dataset_linter_run_request = cls(
            rules=rules,
            random_sample_size=random_sample_size,
        )

        dataset_linter_run_request.additional_properties = d
        return dataset_linter_run_request

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
