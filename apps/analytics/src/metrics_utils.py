"""Utility functions for common loan analytics KPIs."""
from typing import Dict, Iterable

import numpy as np
import pandas as pd

REQUIRED_KPI_COLUMNS = [
    "loan_amount",
    "appraised_value",
    "borrower_income",
    "monthly_debt",
    "loan_status",
    "interest_rate",
    "principal_balance",
]

DELINQUENT_STATUSES = ["30-59 days past due", "60-89 days past due", "90+ days past due"]

NUMERIC_KPI_COLUMNS = [
    "loan_amount",
    "appraised_value",
    "borrower_income",
    "monthly_debt",
    "interest_rate",
    "principal_balance",
]

def _coerce_numeric(series: pd.Series, field_name: str) -> pd.Series:
    """Convert a series to numeric values, preserving NaNs for validation visibility."""

    numeric = pd.to_numeric(series, errors="coerce")
    if numeric.isna().all():
        raise ValueError(f"Field '{field_name}' must contain at least one numeric value")
    return numeric


def validate_kpi_columns(loan_data: pd.DataFrame) -> None:
    """Validate that all KPI columns exist in the provided dataframe."""

    if loan_data.empty:
        raise ValueError("Input loan_data must be a non-empty DataFrame.")

    missing_cols = [col for col in REQUIRED_KPI_COLUMNS if col not in loan_data.columns]
    if missing_cols:
        raise ValueError(f"Missing required columns in loan_data: {', '.join(missing_cols)}")


def loan_to_value(loan_amounts: pd.Series, appraised_values: pd.Series) -> pd.Series:
    """Compute LTV as a percentage while avoiding division by zero."""

    sanitized_amounts = _coerce_numeric(loan_amounts, "loan_amount")
    sanitized_appraised = _coerce_numeric(appraised_values, "appraised_value")
    safe_appraised = sanitized_appraised.replace(0, np.nan)
    return (sanitized_amounts / safe_appraised) * 100


def debt_to_income_ratio(monthly_debts: pd.Series, borrower_incomes: pd.Series) -> pd.Series:
    """Compute DTI as a percentage using monthly income with zero-income safeguards."""

    sanitized_debt = _coerce_numeric(monthly_debts, "monthly_debt")
    monthly_income = _coerce_numeric(borrower_incomes, "borrower_income") / 12
    safe_income = monthly_income.replace({0: np.nan})
    return (sanitized_debt / safe_income) * 100


def portfolio_delinquency_rate(statuses: Iterable[str]) -> float:
    """Return the delinquency rate as a percentage of total rows."""
    series = pd.Series(list(statuses))
    delinquent_count = series.isin(DELINQUENT_STATUSES).sum()
    total = len(series)
    return (delinquent_count / total) * 100 if total else 0.0


def weighted_portfolio_yield(interest_rates: pd.Series, principal_balances: pd.Series) -> float:
    """Calculate weighted yield, returning zero when principal is missing or zero."""

    sanitized_principal = _coerce_numeric(principal_balances, "principal_balance").fillna(0)
    total_principal = sanitized_principal.sum()
    if total_principal == 0:
        return 0.0

    sanitized_interest = _coerce_numeric(interest_rates, "interest_rate").fillna(0)
    weighted_interest = (sanitized_interest * sanitized_principal).sum()
    return (weighted_interest / total_principal) * 100


def _average_null_ratio(loan_data: pd.DataFrame) -> float:
    total_cells = loan_data.size
    if total_cells == 0:
        return 0.0
    null_count = loan_data.isna().sum().sum()
    return null_count / total_cells


def _invalid_numeric_ratio(loan_data: pd.DataFrame) -> float:
    total_cells = 0
    invalid_cells = 0
    for column in NUMERIC_KPI_COLUMNS:
        if column not in loan_data.columns:
            continue
        series = loan_data[column]
        coerced = pd.to_numeric(series, errors="coerce")
        total_cells += len(series)
        invalid_cells += int((coerced.isna() & series.notna()).sum())
    if total_cells == 0:
        return 0.0
    return invalid_cells / total_cells


def _duplicate_ratio(loan_data: pd.DataFrame) -> float:
    if loan_data.empty:
        return 0.0
    return float(loan_data.duplicated().mean())


def _data_quality_score(loan_data: pd.DataFrame) -> Dict[str, float]:
    null_ratio = _average_null_ratio(loan_data)
    invalid_ratio = _invalid_numeric_ratio(loan_data)
    duplicate_ratio = _duplicate_ratio(loan_data)

    score = max(0.0, 100 - (null_ratio * 100) - (duplicate_ratio * 50) - (invalid_ratio * 60))

    return {
        "data_quality_score": round(score, 2),
        "average_null_ratio_percent": round(null_ratio * 100, 2),
        "invalid_numeric_ratio_percent": round(invalid_ratio * 100, 2),
    }


def portfolio_kpis(loan_data: pd.DataFrame) -> Dict[str, float]:
    """Aggregate portfolio KPIs used across analytics modules."""
    validate_kpi_columns(loan_data)

    ltv_series = (
        _coerce_numeric(loan_data["ltv_ratio"], "ltv_ratio")
        if "ltv_ratio" in loan_data.columns
        else loan_to_value(loan_data["loan_amount"], loan_data["appraised_value"])
    )
    dti_series = (
        _coerce_numeric(loan_data["dti_ratio"], "dti_ratio")
        if "dti_ratio" in loan_data.columns
        else debt_to_income_ratio(loan_data["monthly_debt"], loan_data["borrower_income"])
    )

    avg_ltv = ltv_series.mean(skipna=True)
    avg_dti = dti_series.mean(skipna=True)
    quality = _data_quality_score(loan_data)

    return {
        "portfolio_delinquency_rate_percent": portfolio_delinquency_rate(
            loan_data["loan_status"]
        ),
        "portfolio_yield_percent": weighted_portfolio_yield(
            loan_data["interest_rate"], loan_data["principal_balance"]
        ),
        "average_ltv_ratio_percent": float(avg_ltv if not np.isnan(avg_ltv) else 0.0),
        "average_dti_ratio_percent": float(avg_dti if not np.isnan(avg_dti) else 0.0),
        "data_quality_score": quality["data_quality_score"],
        "average_null_ratio_percent": quality["average_null_ratio_percent"],
        "invalid_numeric_ratio_percent": quality["invalid_numeric_ratio_percent"],
    }
