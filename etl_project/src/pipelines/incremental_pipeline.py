import logging
from datetime import date

from etl_project.src.extract.base_extractor import BaseExtractor
from etl_project.src.transform.base_transformer import BaseTransformer
from etl_project.src.load.base_loader import BaseLoader


logger = logging.getLogger(__name__)

class IncrementalPipeline:
    def __init__(self, extractor: BaseExtractor, loader: BaseLoader, transformer: BaseTransformer):
        self.extractor = extractor
        self.loader = loader
        self.transformer = transformer
    
    def run(self):
        try:
            #Extract
            df = self.extractor.extract()
            if df.empty:
                logger.info("No se encontraron registros nuevos o modificados.")
                return None
            # Transform
            df = self.transformer.transform(df)
            # Load
            self.loader.load(df)
        
            return df
        
        except Exception as e:
            logger.error(f"Error crítico en el pipeline: {str(e)}", exc_info=True)
            raise