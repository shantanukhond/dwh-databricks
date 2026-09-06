"""Lakebase connection helper for the DWH-on-Databricks course.

Lakebase is Databricks' managed Postgres. Auth is your Databricks identity:
the password is a short-lived OAuth token minted from the workspace.

Usage in a Databricks notebook:

    %pip install psycopg2-binary
    from lakebase import connect          # upload scripts/lakebase/ as workspace files

    with connect() as conn:
        run_file(conn, "seed_day0.sql")

Locally (with the Databricks CLI profile configured):

    LAKEBASE_HOST=... python events_day1.py
"""

from __future__ import annotations

import os
from contextlib import contextmanager
from typing import Optional

# ---------------------------------------------------------------------------
# Configuration — override via environment variables or by editing DEFAULTS.
# `host` is the one thing you MUST set after creating your Lakebase instance.
# ---------------------------------------------------------------------------
DEFAULTS = {
    "host": None,                    # e.g. "instance-xyz.database.cloud.databricks.com"
    "port": 5432,
    "database": "dwh_course",
    "instance": "dwh-course",        # Lakebase instance name in the workspace
}

# psycopg2 is present on classic clusters; on serverless install it via
# %pip install psycopg2-binary  (notebook-scoped)
import psycopg2  # noqa: E402


def _resolve(key: str):
    """Environment variable wins, then DEFAULTS."""
    return os.environ.get(f"LAKEBASE_{key.upper()}", DEFAULTS.get(key))


def _oauth_token() -> str:
    """Mint a short-lived token from the ambient Databricks identity."""
    try:
        from databricks.sdk import WorkspaceClient

        w = WorkspaceClient()
        return w.config.oauth_token().access_token
    except ImportError:
        # Local fallback: use the CLI-configured PAT if provided
        token = os.environ.get("DATABRICKS_TOKEN")
        if not token:
            raise RuntimeError(
                "databricks-sdk not available and DATABRICKS_TOKEN not set. "
                "Run inside a Databricks notebook or configure the SDK/CLI."
            )
        return token


def _current_user() -> str:
    """Postgres username = your Databricks identity (email)."""
    try:
        from databricks.sdk import WorkspaceClient

        return WorkspaceClient().current_user.me().user_name
    except ImportError:
        user = os.environ.get("DATABRICKS_USER")
        if not user:
            raise RuntimeError(
                "Set DATABRICKS_USER (your Databricks email) for local runs."
            )
        return user


@contextmanager
def connect(database: Optional[str] = None, autocommit: bool = True):
    """Open a psycopg2 connection to Lakebase. Yields the connection."""
    host = _resolve("host")
    if not host:
        raise ValueError(
            "Lakebase host not configured. Set LAKEBASE_HOST or edit DEFAULTS "
            "in lakebase.py — find the host in the Lakebase UI (Instance → Connect)."
        )

    conn = psycopg2.connect(
        host=host,
        port=int(_resolve("port")),
        dbname=database or _resolve("database"),
        user=_current_user(),
        password=_oauth_token(),
        sslmode="require",
        connect_timeout=15,
    )
    conn.autocommit = autocommit
    try:
        yield conn
    finally:
        conn.close()


def run_file(conn, path: str) -> None:
    """Execute every statement in a .sql file (naive ';' splitter — fine for
    our DDL/DML scripts which contain no procedural bodies)."""
    with open(path, "r", encoding="utf-8") as f:
        sql = f.read()
    statements = [s.strip() for s in sql.split(";") if s.strip()]
    with conn.cursor() as cur:
        for stmt in statements:
            cur.execute(stmt)
    print(f"✔ {path}: {len(statements)} statements executed")


def scalar(conn, query: str):
    """Run a query and return the first column of the first row."""
    with conn.cursor() as cur:
        cur.execute(query)
        row = cur.fetchone()
        return row[0] if row else None
