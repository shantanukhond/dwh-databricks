---
slug: /
title: DWH on Databricks
description: Learn data warehousing with Databricks — a YouTube course
hide_table_of_contents: true
---

# DWH on Databricks

Learn **data warehousing** from the ground up — taught through hands-on
**Databricks** lessons, each with a YouTube video and a runnable notebook.

:::warning 🚧 Work in progress
The course is outlined below. Pages get filled in as videos are recorded.
:::

## Course outline

### 01 — Data Loading Types

Every way data can enter the lakehouse.

1. [Batch Loading](/docs/data-loading/batch-loading)
2. [Auto Loader](/docs/data-loading/auto-loader)
3. [Micro-Batches](/docs/data-loading/micro-batches)
4. [Streaming](/docs/data-loading/streaming)
5. [Change Data Capture (CDC)](/docs/data-loading/change-data-capture)
6. [MERGE & SCD](/docs/data-loading/merge-scd) — bridge into module 02
7. [Message Queues](/docs/data-loading/message-queues)
8. [Change Data Feed](/docs/data-loading/change-data-feed)
9. [JDBC & Lakehouse Federation](/docs/data-loading/jdbc-federation)
10. [Zerobus Ingest](/docs/data-loading/zerobus)
11. [Lakeflow Connect](/docs/data-loading/lakeflow-connect)
12. [Custom Sources](/docs/data-loading/custom-sources)
13. [Delta Sharing](/docs/data-loading/delta-sharing)

➡️ Start here: [Module 01 overview](/docs/data-loading) ·
[Demo datasets](/docs/data-loading/datasets)

### 02 — Slowly Changing Dimensions (SCD)

How warehouses track change over time.

1. [SCD Overview](/docs/scd)
2. [Type 0 — Fixed](/docs/scd/scd-type-0)
3. [Type 1 — Overwrite](/docs/scd/scd-type-1)
4. [Type 2 — Full History](/docs/scd/scd-type-2)
5. [Type 3 — Previous Value](/docs/scd/scd-type-3)
6. [Early-Arriving Facts](/docs/scd/early-arriving-facts)

### Coming later

Medallion architecture · Data modeling · Performance tuning · Orchestration

## How to follow along

- 📺 Watch the video embedded on each lesson page
- 📓 Run the matching notebook from the repo's `notebooks/` folder
- 📖 Use these docs as the written reference
