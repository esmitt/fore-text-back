from numpy import ndarray
from typing_extensions import override
from typing import Optional

from core.interfaces.background import BackgroundInterface

class Background(BackgroundInterface):
    def __init__(self):
        self._image_background: Optional[ndarray] = None

    @override
    def extract(self, image: ndarray) -> bool:
        self._image_background = image
        return True

    @override
    def get_background(self) -> ndarray:
        return self._image_background
