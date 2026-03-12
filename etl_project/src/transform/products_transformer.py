from pytz import timezone
from datetime import datetime, timezone
from config.tables import PRODUCTS_PIPELINE_CONFIG

from .base_transformer import BaseTransformer

class ProductsTransformer(BaseTransformer):

    def calcular_margen(self, row):
        if row['category_name'] == 'Electrónica':
            return row['unit_cost'] * 0.15
        return row['unit_cost'] * 0.10

    def transform(self, df):
        
        #Validate
        if df.empty:
            raise ValueError("No hay productos para procesar")        
        
        mapping = PRODUCTS_PIPELINE_CONFIG["column_mapping"]

        # Clean
        df = df.rename(columns=mapping)
        df = df.dropna()
        df = df.drop_duplicates(subset=["product_id"])

        #Enrich
        df['margin_value'] = df.apply(self.calcular_margen, axis=1)
        df['inserted_at'] = datetime.now(timezone.utc) 

        # Los bool de mysql se cargan como 0/1 -> los convertimos a int
        if 'is_active' in df.columns:
            df['is_active'] = df['is_active'].astype(bool)
            
        # Filtramos y ordenamos las columnas
        df_to_insert = df[PRODUCTS_PIPELINE_CONFIG["target"]["columns"]]


        return df_to_insert