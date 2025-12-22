from datetime import datetime
from pathlib import Path

import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[1]

from src.enterprise_analytics_engine import (
    LoanAnalyticsConfig,
    LoanAnalyticsEngine,
    LoanPosition,
    calculate_monthly_payment,
    calculate_portfolio_kpis,
    expected_loss,
)


@pytest.fixture()
def sample_frame() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "loan_id": "L1",
                "principal": 10000,
                "interest_rate": 0.1,
                "term_months": 24,
                "origination_date": datetime(2022, 1, 15),
                "status": "current",
                "days_in_arrears": 0,
                "balance": 8000,
                "payments_made": 2000,
                "write_off_amount": 0,
                "region": "NA",
                "product": "A",
                "currency": "USD",
            },
            {
                "loan_id": "L2",
                "principal": 5000,
                "interest_rate": 0.12,
                "term_months": 12,
                "origination_date": datetime(2022, 2, 10),
                "status": None,
                "days_in_arrears": 120,
                "balance": 4500,
                "payments_made": 500,
                "write_off_amount": 0,
                "region": "EU",
                "product": "B",
                "currency": "USD",
            },
            {
                "loan_id": "L3",
                "principal": 7000,
                "interest_rate": 0.15,
                "term_months": 18,
                "origination_date": datetime(2021, 11, 20),
                "status": "DEFAULT",
                "days_in_arrears": 200,
                "balance": 0,
                "payments_made": 5000,
                "write_off_amount": 2000,
                "region": "NA",
                "product": "B",
                "currency": "USD",
            },
            {
                "loan_id": "L4",
                "principal": 6000,
                "interest_rate": 0.08,
                "term_months": 12,
                "origination_date": datetime(2022, 3, 10),
                "status": "prepaid",
                "days_in_arrears": 0,
                "balance": 0,
                "payments_made": 6000,
                "write_off_amount": 0,
                "region": "SA",
                "product": "A",
                "currency": "USD",
            },
        ]
    )


def test_missing_columns_raise_value_error(sample_frame: pd.DataFrame):
    truncated = sample_frame.drop(columns=["principal"])
    with pytest.raises(ValueError):
        LoanAnalyticsEngine(truncated)


def test_invalid_origination_dates_raise(sample_frame: pd.DataFrame):
    invalid = sample_frame.copy()
    invalid.loc[0, "origination_date"] = "not-a-date"
    with pytest.raises(ValueError):
        LoanAnalyticsEngine(invalid)


def test_arrears_flag_defaults_to_days_threshold(sample_frame: pd.DataFrame):
    engine = LoanAnalyticsEngine(sample_frame, config=LoanAnalyticsConfig(arrears_threshold=90))
    arrears = engine.data.loc[engine.data["loan_id"] == "L2", "arrears_flag"].iloc[0]
    assert bool(arrears) is True


def test_portfolio_kpis(sample_frame: pd.DataFrame):
    engine = LoanAnalyticsEngine(sample_frame)
    kpis = engine.portfolio_kpis()

    assert kpis["currency"] == "USD"
    assert kpis["exposure"] == pytest.approx(28_000)
    assert kpis["weighted_interest_rate"] == pytest.approx((0.1 * 10000 + 0.12 * 5000 + 0.15 * 7000 + 0.08 * 6000) / 28000)
    assert kpis["npl_ratio"] == pytest.approx((5000 + 7000) / 28000)
    assert kpis["default_rate"] == pytest.approx(7000 / 28000)
    assert kpis["lgd"] == pytest.approx(2000 / 7000)
    assert kpis["prepayment_rate"] == pytest.approx(6000 / 28000)
    assert kpis["repayment_velocity"] == pytest.approx(13_500 / 28_000)


def test_segment_kpis_by_region(sample_frame: pd.DataFrame):
    engine = LoanAnalyticsEngine(sample_frame)
    segment_df = engine.segment_kpis("region")

    assert set(segment_df["region"]) == {"NA", "EU", "SA"}
    na_row = segment_df.loc[segment_df["region"] == "NA"].iloc[0]
    assert na_row["exposure"] == pytest.approx(17_000)
    assert na_row["default_rate"] == pytest.approx(7000 / 17_000)


def test_vintage_default_table_sorted(sample_frame: pd.DataFrame):
    engine = LoanAnalyticsEngine(sample_frame)
    vintage = engine.vintage_default_table()

    assert list(vintage["origination_quarter"]) == sorted(vintage["origination_quarter"].tolist())
    row = vintage.loc[vintage["origination_quarter"] == "2021Q4"].iloc[0]
    assert row["default_rate"] == pytest.approx(1.0)


def test_cashflow_curve_shape(sample_frame: pd.DataFrame):
    engine = LoanAnalyticsEngine(sample_frame)
    curve = engine.cashflow_curve(freq="Q")

    assert not curve.empty
    assert curve["cumulative_cashflow"].iloc[-1] == pytest.approx(curve["cashflow"].sum())
    assert curve.shape[1] == 3


def test_calculate_portfolio_kpis_returns_expected_weights():
    loans = [
        LoanPosition(principal=10_000, annual_interest_rate=0.12, term_months=24, default_probability=0.05),
        LoanPosition(principal=5_000, annual_interest_rate=0.10, term_months=12, default_probability=0.02),
    ]

    kpis = calculate_portfolio_kpis(loans, loss_given_default=0.4)

    expected_exposure = sum(loan.principal for loan in loans)
    weighted_rate = sum(loan.annual_interest_rate * loan.principal for loan in loans) / expected_exposure
    weighted_term = sum(loan.term_months * loan.principal for loan in loans) / expected_exposure
    weighted_default_probability = sum(loan.default_probability * loan.principal for loan in loans) / expected_exposure
    expected_payment = sum(calculate_monthly_payment(loan) for loan in loans)
    expected_interest = sum(loan.principal * (loan.annual_interest_rate / 12) for loan in loans)
    expected_loss_value = sum(expected_loss(loan, 0.4) for loan in loans)

    assert kpis.exposure == pytest.approx(expected_exposure)
    assert kpis.weighted_rate == pytest.approx(weighted_rate)
    assert kpis.weighted_term_months == pytest.approx(weighted_term)
    assert kpis.weighted_default_probability == pytest.approx(weighted_default_probability)
    assert kpis.expected_monthly_payment == pytest.approx(expected_payment)
    assert kpis.expected_monthly_interest == pytest.approx(expected_interest)
    assert kpis.expected_loss == pytest.approx(expected_loss_value)
    assert kpis.expected_loss_rate == pytest.approx(expected_loss_value / expected_exposure)
    assert kpis.interest_yield_rate == pytest.approx(expected_interest / expected_exposure)
    assert kpis.risk_adjusted_return == pytest.approx((expected_interest - expected_loss_value) / expected_exposure)
