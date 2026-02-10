import pandas as pd
from src.transform.clean import clean_sales

def test_clean_sales_removes_duplicates():
    df = pd.DataFrame({
        "sale_id": [1, 1],
        "quantity": [1, 1],
        "price": [10, 10]
    })
    result = clean_sales(df)
    assert len(result) == 1
