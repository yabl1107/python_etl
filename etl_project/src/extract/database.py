import pandas as pd
from src.utils.db import get_mysql_connection

def extract_sales(process_date):
    query = """
        SELECT sale_id, product_id, quantity, price, sale_date
        FROM sales_source_db.sales
        WHERE sale_date <= %s
    """

    with get_mysql_connection("source_db") as conn:
        return pd.read_sql(query, conn, params=[process_date])
