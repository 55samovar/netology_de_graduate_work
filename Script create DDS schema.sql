CREATE SCHEMA dds;

-- Измерение филиалов
CREATE TABLE dds.dim_branch (
    branch_id SERIAL PRIMARY KEY,
    branch_code CHAR(1) UNIQUE NOT NULL,
    city VARCHAR(255) NOT NULL
);

-- Измерение клиентов
CREATE TABLE dds.dim_customer (
    customer_id NUMERIC PRIMARY KEY,
    customer_type VARCHAR(50) NOT NULL,
    customer_gender VARCHAR(10) NOT NULL
);

-- Измерение способов оплаты
CREATE TABLE dds.dim_payment (
    payment_id SERIAL PRIMARY KEY,
    payment_method VARCHAR(50) UNIQUE NOT NULL
);

-- Измерение товаров
CREATE TABLE dds.dim_product (
    product_id SERIAL PRIMARY KEY,
    product_line VARCHAR(255) UNIQUE NOT NULL,
    unit_price FLOAT4 NOT NULL
);

-- Измерение времени
CREATE TABLE dds.dim_time (
    time_id SERIAL PRIMARY KEY,
    date DATE NOT NULL,
    year INTEGER NOT NULL,
    month INTEGER NOT NULL,
    day INTEGER NOT NULL,
    day_of_week VARCHAR(15) NOT NULL
);

-- Факты продаж
CREATE TABLE dds.fact_sales (
    sale_id SERIAL PRIMARY KEY,
    time_id INTEGER REFERENCES dds.dim_time(time_id),
    branch_id INTEGER REFERENCES dds.dim_branch(branch_id),
    customer_id NUMERIC REFERENCES dds.dim_customer(customer_id),
    product_id INTEGER REFERENCES dds.dim_product(product_id),
    payment_id INTEGER REFERENCES dds.dim_payment
)