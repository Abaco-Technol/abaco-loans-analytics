from typing import Iterable, Optional

import pandas as pd


def validate_dataframe(
    df: pd.DataFrame,
    required_columns: Optional[Iterable[str]] = None,
    numeric_columns: Optional[Iterable[str]] = None,
    date_columns: Optional[Iterable[str]] = None,
) -> None:
    """Basic validation helper used by the ingestion pipeline.

    Raises ValueError on validation failures.
    """
    cols_lower = {str(c).lower() for c in df.columns}

    if required_columns:
        missing = [c for c in required_columns if c.lower() not in cols_lower]
        if missing:
            raise ValueError(f"Missing required columns: {missing}")

    if numeric_columns:
        for col in numeric_columns:
            resolved = None
            for c in df.columns:
                if str(c).lower() == col.lower():
                    resolved = c
                    break
            if resolved:
                coerced = pd.to_numeric(df[resolved], errors="coerce")
                if coerced.notna().any() and coerced.isna().all():
                    raise ValueError(f"Numeric column '{col}' could not be coerced to numeric")

    if date_columns:
        for col in date_columns:
            resolved = None
            for c in df.columns:
                if str(c).lower() == col.lower():
                    resolved = c
                    break
            if resolved:
                coerced = pd.to_datetime(df[resolved], errors="coerce")
                if coerced.notna().any() and coerced.isna().all():
                    raise ValueError(f"Date column '{col}' could not be coerced to datetime")
