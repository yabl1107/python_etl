import pytest
import pandas as pd
from src.transform.ventasTransformer import VentasTransformer

# SUCCESS (Happy Path)

def test_ventas_transformer_calcula_total_correctamente():
    # mock data
    data = {
        "sale_id": [1, 2],
        "quantity": [2, 10],
        "price": [5.0, 3.0]
    }
    df_input = pd.DataFrame(data)
    transformer = VentasTransformer()

    # transform
    df_output = transformer.transform(df_input)

    # verify
    assert "total_amount" in df_output.columns
    assert df_output.loc[0, "total_amount"] == 10.0
    assert df_output.loc[1, "total_amount"] == 30.0

def test_ventas_transformer_limpia_duplicados_y_nulos():
    data = {
        "sale_id": [1, 1, 2, 3], # duplicate
        "quantity": [1, 1, 1, None], # duplicate
        "price": [10.0, 10.0, 10.0, 10.0]
    }
    df_input = pd.DataFrame(data)
    transformer = VentasTransformer()

    df_output = transformer.transform(df_input)

    assert len(df_output) == 2
    assert df_output["sale_id"].is_unique


# Edge Cases
def test_ventas_transformer_lanza_error_si_esta_vacio():
    df_input = pd.DataFrame()
    transformer = VentasTransformer()
    # Verify 
    with pytest.raises(ValueError, match="No hay ventas para procesar"):
        transformer.transform(df_input)

def test_ventas_transformer_lanza_error_si_cantidad_negativa():
    data = {"sale_id": [1], "quantity": [-5], "price": [100]}
    df_input = pd.DataFrame(data)
    transformer = VentasTransformer()
    with pytest.raises(ValueError, match="Cantidad invalida"):
        transformer.transform(df_input)