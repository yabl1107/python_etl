
import pandas as pd
from src.utils.db import get_mysql_connection
from .base import BaseExtractor

class MySQLSalesExtractor(BaseExtractor):
    def __init__(self, process_date):
        self.process_date = process_date

    def extract(self):
        query = """
            SELECT sale_id, product_id, quantity, price, sale_date
            FROM sales_source_db.sales
            WHERE sale_date <= %s
        """

        with get_mysql_connection("source_db") as conn:
            return pd.read_sql(query, conn, params=[self.process_date])
