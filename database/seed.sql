--------------------------------------------------
-- Customers
--------------------------------------------------

INSERT INTO customers (name, email, city, signup_date) VALUES
('Alice Johnson', 'alice@example.com', 'New York', '2024-01-15'),
('Bob Smith', 'bob@example.com', 'Chicago', '2024-02-10'),
('Charlie Brown', 'charlie@example.com', 'New York', '2024-03-05'),
('David Wilson', 'david@example.com', 'Seattle', '2024-03-20'),
('Emma Davis', 'emma@example.com', 'Boston', '2024-04-12');

--------------------------------------------------
-- Products
--------------------------------------------------

INSERT INTO products (product_name, category, price) VALUES
('Laptop', 'Electronics', 1200.00),
('Mouse', 'Electronics', 25.00),
('Keyboard', 'Electronics', 75.00),
('Office Chair', 'Furniture', 250.00),
('Desk', 'Furniture', 400.00);

--------------------------------------------------
-- Orders
--------------------------------------------------

INSERT INTO orders (customer_id, order_date, status, total_amount) VALUES
(1, '2024-05-01', 'Completed', 1250.00),
(2, '2024-05-03', 'Completed', 425.00),
(3, '2024-05-08', 'Pending', 75.00),
(1, '2024-06-10', 'Completed', 250.00),
(4, '2024-06-15', 'Completed', 1200.00),
(5, '2024-06-20', 'Cancelled', 400.00);

--------------------------------------------------
-- Order Items
--------------------------------------------------

INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES
(1, 1, 1, 1200.00),
(1, 2, 2, 25.00),

(2, 5, 1, 400.00),
(2, 2, 1, 25.00),

(3, 3, 1, 75.00),

(4, 4, 1, 250.00),

(5, 1, 1, 1200.00),

(6, 5, 1, 400.00);

--------------------------------------------------
-- Payments
--------------------------------------------------

INSERT INTO payments (order_id, payment_method, payment_status, amount, payment_date) VALUES
(1, 'Credit Card', 'Paid', 1250.00, '2024-05-01'),
(2, 'UPI', 'Paid', 425.00, '2024-05-03'),
(3, 'Credit Card', 'Pending', 75.00, '2024-05-08'),
(4, 'Debit Card', 'Paid', 250.00, '2024-06-10'),
(5, 'Credit Card', 'Paid', 1200.00, '2024-06-15'),
(6, 'UPI', 'Failed', 400.00, '2024-06-20');

--------------------------------------------------
-- Refunds
--------------------------------------------------

INSERT INTO refunds (
    payment_id,
    refund_amount,
    refund_reason,
    refund_date,
    refund_status
) VALUES
(2, 50.00, 'Damaged item', '2024-05-10', 'Approved'),
(5, 1200.00, 'Order returned', '2024-06-18', 'Approved');