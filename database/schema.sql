-- Drop existing tables (for reproducible setup)

DROP TABLE IF EXISTS refunds;
DROP TABLE IF EXISTS payments;
DROP TABLE IF EXISTS order_items;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS customers;

--------------------------------------------------
-- Customers
--------------------------------------------------

CREATE TABLE customers (
    customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    city TEXT NOT NULL,
    signup_date DATE NOT NULL
);

--------------------------------------------------
-- Products
--------------------------------------------------

CREATE TABLE products (
    product_id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_name TEXT NOT NULL,
    category TEXT NOT NULL,
    price REAL NOT NULL
);

--------------------------------------------------
-- Orders
--------------------------------------------------

CREATE TABLE orders (
    order_id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER NOT NULL,
    order_date DATE NOT NULL,
    status TEXT NOT NULL,
    total_amount REAL NOT NULL,

    FOREIGN KEY (customer_id)
        REFERENCES customers(customer_id)
);

--------------------------------------------------
-- Order Items
--------------------------------------------------

CREATE TABLE order_items (
    item_id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    unit_price REAL NOT NULL,

    FOREIGN KEY (order_id)
        REFERENCES orders(order_id),

    FOREIGN KEY (product_id)
        REFERENCES products(product_id)
);

--------------------------------------------------
-- Payments
--------------------------------------------------

CREATE TABLE payments (
    payment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER UNIQUE NOT NULL,
    payment_method TEXT NOT NULL,
    payment_status TEXT NOT NULL,
    amount REAL NOT NULL,
    payment_date DATE NOT NULL,

    FOREIGN KEY (order_id)
        REFERENCES orders(order_id)
);

--------------------------------------------------
-- Refunds
--------------------------------------------------

CREATE TABLE refunds (
    refund_id INTEGER PRIMARY KEY AUTOINCREMENT,
    payment_id INTEGER NOT NULL,
    refund_amount REAL NOT NULL,
    refund_reason TEXT,
    refund_date DATE NOT NULL,
    refund_status TEXT NOT NULL,

    FOREIGN KEY (payment_id)
        REFERENCES payments(payment_id)
);