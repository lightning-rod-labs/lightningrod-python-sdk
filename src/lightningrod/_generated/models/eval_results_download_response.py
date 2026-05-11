from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.eval_results_download_response_results import EvalResultsDownloadResponseResults


T = TypeVar("T", bound="EvalResultsDownloadResponse")


@_attrs_define
class EvalResultsDownloadResponse:
    """
    Attributes:
        results (EvalResultsDownloadResponseResults):
    """

    results: EvalResultsDownloadResponseResults
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        results = self.results.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "results": results,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.eval_results_download_response_results import EvalResultsDownloadResponseResults

        d = dict(src_dict)
        results = EvalResultsDownloadResponseResults.from_dict(d.pop("results"))

        eval_results_download_response = cls(
            results=results,
        )

        eval_results_download_response.additional_properties = d
        return eval_results_download_response

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
