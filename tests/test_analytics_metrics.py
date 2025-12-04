import pandas as pd
import pytest

from src.analytics_metrics import (
    calculate_quality_score,
    portfolio_kpis,
    project_growth,
    standardize_numeric,
)


@pytest.fixture
def sample_df() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "loan_amount": [12000, 8000, 16000],
            "appraised_value": [15000, 10000, 20000],
            "monthly_debt": [500, 400, 300],
            "borrower_income": [60000, 45000, 80000],
            "principal_balance": [10000, 5000, 15000],
            "interest_rate": [0.05, 0.07, 0.06],
            "loan_status": ["current", "delinquent", "current"],
        }
    )


def test_standardize_numeric_handles_symbols():
    series = pd.Series(["$1,200", "€2,500", "25%", "£3,000", "", None])
    cleaned = standardize_numeric(series)

    assert cleaned.tolist() == [1200.0, 2500.0, 25.0, 3000.0, pytest.approx(float("nan")), pytest.approx(float("nan"))]


def test_project_growth_shapes_schedule():
    projection = project_growth(0.05, 0.08, 1_000_000, 2_000_000, periods=4)

    assert len(projection) == 4
    assert list(projection.columns) == ["date", "yield", "loan_volume"]


@pytest.mark.parametrize("value, expected", [(0.05, 0.05), (0.08, 0.08)])
def test_project_growth_interpolates_targets(value, expected):
    projection = project_growth(0.05, 0.08, 1_000_000, 2_000_000, periods=4)
    assert pytest.approx(projection["yield"].iloc[[0, -1]].tolist()) == [0.05, 0.08]


def test_calculate_quality_score_rewards_completeness(sample_df: pd.DataFrame):
    assert calculate_quality_score(sample_df) == 100

    incomplete = sample_df.copy()
    incomplete.loc[0, "loan_amount"] = None
    assert calculate_quality_score(incomplete) < 100


def test_calculate_quality_score_empty_dataframe_returns_zero():
    empty_df = pd.DataFrame(columns=["loan_amount", "principal_balance"])
    assert calculate_quality_score(empty_df) == 0


def test_portfolio_kpis_returns_expected_metrics(sample_df: pd.DataFrame):
    metrics, enriched = portfolio_kpis(sample_df)

    assert set(metrics.keys()) == {"delinquency_rate", "portfolio_yield", "average_ltv", "average_dti"}
    assert pytest.approx(metrics["delinquency_rate"]) == pytest.approx(5000 / 30000)
    assert pytest.approx(metrics["portfolio_yield"]) == pytest.approx((10000 * 0.05 + 5000 * 0.07 + 15000 * 0.06) / 30000)
    assert pytest.approx(metrics["average_ltv"]) == pytest.approx(0.8)
    assert "ltv_ratio" in enriched.columns and "dti_ratio" in enriched.columns


def test_portfolio_kpis_missing_column_raises(sample_df: pd.DataFrame):
    df = sample_df.drop(columns=["loan_amount"])
    with pytest.raises(ValueError, match="loan_amount"):
        portfolio_kpis(df)
