import logging
from datetime import date

from src.extract.database import MySQLExtractor
from src.transform.clean import clean_sales
from src.transform.validate import validate_sales
from src.transform.enrich import enrich_sales
from src.load.database import load_sales
from src.metadata.manager import ETLMetadataManager

logger = logging.getLogger(__name__)

def run():
    TABLE_NAME = "sales"
    INCREMENTAL_COL = "updated_at"

    # get latest checkpoint for sales
    metadata = ETLMetadataManager(
        schema="etl_metadata",
        table="etl_control"
    )

    last_checkpoint = metadata.get_last_checkpoint(TABLE_NAME)

    logger.info(f"Procesando ventas since: {last_checkpoint}")

    extractor = MySQLExtractor(
        table_name=TABLE_NAME,
        incremental_column=INCREMENTAL_COL,
        last_checkpoint=last_checkpoint
    )
    df = extractor.extract()

    if df.empty:
        logger.info("No se encontraron registros nuevos o modificados. Finalizando.")
        return

    df = clean_sales(df)
    df = validate_sales(df)
    df = enrich_sales(df)

    # Postgres upsert
    load_sales(df)

    # Update checkpoint
    new_checkpoint = df[INCREMENTAL_COL].max()
    metadata.update_checkpoint(TABLE_NAME, new_checkpoint)

    logger.info("ETL finalizado correctamente")
