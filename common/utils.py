from dataclasses import dataclass
from typing import List
from enum import Enum

@dataclass
class RGBAColor:
    r: int = 0
    g: int = 0
    b: int = 0
    a: int = 255

    def to_tuple(self):
        return self.r, self.g, self.b, self.a

    def to_dict(self):
        return {"r": self.r, "g": self.g, "b": self.b, "a":self.a}

@dataclass
class Position:
    x: int = 0
    y: int = 0

    def to_tuple(self):
        return self.x, self.y

    def __sub__(self, other):
        return Position(self.x - other.x, self.y - other.y)

    def __str__(self):
        return f"({self.x}, {self.y})"

    def __floordiv__(self, other):
        return Position(self.x//other, self.y//other)

Size = Position

def tuple_to_size(int_tuple: tuple[int, ...]) -> Size:
    if len(int_tuple) == 2:
        return Size(int_tuple[0], int_tuple[1])
    else:
        raise ValueError("Tuple must have two integers to create a Size.")

def get_list_extensions(extensions_str: str) -> List[str]:
    return [item.strip() for item in extensions_str.split(',')]

class HorizontalAlignment(Enum):
    LEFT = "left"
    CENTER = "center"
    RIGHT = "right"

class VerticalAlignment(Enum):
    UP = "up"
    CENTER = "center"
    BOTTOM = "bottom"