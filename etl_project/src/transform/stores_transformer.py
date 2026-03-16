from pytz import timezone
from datetime import datetime, timezone
from config.tables import SALES_PIPELINE_CONFIG

from .base_transformer import BaseTransformer

class VentasTransformer(BaseTransformer):
    def transform(self, df):
        
        #Validate
        if df.empty:
            raise ValueError("No hay ventas para procesar")
        
        if (df["quantity"] <= 0).any():
            raise ValueError("Cantidad invalida")
        
        mapping = SALES_PIPELINE_CONFIG["column_mapping"]

        # Clean
        df = df.rename(columns=mapping)
        df = df.dropna()
        df = df.drop_duplicates(subset=["sale_id"])

        #Enrich
        df['inserted_at'] = datetime.now(timezone.utc)
        df["total_amount"] = df["quantity"] * df["unit_price"]

        # Filtramos y orden de columnas
        df_to_insert = df[SALES_PIPELINE_CONFIG["target"]["columns"]]

        return df_to_insert