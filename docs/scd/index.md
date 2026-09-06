---
title: 02 · SCD
---

Dimensions change over time — a customer moves, a product is renamed.
SCDs define *how much history* your warehouse keeps when that happens.

:::warning 🚧 Module in progress
Lessons are outlined; content lands as videos are recorded.
:::

## Lessons

| # | Lesson | What it covers |
|---|--------|----------------|
| 1 | [Type 0 — Fixed](/docs/scd/scd-type-0) | Attributes that never change |
| 2 | [Type 1 — Overwrite](/docs/scd/scd-type-1) | Latest value wins, no history |
| 3 | [Type 2 — Full History](/docs/scd/scd-type-2) | One row per change — the workhorse |
| 4 | [Type 3 — Previous Value](/docs/scd/scd-type-3) | One step back in extra columns |
| 5 | [Early-Arriving Facts](/docs/scd/early-arriving-facts) | Facts before dimensions & inferred members |

## Prerequisites

- [Module 01 — Data Loading Types](/docs/data-loading),
  especially [MERGE & SCD](/docs/data-loading/merge-scd)
