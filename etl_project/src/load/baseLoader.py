from abc import ABC, abstractmethod
import pandas as pd

class BaseLoader(ABC):
    @abstractmethod
    def load(self,  df: pd.DataFrame):
        """Método para insertar los datos en el destino"""
        pass