import pandas as pd
import logging
from psycopg2.extras import execute_values
from src.utils.db import get_connection
from src.load.baseLoader import BaseLoader

logger = logging.getLogger(__name__)

INSERT_SQL = """
    INSERT INTO dw.fact_sales_target (
        sale_id,
        product_id,
        quantity,
        price,
        sale_date,
        total_amount
    )
    VALUES %s;
"""

class DatabaseLoader(BaseLoader):

    def __init__(self, df: pd.DataFrame, table_name, columns):
        self.table_name = table_name
        self.columns = columns
        self.df = df

    def load(self):
        if self.df.empty:
            logger.info("No hay datos para insertar")
            return

        logger.info("Insertando %s registros en fact_sales_target", len(df))

        # Filtramos el DF
        df_to_insert = self.df[self.columns]

        # Reemplaza NaN por None
        df = df_to_insert.astype(object).where(df_to_insert.notnull(df), None)

        values = [
            tuple(map(_to_python_type, row)) for row in df.itertuples(index=False, name=None)
        ]

        with get_connection("warehouse_db") as conn:
            with conn.cursor() as cur:
                execute_values(cur, INSERT_SQL, values)
            conn.commit()

        logger.info("Inserción completada correctamente")


def _to_python_type(value):
    """
    Convierte tipos numpy a tipos nativos Python
    """
    if hasattr(value, "item"):
        return value.item()
    return value