import pandas as pd
from .base import BaseExtractor

class CSVExtractor(BaseExtractor):
    def __init__(self, path):
        self.path = path

    def extract(self):
        return pd.read_csv(self.path)
