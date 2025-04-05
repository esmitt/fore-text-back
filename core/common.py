from dataclasses import dataclass
from typing import List

@dataclass
class RGBAColor:
    r: int = 0
    g: int = 0
    b: int = 0
    a: int = 255

    def to_tuple(self):
        return self.r, self.g, self.b, self.a

@dataclass
class Position:
    x: int = 0
    y: int = 0

    def to_tuple(self):
        return self.x, self.y

def get_list_extensions(extensions_str: str) -> List[str]:
    return [item.strip() for item in extensions_str.split(',')]
