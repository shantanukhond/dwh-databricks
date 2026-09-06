# DWH on Databricks — YouTube Course

Learn data warehousing concepts through hands-on Databricks lessons.
Docs site: **https://dwh.shantanukhond.me**

> 🚧 Work in progress — lessons are outlined; content lands as videos are recorded.

## Course outline

### 01 — Data Loading Types ← start here

| # | Lesson | Status |
|---|--------|--------|
| 1 | Batch Loading | 🚧 outline |
| 2 | Auto Loader | 🚧 outline |
| 3 | Micro-Batches | 🚧 outline |
| 4 | Streaming | 🚧 outline |
| 5 | Change Data Capture (CDC) | 🚧 outline |
| 6 | MERGE & SCD (bridge to module 02) | 🚧 outline |
| 7 | Message Queues (Kafka / Event Hubs / Kinesis) | 🚧 outline |
| 8 | Change Data Feed | 🚧 outline |
| 9 | JDBC & Lakehouse Federation | 🚧 outline |
| 10 | Zerobus Ingest | 🚧 outline |
| 11 | Lakeflow Connect (managed connectors) | 🚧 outline |
| 12 | Custom Data Sources | 🚧 outline |
| 13 | Delta Sharing | 🚧 outline |

### 02 — Slowly Changing Dimensions (SCD)

| # | Lesson | Status |
|---|--------|--------|
| 1 | SCD overview | 🚧 outline |
| 2 | Type 0 — fixed | 🚧 outline |
| 3 | Type 1 — overwrite | 🚧 outline |
| 4 | Type 2 — full history | 🚧 outline |
| 5 | Type 3 — previous value | 🚧 outline |
| 6 | Late-arriving data | 🚧 outline |

### Coming later

Medallion architecture · Data modeling · Performance tuning · Orchestration

## Repo layout

- `docs/` — Docusaurus docs (lesson pages, deployed to GitHub Pages)
- `notebooks/` — Databricks notebooks, one folder per module
- `docusaurus.config.ts` / `sidebars.ts` — site config & sidebar

## Run docs locally

```bash
npm install
npm start
```

Site opens at http://localhost:3000 with hot reload.

## Deploy

Push to `main` — the GitHub Action in `.github/workflows/deploy.yml` builds
and publishes to GitHub Pages at [dwh.shantanukhond.me](https://dwh.shantanukhond.me).
