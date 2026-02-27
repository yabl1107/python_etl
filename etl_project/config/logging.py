import logging
from config.settings import LOG_FORMAT
import os

def setup_logging():
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir) # up one level to get to project root
    
    log_dir = os.path.join(project_root, "logs") # logs folder

    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    logging.basicConfig(
        level=logging.INFO,
        format=LOG_FORMAT,
        handlers=[
            logging.FileHandler(f"{log_dir}/etl_process.log"), # save in file
            logging.StreamHandler() # show in console
        ]
    )