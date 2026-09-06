---
title: Getting Started
---

:::warning 🚧 Coming soon
Setup instructions are outlined here and will be expanded with the first lesson.
:::

## What you'll need

- A **Databricks workspace** (Free Edition is enough for every demo)
- **Lakebase** — the workspace's built-in managed Postgres; our demo "source system"
- **Node.js 22** locally — only if you want to run this docs site yourself

## Environment setup

_To be written in full with lesson 1. The shape of it:_

1. Create a Lakebase instance `dwh-course` (app switcher → Lakebase Postgres)
2. Create catalog + schemas: `sandbox` with `ingest`, `bronze`, `silver`
3. Create the landing volume: `sandbox.ingest.landing` (Auto Loader lesson)
4. Seed the source: run `scripts/lakebase/seed_day0.sql` via the helper in
   [`scripts/lakebase/`](https://github.com/shantanukhond/dwh/tree/main/scripts/lakebase)

## Demo source data

The whole course runs on one tiny e-commerce database (customers + orders)
living in Lakebase, plus two generators for live demos.
See [Demo Environment](data-loading/datasets).

## How notebooks map to lessons

| Docs page | Notebook |
|---|---|
| 01 · Data Loading Types | `notebooks/01-data-loading/` |
| 02 · SCD | `notebooks/02-scd/` |

## Running these docs locally

```bash
npm install
npm start
```
