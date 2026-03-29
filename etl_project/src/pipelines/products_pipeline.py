import logging

from src.extract.mysql_extractor import MysqlExtractor
from src.transform.products_transformer import ProductsTransformer
from src.metadata_manager import MetadataManager
from src.load.postgres_loader import PostgresLoader
from src.pipelines.base_pipeline import BasePipeline
from src.extraction_strategies import IncrementalStrategy

from config.tables import PRODUCTS_PIPELINE_CONFIG

logger = logging.getLogger(__name__)


def products_pipeline():

    table_name = PRODUCTS_PIPELINE_CONFIG["source"]["table"]
    incremental_col = PRODUCTS_PIPELINE_CONFIG["source"]["incremental_col"]

    # Instaciar dependencias
    
    metadata_mgr = MetadataManager(schema="etl_metadata", table="etl_control")

    latest_checkpoint = metadata_mgr.get_last_checkpoint(table_name)
    logger.info(f"Último checkpoint para {table_name}: {latest_checkpoint}")
    
    strategy = IncrementalStrategy(column=incremental_col, checkpoint=latest_checkpoint)

    products_extractor = MysqlExtractor(
        schema_name= PRODUCTS_PIPELINE_CONFIG["source"]["schema"],
        table_name= table_name,
        strategy=strategy
    )

    products_loader = PostgresLoader(
        table_name= PRODUCTS_PIPELINE_CONFIG["target"]["table"],
        columns=PRODUCTS_PIPELINE_CONFIG["target"]["columns"],
        schema_name= PRODUCTS_PIPELINE_CONFIG["target"]["schema"],
        incremental_col= incremental_col
    )

    # Ejecutar pipeline
    try:
        pipeline = BasePipeline(
            extractor=products_extractor,
            loader= products_loader,
            transformer=ProductsTransformer()
        )

        processed_df = pipeline.run()
        
        if(processed_df is not None and not processed_df.empty):
            # Actualizar checkpoint
            new_checkpoint = processed_df[incremental_col].max()
            metadata_mgr.update_checkpoint(table_name, new_checkpoint)
            logger.info(f"Pipeline de productos ejecutado exitosamente. Checkpoint actualizado a {new_checkpoint}")
        else:
            logger.info("Pipeline de productos ejecutado exitosamente. No se encontraron nuevos registros para procesar.")

    except Exception:
        logger.error("Pipeline de productos falló", exc_info=True)
        exit(1) #Salida con error