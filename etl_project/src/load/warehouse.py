from src.utils.db import get_connection

def load_sales(df):
    with get_connection("warehouse_db") as conn:
        # insert / copy / upsert
        pass
