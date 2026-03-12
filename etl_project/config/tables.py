# src/config/tables.py

SALES_PIPELINE_CONFIG = {
    "source": {
        "schema": "sales_source_db",
        "table": "sales",
        "incremental_col": "updated_at",
        "columns": [
            "sale_id",
            "product_id",
            "transaction_id",
            "customer_id",
            "store_id",
            "quantity",
            "price",
            "payment_method",
            "status",
            "sale_date",
            "updated_at"
        ]
    },
    "target": {
        "schema": "dw",
        "table": "fact_sales",
        "columns": [
            "sale_id",
            "transaction_id",
            "product_id",
            "customer_id",
            "store_id",
            "quantity",
            "unit_price",
            "total_amount", # Calculado en transofrm
            "payment_method",
            "status",
            "sale_date", # Fecha de la venta
            "inserted_at" # Metadato de carga
        ]
    },
    "column_mapping": { #Bloque para renombrar columns
        "price": "unit_price"
    }
}

PRODUCTS_PIPELINE_CONFIG = {
    "source": {
        "schema": "sales_source_db",
        "table": "products",
        "incremental_col": "created_at",
        "columns": [
            "product_id",
            "name",
            "category",
            "cost_price",
            "supplier_id",
            "is_active",
            "created_at"
        ]
    },
    "target": {
        "schema": "dw",
        "table": "dim_products",
        "columns": [
            "product_id",
            "product_name",
            "category_name",
            "unit_cost",
            "margin_value", #Calculado en transform
            "is_active",
            "created_at", # Fecha de ingreso sistema
            "inserted_at" #Metadato de carga
        ]
    },
    "column_mapping": {
        "name": "product_name",
        "category": "category_name",
        "cost_price": "unit_cost"
    }
}

CUSTOMERS_PIPELINE_CONFIG = {
    "source": {
        "schema": "sales_source_db",
        "table": "customers",
        "incremental_col": "created_at",
        "columns": [
            "customer_id",
            "full_name",
            "email",
            "country",
            "loyalty_score",
            "created_at"
        ]
    },
    "target": {
        "schema": "dw",
        "table": "dim_customers",
        "columns": [
            "customer_id",
            "full_name",
            "email",
            "country",
            "loyalty_segment",
            "created_at", # Fecha de ingreso sistema
            "inserted_at" # Metadato de carga 
        ]
    },
    "column_mapping": {} 
}

STORES_PIPELINE_CONFIG = {
    "source": {
        "schema": "sales_source_db",
        "table": "stores",
        "incremental_col": None,
        "columns": [
            "store_id",
            "store_name",
            "city",
            "region"
        ]
    },
    "target": {
        "schema": "dw",
        "table": "dim_stores",
        "columns": [
            "store_id",
            "store_name",
            "city",
            "region_name",
            "inserted_at"
        ]
    },
    "column_mapping": {
        "region": "region_name"
    }
}