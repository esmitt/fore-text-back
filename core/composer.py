from matplotlib.pyplot import imshow

from core.interfaces.image_loader import ImageLoaderInterface
from core.interfaces.foreground import ForegroundInterface
from core.logger import logger
import cv2

class Composer:
    def __init__(self, image_loader: ImageLoaderInterface, foreground: ForegroundInterface):
        self._image_loader = image_loader
        self._foreground = foreground

    def run(self) -> bool:
        try:
            if not self._image_loader.load():
                logger.error("Cannot be run due the loader")
            if not self._foreground.extract(self._image_loader.get_source()):
                logger.error("Cannot be run due the foreground extractor")

            #     scale = 0.2
            #     # Get the new dimensions
            #     image = self._foreground.get_foreground()
            #     h, w = image.shape[:2]
            #     new_w, new_h = int(w * scale), int(h * scale)
            #
            #     # Resize the image
            #     resized_foreground = cv2.resize(image, (new_w, new_h), interpolation=cv2.INTER_AREA)
            #
            # # cv2.imshow("asda", self._foreground.get_foreground())
            # cv2.imshow("asda", resized_foreground)
            # cv2.waitKey(0)  # Wait for key press
            # cv2.destroyAllWindows()
        except ValueError:
            return False
        return True