def enrich_sales(df):
    df = df.copy()
    df["total_amount"] = df["quantity"] * df["price"]
    return df
