CREATE SCHEMA IF NOT EXISTS dw;

-- Dimensión Productos
CREATE TABLE IF NOT EXISTS dw.dim_products (
    product_id INT PRIMARY KEY,
    product_name VARCHAR(100),
    category_name VARCHAR(50),
    unit_cost DECIMAL(10, 2),
    margin_value DECIMAL(10, 2), 
    is_active BOOLEAN,
    created_at TIMESTAMP,
    inserted_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Dimensión Clientes
CREATE TABLE IF NOT EXISTS dw.dim_customers (
    customer_id INT PRIMARY KEY,
    full_name VARCHAR(150),
    email VARCHAR(100),
    country VARCHAR(50),
    loyalty_segment VARCHAR(20), 
    created_at TIMESTAMP,
    inserted_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Dimensión Tiendas
CREATE TABLE IF NOT EXISTS dw.dim_stores (
    store_id INT PRIMARY KEY,
    store_name VARCHAR(100),
    city VARCHAR(50),
    region_name VARCHAR(50),
    inserted_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de Hechos: Ventas
CREATE TABLE IF NOT EXISTS dw.fact_sales (
    sale_id INT PRIMARY KEY,
    transaction_id VARCHAR(50),
    product_id INT,  --REFERENCES dw.dim_products(product_id),
    customer_id INT,  -- REFERENCES dw.dim_customers(customer_id),
    store_id INT, -- REFERENCES dw.dim_stores(store_id),
    quantity INT,
    unit_price DECIMAL(10, 2),
    total_amount DECIMAL(10, 2),
    payment_method VARCHAR(20),
    status VARCHAR(20),
    sale_date TIMESTAMP,
    inserted_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);


CREATE SCHEMA IF NOT EXISTS etl_metadata;

CREATE TABLE IF NOT EXISTS etl_metadata.etl_control (
    table_name      VARCHAR(100) PRIMARY KEY,
    last_updated_at TIMESTAMP NOT NULL,      -- latest checkpoint
    last_run_at     TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- last time etl ran
);


INSERT INTO etl_metadata.etl_control (table_name, last_updated_at, last_run_at)
VALUES 
    ('sales', '1900-01-01 00:00:00', CURRENT_TIMESTAMP),
    ('products', '1900-01-01 00:00:00', CURRENT_TIMESTAMP),
    ('customers', '1900-01-01 00:00:00', CURRENT_TIMESTAMP),
    ('stores', '1900-01-01 00:00:00', CURRENT_TIMESTAMP);