"""scratch-object-format version 1 encoder."""

from __future__ import annotations
from typing import TYPE_CHECKING, Mapping, Sequence
from unittest import TestCase

if TYPE_CHECKING:
    from . import Value


__all__ = ["encode"]


class Encoder:
    def __init__(self, optimize: bool = False) -> None:
        self.optimize = optimize
        self.data: list[str] = []

    def encode(self, value: Value) -> str:
        pointer = len(self.data)
        if isinstance(value, str):
            self.encode_value(value)
        elif isinstance(value, Mapping):
            if self.optimize and all(isinstance(item, str) for item in value.values()):
                self.encode_dict_of_values(value)  # pyright: ignore[reportArgumentType]
            else:
                self.encode_dict(value)
        elif self.optimize and all(isinstance(item, str) for item in value):
            self.encode_array_of_values(value)  # pyright: ignore[reportArgumentType]
        else:
            self.encode_array(value)
        return str(1 + pointer)

    def encode_value(self, value: str) -> None:
        self.data.append("V")
        self.data.append(value)

    def encode_array(self, value: Sequence[Value]) -> None:
        self.data.append("A")
        self.data.append(str(len(value)))
        referenced: dict[int, int] = {}
        for i, item in enumerate(value):
            if isinstance(item, str):
                self.encode_value(item)
            else:
                self.data.append("P")
                referenced[i] = len(self.data)
                self.data.append("")
        for i, index in referenced.items():
            pointer = self.encode(value[i])
            self.data[index] = str(pointer)

    def encode_dict(self, value: Mapping[str, Value]) -> None:
        self.data.append("D")
        self.data.append(str(len(value)))
        referenced: dict[str, int] = {}
        for key, item in value.items():
            self.data.append(key)
            if isinstance(item, str):
                self.encode_value(item)
            else:
                self.data.append("P")
                referenced[key] = len(self.data)
                self.data.append("")
        for i, index in referenced.items():
            pointer = self.encode(value[i])
            self.data[index] = str(pointer)

    def encode_array_of_values(self, value: Sequence[str]) -> None:
        self.data.append("AV")
        self.data.append(str(len(value)))
        for item in value:
            self.data.append(item)

    def encode_dict_of_values(self, value: Mapping[str, str]) -> None:
        self.data.append("DV")
        self.data.append(str(len(value)))
        for key in value:
            self.data.append(key)
            self.data.append(value[key])


def encode(value: Value, optimize: bool = False) -> list[str]:
    """Encode a value into scratch-object-format version 1.

    Args:
    ----
    value: The value to encode.
    optimize: If True, the encoder will use the array of values and dict of values
    types.

    """
    encoder = Encoder(optimize=optimize)
    encoder.encode(value)
    return encoder.data


class TestEncode(TestCase):
    def test(self) -> None:
        self.assertEqual(
            encode(
                {
                    "id": "1882674",
                    "username": "griffpatch",
                    "scratchteam": "False",
                    "history": {
                        "joined": "2012-10-24T12:59:31.000Z",
                    },
                    "profile": {
                        "id": "1267661",
                        "images": {
                            "90x90": "https://cdn2.scratch.mit.edu/get_image/user/1882674_90x90.png?v=",
                            "60x60": "https://cdn2.scratch.mit.edu/get_image/user/1882674_60x60.png?v=",
                            "55x55": "https://cdn2.scratch.mit.edu/get_image/user/1882674_55x55.png?v=",
                            "50x50": "https://cdn2.scratch.mit.edu/get_image/user/1882674_50x50.png?v=",
                            "32x32": "https://cdn2.scratch.mit.edu/get_image/user/1882674_32x32.png?v=",
                        },
                        "status": "YouTube Tutorials - Subscribe!  www.youtube.com/griffpatch Only 2 accounts: griffpatch + griffpatch_tutor [Sorry no F4F, and limit of 1 Ad per day]",
                        "bio": "Got hooked on coding when I was a kid, now I'm a parent and nothing's changed! My day job involves java coding. In my spare time I love making games, being creative & drumming in church.",
                        "country": "United Kingdom",
                    },
                },
            ),
            [
                "D",
                "5",
                "id",
                "V",
                "1882674",
                "username",
                "V",
                "griffpatch",
                "scratchteam",
                "V",
                "False",
                "history",
                "P",
                "18",
                "profile",
                "P",
                "27",
                "DV",
                "1",
                "joined",
                "2012-10-24T12:59:31.000Z",
                "D",
                "1",
                "joined",
                "V",
                "2012-10-24T12:59:31.000Z",
                "D",
                "5",
                "id",
                "V",
                "1267661",
                "images",
                "P",
                "44",
                "status",
                "V",
                "YouTube Tutorials - Subscribe!  www.youtube.com/griffpatch Only 2 accounts: griffpatch + griffpatch_tutor [Sorry no F4F, and limit of 1 Ad per day]",
                "bio",
                "V",
                "Got hooked on coding when I was a kid, now I'm a parent and nothing's changed! My day job involves java coding. In my spare time I love making games, being creative & drumming in church.",
                "country",
                "V",
                "United Kingdom",
                "DV",
                "5",
                "90x90",
                "https://cdn2.scratch.mit.edu/get_image/user/1882674_90x90.png?v=",
                "60x60",
                "https://cdn2.scratch.mit.edu/get_image/user/1882674_60x60.png?v=",
                "55x55",
                "https://cdn2.scratch.mit.edu/get_image/user/1882674_55x55.png?v=",
                "50x50",
                "https://cdn2.scratch.mit.edu/get_image/user/1882674_50x50.png?v=",
                "32x32",
                "https://cdn2.scratch.mit.edu/get_image/user/1882674_32x32.png?v=",
                "D",
                "5",
                "90x90",
                "V",
                "https://cdn2.scratch.mit.edu/get_image/user/1882674_90x90.png?v=",
                "60x60",
                "V",
                "https://cdn2.scratch.mit.edu/get_image/user/1882674_60x60.png?v=",
                "55x55",
                "V",
                "https://cdn2.scratch.mit.edu/get_image/user/1882674_55x55.png?v=",
                "50x50",
                "V",
                "https://cdn2.scratch.mit.edu/get_image/user/1882674_50x50.png?v=",
                "32x32",
                "V",
                "https://cdn2.scratch.mit.edu/get_image/user/1882674_32x32.png?v=",
            ],
        )
