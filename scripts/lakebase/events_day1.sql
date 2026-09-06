-- Day 1 · Business events (run after the batch/CDC lessons have taken day 0)
--
-- These mutations are the raw material for the SCD module:
--   * cust 3 changes CITY   → tracked with history (SCD Type 2)
--   * cust 5 changes EMAIL  → overwrite is fine  (SCD Type 1)
--   * cust 7 name typo fix  → overwrite          (SCD Type 1)
--   * cust 11 signs up      → new member insert

BEGIN;

SET search_path = app, public;

-- Priya moves from Pune to Mumbai
UPDATE app.customers
SET city = 'Mumbai', updated_at = now()
WHERE customer_id = 3;

-- Lena changes her email
UPDATE app.customers
SET email = 'lena.fischer@example.com', updated_at = now()
WHERE customer_id = 5;

-- Typo fix: Jonh → John
UPDATE app.customers
SET name = 'John Smith', updated_at = now()
WHERE customer_id = 7;

-- New customer
INSERT INTO app.customers (customer_id, name, email, city, plan, created_at)
VALUES (11, 'Yuki Tanaka', 'yuki@example.com', 'Tokyo', 'pro', CURRENT_DATE);

-- A handful of new orders through the day
INSERT INTO app.orders (order_id, customer_id, amount, status)
VALUES
    (1016,  1,  59.90, 'placed'),
    (1017, 11, 210.00, 'placed'),
    (1018,  6,  43.25, 'placed'),
    (1019,  4,  92.10, 'shipped');

-- And an order STATUS change (shows updates, not just inserts)
UPDATE app.orders
SET status = 'shipped'
WHERE order_id = 1004;

COMMIT;

SELECT customer_id, name, email, city, updated_at
FROM app.customers
ORDER BY customer_id;
