"""Continuous random order generator — the "business keeps happening" script.

Inserts random orders into app.orders at a steady clip, so the streaming,
micro-batch, and CDC lessons have something live to chew on.

Run inside a Databricks notebook (after %pip install psycopg2-binary):

    from generate_orders import run
    run(minutes=10, per_minute=6)          # ~60 orders over 10 minutes

…or locally against Lakebase (Databricks CLI profile configured):

    LAKEBASE_HOST=... python generate_orders.py --minutes 10 --per-minute 6
"""

from __future__ import annotations

import argparse
import random
import time

from lakebase import connect, scalar

FIRST_NAMES = ["Asha", "Marco", "Priya", "Tom", "Lena", "Omar", "John", "Mei",
               "Sofia", "Diego", "Yuki", "Grace", "Nina", "Alex", "Ravi"]
CITIES = ["Bengaluru", "Mexico City", "Mumbai", "Berlin", "Hamburg", "Dubai",
          "Austin", "Singapore", "Milan", "Bogotá", "Tokyo", "Arlington"]
PLANS = ["free", "pro"]
STATUSES = ["placed", "placed", "placed", "shipped"]   # skew toward 'placed'


def _existing_customer_ids(conn) -> list[int]:
    with conn.cursor() as cur:
        cur.execute("SELECT customer_id FROM app.customers ORDER BY customer_id")
        return [r[0] for r in cur.fetchall()]


def insert_random_order(conn, customer_ids: list[int], order_id: int) -> None:
    with conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO app.orders (order_id, customer_id, amount, status)
            VALUES (%s, %s, %s, %s)
            """,
            (
                order_id,
                random.choice(customer_ids),
                round(random.uniform(5, 500), 2),
                random.choice(STATUSES),
            ),
        )


def maybe_signup_new_customer(conn, customer_ids: list[int], p: float = 0.05) -> None:
    """Occasionally a brand-new customer appears — keeps CDC/SCD inputs alive."""
    if random.random() > p:
        return
    new_id = max(customer_ids + [100]) + 1
    name = f"{random.choice(FIRST_NAMES)} {random.choice(['K', 'M', 'S', 'L'])}."
    with conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO app.customers (customer_id, name, email, city, plan, created_at)
            VALUES (%s, %s, %s, %s, %s, CURRENT_DATE)
            ON CONFLICT (customer_id) DO NOTHING
            """,
            (new_id, name, f"user{new_id}@example.com",
             random.choice(CITIES), random.choice(PLANS)),
        )
    print(f"  + new customer {new_id} ({name})")


def run(minutes: float = 10.0, per_minute: float = 6.0) -> None:
    interval = 60.0 / per_minute
    deadline = time.monotonic() + minutes * 60.0
    n = 0

    with connect() as conn:
        customer_ids = _existing_customer_ids(conn)
        if not customer_ids:
            raise RuntimeError("app.customers is empty — run seed_day0.sql first")
        next_id = (scalar(conn, "SELECT COALESCE(MAX(order_id), 1000) FROM app.orders") or 1000) + 1

        print(f"Generating ~{per_minute:.0f} orders/min for {minutes:.0f} min "
              f"(starting at order_id {next_id}) …")
        while time.monotonic() < deadline:
            insert_random_order(conn, customer_ids, next_id)
            next_id += 1
            n += 1
            maybe_signup_new_customer(conn, customer_ids)
            customer_ids = _existing_customer_ids(conn)
            if n % 10 == 0:
                print(f"  …{n} orders inserted")
            time.sleep(interval)

    print(f"Done — {n} orders inserted.")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--minutes", type=float, default=10.0)
    ap.add_argument("--per-minute", type=float, default=6.0)
    args = ap.parse_args()
    run(minutes=args.minutes, per_minute=args.per_minute)
