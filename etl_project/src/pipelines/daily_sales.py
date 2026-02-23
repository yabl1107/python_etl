import logging
from datetime import date

from src.extract.database import MySQLExtractor
from src.transform.clean import clean_sales
from src.transform.validate import validate_sales
from src.transform.enrich import enrich_sales
from src.load.database import load_sales
from src.metadata.manager import ETLMetadataManager

logger = logging.getLogger(__name__)

def daily_sales_pipeline(extractor: MySQLExtractor, metadata: ETLMetadataManager):
    TABLE_NAME = "sales"
    INCREMENTAL_COL = "updated_at"

    try:
        # get checkpoint
        last_checkpoint = metadata.get_last_checkpoint(TABLE_NAME)
        logger.info(f"Iniciando extracción de {TABLE_NAME} desde: {last_checkpoint}")

        # Extract
        df = extractor.extract(last_checkpoint)

        if df.empty:
            logger.info("No se encontraron registros nuevos o modificados.")
            return

        # Transform
        df = clean_sales(df)
        df = validate_sales(df)
        df = enrich_sales(df)

        # Load
        load_sales(df) # Tu Upsert en Postgres

        # Update checkpoint
        new_checkpoint = df[INCREMENTAL_COL].max()
        metadata.update_checkpoint(TABLE_NAME, new_checkpoint)

        logger.info(f"ETL finalizado: {len(df)} filas procesadas.")

        return df

    except Exception as e:
        logger.error(f"Error crítico en el pipeline de ventas: {str(e)}", exc_info=True)
        raise


def run_daily_sales_pipeline():
    # Instaciar dependencias
    metadata_mgr = ETLMetadataManager(schema="etl_metadata", table="etl_control")

    sales_extractor = MySQLExtractor(
        table_name="sales",
        incremental_column="updated_at"
    )
    # Ejecutar pipeline
    try:
        daily_sales_pipeline(
            extractor=sales_extractor,
            metadata=metadata_mgr
        )
    except Exception:
        exit(1) # Salida con error