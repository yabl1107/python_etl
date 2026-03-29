

import logging

from src.extract.mysql_extractor import MysqlExtractor
from src.transform.customers_transformer import CustomersTransformer
from src.metadata_manager import MetadataManager
from src.extraction_strategies import IncrementalStrategy
from src.load.postgres_loader import PostgresLoader
from src.pipelines.base_pipeline import BasePipeline

from config.tables import CUSTOMERS_PIPELINE_CONFIG

logger = logging.getLogger(__name__)

def run_daily_customers_pipeline():

    table_name = CUSTOMERS_PIPELINE_CONFIG["source"]["table"]
    incremental_col = CUSTOMERS_PIPELINE_CONFIG["source"]["incremental_col"]

    # Instaciar dependencias
    
    metadata_mgr = MetadataManager(schema="etl_metadata", table="etl_control")

    latest_checkpoint = metadata_mgr.get_last_checkpoint(table_name)
    logger.info(f"Último checkpoint para {table_name}: {latest_checkpoint}")

    strategy = IncrementalStrategy(incremental_column=incremental_col, checkpoint=latest_checkpoint)

    customers_extractor = MysqlExtractor(
        schema_name= CUSTOMERS_PIPELINE_CONFIG["source"]["schema"],
        table_name= table_name,
        strategy=strategy
    )

    # Loader recibe incremental_col para eliminar data con fecha dentro del rango de fechas a cargar, esto es necesario para evitar duplicados en caso de que el proceso falle después de cargar data pero antes de actualizar el checkpoint
    customers_loader = PostgresLoader(
        table_name= CUSTOMERS_PIPELINE_CONFIG["target"]["table"],
        columns=CUSTOMERS_PIPELINE_CONFIG["target"]["columns"],
        schema_name= CUSTOMERS_PIPELINE_CONFIG["target"]["schema"],
        incremental_col= incremental_col
    )

    # Ejecutar pipeline
    try:
        pipeline = BasePipeline(
            extractor=customers_extractor,
            loader= customers_loader,
            transformer=CustomersTransformer()
        )

        processed_df = pipeline.run()
        
        if(processed_df is not None and not processed_df.empty):
            # Actualizar checkpoint
            new_checkpoint = processed_df[incremental_col].max()
            metadata_mgr.update_checkpoint(table_name, new_checkpoint)
            logger.info(f"Pipeline de clientes diarias ejecutado exitosamente. Checkpoint actualizado a {new_checkpoint}")
        else:
            logger.info("Pipeline de clientes diarias ejecutado exitosamente. No se encontraron nuevos registros para procesar.")

    except Exception:
        logger.error("Pipeline de clientes diarias falló", exc_info=True)
        exit(1) #Salida con error