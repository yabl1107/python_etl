def clean_sales(df):
    df = df.copy()
    df = df.dropna()
    df = df.drop_duplicates(subset=["sale_id"])
    return df
