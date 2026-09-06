-- Day 2 · Business events — the tricky day
--
--   * cust 3 moves AGAIN (Pune→Mumbai happened day 1, now Mumbai→Goa)
--         → produces a multi-version Type 2 chain
--   * order #5051 arrives for customer 999 WHO DOES NOT EXIST YET
--         → the early-arriving fact (foreign key removed just for this insert)
--   * customer 999's dimension row arrives TOMORROW (events_day3.sql)

BEGIN;

SET search_path = app, public;

-- Priya moves again: Mumbai → Goa
UPDATE app.customers
SET city = 'Goa', updated_at = now()
WHERE customer_id = 3;

-- The early-arriving fact. We drop the FK, insert, restore the FK as
-- NOT VALID so future rows are still checked.
ALTER TABLE app.orders DROP CONSTRAINT orders_customer_id_fkey;

INSERT INTO app.orders (order_id, customer_id, amount, status)
VALUES (5051, 999, 499.99, 'placed');

ALTER TABLE app.orders
ADD CONSTRAINT orders_customer_id_fkey
FOREIGN KEY (customer_id) REFERENCES app.customers (customer_id) NOT VALID;

-- Regular traffic continues
INSERT INTO app.orders (order_id, customer_id, amount, status)
VALUES
    (1020,  2,  66.40, 'placed'),
    (1021, 10,  38.75, 'placed');

COMMIT;

-- The smoking gun: an order whose customer doesn't exist
SELECT o.order_id, o.customer_id, c.name
FROM app.orders o
LEFT JOIN app.customers c USING (customer_id)
WHERE c.customer_id IS NULL;
