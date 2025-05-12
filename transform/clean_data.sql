
-- Clean customers
CREATE OR REPLACE TABLE customers_clean AS
SELECT 
    *,
    CASE 
        WHEN lower(gender) IN ('m', 'male') THEN 'Male'
        WHEN lower(gender) IN ('f', 'female') THEN 'Female'
        ELSE 'Other'
    END AS gender_clean,
    CASE 
        WHEN lower(CAST(is_active AS TEXT)) IN ('true', '1') THEN TRUE
        ELSE FALSE
    END AS is_active_clean
FROM customers;

-- Clean suppliers
CREATE OR REPLACE TABLE suppliers_clean AS
SELECT 
    *,
    CASE 
        WHEN lower(CAST(active AS TEXT)) IN ('true', 'yes', 'y', '1') THEN TRUE
        ELSE FALSE
    END AS active_clean
FROM suppliers;

-- Clean employees
CREATE OR REPLACE TABLE employees_clean AS
SELECT 
    *,
    CASE 
        WHEN lower(CAST(is_active AS TEXT)) IN ('true', '1') THEN TRUE
        ELSE FALSE
    END AS is_active_clean
FROM employees;

-- Clean products
CREATE OR REPLACE TABLE products_clean AS
SELECT 
    *,
    CASE 
        WHEN price < 0 THEN 0
        ELSE price
    END AS price_clean,
    CASE 
        WHEN rating > 5 THEN 5
        WHEN rating < 0 THEN 0
        ELSE rating
    END AS rating_clean
FROM products;

-- Clean orders
CREATE OR REPLACE TABLE orders_clean AS
SELECT 
    *,
    CASE 
        WHEN price_per_unit < 0 THEN 0
        ELSE price_per_unit
    END AS price_per_unit_clean
FROM orders;

-- Clean feedback: add synthetic key for duplicate detection
CREATE OR REPLACE TABLE feedback_clean AS
SELECT 
    *,
    CONCAT(supplier_id, '_', submitted_at) AS feedback_id
FROM feedback;

-- Clean deliveries: just verify unique delivery_id
CREATE OR REPLACE TABLE deliveries_clean AS
SELECT * FROM deliveries;
