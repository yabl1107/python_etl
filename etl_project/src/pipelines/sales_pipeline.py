

import logging

from src.extract.mysql_extractor import MysqlExtractor
from src.transform.ventas_transformer import VentasTransformer
from src.metadata_manager import MetadataManager
from src.load.postgres_loader import PostgresLoader
from src.pipelines.base_pipeline import BasePipeline
from src.extraction_strategies import IncrementalStrategy

from config.tables import SALES_PIPELINE_CONFIG

logger = logging.getLogger(__name__)


def run_daily_sales_pipeline():

    table_name = SALES_PIPELINE_CONFIG["source"]["table"]
    incremental_col = SALES_PIPELINE_CONFIG["source"]["incremental_col"]

    # Instaciar dependencias
    
    metadata_mgr = MetadataManager(schema="etl_metadata", table="etl_control")

    latest_checkpoint = metadata_mgr.get_last_checkpoint(table_name)

    logger.info(f"Último checkpoint para {table_name}: {latest_checkpoint}")

    sales_extractor = MysqlExtractor(
        schema_name= SALES_PIPELINE_CONFIG["source"]["schema"],
        table_name= table_name,
        strategy=IncrementalStrategy(column=incremental_col, checkpoint=latest_checkpoint)
    )

    sales_loader = PostgresLoader(
        table_name= SALES_PIPELINE_CONFIG["target"]["table"],
        columns=SALES_PIPELINE_CONFIG["target"]["columns"],
        schema_name= SALES_PIPELINE_CONFIG["target"]["schema"],
        incremental_col= incremental_col
    )

    # Ejecutar pipeline
    try:
        pipeline = BasePipeline(
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