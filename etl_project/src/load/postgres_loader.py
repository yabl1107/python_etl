import pandas as pd
import logging
from psycopg2.extras import execute_values
from src.utils.db import get_postgres_connection
from src.load.base_loader import BaseLoader

logger = logging.getLogger(__name__)


class PostgresLoader(BaseLoader):
    def __init__(self, schema_name, table_name, columns,incremental_col=None):
        self.schema = schema_name
        self.table_name = table_name
        self.columns = columns
        self.incremental_col = incremental_col #Para idempotencia

        self.full_table_path = f"{self.schema}.{self.table_name}"
        self.insert_sql = self._generate_insert_sql()

    def _generate_insert_sql(self):
        cols_str = ", ".join(self.columns)
        return f"INSERT INTO {self.full_table_path} ({cols_str}) VALUES %s;"
    

    def load(self, df: pd.DataFrame):
        if df.empty:
            logger.info("No hay datos para insertar")
            return

        logger.info("Insertando %s registros en %s", len(df), self.full_table_path)

        # Reemplaza NaN por None
        df = df.astype(object).where(df.notnull(), None)


        # Validar orden de columnas
        if list(df.columns) != self.columns:
            logger.warning("El orden de las columnas del DF no coincide")
            df = df[self.columns]
        
        values = [
            tuple(map(_to_python_type, row)) for row in df.itertuples(index=False, name=None)
        ]


        with get_postgres_connection("warehouse_db") as conn:
            with conn.cursor() as cur:
                
                if self.incremental_col:
                    min_val = df[self.incremental_col].min()
                    max_val = df[self.incremental_col].max()
                    delete_sql = f"DELETE FROM {self.full_table_path} WHERE {self.incremental_col} BETWEEN %s AND %s"
                    
                    logger.info("Carga Incremental: Limpiando rango %s - %s", min_val, max_val)
                    cur.execute(delete_sql, (min_val, max_val))
                else:
                    logger.info("Carga Full: Limpiando tabla completa %s", self.full_table_path)
                    cur.execute(f"TRUNCATE TABLE {self.full_table_path}")

                
                logger.info("Insertando %s registros en %s", len(df), self.full_table_path)
                execute_values(cur, self.insert_sql, values)
                
            conn.commit()

        logger.info("Carga completada correctamente")


def _to_python_type(value):
    """
    Convierte tipos numpy a tipos nativos Python
    """
    if hasattr(value, "item"):
        return value.item()
    return value