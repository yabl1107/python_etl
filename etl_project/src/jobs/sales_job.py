

import logging

from src.extract.mysqlExtractor import MysqlExtractor
from src.transform.ventasTransformer import VentasTransformer
from src.metadata.manager import ETLMetadataManager
from src.load.postgresLoader import PostgresLoader
from src.pipelines.incremental import IncrementalETLPipeline

from config.tables import SALES_PIPELINE_CONFIG

logger = logging.getLogger(__name__)


def run_daily_sales_pipeline():

    table_name = SALES_PIPELINE_CONFIG["source"]["table"]
    incremental_col = SALES_PIPELINE_CONFIG["source"]["incremental_col"]

    # Instaciar dependencias
    
    metadata_mgr = ETLMetadataManager(schema="etl_metadata", table="etl_control")

    latest_checkpoint = metadata_mgr.get_last_checkpoint(table_name)

    logger.info(f"Último checkpoint para {table_name}: {latest_checkpoint}")

    sales_extractor = MysqlExtractor(
        schema_name= SALES_PIPELINE_CONFIG["source"]["schema"],
        table_name= table_name,
        incremental_column= incremental_col,
        latest_checkpoint= latest_checkpoint
    )

    sales_loader = PostgresLoader(
        table_name= SALES_PIPELINE_CONFIG["target"]["table"],
        columns=SALES_PIPELINE_CONFIG["target"]["columns"],
        schema_name= SALES_PIPELINE_CONFIG["target"]["schema"]
    )

    # Ejecutar pipeline
    try:
        pipeline = IncrementalETLPipeline(
            extractor=sales_extractor,
            loader= sales_loader,
            transformer=VentasTransformer()
        )

        processed_df = pipeline.run()
        
        if(processed_df is not None and not processed_df.empty):
            # Actualizar checkpoint
            new_checkpoint = processed_df[incremental_col].max()
            metadata_mgr.update_checkpoint(table_name, new_checkpoint)
            logger.info(f"Pipeline de ventas diarias ejecutado exitosamente. Checkpoint actualizado a {new_checkpoint}")
        else:
            logger.info("Pipeline de ventas diarias ejecutado exitosamente. No se encontraron nuevos registros para procesar.")

    except Exception:
        logger.error("Pipeline de ventas diarias falló", exc_info=True)
        exit(1) #Salida con error