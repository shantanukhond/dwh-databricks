#!/usr/bin/env python3
"""Day 2 · The tricky day — second move (Type 2 chain) + early-arriving fact."""

from lakebase import connect, run_file

if __name__ == "__main__":
    with connect() as conn:
        run_file(conn, "events_day2.sql")
    print("✔ Day 2 applied (watch order 5051 — customer 999 doesn't exist yet)")
