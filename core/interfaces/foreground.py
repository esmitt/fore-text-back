from abc import ABC, abstractmethod
import numpy as np

class ForegroundInterface(ABC):
    @abstractmethod
    def extract(self, image: np.ndarray):
        raise NotImplemented
    @abstractmethod
    def get_foreground(self) -> np.ndarray:
        raise NotImplemented