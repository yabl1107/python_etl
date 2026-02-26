import pandas as pd
import logging
from psycopg2.extras import execute_values
from src.utils.db import get_postgres_connection
from src.load.baseLoader import BaseLoader

logger = logging.getLogger(__name__)


class PostgresLoader(BaseLoader):
    def __init__(self, schema_name, table_name, columns):
        self.schema = schema_name
        self.table_name = table_name
        self.columns = columns
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

        # Filtramos el DF
        df_to_insert = df[self.columns]

        # Reemplaza NaN por None
        df = df_to_insert.astype(object).where(df_to_insert.notnull(), None)

        values = [
            tuple(map(_to_python_type, row)) for row in df.itertuples(index=False, name=None)
        ]

        with get_postgres_connection("warehouse_db") as conn:
            with conn.cursor() as cur:
                execute_values(cur, self.insert_sql, values)
            conn.commit()

        logger.info("Inserción completada correctamente")


def _to_python_type(value):
    """
    Convierte tipos numpy a tipos nativos Python
    """
    if hasattr(value, "item"):
        return value.item()
    return value