from typing_extensions import override
from core.interfaces.image_loader import ImageLoaderInterface
from core.logger import logger
import cv2
import numpy as np
from typing import Optional
from os.path import exists

class ImageLoaderFromFile(ImageLoaderInterface):
    def __init__(self):
        self._path: str = ""
        self._image: Optional[np.ndarray] = None

    @override
    def set_source(self, source: str) -> bool:
        self._path = ""
        if not exists(source):
            logger.error(f"File {source} doesn't exist")
            return False
        self._path = source
        logger.debug(f"File {self._path} exists")
        return True

    @override
    def load(self) -> bool:
        if len(self._path) == 0:
            logger.warning(f"The path file is empty")
            return False
        try:
            self._image = cv2.imread(self._path)
            if self._image is None:
                logger.debug(f"Image couldn't be loaded {self._path}")
                raise ValueError
            logger.debug(f"File of dimensions {self._image.shape}")
            return True
        except Exception as e:
            logger.exception(f"Error loading image from {self._path}: {e}")
            return False

    @override
    def get_source(self) -> np.ndarray:
        return self._image
