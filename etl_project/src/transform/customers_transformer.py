from pytz import timezone
from datetime import datetime, timezone
from config.tables import CUSTOMERS_PIPELINE_CONFIG

from .base_transformer import BaseTransformer

class CustomersTransformer(BaseTransformer):
    def transform(self, df):
        
        if df.empty:
            return df
        
        df = df.copy()
        df = df.dropna(subset=["customer_id", "email"])
        df = df.drop_duplicates(subset=["customer_id"])

        # Loyalty score segmentation
        def segmentar_cliente(score):
            if score >= 100:
                return 'Gold'
            elif score >= 50:
                return 'Silver'
            else:
                return 'Bronze'

        df["loyalty_segment"] = df["loyalty_score"].apply(segmentar_cliente)

        # Metadata de carga
        df['inserted_at'] = datetime.now(timezone.utc)

        # Clean
        df["full_name"] = df["full_name"].str.strip().str.title()
        df["country"] = df["country"].fillna("Desconocido").str.strip()

        # Table mapping
        mapping = CUSTOMERS_PIPELINE_CONFIG.get("column_mapping", {})
        df = df.rename(columns=mapping)

        # Filtramos para que SOLO pasen las columnas definidas en el target
        # Esto elimina automáticamente 'loyalty_score', que no está en el target
        target_columns = CUSTOMERS_PIPELINE_CONFIG["target"]["columns"]
        df_to_insert = df[target_columns]

        return df_to_insert