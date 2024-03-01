"""awesome-llama's scratch-object-format."""

from __future__ import annotations
from typing import Mapping, Sequence, TypeAlias

Value: TypeAlias = str | Sequence["Value"] | Mapping[str, "Value"]

__all__ = ["Value"]
