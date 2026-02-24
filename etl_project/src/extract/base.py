from abc import ABC, abstractmethod

class BaseExtractor(ABC):
    @abstractmethod
    def extract(self, checkpoint=None):
        """Debe devolver un dataframe."""
        pass