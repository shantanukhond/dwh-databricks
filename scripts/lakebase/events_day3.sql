-- Day 3 · Resolution
--
-- Customer 999 finally signs up — the dimension row that order #5051
-- needed yesterday. In the warehouse, the inferred placeholder member
-- gets patched up (Type 1 update, is_inferred flag cleared).

BEGIN;

SET search_path = app, public;

INSERT INTO app.customers (customer_id, name, email, city, plan, created_at)
VALUES (999, 'Grace Hopper', 'grace@example.com', 'Arlington', 'pro', CURRENT_DATE);

-- Prove the FK is satisfied now and re-validate the constraint
ALTER TABLE app.orders VALIDATE CONSTRAINT orders_customer_id_fkey;

COMMIT;

SELECT o.order_id, o.amount, c.name, c.city
FROM app.orders o
JOIN app.customers c USING (customer_id)
WHERE o.order_id = 5051;
