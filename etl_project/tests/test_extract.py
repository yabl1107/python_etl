import pandas as pd
import pytest
from unittest.mock import Mock, patch

from src.pipelines.daily_sales import daily_sales_pipeline

def test_pipeline_success():

    # --- Fake DataFrame ---
    df = pd.DataFrame({
        "sale_id": [1, 2],
        "product_id": [10, 20],
        "quantity": [2, 3],
        "price": [100.00, 50.00],
        "sale_date": pd.to_datetime(["2024-01-01", "2024-01-02"]),
        "created_at": pd.to_datetime(["2024-01-01", "2024-01-02"]),
        "updated_at": pd.to_datetime(["2024-01-02", "2024-01-03"]),
    })

    # --- Mocks ---
    extractor_mock = Mock()
    extractor_mock.extract.return_value = df

    metadata_mock = Mock()
    metadata_mock.get_last_checkpoint.return_value = "2023-12-31"

    df = daily_sales_pipeline(extractor_mock, metadata_mock)

    
    print(df)

    '''
    with patch("src.pipeline.daily_sales.clean_sales", return_value=df), \
         patch("src.pipeline.daily_sales.validate_sales", return_value=df), \
         patch("src.pipeline.daily_sales.enrich_sales", return_value=df), \
         patch("src.pipeline.daily_sales.load_sales") as load_mock:

        

        # Verificaciones
        extractor_mock.extract.assert_called_once_with("2023-12-31")
        load_mock.assert_called_once()
        metadata_mock.update_checkpoint.assert_called_once()
        # Assert sobre comportamiento real
        assert "amount" in df.columns
        assert len(result_df) == 1
    '''

if __name__ == "__main__":
    test_pipeline_success()