import logging
from datetime import date

from src.extract.base import BaseExtractor
from src.load.database import DatabaseLoader
from etl_project.src.extract.mysql_db import MySQLExtractor
from src.transform.clean import clean_sales
from src.transform.validate import validate_sales
from src.transform.enrich import enrich_sales
from src.load.baseLoader import BaseLoader
from src.metadata.manager import ETLMetadataManager

logger = logging.getLogger(__name__)

def daily_sales_pipeline(
        extractor: BaseExtractor,
        loader : BaseLoader,
        metadata: ETLMetadataManager,
        TABLE_NAME : str,
        INCREMENTAL_COL = str
    ):
    try:
        #Get checkpoint
        last_checkpoint = metadata.get_last_checkpoint(TABLE_NAME)
        logger.info(f"Iniciando extracción de {TABLE_NAME} desde: {last_checkpoint}")

        #Extract
        df = extractor.extract(last_checkpoint)

        if df.empty:
            logger.info("No se encontraron registros nuevos o modificados.")
            return

        # Transform
        df = clean_sales(df)
        df = validate_sales(df)
        df = enrich_sales(df)

        # Load
        loader.load(df)

        # Update checkpoint
        new_checkpoint = df[INCREMENTAL_COL].max()
        metadata.update_checkpoint(TABLE_NAME, new_checkpoint)

        logger.info(f"ETL finalizado: {len(df)} filas procesadas.")
        return df

    except Exception as e:
        logger.error(f"Error crítico en el pipeline de ventas: {str(e)}", exc_info=True)
        raise


def run_daily_sales_pipeline():

    table_name = "sales"
    incremental_col = "updated_at"

    # Instaciar dependencias
    metadata_mgr = ETLMetadataManager(schema="etl_metadata", table="etl_control")

    sales_extractor = MySQLExtractor(
        table_name= table_name,
        incremental_column= incremental_col
    )

    sales_loader = DatabaseLoader()

    # Ejecutar pipeline
    try:
        daily_sales_pipeline(
            extractor=sales_extractor,
            loader= sales_loader,
            metadata=metadata_mgr,
            TABLE_NAME=table_name,
            INCREMENTAL_COL=incremental_col
        )
    except Exception:
        exit(1) #Salida con error