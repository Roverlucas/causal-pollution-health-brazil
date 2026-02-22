#!/usr/bin/env python3
"""
Extract all five core tables from the Clima360 Supabase instance.

Uses the Supabase PostgREST API directly via ``requests`` to handle
pagination (default server limit is 1000 rows per request).  Each table
is saved as a Parquet file in ``data/raw/``.

Usage
-----
    python src/data/extract.py          # extract all tables
    python src/data/extract.py weather  # extract only weather_history
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
import time
from pathlib import Path
from typing import Any

import pandas as pd
import requests

# ---------------------------------------------------------------------------
# Project imports
# ---------------------------------------------------------------------------
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from src.utils.config import (
    SUPABASE_URL,
    SUPABASE_ANON_KEY,
    TABLES,
    TABLE_COLUMNS,
    RAW_DIR,
    LOG_FORMAT,
    LOG_DATE_FORMAT,
)

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
logging.basicConfig(format=LOG_FORMAT, datefmt=LOG_DATE_FORMAT, level=logging.INFO)
logger = logging.getLogger("extract")

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
PAGE_SIZE = 1000          # Supabase default row limit
MAX_RETRIES = 5           # retries per page on transient errors
RETRY_BACKOFF = 2.0       # exponential backoff base (seconds)
REQUEST_TIMEOUT = 60      # seconds per HTTP request


# ---------------------------------------------------------------------------
# Core extraction logic
# ---------------------------------------------------------------------------
def _build_headers() -> dict[str, str]:
    """Build HTTP headers for the Supabase REST API."""
    return {
        "apikey": SUPABASE_ANON_KEY,
        "Authorization": f"Bearer {SUPABASE_ANON_KEY}",
        "Content-Type": "application/json",
        "Prefer": "count=exact",          # ask for total row count in header
        "Accept-Profile": "public",
    }


def _fetch_page(
    table: str,
    columns: list[str],
    offset: int,
    limit: int,
    order_col: str = "id",
) -> tuple[list[dict[str, Any]], int | None]:
    """
    Fetch a single page from the Supabase REST endpoint.

    Returns
    -------
    rows : list[dict]
        The deserialized JSON rows.
    total : int or None
        Total row count (from Content-Range header), or None if unavailable.
    """
    url = f"{SUPABASE_URL}/rest/v1/{table}"
    params = {
        "select": ",".join(columns),
        "order": f"{order_col}.asc",
        "offset": str(offset),
        "limit": str(limit),
    }
    headers = _build_headers()
    # Request exact count via Range header
    headers["Range-Unit"] = "items"
    headers["Range"] = f"{offset}-{offset + limit - 1}"

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            resp = requests.get(
                url, headers=headers, params=params, timeout=REQUEST_TIMEOUT
            )
            if resp.status_code == 416:
                # Range not satisfiable — we've gone past the end
                return [], 0
            resp.raise_for_status()
            rows = resp.json()

            # Parse total from Content-Range: "0-999/40581"
            total = None
            cr = resp.headers.get("Content-Range", "")
            if "/" in cr:
                try:
                    total = int(cr.split("/")[1])
                except (ValueError, IndexError):
                    pass

            return rows, total

        except requests.exceptions.RequestException as exc:
            wait = RETRY_BACKOFF ** attempt
            logger.warning(
                "Attempt %d/%d for %s offset=%d failed: %s — retrying in %.1fs",
                attempt, MAX_RETRIES, table, offset, exc, wait,
            )
            time.sleep(wait)

    raise RuntimeError(
        f"Failed to fetch {table} offset={offset} after {MAX_RETRIES} attempts"
    )


def extract_table(table_key: str) -> pd.DataFrame:
    """
    Extract a full table from Supabase with automatic pagination.

    Parameters
    ----------
    table_key : str
        Friendly key in ``config.TABLES`` (e.g. ``"weather"``).

    Returns
    -------
    pd.DataFrame
    """
    table_name = TABLES[table_key]
    columns = TABLE_COLUMNS[table_name]
    logger.info("Extracting table '%s' (%s) ...", table_key, table_name)

    all_rows: list[dict[str, Any]] = []
    offset = 0
    total_known: int | None = None

    while True:
        rows, total = _fetch_page(table_name, columns, offset, PAGE_SIZE)
        if total is not None:
            total_known = total
        if not rows:
            break
        all_rows.extend(rows)
        offset += len(rows)

        pct = (
            f" ({offset}/{total_known}, {100*offset/total_known:.1f}%)"
            if total_known
            else ""
        )
        logger.info("  ... fetched %d rows so far%s", offset, pct)

        # If we received fewer than PAGE_SIZE rows we are done
        if len(rows) < PAGE_SIZE:
            break

    df = pd.DataFrame(all_rows)
    logger.info(
        "Table '%s': %d rows x %d columns extracted.",
        table_key, len(df), len(df.columns),
    )
    return df


def save_parquet(df: pd.DataFrame, table_key: str) -> Path:
    """Save a DataFrame as Parquet in ``data/raw/``."""
    table_name = TABLES[table_key]
    out_path = RAW_DIR / f"{table_name}.parquet"
    df.to_parquet(out_path, index=False, engine="pyarrow")
    size_mb = out_path.stat().st_size / 1024 / 1024
    logger.info("Saved %s (%.2f MB)", out_path, size_mb)
    return out_path


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------
def main(table_keys: list[str] | None = None) -> None:
    """
    Extract tables from Supabase and write Parquet files.

    Parameters
    ----------
    table_keys : list[str] or None
        Subset of keys from ``config.TABLES`` to extract.  If ``None``,
        extract all five tables.
    """
    if table_keys is None:
        table_keys = list(TABLES.keys())

    for key in table_keys:
        if key not in TABLES:
            logger.error("Unknown table key '%s'. Valid keys: %s", key, list(TABLES.keys()))
            continue
        t0 = time.time()
        df = extract_table(key)
        save_parquet(df, key)
        elapsed = time.time() - t0
        logger.info("Table '%s' done in %.1f s.\n", key, elapsed)

    logger.info("Extraction complete.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract Clima360 data from Supabase")
    parser.add_argument(
        "tables",
        nargs="*",
        default=None,
        help=f"Table keys to extract (default: all). Choices: {list(TABLES.keys())}",
    )
    args = parser.parse_args()
    main(args.tables if args.tables else None)
