from abc import ABC, abstractmethod
from numpy import ndarray

class ImageLoaderInterface(ABC):
    @abstractmethod
    def load(self) -> bool:
        raise NotImplementedError
    def set_source(self, source: str):
        raise NotImplementedError
    def get_source(self) -> ndarray:
        raise NotImplementedError