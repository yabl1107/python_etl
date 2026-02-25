from config.logging import setup_logging
from src.jobs.sales_job import run_daily_sales_pipeline
from dotenv import load_dotenv

load_dotenv()

def main():
    setup_logging()
    
    run_daily_sales_pipeline()

if __name__ == "__main__":
    main()