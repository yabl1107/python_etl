
import pandas as pd
from src.utils.db import get_mysql_connection
from .base import BaseExtractor

class MysqlExtractor(BaseExtractor):
    def __init__(self, schema_name, table_name, incremental_column,latest_checkpoint, columns=None):
        self.schema = schema_name
        self.table_name = table_name
        self.incremental_column = incremental_column
        self.checkpoint = latest_checkpoint
        self.columns = columns

    def extract(self):
        # Get columns to select, otherwise *
        select_clause = ", ".join(self.columns) if self.columns else "*"
        
        if self.columns and self.incremental_column not in self.columns: #Make sure IC is included
            select_clause += f", {self.incremental_column}"

        query = f"""
            SELECT {select_clause} 
            FROM {self.schema}.{self.table_name} 
            WHERE {self.incremental_column} > %s
        """
        
        checkpoint_to_use = self.checkpoint or "2026-01-01 00:00:00"

        with get_mysql_connection("source_db") as conn:
            df = pd.read_sql(query, conn, params=[checkpoint_to_use])
            return df