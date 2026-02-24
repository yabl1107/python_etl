from abc import ABC, abstractmethod

class BaseLoader(ABC):
    @abstractmethod
    def load(self):
        """ Load data to a table"""
        pass