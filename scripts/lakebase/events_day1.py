#!/usr/bin/env python3
"""Day 1 · Business events — city change, email change, typo fix, new signup."""

from lakebase import connect, run_file

if __name__ == "__main__":
    with connect() as conn:
        run_file(conn, "events_day1.sql")
    print("✔ Day 1 applied")
