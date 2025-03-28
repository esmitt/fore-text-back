from abc import ABC, abstractmethod
from numpy import ndarray
from typing import Optional

class ForegroundInterface(ABC):
    @abstractmethod
    def extract(self, image: ndarray, threshold: float) -> bool:
        raise NotImplemented

    @abstractmethod
    def get_foreground(self) -> Optional[ndarray]:
        raise NotImplemented

    @abstractmethod
    def get_mask3d(self) -> Optional[ndarray]:
        raise NotImplemented