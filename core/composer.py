from core.interfaces.background import BackgroundInterface
from core.interfaces.image_loader import ImageLoaderInterface
from core.interfaces.foreground import ForegroundInterface
from core.text import TextTTF
from core.logger import logger
from typing import Optional
import cv2
import numpy as np

class Composer:
    def __init__(self, image_loader: ImageLoaderInterface, foreground: ForegroundInterface, background: BackgroundInterface, text: Optional[TextTTF] = None):
        self._image_loader: ImageLoaderInterface = image_loader
        self._foreground: ForegroundInterface = foreground
        self._background: BackgroundInterface = background
        self._text: TextTTF = text
        self._processed = self._processing()
        self._output = None
        self._composing()

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

            resized_image = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_AREA)
            cv2.imshow(window_name, resized_image)
        else:
            cv2.imshow(window_name, image)

        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def set_text(self, text: TextTTF):
        self._text = text
        self._composing()

    def _processing(self) -> bool:
        try:
            if not self._image_loader.load():
                logger.error("Cannot be run due the loader")
                return False

            if not self._foreground.extract(image=self._image_loader.get_source(), threshold=0.95):
                logger.error("Cannot be run due the foreground extractor")
            self.show_image(self._foreground.get_foreground())

            if not self._background.extract(image=self._image_loader.get_source().copy()):
                logger.error("Cannot be run due the background extractor")
            self.show_image(self._background.get_background())
        except ValueError:
            return False
        return True

    def _composing(self):
        shape = self._background.get_background().shape
        self._output = np.zeros(shape)
        background_output = self._background.get_background().copy()
        image_with_text = self._text.render(background_output)
        # image_with_text = cv2.putText(background_output,
        #                               self._text.get_text(),
        #                               (150, 600),
        #                               cv2.FONT_HERSHEY_SIMPLEX,
        #                               9,
        #                               (10, 25, 255),
        #                               9,
        #                               cv2.LINE_AA)


        self._output = np.where(self._foreground.get_mask3d() == 255,
                                self._foreground.get_foreground(),
                                image_with_text)

    def get_output(self) -> np.ndarray:
        if self._output is not None:
            return self._output
        raise FileNotFoundError