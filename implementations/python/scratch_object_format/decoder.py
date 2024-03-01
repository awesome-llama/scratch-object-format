"""scratch-object-format version 1 decoder."""

from __future__ import annotations
from typing import TYPE_CHECKING, Sequence
from unittest import TestCase

if TYPE_CHECKING:
    from . import Value


__all__ = ["decode"]


class Decoder:
    def __init__(self, data: Sequence[str]) -> None:
        self.data = data
        self.index = 0

    def decode(self) -> Value:
        kind = self.data[self.index]
        self.index += 1
        if kind == "V":
            return self.decode_value()
        if kind == "A":
            return self.decode_array()
        if kind == "D":
            return self.decode_dict()
        if kind == "AV":
            return self.decode_array_of_values()
        if kind == "DV":
            return self.decode_dict_of_values()
        msg = f"Unknown kind: {kind}"
        raise ValueError(msg)

    def decode_value(self) -> str:
        value = self.data[self.index]
        self.index += 1
        return value

    def decode_array(self) -> list[Value]:
        length = int(self.data[self.index])
        self.index += 1
        items: list[Value] = []
        for _ in range(length):
            kind = self.data[self.index]
            self.index += 1
            if kind == "P":
                index = self.index + 1
                self.index = int(self.data[self.index]) - 1
                items.append(self.decode())
                self.index = index
            else:
                items.append(self.decode_value())
        return items

    def decode_dict(self) -> dict[str, Value]:
        length = int(self.data[self.index])
        self.index += 1
        items: dict[str, Value] = {}
        for _ in range(length):
            key = self.data[self.index]
            self.index += 1
            kind = self.data[self.index]
            self.index += 1
            if kind == "P":
                index = self.index + 1
                self.index = int(self.data[self.index]) - 1
                items[key] = self.decode()
                self.index = index
            else:
                items[key] = self.decode_value()
        return items

    def decode_array_of_values(self) -> list[Value]:
        length = int(self.data[self.index])
        self.index += 1
        return [self.decode_value() for _ in range(length)]

    def decode_dict_of_values(self) -> dict[str, Value]:
        length = int(self.data[self.index])
        self.index += 1
        items: dict[str, Value] = {}
        for _ in range(length):
            key = self.data[self.index]
            self.index += 1
            items[key] = self.decode_value()
        return items


def decode(data: Sequence[str]) -> Value:
    """Decode data in scratch-object-format version 1."""
    decoder = Decoder(data)
    return decoder.decode()


class TestDecode(TestCase):
    def test(self) -> None:
        self.assertEqual(
            decode(
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
            ),
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
        )
