from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.preview_sample import PreviewSample


T = TypeVar("T", bound="PreviewResults")


@_attrs_define
class PreviewResults:
    """Results from a preview run.

    Attributes:
        job_id (str): ID of the preview job
        status (str): Status of the preview (completed, failed, etc.)
        output_dataset_id (None | str | Unset): ID of output dataset
        total_samples (int | Unset): Total number of samples generated Default: 0.
        samples (list[PreviewSample] | Unset): Sample results
        notes (list[str] | None | Unset): Notes or warnings about the preview
    """

    job_id: str
    status: str
    output_dataset_id: None | str | Unset = UNSET
    total_samples: int | Unset = 0
    samples: list[PreviewSample] | Unset = UNSET
    notes: list[str] | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        job_id = self.job_id

        status = self.status

        output_dataset_id: None | str | Unset
        if isinstance(self.output_dataset_id, Unset):
            output_dataset_id = UNSET
        else:
            output_dataset_id = self.output_dataset_id

        total_samples = self.total_samples

        samples: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.samples, Unset):
            samples = []
            for samples_item_data in self.samples:
                samples_item = samples_item_data.to_dict()
                samples.append(samples_item)

        notes: list[str] | None | Unset
        if isinstance(self.notes, Unset):
            notes = UNSET
        elif isinstance(self.notes, list):
            notes = self.notes

        else:
            notes = self.notes

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "job_id": job_id,
                "status": status,
            }
        )
        if output_dataset_id is not UNSET:
            field_dict["output_dataset_id"] = output_dataset_id
        if total_samples is not UNSET:
            field_dict["total_samples"] = total_samples
        if samples is not UNSET:
            field_dict["samples"] = samples
        if notes is not UNSET:
            field_dict["notes"] = notes

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.preview_sample import PreviewSample

        d = dict(src_dict)
        job_id = d.pop("job_id")

        status = d.pop("status")

        def _parse_output_dataset_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        output_dataset_id = _parse_output_dataset_id(d.pop("output_dataset_id", UNSET))

        total_samples = d.pop("total_samples", UNSET)

        _samples = d.pop("samples", UNSET)
        samples: list[PreviewSample] | Unset = UNSET
        if _samples is not UNSET:
            samples = []
            for samples_item_data in _samples:
                samples_item = PreviewSample.from_dict(samples_item_data)

                samples.append(samples_item)

        def _parse_notes(data: object) -> list[str] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                notes_type_0 = cast(list[str], data)

                return notes_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[str] | None | Unset, data)

        notes = _parse_notes(d.pop("notes", UNSET))

        preview_results = cls(
            job_id=job_id,
            status=status,
            output_dataset_id=output_dataset_id,
            total_samples=total_samples,
            samples=samples,
            notes=notes,
        )

        preview_results.additional_properties = d
        return preview_results

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
