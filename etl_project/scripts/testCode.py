import pandas as pd
import pytest
from unittest.mock import Mock, patch

from src.pipelines.daily_sales import daily_sales_pipeline


def main():
    # --- Fake DataFrame ---
    df = pd.DataFrame({
            "sale_id": [1, 2],
            "product_id": [10, 20],
            "quantity": [2, None],
            "price": [100.00, 50.00],
            "sale_date": pd.to_datetime(["2024-01-01", "2024-01-02"]),
            "created_at": pd.to_datetime(["2024-01-01", "2024-01-02"]),
            "updated_at": pd.to_datetime(["2024-01-02", "2024-01-03"]),
        })

    print(df)
    # Reemplaza NaN por None
    df = df.astype(object).where(pd.notnull(df), None)

    print(df)

    values = [
        tuple(map(_to_python_type, row)) for row in df.itertuples(index=False, name=None)
    ]

    print(values)

def _to_python_type(value):
    """
    Convierte tipos numpy a tipos nativos Python
    """
    if hasattr(value, "item"):
        return value.item()
    return value

if __name__ == "__main__":
    main()