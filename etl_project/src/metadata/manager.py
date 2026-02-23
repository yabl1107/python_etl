import pandas as pd
import logging
from src.utils.db import get_connection # Asegúrate de tener esta utilidad

logger = logging.getLogger(__name__)

class ETLMetadataManager:
    def __init__(self, schema="etl_metadata", table="etl_control"):
        self.schema = schema
        self.table = table
        self.full_table_name = f"{self.schema}.{self.table}"

    def get_last_checkpoint(self, table_name):
        """
        Obtiene el último valor de updated_at para una tabla específica.
        Si la tabla no existe en el control, devuelve una fecha por defecto.
        """
        query = f"SELECT last_updated_at FROM {self.full_table_name} WHERE table_name = %s"
        
        try:
            with get_connection("warehouse_db") as conn:
                df = pd.read_sql(query, conn, params=[table_name])
                
                if not df.empty:
                    return df.iloc[0, 0]
                
                logger.warning(f"No se encontró checkpoint para {table_name}. Usando fecha base.")
                return "1900-01-01 00:00:00"
        
        except Exception as e:
            logger.error(f"Error al leer metadatos: {e}") #Si la tabla no existe
            return "1900-01-01 00:00:00"

    def update_checkpoint(self, table_name, new_checkpoint):
        """
        Actualiza o inserta el nuevo checkpoint en la tabla de control.
        """
        # SQL de tipo UPSERT para Postgres
        query = f"""
            INSERT INTO {self.full_table_name} (table_name, last_updated_at, last_run_at)
            VALUES (%s, %s, CURRENT_TIMESTAMP)
            ON CONFLICT (table_name) 
            DO UPDATE SET 
                last_updated_at = EXCLUDED.last_updated_at,
                last_run_at = CURRENT_TIMESTAMP;
        """
        try:
            with get_connection("warehouse_db") as conn:
                with conn.cursor() as cur:
                    cur.execute(query, (table_name, new_checkpoint))
                    conn.commit() # ¡Importante en escrituras!
                logger.info(f"Checkpoint actualizado para {table_name}: {new_checkpoint}")
        
        except Exception as e:
            logger.error(f"No se pudo actualizar el checkpoint para {table_name}: {e}")
            raise e