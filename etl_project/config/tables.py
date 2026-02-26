
SALES_PIPELINE_CONFIG = {
    "source": { # Mysql
        "schema": "sales_source_db",
        "table": "sales",
        "incremental_col": "updated_at",
        "columns": [
            "id", 
            "prod_id", 
            "qty", 
            "unit_price", 
            "updated_at"
        ]
    },
    "target": { #Postgres
        "schema": "dw",
        "table": "fact_sales_target",
        "columns": [
            "sale_id", 
            "product_id", 
            "quantity", 
            "price", 
            "sale_date", 
            "total_amount" #created in transform
        ]
    }
}