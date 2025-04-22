from core.interfaces.background import BackgroundInterface
from core.interfaces.image_loader import ImageLoaderInterface
from core.interfaces.foreground import ForegroundInterface
from core.text import TextFT
from common.logger import logger
from common.utils import Position
from typing import Optional
import cv2
import numpy as np

class Composer:
    def __init__(self,
                 image_loader: ImageLoaderInterface,
                 foreground: ForegroundInterface,
                 background: BackgroundInterface,
                 text: Optional[TextFT] = None):
        self._image_loader: ImageLoaderInterface = image_loader
        self._foreground: ForegroundInterface = foreground
        self._background: BackgroundInterface = background
        self._text: TextFT = text
        self._processed = self._processing()
        self._output = None
        if self._processed:
            self._composing()
        else:
            logger.error("Composer: Skipping composition due to processing errors.")


    @staticmethod
    def show_image(image: np.ndarray, max_size: tuple = (800, 600)):
        height, width = image.shape[:2]
        max_width, max_height = max_size
        aspect_ratio = width / height
        window_name = "output"

        if width > max_width or height > max_height:
            if aspect_ratio > 1:  # Image is wider than it is tall
                new_width = max_width
                new_height = int(max_width / aspect_ratio)
                if new_height > max_height:  # check if new_height exceeds max_height
                    new_height = max_height
                    new_width = int(max_height * aspect_ratio)
            else:  # Image is taller than it is wide or square
                new_height = max_height
                new_width = int(max_height * aspect_ratio)
                if new_width > max_width:  # check if new_width exceeds max_width
                    new_width = max_width
                    new_height = int(max_width / aspect_ratio)
            resized_image = cv2.resize(image, dsize=(new_width, new_height), interpolation=cv2.INTER_AREA)
            cv2.imshow(window_name, resized_image)
        else:
            cv2.imshow(window_name, image)

        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def set_text(self, text: TextFT) -> tuple[bool, Position]:
        self._text = text
        # Only reset position if it's zero or invalid
        if text.is_position_zero() or not self.check_text_bounds():
            logger.debug(f"Resetting position: is_zero={text.is_position_zero()}, bounds_valid={self.check_text_bounds()}")
            self._text.set_position(Position(0, 0))
        self._composing()
        if self._output is None:
            # If composition failed, reset to original background
            self._output = self._background.get_background().copy() if self._background.get_background() is not None else None
            return False, Position(0, 0)
        return True, self._text.get_position()

    def check_text_bounds(self):
        """Check if the text fits within the image boundaries."""
        if self._text is None:
            logger.warning("No text provided for boundary check.")
            return True
        background_img = self._background.get_background()
        if background_img is None:
            logger.error("Cannot check bounds: background is None.")
            return False
        height, width = background_img.shape[:2]
        text_size = self._text.get_text_size()
        position = self._text.get_position()
        if (position.x < 0 or position.y < 0 or
            position.x + text_size.x > width or
            position.y + text_size.y > height):
            logger.error(f"Text out of bounds: Position ({position.x}, {position.y}), Size ({text_size.x}, {text_size.y}), Image ({width}, {height})")
            return False
        return True

    def _processing(self) -> bool:
        try:
            if not self._image_loader.load():
                logger.error("Cannot be run due the loader")
                return False

            if not self._foreground.extract(image=self._image_loader.get_source(), threshold=0.95):
                logger.error("Cannot be run due the foreground extractor")
                return False
            # self.show_image(self._foreground.get_foreground())

            if not self._background.extract(image=self._image_loader.get_source().copy()):
                logger.error("Cannot be run due the background extractor")
                return False
            # self.show_image(self._background.get_background())
        except ValueError:
            return False
        return True

    def _composing(self):
        try:
            background_img = self._background.get_background()
            if background_img is None:
                logger.error("Composer: Cannot compose, background is None.")
                self._output = None
                return
            if not isinstance(background_img, np.ndarray):
                logger.error(f"Composer: Background is not a NumPy array, type is {type(background_img)}")
                self._output = None
                return

            # Ensure background is in the correct format (BGR, 3 channels)
            if background_img.ndim != 3 or background_img.shape[2] != 3:
                logger.error(f"Composer: Background image has invalid shape {background_img.shape}")
                self._output = None
                return

            shape = background_img.shape
            self._output = np.zeros(shape, dtype=background_img.dtype) # match dtype
            background_output = background_img.copy()

            if self._text is not None:
                if self._text.is_position_zero():
                    self._text.compute_auto_position(background_img)
                if not self.check_text_bounds():
                    logger.error("Text position after auto-positioning is out of bounds")
                    self._output = None
                    return
                image_with_text = self._text.render(background_output)
                if image_with_text is None:
                    logger.error("Composer: Text rendering failed.")
                    self._output = None
                    return
                if not isinstance(image_with_text, np.ndarray):
                    logger.error(f"Composer: Text rendering returned non-array type: {type(image_with_text)}")
                    self._output = None
                    return
            else:
                logger.warning("Composer: No text object provided, composing without text.")
                image_with_text = background_output # Use original background if no text

            foreground_img = self._foreground.get_foreground()
            mask_3d = self._foreground.get_mask3d()

            if foreground_img is None or not isinstance(foreground_img, np.ndarray):
                logger.error(f"Composer: Invalid foreground image (None or type {type(foreground_img)}).")
                self._output = None
                return
            if mask_3d is None or not isinstance(mask_3d, np.ndarray):
                logger.error(f"Composer: Invalid foreground mask (None or type {type(mask_3d)}).")
                self._output = None
                return

            # Ensure shapes match
            if foreground_img.shape != background_img.shape:
                logger.error(f"Shape mismatch: Foreground {foreground_img.shape} vs Background {background_img.shape}")
                self._output = None
                return
            if mask_3d.shape != background_img.shape:
                logger.error(f"Shape mismatch: Mask {mask_3d.shape} vs Background {background_img.shape}")
                self._output = None
                return

            # Normalize mask to binary (0 or 255) for each channel
            mask_3d = (mask_3d > 128).astype(np.uint8) * 255

            # Ensure mask and images have the same dtype
            foreground_img = foreground_img.astype(background_img.dtype)
            image_with_text = image_with_text.astype(background_img.dtype)

            # Apply the mask to combine foreground and background with text
            self._output = np.where(mask_3d == 255, foreground_img, image_with_text)
            logger.debug(f"Composer: Composition successful. Output shape: {self._output.shape}, dtype: {self._output.dtype}")

        except Exception as exc:
            logger.error(f"Composer: Unexpected error during composing: {exc}", exc_info=True)
            self._output = None

    def get_output(self) -> tuple[Optional[np.ndarray], dict]:
        parameters = {}
        if self._text is not None:
            parameters = {
                "text": self._text._text,
                "font_size": self._text.font_size,
                "font_type": self._text.font_type.getname()[0] if self._text.font_type else None,
                "font_color": self._text.font_color.to_dict(),
                "h_align": self._text.h_align.value,
                "v_align": self._text.v_align.value,
                "position": (self._text.get_position().x, self._text.get_position().y)
            }
        if self._output is not None:
            return self._output, parameters
        logger.warning("Composer.get_output: Output is None.")
        return None, parameters