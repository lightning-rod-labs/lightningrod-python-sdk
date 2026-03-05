from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Literal, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.model_object_pricing import ModelObjectPricing


T = TypeVar("T", bound="ModelObject")


@_attrs_define
class ModelObject:
    """
    Attributes:
        id (str): The model identifier
        object_ (Literal['model'] | Unset): The object type Default: 'model'.
        created (int | Unset): Unix timestamp of when the model was created Default: 0.
        owned_by (str | Unset): The organization that owns the model Default: 'lightningrodlabs'.
        name (str | Unset): Display name of the model Default: ''.
        description (str | Unset): Description of the model Default: ''.
        context_length (int | Unset): Maximum context length in tokens Default: 0.
        max_completion_tokens (int | Unset): Maximum number of tokens to generate Default: 0.
        pricing (ModelObjectPricing | Unset): Per-token pricing
    """

    id: str
    object_: Literal["model"] | Unset = "model"
    created: int | Unset = 0
    owned_by: str | Unset = "lightningrodlabs"
    name: str | Unset = ""
    description: str | Unset = ""
    context_length: int | Unset = 0
    max_completion_tokens: int | Unset = 0
    pricing: ModelObjectPricing | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        object_ = self.object_

        created = self.created

        owned_by = self.owned_by

        name = self.name

        description = self.description

        context_length = self.context_length

        max_completion_tokens = self.max_completion_tokens

        pricing: dict[str, Any] | Unset = UNSET
        if not isinstance(self.pricing, Unset):
            pricing = self.pricing.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
            }
        )
        if object_ is not UNSET:
            field_dict["object"] = object_
        if created is not UNSET:
            field_dict["created"] = created
        if owned_by is not UNSET:
            field_dict["owned_by"] = owned_by
        if name is not UNSET:
            field_dict["name"] = name
        if description is not UNSET:
            field_dict["description"] = description
        if context_length is not UNSET:
            field_dict["context_length"] = context_length
        if max_completion_tokens is not UNSET:
            field_dict["max_completion_tokens"] = max_completion_tokens
        if pricing is not UNSET:
            field_dict["pricing"] = pricing

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.model_object_pricing import ModelObjectPricing

        d = dict(src_dict)
        id = d.pop("id")

        object_ = cast(Literal["model"] | Unset, d.pop("object", UNSET))
        if object_ != "model" and not isinstance(object_, Unset):
            raise ValueError(f"object must match const 'model', got '{object_}'")

        created = d.pop("created", UNSET)

        owned_by = d.pop("owned_by", UNSET)

        name = d.pop("name", UNSET)

        description = d.pop("description", UNSET)

        context_length = d.pop("context_length", UNSET)

        max_completion_tokens = d.pop("max_completion_tokens", UNSET)

        _pricing = d.pop("pricing", UNSET)
        pricing: ModelObjectPricing | Unset
        if isinstance(_pricing, Unset):
            pricing = UNSET
        else:
            pricing = ModelObjectPricing.from_dict(_pricing)

        model_object = cls(
            id=id,
            object_=object_,
            created=created,
            owned_by=owned_by,
            name=name,
            description=description,
            context_length=context_length,
            max_completion_tokens=max_completion_tokens,
            pricing=pricing,
        )

        model_object.additional_properties = d
        return model_object

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
