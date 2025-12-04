"""Reusable ingestion utilities for the Streamlit app."""

import re
from typing import Set

import numpy as np
import pandas as pd


def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    clean = (
        df.rename(
            columns=lambda col: re.sub(r"[^a-z0-9_]", "_", re.sub(r"\s+", "_", col.strip().lower()))
        )
        .pipe(lambda d: d.loc[:, ~d.columns.duplicated()])
    )
    return clean


def safe_numeric(series: pd.Series) -> pd.Series:
    cleaned = (
        series.astype(str)
        .str.replace(r"[₡$€,,%]", "", regex=True)
        .str.replace(",", "", regex=False)
        .replace("", np.nan)
    )
    return pd.to_numeric(cleaned, errors="coerce")


def coerce_numeric_columns(df: pd.DataFrame, required_numeric: Set[str]) -> pd.DataFrame:
    """Convert required numeric columns to numeric and coerce optional numeric-like fields."""

    payload = df.copy()
    object_columns = set(payload.select_dtypes(include=["object"]).columns)

    for col in object_columns:
        converted = safe_numeric(payload[col])
        if col in required_numeric or converted.notna().sum() > 0:
            payload[col] = converted

    for col in required_numeric - object_columns:
        if col in payload.columns:
            payload[col] = safe_numeric(payload[col])

    return payload

