"""Lakebase connection helper for the DWH-on-Databricks course.

Local-first: reads connection details from `.env` in this directory
(or real environment variables). Copy `.env.example` to `.env` and fill it in.

Auth options (checked in this order):
  1. Personal Access Token  — DATABRICKS_HOST + DATABRICKS_TOKEN in .env
     (the SDK exchanges it for a short-lived Lakebase OAuth token)
  2. Inside a Databricks notebook — ambient identity via databricks-sdk

Usage (locally):

    cd scripts/lakebase
    source ../../.venv/bin/activate
    python events_day1.py

In a Databricks notebook:

    %pip install psycopg2-binary
    from lakebase import connect, run_file
"""

from __future__ import annotations

import os
from contextlib import contextmanager
from pathlib import Path
from typing import Optional
from urllib.parse import unquote, urlparse

from dotenv import load_dotenv

# Load .env sitting next to this file (no-op if it doesn't exist)
load_dotenv(Path(__file__).parent / ".env")

import psycopg2  # noqa: E402


def _env(key: str, default=None):
    return os.environ.get(key, default)


# ---------------------------------------------------------------------------
# Auth helpers
# ---------------------------------------------------------------------------

def _workspace_client():
    """databricks-sdk client, configured from DATABRICKS_HOST/TOKEN (or CLI
    profile env vars) when local, or ambient identity inside a workspace."""
    try:
        from databricks.sdk import WorkspaceClient
    except ImportError as e:
        raise RuntimeError(
            "databricks-sdk not installed. Run: pip install -r requirements.txt"
        ) from e
    return WorkspaceClient()  # SDK auto-reads DATABRICKS_HOST / DATABRICKS_TOKEN


def _database_credential(client, instance_name: str) -> str:
    """Short-lived Lakebase Postgres password, minted via the Database
    Instances API — works regardless of how the client itself authenticated
    (PAT, OAuth, ambient identity), unlike `client.config.oauth_token()`."""
    cred = client.database.generate_database_credential(instance_names=[instance_name])
    return cred.token


def _current_user(client) -> str:
    """Postgres username = your Databricks identity (email)."""
    user = client.current_user.me().user_name
    if not user:
        raise RuntimeError("Could not resolve Databricks user identity.")
    return user


def _conn_params_from_url(url: str) -> dict:
    """Parse `postgresql://user@host/db?sslmode=require` (password omitted —
    it's injected separately as the short-lived OAuth token)."""
    parsed = urlparse(url)
    return {
        "host": parsed.hostname,
        "port": parsed.port or 5432,
        "dbname": parsed.path.lstrip("/") or None,
        "user": unquote(parsed.username) if parsed.username else None,
        "sslmode": (parsed.query.split("sslmode=")[-1].split("&")[0]
                    if "sslmode=" in parsed.query else "require"),
    }


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

@contextmanager
def connect(database: Optional[str] = None, autocommit: bool = True):
    """Open a psycopg2 connection to Lakebase. Yields the connection."""
    url = _env("LAKEBASE_URL")
    if url:
        params = _conn_params_from_url(url)
    else:
        host = _env("LAKEBASE_HOST")
        if not host:
            raise ValueError(
                "Neither LAKEBASE_URL nor LAKEBASE_HOST is set. Copy "
                ".env.example to .env and paste the connection string (or "
                "hostname) from Lakebase UI → your instance → Connect."
            )
        params = {
            "host": host,
            "port": int(_env("LAKEBASE_PORT", "5432")),
            "dbname": _env("LAKEBASE_DATABASE", "dwh_course"),
            "user": None,
            "sslmode": "require",
        }

    client = _workspace_client()
    instance_name = _env("LAKEBASE_INSTANCE_NAME", "dwh-course")

    conn = psycopg2.connect(
        host=params["host"],
        port=params["port"],
        dbname=database or params["dbname"] or "dwh_course",
        user=_env("DATABRICKS_USER") or params["user"] or _current_user(client),
        password=_database_credential(client, instance_name),
        sslmode=params["sslmode"],
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
