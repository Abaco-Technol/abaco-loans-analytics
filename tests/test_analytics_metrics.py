import pandas as pd
import pytest
from src.analytics_metrics import calculate_quality_score, portfolio_kpis, project_growth, standardize_numeric


@pytest.fixture
def sample_df():
    return pd.DataFrame(
        {
            "loan_amount": [100000, 200000, 150000],
            "appraised_value": [125000, 210000, 180000],
            "borrower_income": [60000, 80000, 75000],
            "monthly_debt": [1200, 1800, 1500],
            "loan_status": ["current", "30-59 days past due", "current"],
            "principal_balance": [90000, 195000, 140000],
            "interest_rate": [0.05, 0.06, 0.055],
        }
    )


def test_standardize_numeric_handles_symbols():
    series = pd.Series(["$1,200", "€2,500", "", None])
    cleaned = standardize_numeric(series)
    assert cleaned.iloc[0] == 1200.0
    assert cleaned.iloc[1] == 2500.0
    assert pd.isna(cleaned.iloc[2])
    assert pd.isna(cleaned.iloc[3])


def test_calculate_quality_score_rewards_complete_data():
    df = sample_df()
    assert calculate_quality_score(df) == 100

    df_with_missing = df.copy()
    df_with_missing.loc[0, "loan_amount"] = None
    assert calculate_quality_score(df_with_missing) < 100


def test_portfolio_kpis_returns_expected_metrics():
    metrics, enriched = portfolio_kpis(sample_df())
    assert set(metrics.keys()) == {"delinquency_rate", "portfolio_yield", "average_ltv", "average_dti"}
    assert "ltv_ratio" in enriched.columns
    assert "dti_ratio" in enriched.columns


def test_project_growth_builds_monotonic_path():
    projection = project_growth(1.0, 2.0, 100, 200, periods=4)
    assert len(projection) == 4
    assert projection["yield"].iloc[0] == 1.0
    assert projection["yield"].iloc[-1] == 2.0
    assert projection["loan_volume"].iloc[0] == 100
    assert projection["loan_volume"].iloc[-1] == 200
