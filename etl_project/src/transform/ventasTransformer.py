from .baseTransformer import BaseTransformer

class VentasTransformer(BaseTransformer):
    def transform(self, df):
        
        #Validate
        if df.empty:
            raise ValueError("No hay ventas para procesar")
        
        if (df["quantity"] <= 0).any():
            raise ValueError("Cantidad invalida")
        
        
        # Clean
        df = df.copy()
        df = df.dropna()
        df = df.drop_duplicates(subset=["sale_id"])

        #Enrich
        df = df.copy()
        df["total_amount"] = df["quantity"] * df["price"]


        return df