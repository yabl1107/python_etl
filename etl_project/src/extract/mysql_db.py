
import pandas as pd
from src.utils.db import get_mysql_connection
from .base import BaseExtractor

class MySQLExtractor(BaseExtractor):
    def __init__(self, table_name, incremental_column, columns=None):
        self.table_name = table_name
        self.incremental_column = incremental_column
        self.columns = columns

    def extract(self, checkpoint=None):
        # Get columns to select, otherwise *
        select_clause = ", ".join(self.columns) if self.columns else "*"
        
        if self.columns and self.incremental_column not in self.columns:
            select_clause += f", {self.incremental_column}"

        query = f"""
            SELECT {select_clause} 
            FROM {self.table_name} 
            WHERE {self.incremental_column} > %s
        """
        
        checkpoint_to_use = checkpoint or "2026-01-01 00:00:00"

        with get_mysql_connection("source_db") as conn:
            df = pd.read_sql(query, conn, params=[checkpoint_to_use])
            return df