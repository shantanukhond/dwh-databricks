---
title: Demo Environment
---

:::warning 🚧 Coming soon
Scripts exist in the repo ([`scripts/lakebase/`](https://github.com/shantanukhond/dwh/tree/main/scripts/lakebase));
this page gets the full walkthrough when the videos are recorded.
:::

## The story

A tiny e-commerce app runs on **Lakebase** (Databricks' managed Postgres) —
two tables, `app.customers` and `app.orders`. Business happens day by day,
and each lesson watches the data arrive through a different loading pattern.

```
Lakebase (Postgres)              Unity Catalog
┌──────────────────┐             ┌─────────────────────────────┐
│ app.customers    │── batch ──► │ sandbox.bronze.customers_raw│
│ app.orders       │── CDC ────► │ sandbox.bronze.orders_raw   │
└──────────────────┘             └─────────────────────────────┘
        ▲                                    │
   day-by-day                                ▼ module 02
   event scripts                    sandbox.silver.dim_customers
```

## The demo "week"

| Day | Script | What happens | Feeds lesson |
|-----|--------|--------------|--------------|
| 0 | `seed_day0.sql` | 10 customers, 15 orders | [Batch Loading](/docs/data-loading/batch-loading) |
| 1 | `events_day1.sql` | City change (Type 2), email change + typo fix (Type 1), new signup | [CDC](/docs/data-loading/change-data-capture), [MERGE & SCD](/docs/data-loading/merge-scd) |
| 2 | `events_day2.sql` | Same customer moves *again* + **order for a customer who doesn't exist** | Type 2 chain · [Early-Arriving Facts](/docs/scd/early-arriving-facts) |
| 3 | `events_day3.sql` | Customer 999 finally signs up | Early-arriving fact resolution |

## Live generators

| Generator | Used in | What it does |
|-----------|---------|--------------|
| `generate_orders.py` | [Streaming](/docs/data-loading/streaming), [Micro-Batches](/docs/data-loading/micro-batches), CDC | Inserts random orders into Lakebase at a steady rate (and occasionally a new customer) |
| `generate_files.py` | [Auto Loader](/docs/data-loading/auto-loader) | Drops small JSON files into a UC volume on a timer |

## Source per lesson

| Lesson | Source |
|--------|--------|
| Batch Loading | Lakebase via JDBC (`app.customers`) |
| Auto Loader | UC volume + `generate_files.py` |
| Micro-Batches | Lakebase polling / `rate` source |
| Streaming | `rate` source + `generate_orders.py` |
| CDC | Lakebase changes → lakehouse |
| Message Queues | Kafka (managed trial) |
| Change Data Feed | Delta `table_changes()` |
| JDBC & Federation | The same Lakebase instance |
| Zerobus | Python producer |
| Delta Sharing | Databricks Marketplace free share |

## The bronze contract

Module 01 lands exactly two tables; module 02 builds SCD dimensions from them
and nothing else:

- `sandbox.bronze.customers_raw`
- `sandbox.bronze.orders_raw`

## Setup

See [Getting Started](/docs/getting-started) for the Lakebase + volume
prerequisites, then follow [`scripts/lakebase/README.md`](https://github.com/shantanukhond/dwh/tree/main/scripts/lakebase).
