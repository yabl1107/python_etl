from abc import ABC, abstractmethod

class BaseExtractor(ABC):
    @abstractmethod
    def extract(self):
        """Debe devolver un dataframe."""
        pass