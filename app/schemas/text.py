from pydantic import BaseModel
from typing import Optional

class TextParameters(BaseModel):
    text: str
    font_size: Optional[int] = None
    position_x: Optional[int] = None
    position_y: Optional[int] = None
    font_color_r: Optional[int] = 128
    font_color_g: Optional[int] = 128
    font_color_b: Optional[int] = 128
    font_color_a: Optional[int] = 255
    font_name: Optional[str] = None