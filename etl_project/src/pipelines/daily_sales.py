import logging
from datetime import date

from src.extract.database import MySQLSalesExtractor
from src.transform.clean import clean_sales
from src.transform.validate import validate_sales
from src.transform.enrich import enrich_sales
from src.load.database import load_sales

logger = logging.getLogger(__name__)

def run():
    process_date = date.today()
    
    #process_date = '2025-03-27'

    logger.info(f"Procesando ventas: {process_date}")

    extractor = MySQLSalesExtractor(process_date)
    df = extractor.extract()

    df = clean_sales(df)
    df = validate_sales(df)
    df = enrich_sales(df)

    load_sales(df)

    logger.info("ETL finalizado correctamente")
