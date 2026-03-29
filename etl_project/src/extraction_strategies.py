from typing import Protocol


#Usamos protocols para definir estrategias de extraccion.

class ExtractionStrategy(Protocol):
    def build_query(self, base_query: str) -> tuple[str, list]:
        ...

class FullLoadStrategy:
    def build_query(self, base_query: str):
        return base_query, []


class IncrementalStrategy:
    def __init__(self, column: str, checkpoint):
        self.column = column
        self.checkpoint = checkpoint

    def build_query(self, base_query: str):
        query = base_query + f" WHERE {self.column} > %s"
        checkpoint_to_use = self.checkpoint or "1900-01-01"
        return query, [checkpoint_to_use]