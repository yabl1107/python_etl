from config.logging import setup_logging
from src.pipelines.sales_pipeline import run_daily_sales_pipeline
from src.pipelines.products_pipeline import products_pipeline
from src.pipelines.customers_pipeline import run_daily_customers_pipeline

from dotenv import load_dotenv

load_dotenv()

def main():
    setup_logging()
    
    #run_daily_sales_pipeline()
    #products_pipeline()
    run_daily_customers_pipeline()

if __name__ == "__main__":
    main()