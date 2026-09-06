---
title: 01 · Data Loading
---

Every way data can enter a Databricks lakehouse — from a nightly CSV dump
to a continuous CDC stream. This is where the course starts.

:::warning 🚧 Module in progress
Lessons are outlined; content lands as videos are recorded.
:::

## Lessons

### Core patterns (watch in order)

| # | Lesson | What it answers |
|---|--------|-----------------|
| 1 | [Batch Loading](/docs/data-loading/batch-loading) | "Load a chunk of data on a schedule" |
| 2 | [Auto Loader](/docs/data-loading/auto-loader) | "Files keep landing in S3 — pick up the new ones" |
| 3 | [Micro-Batches](/docs/data-loading/micro-batches) | "Near-real-time, but small scheduled chunks are fine" |
| 4 | [Streaming](/docs/data-loading/streaming) | "Process events continuously as they arrive" |
| 5 | [CDC](/docs/data-loading/change-data-capture) | "Replicate changes from a source database" |
| 6 | [MERGE & SCD](/docs/data-loading/merge-scd) | "Apply upserts idempotently" → bridge to module 02 |

### Extended sources (any order)

| # | Lesson | What it answers |
|---|--------|-----------------|
| 7 | [Message Queues](/docs/data-loading/message-queues) | Kafka / Event Hubs / Kinesis as sources |
| 8 | [Change Data Feed](/docs/data-loading/change-data-feed) | CDC *between* Delta tables |
| 9 | [JDBC & Federation](/docs/data-loading/jdbc-federation) | Query external databases in place |
| 10 | [Zerobus Ingest](/docs/data-loading/zerobus) | Push-based streaming, no message bus |
| 11 | [Lakeflow Connect](/docs/data-loading/lakeflow-connect) | Managed SaaS connectors |
| 12 | [Custom Sources](/docs/data-loading/custom-sources) | REST APIs via the Python Data Source API |
| 13 | [Delta Sharing](/docs/data-loading/delta-sharing) | Consuming shared data |

## Demo datasets

All hands-on demos use free public data (NOAA weather, OpenAQ air quality).
See [Demo Datasets](/docs/data-loading/datasets).

## Prerequisites

- A Databricks workspace — see [Getting Started](/docs/getting-started)
- No prior Spark knowledge assumed for lesson 1
