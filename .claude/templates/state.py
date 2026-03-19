"""
Shared utilities for Lightningrod projects.
Auto-copied by project setup — do not modify.
"""
import json
import os
from typing import Optional

from lightningrod import LightningRod

STATE_FILE = "state.json"


def get_client() -> LightningRod:
    """Return an initialized LightningRod client."""
    api_key = os.environ.get("LIGHTNINGROD_API_KEY")
    if not api_key:
        raise EnvironmentError(
            "LIGHTNINGROD_API_KEY environment variable is not set."
        )
    return LightningRod(api_key=api_key)


class State:
    """
    Typed project state. All field accesses raise if the value hasn't been set yet.
    Use `is_set(field)` to check presence without raising (e.g. for optional fields
    like `input_dataset_id`, which is None for news/GDELT seeds).
    """

    def __init__(
        self,
        input_dataset_id: Optional[str] = None,
        dataset_id: Optional[str] = None,
        model_id: Optional[str] = None,
    ):
        self._input_dataset_id = input_dataset_id
        self._dataset_id = dataset_id
        self._model_id = model_id

    def _require(self, name: str) -> str:
        value = getattr(self, f"_{name}")
        if value is None:
            raise RuntimeError(
                f"State field '{name}' is not set. "
                f"Make sure the previous pipeline step has been run successfully.\n"
                f"Current state: {self._as_dict()}"
            )
        return value

    # --- fields ---

    @property
    def input_dataset_id(self) -> Optional[str]:
        return self._input_dataset_id

    @input_dataset_id.setter
    def input_dataset_id(self, value: Optional[str]) -> None:
        self._input_dataset_id = value

    @property
    def dataset_id(self) -> str:
        return self._require("dataset_id")

    @dataset_id.setter
    def dataset_id(self, value: Optional[str]) -> None:
        self._dataset_id = value

    @property
    def model_id(self) -> str:
        return self._require("model_id")

    @model_id.setter
    def model_id(self, value: Optional[str]) -> None:
        self._model_id = value

    # --- persistence ---

    def _as_dict(self) -> dict:
        return {
            "input_dataset_id": self._input_dataset_id,
            "dataset_id": self._dataset_id,
            "model_id": self._model_id,
        }

    @classmethod
    def load(cls) -> "State":
        if not os.path.exists(STATE_FILE):
            raise FileNotFoundError(
                f"{STATE_FILE} not found. Run `python setup.py` to initialize this project."
            )
        with open(STATE_FILE) as f:
            return cls(**json.load(f))

    def save(self) -> None:
        with open(STATE_FILE, "w") as f:
            json.dump(self._as_dict(), f, indent=2)
        print(f"  state.json updated: {self._as_dict()}")
