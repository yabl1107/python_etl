INSERT INTO sales_source_db.sales 
(product_id, transaction_id, customer_id, store_id, quantity, price, payment_method, status, sale_date)
VALUES 
(101, 'TXN-2026-001', 1, 1, 2, 1500.00, 'credit_card', 'completed', '2026-02-20 10:15:00'),
(102, 'TXN-2026-002', 2, 1, 1, 25.50,   'cash',        'completed', '2026-02-20 11:30:00'),
(103, 'TXN-2026-003', 3, 2, 5, 120.00,  'transfer',    'completed', '2026-02-21 09:00:00'),
(101, 'TXN-2026-004', 4, 1, 1, 750.00,  'crypto',      'completed', '2026-02-21 15:45:00'),
(105, 'TXN-2026-005', 1, 3, 3, 45.00,   'credit_card', 'pending',   '2026-02-22 18:20:00'),
(102, 'TXN-2026-006', 5, 2, 10, 250.00, 'cash',        'completed', '2026-02-23 08:10:00'),
(104, 'TXN-2026-007', 2, 1, 1, 500.00,  'transfer',    'canceled',  '2026-02-24 12:00:00'),
(106, 'TXN-2026-008', 6, 3, 2, 30.00,   'credit_card', 'completed', '2026-02-25 14:30:00'),
(101, 'TXN-2026-009', 3, 1, 1, 750.00,  'crypto',      'completed', '2026-02-26 11:00:00'),
(103, 'TXN-2026-010', 7, 2, 4, 96.00,   'cash',        'completed', '2026-02-26 16:45:00');


INSERT INTO sales_source_db.sales 
(transaction_id, customer_id, product_id, store_id, quantity, unit_price, discount_amount, sale_date)
VALUES 
('TXN-001', 101, 50, 1, 2, 25.00, 5.00, '2026-02-25 10:30:00'),
('TXN-002', 102, 55, 2, 1, 100.00, 0.00, '2026-02-26 12:00:00'),
('TXN-003', 103, 50, 1, 5, 25.00, 10.00, '2026-02-26 14:15:00');

-- Insertar Productos
INSERT INTO sales_source_db.products (name, category, cost_price) VALUES 
('Laptop Pro', 'Electrónica', 800.00),
('Mouse Inalámbrico', 'Accesorios', 15.00),
('Monitor 4K', 'Electrónica', 250.00);

-- Insertar Clientes
INSERT INTO sales_source_db.customers (full_name, email, country) VALUES 
('Abel DE', 'abel@example.com', 'Perú'),
('Maria Lopez', 'maria.l@gmail.com', 'México'),
('John Doe', 'jdoe@outlook.com', 'USA');

-- Insertar Tiendas
INSERT INTO sales_source_db.stores (store_name, city, region) VALUES 
('Tienda Centro', 'Lima', 'LATAM'),
('Online Store', 'N/A', 'Global');