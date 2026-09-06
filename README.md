# DWH on Databricks — YouTube Course

Learn data warehousing concepts through hands-on Databricks lessons.
Docs site: **https://dwh.shantanukhond.me**

> 🚧 Work in progress — lessons are outlined; content lands as videos are recorded.

## Course outline

### 01 — Data Loading Types ← start here

| # | Lesson | Status |
|---|--------|--------|
| 1 | [Batch Loading](docs/data-loading/batch-loading.md) | 🚧 outline |
| 2 | [Auto Loader](docs/data-loading/auto-loader.md) | 🚧 outline |
| 3 | [Micro-Batches](docs/data-loading/micro-batches.md) | 🚧 outline |
| 4 | [Streaming](docs/data-loading/streaming.md) | 🚧 outline |
| 5 | [Change Data Capture (CDC)](docs/data-loading/change-data-capture.md) | 🚧 outline |
| 6 | [MERGE & SCD](docs/data-loading/merge-scd.md) (bridge to module 02) | 🚧 outline |
| 7 | [Message Queues](docs/data-loading/message-queues.md) (Kafka / Event Hubs / Kinesis) | 🚧 outline |
| 8 | [Change Data Feed](docs/data-loading/change-data-feed.md) | 🚧 outline |
| 9 | [JDBC & Lakehouse Federation](docs/data-loading/jdbc-federation.md) | 🚧 outline |
| 10 | [Zerobus Ingest](docs/data-loading/zerobus.md) | 🚧 outline |
| 11 | [Lakeflow Connect](docs/data-loading/lakeflow-connect.md) (managed connectors) | 🚧 outline |
| 12 | [Custom Data Sources](docs/data-loading/custom-sources.md) | 🚧 outline |
| 13 | [Delta Sharing](docs/data-loading/delta-sharing.md) | 🚧 outline |

### 02 — Slowly Changing Dimensions (SCD)

| # | Lesson | Status |
|---|--------|--------|
| 1 | [SCD overview](docs/scd/index.md) | 🚧 outline |
| 2 | [Type 0 — fixed](docs/scd/scd-type-0.md) | 🚧 outline |
| 3 | [Type 1 — overwrite](docs/scd/scd-type-1.md) | 🚧 outline |
| 4 | [Type 2 — full history](docs/scd/scd-type-2.md) | 🚧 outline |
| 5 | [Type 3 — previous value](docs/scd/scd-type-3.md) | 🚧 outline |
| 6 | [Early-arriving facts](docs/scd/early-arriving-facts.md) | 🚧 outline |

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
