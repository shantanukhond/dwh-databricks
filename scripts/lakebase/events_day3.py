#!/usr/bin/env python3
"""Day 3 · Resolution — customer 999 finally signs up."""

from lakebase import connect, run_file

if __name__ == "__main__":
    with connect() as conn:
        run_file(conn, "events_day3.sql")
    print("✔ Day 3 applied (order 5051 now resolves to Grace Hopper)")
