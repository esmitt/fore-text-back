from core.interfaces.background import BackgroundInterface
from core.interfaces.image_loader import ImageLoaderInterface
from core.interfaces.foreground import ForegroundInterface
from core.text import TextFT
from core.logger import logger
from typing import Optional
import cv2
import numpy as np

class Composer:
    def __init__(self, image_loader: ImageLoaderInterface, foreground: ForegroundInterface, background: BackgroundInterface, text: Optional[TextFT] = None):
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
    def show_image(image: np.ndarray, max_size:tuple =(800, 600)):
        height, width = image.shape[:2]
        max_width, max_height = max_size

        aspect_ratio = width / height
        window_name = "output"

        if width > max_width or height > max_height:
            # Resize the image while maintaining aspect ratio
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

    def set_text(self, text: TextFT):
        self._text = text
        self._composing()

    def _processing(self) -> bool:
        try:
            if not self._image_loader.load():
                logger.error("Cannot be run due the loader")
                return False

            if not self._foreground.extract(image=self._image_loader.get_source(), threshold=0.95):
                logger.error("Cannot be run due the foreground extractor")
            # self.show_image(self._foreground.get_foreground())

            if not self._background.extract(image=self._image_loader.get_source().copy()):
                logger.error("Cannot be run due the background extractor")
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

            shape = background_img.shape
            self._output = np.zeros(shape, dtype=background_img.dtype) # match dtype
            background_output = background_img.copy()

            if self._text is not None:
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

            self._output = np.where(mask_3d == 255, foreground_img, image_with_text)
            logger.debug(f"Composer: Composition successful. Output shape: {self._output.shape}, dtype: {self._output.dtype}")
        except Exception as exc:
            logger.error(f"Composer: Unexpected error during composing: {exc}", exc_info=True) # Log traceback
            self._output = None

    def get_output(self) -> Optional[np.ndarray]:
        if self._output is not None:
            return self._output
        logger.warning("Composer.get_output: Output is None.")
        return None