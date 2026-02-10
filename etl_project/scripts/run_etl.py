from config.logging import setup_logging
from src.pipelines.daily_sales import run

from dotenv import load_dotenv

load_dotenv()

def main():
    setup_logging()
    run()

if __name__ == "__main__":
    main()
