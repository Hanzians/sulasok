USE milktea;

CREATE TABLE IF NOT EXISTS orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    item VARCHAR(100),
    quantity INT,
    amount DECIMAL(10, 2),
    date_ordered DATE
);
INSERT INTO orders (item, quantity, amount, date_ordered) VALUES
('Classic Milk Tea', 2, 200.00, DATE('now')),
('Taro Milk Tea', 1, 100.00, DATE('now'));
    
