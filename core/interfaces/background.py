from abc import ABC, abstractmethod


class BackgroundInterface(ABC):
    @abstractmethod
    def apply(self, image, **kwargs):
        pass