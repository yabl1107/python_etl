
import pandas as pd
import logging
from src.utils.db import get_mysql_connection
from .base_extractor import BaseExtractor
from src.extraction_strategies import ExtractionStrategy
    

logger = logging.getLogger(__name__)

class MysqlExtractor(BaseExtractor):
    def __init__(self, schema_name, table_name, strategy: ExtractionStrategy, columns=None):
        self.schema = schema_name
        self.table_name = table_name
        self.strategy = strategy
        self.columns = columns

    def extract(self):
        logger.info(f"Extrayendo datos de {self.schema}.{self.table_name}")
        
        # Get columns to select, otherwise *
        select_clause = ", ".join(self.columns) if self.columns else "*"
        # Query base
        base_query = f"SELECT {select_clause} FROM {self.schema}.{self.table_name}"

        query, params = self.strategy.build_query(base_query)

        #logger.debug(f"Query: {query}")
        #logger.debug(f"Params: {params}")
            
        try:
            with get_mysql_connection("source_db") as conn:
                df = pd.read_sql(query, conn, params=params)
                return df
        except Exception as e:
            logger.error(f"Error extrayendo {self.table_name}: {e}")
            raise