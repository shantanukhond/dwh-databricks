#!/usr/bin/env python3
"""Day 0 · Seed the demo OLTP schema (wrapper around seed_day0.sql)."""

from lakebase import connect, run_file

if __name__ == "__main__":
    with connect() as conn:
        run_file(conn, "seed_day0.sql")
    print("✔ Day 0 seeded: retail.customers (10) + retail.orders (15)")
