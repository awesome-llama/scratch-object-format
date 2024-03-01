"""Build examples."""

import sys
from typing import Any

sys.path.append("implementations/python")

import json
from pathlib import Path

from scratch_object_format.decoder import decode
from scratch_object_format.encoder import encode

path = Path.cwd() / "examples"


def stringify(data: Any) -> Any:
    if isinstance(data, list):
        return [stringify(item) for item in data]
    if isinstance(data, dict):
        return {key: stringify(value) for key, value in data.items()}
    return str(data)


for file in path.glob("*.json"):
    with open(file) as f:
        data = stringify(json.load(f))
    encoded = encode(data, optimize=True)
    (path / "encoded" / file.stem).with_suffix(".txt").write_text("\n".join(encoded))
    decoded = decode(encoded)
    (path / "decoded" / file.stem).with_suffix(".json").write_text(
        json.dumps(decoded, indent=4)
    )
    assert decoded == data
