INSERT INTO sales_source_db.products (name, category, cost_price, supplier_id)
VALUES
('Laptop Pro 14', 'Electronics', 900.00, 101),
('Wireless Mouse', 'Electronics', 10.50, 102),
('Mechanical Keyboard', 'Electronics', 45.00, 102),
('Office Chair', 'Furniture', 120.00, 201),
('Standing Desk', 'Furniture', 250.00, 201),
('Gaming Monitor', 'Electronics', 180.00, 103),
('USB-C Hub', 'Accessories', 15.00, 104),
('External SSD 1TB', 'Electronics', 75.00, 105);


INSERT INTO sales_source_db.customers (full_name, email, country, loyalty_score)
VALUES
('John Smith', 'john.smith@email.com', 'USA', 120),
('Maria Garcia', 'maria.garcia@email.com', 'Spain', 80),
('Carlos Lopez', 'carlos.lopez@email.com', 'Mexico', 50),
('Anna Müller', 'anna.mueller@email.com', 'Germany', 200),
('Lucas Silva', 'lucas.silva@email.com', 'Brazil', 30),
('Yuki Tanaka', 'yuki.tanaka@email.com', 'Japan', 150);

INSERT INTO sales_source_db.stores (store_name, city, region)
VALUES
('Tech Store Lima', 'Lima', 'South America'),
('Tech Store Madrid', 'Madrid', 'Europe'),
('Tech Store Berlin', 'Berlin', 'Europe'),
('Tech Store Tokyo', 'Tokyo', 'Asia');

INSERT INTO sales_source_db.sales
(product_id, transaction_id, customer_id, store_id, quantity, price, payment_method, status, sale_date)
VALUES
(1, 'TXN-10001', 1, 1, 1, 1200.00, 'credit_card', 'completed', '2026-01-10 10:15:00'),
(2, 'TXN-10002', 2, 1, 2, 25.00, 'cash', 'completed', '2026-01-11 11:30:00'),
(3, 'TXN-10003', 3, 2, 1, 70.00, 'transfer', 'completed', '2026-01-12 09:20:00'),
(4, 'TXN-10004', 4, 3, 1, 200.00, 'credit_card', 'completed', '2026-01-12 14:45:00'),
(5, 'TXN-10005', 5, 2, 1, 350.00, 'crypto', 'completed', '2026-01-13 16:10:00'),
(6, 'TXN-10006', 1, 4, 2, 400.00, 'credit_card', 'completed', '2026-01-14 13:00:00'),
(7, 'TXN-10007', 6, 3, 3, 45.00, 'cash', 'completed', '2026-01-15 18:25:00'),
(8, 'TXN-10008', 2, 1, 1, 80.00, 'transfer', 'completed', '2026-01-16 12:40:00');