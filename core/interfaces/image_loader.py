from abc import ABC, abstractmethod
from numpy import ndarray
from typing import Union

class ImageLoaderInterface(ABC):
    @abstractmethod
    def load(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def set_source(self, source: Union[str, bytes]):
        raise NotImplementedError

    @abstractmethod
    def get_source(self) -> ndarray:
        raise NotImplementedError