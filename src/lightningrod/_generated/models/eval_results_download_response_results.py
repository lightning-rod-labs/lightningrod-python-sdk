from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.eval_model_result_download import EvalModelResultDownload


T = TypeVar("T", bound="EvalResultsDownloadResponseResults")


@_attrs_define
class EvalResultsDownloadResponseResults:
    """ """

    additional_properties: dict[str, EvalModelResultDownload] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        field_dict: dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            field_dict[prop_name] = prop.to_dict()

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.eval_model_result_download import EvalModelResultDownload

        d = dict(src_dict)
        eval_results_download_response_results = cls()

        additional_properties = {}
        for prop_name, prop_dict in d.items():
            additional_property = EvalModelResultDownload.from_dict(prop_dict)

            additional_properties[prop_name] = additional_property

        eval_results_download_response_results.additional_properties = additional_properties
        return eval_results_download_response_results

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> EvalModelResultDownload:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: EvalModelResultDownload) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
