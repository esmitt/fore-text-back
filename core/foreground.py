from core.interfaces.foreground import ForegroundInterface
import mediapipe as mp
from common.logger import logger
import types
from typing import Optional, override
import numpy as np
import cv2

class Foreground(ForegroundInterface):
    def __init__(self):
        self._mp_segmentation: types.ModuleType = mp.solutions.selfie_segmentation
        self._image_foreground: Optional[np.ndarray] = None
        self._mask_3d: Optional[np.ndarray] = None

    @override
    def extract(self, image: np.ndarray, threshold: float=0.55) -> bool:
        with self._mp_segmentation.SelfieSegmentation(model_selection=1) as segmenter:
            img_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) # rgb to mediapipe
            results = segmenter.process(img_rgb)
            if results.segmentation_mask is None:
                logger.error("Failed to generate the segmentation mask")
                return False
            # create a binary mask where foreground pixels are 255
            foreground_mask = (results.segmentation_mask > threshold).astype(np.uint8) * 255
            self._mask_3d = np.repeat(foreground_mask[:, :, np.newaxis], 3, axis=2).astype(np.uint8)

            self._image_foreground = np.where(self._mask_3d == 255, image, 0)  # Extract the foreground (people)
            logger.debug(f"Foreground extracted {self._image_foreground.shape}")
        return True

    @override
    def get_foreground(self) -> Optional[np.ndarray]:
        return self._image_foreground

    @override
    def get_mask3d(self) -> Optional[np.ndarray]:
        return self._mask_3d