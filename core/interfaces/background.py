from abc import ABC, abstractmethod
from numpy import ndarray

class BackgroundInterface(ABC):
    @abstractmethod
    def extract(self, image: ndarray) -> bool:
        raise NotImplemented

    @abstractmethod
    def get_background(self) -> ndarray:
        raise NotImplemented