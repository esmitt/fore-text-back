from PIL import Image, ImageDraw, ImageFont
import numpy as np
import cv2
import os
from PIL.ImageFont import FreeTypeFont

from common.logger import logger
from common.utils import RGBAColor, Position, Size, tuple_to_size, HorizontalAlignment, VerticalAlignment
from core.fonts import Fonts
from typing import Optional, List

class TextFT:
    def __init__(self, text: str = "Sample",
                 font_size: int = None,
                 position: Position = Position(0, 0),
                 font_color: RGBAColor = RGBAColor(128, 128, 128),
                 h_align: HorizontalAlignment = HorizontalAlignment.CENTER,
                 v_align: VerticalAlignment = VerticalAlignment.CENTER):
        try:
            self._font_engine = Fonts()
        except Exception as exc:
            logger.error(f"The fonts raised exception in class TextFT: {exc}")
            raise ValueError("Not possible to create the object font engine") from exc
        self._text: str = text
        self._font_size: int = font_size if font_size else int(os.environ.get("DEFAULT_FONT_SIZE", "100"))
        logger.debug(f"Initializing TextFT with font size: {self._font_size}")
        self._current_font: Optional[FreeTypeFont] = self._load_font(None)
        if self._current_font is None:
            logger.error("Not possible to load a font")
            raise ValueError("No font loaded")
        self._position: Position = position
        self._font_color: RGBAColor = font_color
        self._h_align: HorizontalAlignment = h_align
        self._v_align: VerticalAlignment = v_align

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
        font_path: Optional[str]
        if font_name is None:
            font_name_list: list[str] = self._font_engine.get_fonts()
            if not font_name_list:
                logger.error("No fonts available to load", exc_info=True)
                raise ValueError("No fonts available to load")
            # choose the first one in the list
            font_name = font_name_list[0]
            logger.info(f"No font specified, selecting the first available: {font_name}")
        else:
            # if a font name is provided, use it
            logger.info(f"Load requested font: {font_name}")

        font_path = self._font_engine.get_font(font_name)
        try:
            return self._load_true_font(font_name, font_path)
        except RuntimeError as e:
            logger.warning(f"Failed to load font '{font_name}'. Attempting fallback font.")
            fallback_fonts = [f for f in self._font_engine.get_fonts() if f != font_name]
            for fallback in fallback_fonts:
                font_path = self._font_engine.get_font(fallback)
                try:
                    return self._load_true_font(fallback, font_path)
                except RuntimeError:
                    continue
            logger.error("All font loading attempts failed.")
            return None

    def _load_true_font(self, font_name: str, font_path: str) -> Optional[FreeTypeFont]:
        font_loaded: Optional[FreeTypeFont]
        try:
            font_loaded = ImageFont.truetype(font_path, self._font_size)
            logger.debug(f"Font {font_loaded.getname()} loaded correctly")
        except IOError as io_exc:
            logger.error(f"IOError loading font file '{font_path}': {io_exc}. The font couldn't be changed.")
            raise RuntimeError(f"Not possible to load the font {font_name}") from io_exc
        except Exception as exc:
            logger.error(f"Unexpected error loading font '{font_path}': {exc}", exc_info=True)
            raise RuntimeError(f"Failed to load font '{font_name}' due to an unexpected error.") from exc
        return font_loaded

    def set_text(self, value: str) -> None:
        self._text = value

    def get_available_fonts(self) -> List[str]:
        return self._font_engine.get_fonts()

    def get_position(self) -> Position:
        return self._position

    def is_position_zero(self) -> bool:
        logger.debug(f"Checking if position is zero: ({self._position.x}, {self._position.y})")
        return self._position.x == 0 and self._position.y == 0

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
        if self._current_font:
            self._current_font = self._load_font(self._current_font.getname()[0])
        else:
            self._current_font = self._load_font(None)
        # self._current_font = self._load_font(self._current_font.getname() if self._current_font else None)

    @property
    def font_color(self):
        return self._font_color

    @font_color.setter
    def font_color(self, color: RGBAColor):
        self._font_color = color

    @property
    def h_align(self):
        return self._h_align

    @h_align.setter
    def h_align(self, value: HorizontalAlignment):
        logger.debug(f"Setting h_align to {value.value}")
        self._h_align = value

    @property
    def v_align(self):
        return self._v_align

    @v_align.setter
    def v_align(self, value: VerticalAlignment):
        self._v_align = value

    def set_position(self, position: Position):
        logger.debug(f"Setting text position to ({position.x}, {position.y})")
        self._position = position

    def get_text_size(self) -> Size:
        """Calculate the width and height of the text."""
        if not self._current_font:
            logger.error("There are not font loaded, not possible to calculate size")
            return Size()
        try:
            bbox = self._current_font.getbbox(self._text)
            text_width = int(bbox[2] - bbox[0])
            text_height = int(bbox[3] - bbox[1])
            return Size(text_width, text_height)
        except Exception as exc:
            logger.error(f"Error computing the text size: {exc}")
            return Size()

    def compute_auto_position(self, background_image: np.ndarray, mask_3d: Optional[np.ndarray] = None):
        if not isinstance(background_image, np.ndarray):
            logger.warning("Not possible to compute auto position due to the background image")
            return

        # shape[:2] gives (height, width), so swap to (width, height)
        dim_image: Size = tuple_to_size((background_image.shape[1], background_image.shape[0]))
        logger.debug(f"Image dimensions: ({dim_image.x}, {dim_image.y})")

        dim_text = self.get_text_size()
        logger.debug(f"Initial text size: ({dim_text.x}, {dim_text.y}), font size: {self._font_size}, alignment: {self._h_align.value}-{self._v_align.value}")

        # Reduce font size until text fits within bounds after positioning
        min_font_size = 20
        max_attempts = 10
        attempt = 0

        while attempt < max_attempts and self._font_size > min_font_size:
            dim_text = self.get_text_size()
            if dim_text.x <= 0 or dim_text.y <= 0:
                logger.error("Text size is invalid")
                self._position = Position(0, 0)
                return

            # Calculate tentative position based on alignment
            if self._h_align == HorizontalAlignment.LEFT:
                pos_x = 0
            elif self._h_align == HorizontalAlignment.RIGHT:
                pos_x = dim_image.x - dim_text.x
            else:  # CENTER
                pos_x = (dim_image.x - dim_text.x) // 2

            if self._v_align == VerticalAlignment.UP:
                pos_y = 0
            elif self._v_align == VerticalAlignment.BOTTOM:
                pos_y = dim_image.y - dim_text.y
            else:  # CENTER
                pos_y = (dim_image.y - dim_text.y) // 2

            # Check if text fits within image bounds
            fits_bounds = (pos_x >= 0 and pos_y >= 0 and
                           pos_x + dim_text.x <= dim_image.x and
                           pos_y + dim_text.y <= dim_image.y)
            logger.debug(f"Attempt {attempt}: Position ({pos_x}, {pos_y}), Text size ({dim_text.x}, {dim_text.y}), Fits bounds: {fits_bounds}")

            if fits_bounds:
                break

            # Reduce font size if text doesn't fit
            self._font_size = max(min_font_size, self._font_size // 2)
            self._current_font = self._load_font(self._current_font.getname()[0])
            attempt += 1
            logger.debug(f"Font size adjustment attempt {attempt}: size={self._font_size}, text size ({dim_text.x}, {dim_text.y})")

        if dim_text.x <= 0 or dim_text.y <= 0:
            logger.error("Text size is invalid after adjustment")
            self._position = Position(0, 0)
            return

        # Recalculate position with final text size
        if self._h_align == HorizontalAlignment.LEFT:
            pos_x = 0
        elif self._h_align == HorizontalAlignment.RIGHT:
            pos_x = dim_image.x - dim_text.x
        else:  # CENTER
            pos_x = (dim_image.x - dim_text.x) // 2

        if self._v_align == VerticalAlignment.UP:
            pos_y = 0
        elif self._v_align == VerticalAlignment.BOTTOM:
            pos_y = dim_image.y - dim_text.y
        else:  # CENTER
            pos_y = (dim_image.y - dim_text.y) // 2

        # Clamp position to ensure text stays within bounds
        pos_x = max(0, min(pos_x, dim_image.x - dim_text.x))
        pos_y = max(0, min(pos_y, dim_image.y - dim_text.y))

        self._position = Position(pos_x, pos_y)
        logger.debug(f"Auto-positioned text at ({pos_x}, {pos_y}) with alignment {self._h_align.value}-{self._v_align.value}, text size ({dim_text.x}, {dim_text.y})")

    def render(self, background_image: np.ndarray) -> Optional[np.ndarray]:
        try:
            # Ensure input is valid BGR numpy array
            if not isinstance(background_image, np.ndarray) or background_image.ndim != 3:
                logger.error("Render: Invalid background image input.")
                return None

            # Convert to RGBA for text rendering
            image_pil = Image.fromarray(cv2.cvtColor(background_image, cv2.COLOR_BGR2RGBA))
            if image_pil.mode != 'RGBA':
                image_pil = image_pil.convert('RGBA')

            # Ensure font is loaded
            if not self._current_font:
                logger.error("Render: Font not loaded.")
                return None

            try:
                # Get text bounding box with anchor='lt' for top-left positioning
                bbox = self._current_font.getbbox(self._text, anchor='lt')
                logger.debug(f"Font getbbox: {bbox}")
                text_width = bbox[2] - bbox[0]
                text_height = bbox[3] - bbox[1]
                if text_width <= 0 or text_height <= 0:
                    logger.error(f"Invalid text dimensions: width={text_width}, height={text_height}")
                    return None
            except Exception as e:
                logger.error(f"Render: Error calculating text size: {e}")
                return None

            # Add padding to prevent clipping of ascenders/descenders
            padding = 20
            surface_width = text_width + 2 * padding
            surface_height = text_height + 2 * padding
            text_surface = Image.new(mode='RGBA', size=(surface_width, surface_height), color=(0, 0, 0, 0))
            text_draw = ImageDraw.Draw(text_surface)

            # Draw text at (padding, padding) to center it in the padded surface
            text_draw.text((padding, padding), self._text, font=self._current_font, fill=self._font_color.to_tuple(), anchor='lt')
            logger.debug(f"Text drawn on surface with color: {self._font_color.to_tuple()}")

            # Paste text surface onto main image, adjusting for bbox offset
            paste_x = self._position.x
            paste_y = self._position.y
            # Clamp to ensure text stays within image
            paste_x = max(0, min(paste_x, image_pil.width - text_width))
            paste_y = max(0, min(paste_y, image_pil.height - text_height))
            logger.debug(f"Pasting text at ({paste_x}, {paste_y}), text size ({text_width}, {text_height}), surface size ({surface_width}, {surface_height}), image size ({image_pil.width}, {image_pil.height})")

            image_pil.paste(text_surface, (paste_x, paste_y), text_surface)

            # Convert back to OpenCV BGR
            image_cv = cv2.cvtColor(np.array(image_pil), cv2.COLOR_RGBA2BGR)
            logger.debug(f"Rendered image shape: {image_cv.shape}")

            return image_cv

        except Exception as exc:
            logger.error(f"Error rendering text: {exc}", exc_info=True)
            return None