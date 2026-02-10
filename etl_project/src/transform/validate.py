def validate_sales(df):
    if df.empty:
        raise ValueError("No hay ventas para procesar")

    if (df["quantity"] <= 0).any():
        raise ValueError("Cantidad inválida")

    return df