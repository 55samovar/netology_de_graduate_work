create schema nds

-- Создаем таблицу branch (филиалы)
CREATE TABLE nds.branch (
    branch_id SERIAL PRIMARY KEY,
    branch_code CHAR(1) UNIQUE NOT NULL,
    city VARCHAR(255) NOT NULL
);

-- Создаем таблицу customer (клиенты)
CREATE TABLE nds.customer (
    customer_id NUMERIC PRIMARY KEY,
    customer_type VARCHAR(50) NOT NULL,
    customer_gender VARCHAR(10) NOT NULL
);

-- Создаем таблицу payment (способы оплаты)
CREATE TABLE nds.payment (
    payment_id SERIAL PRIMARY KEY,
    payment_method VARCHAR(50) UNIQUE NOT NULL
);

-- Создаем таблицу product (товары)
CREATE TABLE nds.product (
    product_id SERIAL PRIMARY KEY,
    product_line VARCHAR(255) UNIQUE NOT NULL,
    unit_price FLOAT4 NOT NULL
);

-- Создаем таблицу invoice (чек)
CREATE TABLE nds.invoice (
    invoice_id VARCHAR(50) PRIMARY KEY,
    date DATE NOT NULL,
    time TIME NOT NULL,
    branch_id INTEGER REFERENCES nds.branch(branch_id),
    customer_id NUMERIC REFERENCES nds.customer(customer_id),
    payment_id INTEGER REFERENCES nds.payment(payment_id)
);

-- Создаем таблицу sales (продажи)
CREATE TABLE nds.sale (
    sale_id SERIAL PRIMARY KEY,
    invoice_id VARCHAR(50) REFERENCES nds.invoice(invoice_id),
    product_id INTEGER REFERENCES nds.product(product_id),
    quantity INTEGER NOT NULL,
    tax NUMERIC NOT NULL,
    total NUMERIC NOT NULL,
    cogs NUMERIC NOT NULL,
    gross_income NUMERIC NOT NULL,
    gross_margin_percentage NUMERIC NOT NULL
);