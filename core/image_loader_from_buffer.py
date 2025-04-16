from typing import override, Optional

import cv2

from core.interfaces.image_loader import ImageLoaderInterface
from common.logger import logger
import numpy as np

class ImageLoaderFromBuffer(ImageLoaderInterface):
    def __init__(self):
        self._buffer: Optional[bytes] = None
        self._image: Optional[np.ndarray] = None

    @override
    def load(self) -> bool:
        if self._buffer is None:
            logger.warning("No buffer provided")
            return False
        try:
            image_np = np.frombuffer(self._buffer, np.uint8)
            self._image = cv2.imdecode(image_np, cv2.IMREAD_COLOR)
            if self._image is None:
                logger.error("Failed to decode image from buffer")
                raise ValueError("Image decoding failed")
            logger.debug(f"Image loaded from buffer with dimensions {self._image.shape}")
            return True
        except Exception as exc:
            logger.debug(f"Error loading image from buffer: {exc}")
            return False

    @override
    def set_source(self, source: bytes):
        if not isinstance(source, bytes):
            logger.error("Source must be bytes")
            return False
        self._buffer = source
        logger.debug("Buffer source set")
        return True

    @override
    def get_source(self) -> np.ndarray:
        return self._image