from PIL import Image, ImageDraw, ImageFont
import numpy as np
import cv2
from PIL.ImageFont import FreeTypeFont

from core.logger import logger
from core.common import RGBAColor, Position
from core.fonts import Fonts
from typing import Optional, List

class TextFT:
    def __init__(self, text: str = "Sample",
                 font_size: int = 100,
                 position: Position = Position(0, 0),
                 font_color: RGBAColor = RGBAColor(128, 128, 128)):
        try:
            self._font_engine = Fonts()
        except Exception as exc:
            logger.error(f"The fonts raised exception in class TextTTF: {exc}")
            raise ValueError("Not possible to create the object font engine") from exc

        self._text:str = text
        # this should be before the load_font
        self._font_size: int = font_size
        self._current_font: Optional[FreeTypeFont] = self._load_font(None)
        self._position:Position = position
        self._font_color: RGBAColor = font_color

    def _load_font(self, font_name: Optional[str]) -> Optional[FreeTypeFont]:
        """
        Loads a font for text rendering.

        Args:
            font_name: The name of the font to load. If None, the first available font
                       from the font engine is used.

        Raises:
            ValueError: If no fonts are available and font_name is None.
            RuntimeError: If an unexpected error occurs during font loading.
        """
        font_to_load: Optional[str]
        font_path: Optional[str]

        if font_name is None:
            font_name_list: list[str] = self._font_engine.get_fonts()
            if not font_name_list:
                logger.debug(f"The variable font_types_list is empty")
                raise ValueError("No fonts available to load")
            # choose the first one in the list
            font_to_load = font_name_list[0]
            logger.info(f"No font specified, selecting the first available: {font_to_load}")
            font_path = self._font_engine.get_font(font_to_load)
        else:
            # if a font name is provided, use it
            font_to_load = font_name
            logger.info(f"Load requested font: {font_to_load}")
            font_path = self._font_engine.get_font(font_name)

        return self._load_true_font(font_name, font_path)

    def _load_true_font(self, font_name: str, font_path: str) -> Optional[FreeTypeFont]:
        font_loaded: Optional[FreeTypeFont]
        try:
            font_loaded = ImageFont.truetype(font_path, self._font_size)
            logger.debug(f"Font {font_loaded.getname()} loaded correctly")
        except IOError as io_exc:
            logger.error(f"Error loading font file '{font_path}': {io_exc}. The font couldn't be changed.")
            raise RuntimeError(f"Not possible to load the font {font_name}") from io_exc
        except Exception as exc:
            logger.error(f"An unexpected error occurred during font loading for '{font_path}': {exc}")
            raise RuntimeError(f"Failed to load font '{font_path}' due to an unexpected error. The font couldn't be changed.") from exc
        return font_loaded

    def set_text(self, value: str) -> None:
        self._text = value

    def get_available_fonts(self) -> List[str]:
        return self._font_engine.get_fonts()

    # def set_font(self, font_name: str) -> None:
    #     font_path: str = self._font_engine.get_font(font_name)
    #     self._current_font = self._load_true_font(font_name, font_path)

    @property
    def font_type(self) -> FreeTypeFont:
        return self._current_font

    @font_type.setter
    def font_type(self, value: str) -> None:
        try:
            self._current_font = self._load_font(value)
        except Exception as exc:
            logger.error(f"Font {value} isn't valid: {exc}")

    @property
    def font_size(self):
        return self._font_size

    @font_size.setter
    def font_size(self, value: int):
        self._font_size = value
        self._load_font(None)

    @property
    def font_color(self):
        return self._font_color

    @font_color.setter
    def font_color(self, color: RGBAColor):
        self._font_color = color

    def set_position(self, position: Position):
        self._position = position

    def render(self, background_image: np.ndarray) -> np.ndarray:
        try:
            image_pil = Image.fromarray(cv2.cvtColor(background_image, cv2.COLOR_BGR2RGB))
            draw = ImageDraw.Draw(image_pil)

            draw.text(xy=self._position.to_tuple(), text=self._text, font=self._current_font, fill=self._font_color.to_tuple())

            image_cv = cv2.cvtColor(np.array(image_pil), cv2.COLOR_RGB2BGR)
            return image_cv
        except Exception as exc:
            logger.error(f"Error rendering text: {exc}")
            return background_image # return the original image