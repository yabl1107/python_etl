CREATE SCHEMA IF NOT EXISTS dw;

CREATE TABLE IF NOT EXISTS dw.fact_sales_target (
    sale_id      INT PRIMARY KEY,
    product_id   INT NOT NULL,
    quantity     INT NOT NULL,
    price        NUMERIC(12, 2) NOT NULL,
    sale_date    TIMESTAMP NOT NULL,
    total_amount NUMERIC(12, 2) NOT NULL
);

-- schema for metadata (checkpoint, logs)

CREATE SCHEMA IF NOT EXISTS etl_metadata;

CREATE TABLE IF NOT EXISTS etl_metadata.etl_control (
    table_name      VARCHAR(100) PRIMARY KEY,
    last_updated_at TIMESTAMP NOT NULL,      -- latest checkpoint
    last_run_at     TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- last time etl ran
);