CREATE TABLE IF NOT EXISTS sales_source_db.sales (
    sale_id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT NOT NULL,
    transaction_id VARCHAR(50) NOT NULL UNIQUE,
    customer_id INT NOT NULL,      
    store_id INT NOT NULL,                   
    
    quantity INT NOT NULL,
    price DECIMAL(10, 2) NOT NULL,

    payment_method ENUM('credit_card', 'cash', 'transfer', 'crypto') DEFAULT 'cash',
    status VARCHAR(20) DEFAULT 'completed',
    sale_date DATETIME NOT NULL,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS sales_source_db.products (
    product_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    category VARCHAR(50),
    cost_price DECIMAL(10, 2),
    supplier_id INT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS sales_source_db.customers (
    customer_id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(150) NOT NULL,
    email VARCHAR(100) UNIQUE,
    country VARCHAR(50) DEFAULT 'Desconocido',
    loyalty_score INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS sales_source_db.stores (
    store_id INT AUTO_INCREMENT PRIMARY KEY,
    store_name VARCHAR(100) NOT NULL,
    city VARCHAR(50),
    region VARCHAR(50)
);