
import pandas as pd
import logging
from src.utils.db import get_mysql_connection
from .base_extractor import BaseExtractor
    

logger = logging.getLogger(__name__)

class MysqlExtractor(BaseExtractor):
    def __init__(self, schema_name, table_name, incremental_column=None, latest_checkpoint=None, columns=None):
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

        # Query base
        query = f"SELECT {select_clause} FROM {self.schema}.{self.table_name}"
        params = []

        # Lógica Incremental vs Full
        if self.incremental_column:
            # Si hay columna incremental, añadimos el filtro WHERE
            query += f" WHERE {self.incremental_column} > %s"
            
            # Usar checkpoint
            checkpoint_to_use = self.checkpoint or "1900-01-01 00:00:00"
            params.append(checkpoint_to_use)
            logger.info(f"Extrayendo incremental de {self.table_name} desde {checkpoint_to_use}")
        else:
            # Sin columna incremental, es un Full Load
            logger.info(f"Extrayendo carga completa (Full Load) de {self.table_name}")

        with get_mysql_connection("source_db") as conn:
            df = pd.read_sql(query, conn, params=params)
            return df