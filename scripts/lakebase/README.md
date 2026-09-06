# Demo Environment — Lakebase source + generators

Everything the course demos run against. Scripts run **locally** (your laptop)
against Lakebase over TLS — one-time setup, then the "days" scripts simulate
the business changing.

## What's here

| File | Purpose |
|------|---------|
| `lakebase.py` | Connection helper — reads `.env`, auth via PAT → short-lived Lakebase OAuth token |
| `seed_day0.py` / `.sql` | Creates `retail.customers` + `retail.orders`, loads day 0 (10 customers, 15 orders) |
| `events_day1.py` / `.sql` | City change (→ Type 2), email change + typo fix (→ Type 1), new signup |
| `events_day2.py` / `.sql` | Second move for the same customer (Type 2 chain) + **order for a nonexistent customer** (early-arriving fact) |
| `events_day3.py` / `.sql` | Customer 999 finally arrives (placeholder member catch-up) |
| `generate_orders.py` | Continuous random orders — live input for streaming / micro-batch / CDC lessons |
| `generate_files.py` | Drops JSON files into a UC volume — live input for the Auto Loader lesson |

## One-time setup

1. **Lakebase**: workspace app switcher → *Lakebase Postgres* → create instance
   `dwh-course`. Copy the hostname from *Instance → Connect*.
2. **Database**: `CREATE DATABASE dwh_course;` (Lakebase UI query editor or psql).
3. **Config**:

   ```bash
   cd scripts/lakebase
   cp .env.example .env   # fill in LAKEBASE_HOST, DATABRICKS_HOST, DATABRICKS_TOKEN
   ```

   Get the PAT at *Workspace → User Settings → Developer → Access tokens*.
4. **Python env** (from the repo root):

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r scripts/lakebase/requirements.txt
   ```

## Schema isolation

All source tables live in the `retail` Postgres schema (`retail.customers`,
`retail.orders`), not `public`. Every module/demo gets its own schema in the
same Lakebase database instead of a shared namespace — e.g. a future
CDC-specific lesson would seed into `cdc.*` rather than reusing `retail.*`.
`seed_day0.sql` creates the schema (`CREATE SCHEMA IF NOT EXISTS retail;`).

## The demo "week"

```bash
cd scripts/lakebase && source ../../.venv/bin/activate

python seed_day0.py        # baseline — module 01 batch lesson reads this
python events_day1.py      # run between batch and CDC lessons
python events_day2.py      # the tricky day (Type 2 chain + early-arriving fact)
python events_day3.py      # resolution (placeholder member patched up)

python generate_orders.py --minutes 10 --per-minute 6   # during streaming/CDC lessons
python generate_files.py /Volumes/sandbox/ingest/landing/orders --minutes 10
```

> `generate_files.py` targets a UC volume — run that one **in the Databricks
> notebook** (volumes aren't writable from your laptop), or use the
> Databricks CLI/SDK variant noted in the Auto Loader lesson.

## The bronze contract

Module 01's job is to land this data in the lakehouse; module 02 (SCD)
consumes exactly these two tables — nothing else:

```text
sandbox.bronze.customers_raw   ← full/incremental/CDC loads from retail.customers
sandbox.bronze.orders_raw      ← from retail.orders
```

`dim_customers` (silver) is built in module 02 from `customers_raw`.
