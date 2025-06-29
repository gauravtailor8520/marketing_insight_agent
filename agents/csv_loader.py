# File: agents/csv_loader.py
"""CSV cleaning and normalization utilities for marketing insight agent."""

from __future__ import annotations

import re
from typing import Union
import pandas as pd

# List of money columns that may contain $ signs or commas
_MONEY_COLS = [
    "acquisition_cost",
]

# Columns expected to be numeric (we'll coerce errors to NaN)
_NUMERIC_COLS = [
    "conversion_rate",
    "roi",
    "clicks",
    "impressions",
    "engagement_score",
]


def _sanitize_money(value: str) -> str:
    """Remove currency symbols, commas, and whitespace from a string representation
    of a monetary value.
    """
    return re.sub(r"[^0-9.\-]", "", str(value)).strip()


def clean_csv(path_or_buffer: Union[str, bytes]) -> pd.DataFrame:
    """Load a marketing‑campaign CSV and return a cleaned Pandas DataFrame.

    Steps performed:
    1. Standardise column names (lower‑snake‑case, trimmed).
    2. Parse the ``date`` column into ``datetime64[ns]``.
    3. Strip currency symbols (e.g. ``$16,174.00`` → ``16174.00``).
    4. Coerce numeric columns to floats / ints; invalid entries become NaN.
    5. Compute ``ctr`` if missing ( ``clicks / impressions`` ).
    6. Drop rows with missing ``campaign_id``.
    """

    # --- Load -------------------------------------------------------------------
    df = pd.read_csv(path_or_buffer)

    # --- Normalise column names -------------------------------------------------
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]

    # --- Parse dates ------------------------------------------------------------
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce")

    # --- Clean monetary values --------------------------------------------------
    for col in _MONEY_COLS:
        if col in df.columns:
            df[col] = df[col].apply(_sanitize_money).replace("", "0").astype(float)

    # --- Coerce numeric columns -------------------------------------------------
    for col in _NUMERIC_COLS:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # --- Derived metrics --------------------------------------------------------
    if "ctr" not in df.columns and {"clicks", "impressions"}.issubset(df.columns):
        with pd.option_context("mode.use_inf_as_na", True):
            df["ctr"] = df["clicks"] / df["impressions"].replace(0, pd.NA)

    # --- Final tidy‑up ----------------------------------------------------------
    if "campaign_id" in df.columns:
        df = df.dropna(subset=["campaign_id"])

    return df.reset_index(drop=True)
