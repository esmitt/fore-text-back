from PIL import Image, ImageDraw, ImageFont
import os
import numpy as np
import cv2
from core.logger import logger

class TextTTF:
    def __init__(self, text: str):
        self._text = text
        self._path = os.path.join(os.getcwd(), 'fonts', 'BebasNeue-Regular.ttf')
        self._font_size = 100 # any default for now
        self._font = ImageFont.truetype(self._path, self._font_size)
        self._position:tuple[int, int] = (0, 0)
        self._font_color: tuple[int, int, int, int] = (128, 128, 128, 255)
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

    def set_position(self, x: int, y: int):
        self._position = (x, y)

    def set_font_color(self, color: tuple[int, int, int, int]):
        self._font_color = color

    def _update_font(self):
        try:
            self._font = ImageFont.truetype(self._path, self._font_size)
        except Exception as e:
            logger.error(f"Error updating font: {e}")

    def render(self, background_image: np.ndarray) -> np.ndarray:
        try:
            position = (150, 350)
            self._position = (0, 0)
            self._font_color = (229, 230, 245, 255)
            font_color = (229, 230, 245)

            image_pil = Image.fromarray(cv2.cvtColor(background_image, cv2.COLOR_BGR2RGB))
            draw = ImageDraw.Draw(image_pil)

            draw.text(position, self._text, font=self._font, fill=font_color)

            image_cv = cv2.cvtColor(np.array(image_pil), cv2.COLOR_RGB2BGR)
            return image_cv
        except Exception as e:
            logger.error(f"Error rendering text: {e}")
            return background_image # return the original image