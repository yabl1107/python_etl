
import pandas as pd
from src.utils.db import get_mysql_connection
from .base import BaseExtractor

class MySQLExtractor(BaseExtractor):
    def __init__(self, table_name, incremental_column, last_checkpoint, columns=None):
        self.table_name = table_name
        self.incremental_column = incremental_column
        self.last_checkpoint = last_checkpoint
        self.columns = columns

    def extract(self):
        # Get columns to select, otherwise *
        select_clause = ", ".join(self.columns) if self.columns else "*"
        
        if self.columns and self.incremental_column not in self.columns:
            select_clause += f", {self.incremental_column}"

        query = f"""
            SELECT {select_clause} 
            FROM {self.table_name} 
            WHERE {self.incremental_column} > %s
        """
        
        with get_mysql_connection("source_db") as conn:
            df = pd.read_sql(query, conn, params=[self.last_checkpoint])
            return df