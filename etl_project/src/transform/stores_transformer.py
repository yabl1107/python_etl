from datetime import datetime, timezone
import pandas as pd
from config.tables import STORES_PIPELINE_CONFIG
from .base_transformer import BaseTransformer

class StoresTransformer(BaseTransformer):
    def transform(self, df):
        
        if df.empty:
            return df

        df = df.copy()

        # Mapping
        mapping = STORES_PIPELINE_CONFIG.get("column_mapping", {})
        df = df.rename(columns=mapping)

        # Limpieza y normalización
        df["store_name"] = df["store_name"].str.strip()
        df["city"] = df["city"].str.strip().str.title()
        df["region_name"] = df["region_name"].str.strip().str.title()

        # Metadata de carga
        df['inserted_at'] = datetime.now(timezone.utc)

        # Select
        target_columns = STORES_PIPELINE_CONFIG["target"]["columns"]
        df_to_insert = df[target_columns]

        return df_to_insert