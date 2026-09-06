-- Day 0 · Seed the demo OLTP schema
-- DWH on Databricks — source database for module 01 (and input to module 02 SCD)
--
-- The storyline: a tiny e-commerce app. Customers mutate over "days";
-- orders reference customers. All dates below are anchors only — the demo
-- treats each script run as one business day.

BEGIN;

CREATE SCHEMA IF NOT EXISTS retail;

SET search_path = retail, public;

-- ---------------------------------------------------------------------------
-- customers — the dimension source
-- email changes are throwaway (→ SCD Type 1)
-- city  changes matter        (→ SCD Type 2)
-- ---------------------------------------------------------------------------
DROP TABLE IF EXISTS retail.customers CASCADE;
CREATE TABLE retail.customers (
    customer_id  INTEGER      PRIMARY KEY,
    name         TEXT         NOT NULL,
    email        TEXT         NOT NULL,
    city         TEXT         NOT NULL,
    plan         TEXT         NOT NULL DEFAULT 'free',
    created_at   DATE         NOT NULL,
    updated_at   TIMESTAMPTZ  NOT NULL DEFAULT now()
);

-- ---------------------------------------------------------------------------
-- orders — the fact source
-- ---------------------------------------------------------------------------
DROP TABLE IF EXISTS retail.orders CASCADE;
CREATE TABLE retail.orders (
    order_id     INTEGER      PRIMARY KEY,
    customer_id  INTEGER      NOT NULL REFERENCES retail.customers (customer_id),
    amount       NUMERIC(10,2) NOT NULL,
    status       TEXT         NOT NULL DEFAULT 'placed',
    order_ts     TIMESTAMPTZ  NOT NULL DEFAULT now()
);

-- ---------------------------------------------------------------------------
-- Day 0 customers (10 rows)
-- ---------------------------------------------------------------------------
INSERT INTO retail.customers (customer_id, name, email, city, plan, created_at) VALUES
    ( 1, 'Asha Verma',    'asha@example.com',    'Bengaluru',  'pro',  DATE '2026-09-01'),
    ( 2, 'Marco Ruiz',    'marco@example.com',   'Mexico City','free', DATE '2026-09-01'),
    ( 3, 'Priya Nair',    'priya@example.com',   'Pune',       'pro',  DATE '2026-09-01'),
    ( 4, 'Tom Becker',    'tom@example.com',     'Berlin',     'free', DATE '2026-09-01'),
    ( 5, 'Lena Fischer',  'lena@example.com',    'Hamburg',    'pro',  DATE '2026-09-01'),
    ( 6, 'Omar Haddad',   'omar@example.com',    'Dubai',      'free', DATE '2026-09-02'),
    ( 7, 'Jonh Smith',    'john@example.com',    'Austin',     'free', DATE '2026-09-02'),  -- note the typo: fixed on day 1
    ( 8, 'Mei Chen',      'mei@example.com',     'Singapore',  'pro',  DATE '2026-09-02'),
    ( 9, 'Sofia Rossi',   'sofia@example.com',   'Milan',      'free', DATE '2026-09-02'),
    (10, 'Diego Torres',  'diego@example.com',   'Bogotá',     'free', DATE '2026-09-02');

-- ---------------------------------------------------------------------------
-- Day 0 orders (15 rows)
-- ---------------------------------------------------------------------------
INSERT INTO retail.orders (order_id, customer_id, amount, status, order_ts) VALUES
    (1001,  1, 129.99, 'placed',    TIMESTAMPTZ '2026-09-01 09:14:00+00'),
    (1002,  3,  54.50, 'placed',    TIMESTAMPTZ '2026-09-01 10:02:00+00'),
    (1003,  2,  12.00, 'shipped',   TIMESTAMPTZ '2026-09-01 10:41:00+00'),
    (1004,  5, 220.00, 'placed',    TIMESTAMPTZ '2026-09-01 11:05:00+00'),
    (1005,  1,  18.75, 'delivered', TIMESTAMPTZ '2026-09-01 12:30:00+00'),
    (1006,  8,  99.00, 'placed',    TIMESTAMPTZ '2026-09-01 13:12:00+00'),
    (1007,  4,  45.10, 'shipped',   TIMESTAMPTZ '2026-09-01 14:47:00+00'),
    (1008,  6, 310.40, 'placed',    TIMESTAMPTZ '2026-09-01 15:03:00+00'),
    (1009, 10,  27.99, 'placed',    TIMESTAMPTZ '2026-09-01 16:22:00+00'),
    (1010,  7,  61.00, 'shipped',   TIMESTAMPTZ '2026-09-01 17:40:00+00'),
    (1011,  9,  88.20, 'placed',    TIMESTAMPTZ '2026-09-01 18:15:00+00'),
    (1012,  3, 142.30, 'delivered', TIMESTAMPTZ '2026-09-02 08:55:00+00'),
    (1013,  5,  33.45, 'placed',    TIMESTAMPTZ '2026-09-02 09:31:00+00'),
    (1014,  2,  74.80, 'placed',    TIMESTAMPTZ '2026-09-02 10:26:00+00'),
    (1015,  8,  19.99, 'shipped',   TIMESTAMPTZ '2026-09-02 11:12:00+00');

COMMIT;

-- Quick check
SELECT 'customers' AS table_name, COUNT(*) AS rows FROM retail.customers
UNION ALL
SELECT 'orders', COUNT(*) FROM retail.orders;
