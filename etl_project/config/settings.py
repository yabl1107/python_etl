import os

ENV = os.getenv("ENV", "dev")
DEBUG = ENV == "dev"

LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_LEVEL = "INFO" if ENV == "prod" else "DEBUG"