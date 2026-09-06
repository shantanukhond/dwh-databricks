# Demo Environment — Lakebase source + generators

Everything the course demos run against. One-time setup, then the "days"
scripts simulate the business changing.

## What's here

| File | Purpose |
|------|---------|
| `lakebase.py` | Connection helper — auth via your Databricks identity (OAuth token). Import it from every notebook. |
| `seed_day0.sql` | Creates `app.customers` + `app.orders`, loads day 0 (10 customers, 15 orders) |
| `events_day1.sql` | City change (→ Type 2), email change + typo fix (→ Type 1), new signup |
| `events_day2.sql` | Second move for the same customer (Type 2 chain) + **order for a nonexistent customer** (early-arriving fact) |
| `events_day3.sql` | Customer 999 finally arrives (placeholder member catch-up) |
| `generate_orders.py` | Continuous random orders — live input for streaming / micro-batch / CDC lessons |
| `generate_files.py` | Drops JSON files into a UC volume — live input for the Auto Loader lesson |

## One-time setup

1. **Create the Lakebase instance** — workspace app switcher → *Lakebase Postgres* → create instance `dwh-course` (defaults are fine).
2. **Copy the host** — Instance → *Connect* → hostname. Put it in `lakebase.py` (`DEFAULTS["host"]`) or export `LAKEBASE_HOST`.
3. **Create the database** — in the Lakebase UI or `psql`: `CREATE DATABASE dwh_course;`
4. **Install the driver** in notebooks: `%pip install psycopg2-binary`
5. **Seed** — run the cells below in a notebook (files uploaded as workspace files), or locally with `psql`.

## The demo "week"

```text
seed_day0.sql      → baseline; module 01 batch lesson reads this
events_day1.sql    → run between batch and CDC lessons
events_day2.sql    → the tricky day (Type 2 chain + early-arriving fact)
events_day3.sql    → resolution (placeholder member patched up)
generate_orders.py → leave running during streaming/micro-batch/CDC lessons
generate_files.py  → leave running during the Auto Loader lesson
```

## Running the SQL scripts

In a notebook:

```python
from lakebase import connect, run_file
with connect() as conn:
    run_file(conn, "seed_day0.sql")
```

From your laptop (Databricks CLI configured, `psql` installed):

```bash
psql "$(python -c "from lakebase import *; print(f'host={_resolve(\"host\")} dbname={_resolve(\"database\")} user={_current_user()} password={_oauth_token()} sslmode=require')")" \
     -f seed_day0.sql
```

## The bronze contract

Module 01's job is to land this data in the lakehouse; module 02 (SCD)
consumes exactly these two tables — nothing else:

```text
sandbox.bronze.customers_raw   ← full/incremental/CDC loads from app.customers
sandbox.bronze.orders_raw      ← from app.orders
```

`dim_customers` (silver) is built in module 02 from `customers_raw`.
