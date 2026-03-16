

import logging

from src.extract.mysql_extractor import MysqlExtractor
from src.transform.stores_transformer import StoresTransformer
from src.load.postgres_loader import PostgresLoader
from src.pipelines.base_pipeline import BasePipeline

from config.tables import STORES_PIPELINE_CONFIG

logger = logging.getLogger(__name__)


def stores_pipeline():

    table_name = STORES_PIPELINE_CONFIG["source"]["table"]
    incremental_col = STORES_PIPELINE_CONFIG["source"]["incremental_col"]

    # Instaciar dependencias
    logger.info(f"Full load para {table_name}")

    sales_extractor = MysqlExtractor(
        schema_name= STORES_PIPELINE_CONFIG["source"]["schema"],
        table_name= table_name
    )

    sales_loader = PostgresLoader(
        table_name= STORES_PIPELINE_CONFIG["target"]["table"],
        columns=STORES_PIPELINE_CONFIG["target"]["columns"],
        schema_name= STORES_PIPELINE_CONFIG["target"]["schema"]
    )

    # Ejecutar pipeline
    try:
        pipeline = BasePipeline(
            extractor=sales_extractor,
            loader= sales_loader,
            transformer=StoresTransformer()
        )

        processed_df = pipeline.run()
        
        logger.info("Pipeline de tiendas ejecutado exitosamente.")

    except Exception:
        logger.error("Pipeline de tiendas falló", exc_info=True)
        exit(1) #Salida con error