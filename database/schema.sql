-- STEPS TO FOLLOW -
-- 1) PS D:\Deepansh\Nexus> psql -U postgres
-- 2)Password for user postgres: 
-- 3) postgres=# \c nexus

CREATE TABLE regions (
    region_id VARCHAR(10) PRIMARY KEY,
    region_name VARCHAR(100) NOT NULL
);

CREATE TABLE customers (
    customer_id VARCHAR(20) PRIMARY KEY,
    segment VARCHAR(50) NOT NULL,
    region_id VARCHAR(10) NOT NULL,
    join_date DATE NOT NULL,
    status VARCHAR(20) NOT NULL,
    FOREIGN KEY (region_id) REFERENCES regions(region_id)
);

CREATE TABLE products (
    product_id VARCHAR(20) PRIMARY KEY,
    category VARCHAR(50) NOT NULL,
    price NUMERIC(12, 2) NOT NULL,
    cost NUMERIC(12, 2) NOT NULL
);

CREATE TABLE sales_reps (
    rep_id VARCHAR(20) PRIMARY KEY,
    region_id VARCHAR(10) NOT NULL,
    hire_date DATE NOT NULL,
    FOREIGN KEY (region_id) REFERENCES regions(region_id)
);

CREATE TABLE sales (
    sale_id VARCHAR(20) PRIMARY KEY,
    customer_id VARCHAR(20) NOT NULL,
    product_id VARCHAR(20) NOT NULL,
    rep_id VARCHAR(20) NOT NULL,
    sale_date DATE NOT NULL,
    quantity INTEGER NOT NULL,
    unit_price NUMERIC(12, 2) NOT NULL,

    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id),
    FOREIGN KEY (rep_id) REFERENCES sales_reps(rep_id)
);