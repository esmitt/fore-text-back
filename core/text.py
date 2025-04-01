from PIL import Image, ImageDraw, ImageFont
import os
import numpy as np
import cv2
from PIL.ImageFont import FreeTypeFont

from core.logger import logger
from core.common import RGBAColor, Position
from core.fonts import Fonts

class TextTTF:
    def __init__(self, text: str, font_size: int = 100, position: Position = Position(0, 0), font_color: RGBAColor = RGBAColor(128, 128, 128) ):
        try:
            self._font_type = Fonts()
        except FileNotFoundError as exc:
            logger.error(f"The fonts raised exception in class TextTTF: {exc}")
            raise FileNotFoundError
        self._text:str = text
        self._font_size: int = font_size

        # choose the first one in the list
        font_types_list: list = self._font_type.get_fonts()
        if len(font_types_list) == 0:
            logger.debug(f"The variable font_types_list is empty")
            raise ReferenceError
        font_name: str = font_types_list[0]
        logger.info(f"The font used is {font_name}")
        self._font: FreeTypeFont = ImageFont.truetype(self._font_type.get_font(font_name), self._font_size)

        self._position:Position = position
        self._font_color: RGBAColor = font_color
        # self._stroke_width = 0
        # self._stroke_color = (0, 0, 0, 255)
        # self._shadow_offset = (0, 0)
        # self._shadow_color = (100, 100, 100, 255) # RGBA
        # self._rotation = 0

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value: str):
        self._text = value

    @property
    def font_size(self):
        return self._font_size

    @font_size.setter
    def font_size(self, value: int):
        self._font_size = value
        self._update_font()

    def set_position(self, position: Position):
        self._position = position

    def set_font_color(self, color: RGBAColor):
        self._font_color = color

    def _update_font(self):
        try:
            self._font = ImageFont.truetype(self._path, self._font_size)
        except Exception as e:
            logger.error(f"Error updating font: {e}")

    def render(self, background_image: np.ndarray) -> np.ndarray:
        try:
            image_pil = Image.fromarray(cv2.cvtColor(background_image, cv2.COLOR_BGR2RGB))
            draw = ImageDraw.Draw(image_pil)

            draw.text(xy=self._position.to_tuple(), text=self._text, font=self._font, fill=self._font_color.to_tuple())

            image_cv = cv2.cvtColor(np.array(image_pil), cv2.COLOR_RGB2BGR)
            return image_cv
        except Exception as e:
            logger.error(f"Error rendering text: {e}")
            return background_image # return the original image