import pandas as pd
import pytest

from apps.analytics.src.enterprise_analytics_engine import LoanAnalyticsEngine


class StubExporter:
    def __init__(self):
        self.received_metrics = None
        self.received_blob_name = None

    def upload_metrics(self, metrics, blob_name=None):
        self.received_metrics = metrics
        self.received_blob_name = blob_name
        return f"test-container/{blob_name or 'kpi-dashboard.json'}"


def test_export_kpis_to_blob_uses_blob_name_and_metrics():
    data = {
        "loan_amount": [100000],
        "appraised_value": [200000],
        "borrower_income": [120000],
        "monthly_debt": [2000],
        "loan_status": ["current"],
        "interest_rate": [0.05],
        "principal_balance": [100000],
    }
    engine = LoanAnalyticsEngine(pd.DataFrame(data))
    exporter = StubExporter()

    result_path = engine.export_kpis_to_blob(exporter, blob_name="custom-kpis.json")

    expected_metrics = {
        "portfolio_delinquency_rate_percent": pytest.approx(0.0),
        "portfolio_yield_percent": pytest.approx(5.0),
        "average_ltv_ratio_percent": pytest.approx(50.0),
        "average_dti_ratio_percent": pytest.approx(20.0),
    }

    assert result_path == "test-container/custom-kpis.json"
    assert exporter.received_blob_name == "custom-kpis.json"
    assert exporter.received_metrics == expected_metrics


def test_export_kpis_to_blob_defaults_when_blob_name_missing():
    data = {
        "loan_amount": [180000, 220000],
        "appraised_value": [200000, 240000],
        "borrower_income": [90000, 130000],
        "monthly_debt": [1500, 2500],
        "loan_status": ["current", "current"],
        "interest_rate": [0.045, 0.04],
        "principal_balance": [175000, 210000],
    }
    engine = LoanAnalyticsEngine(pd.DataFrame(data))
    exporter = StubExporter()

    result_path = engine.export_kpis_to_blob(exporter)

    expected_metrics = {
        "portfolio_delinquency_rate_percent": pytest.approx(0.0),
        "portfolio_yield_percent": pytest.approx(4.23, rel=1e-3),
        "average_ltv_ratio_percent": pytest.approx(90.83, rel=1e-3),
        "average_dti_ratio_percent": pytest.approx(21.54, rel=1e-3),
    }

    assert result_path == "test-container/kpi-dashboard.json"
    assert exporter.received_blob_name is None
    assert exporter.received_metrics == expected_metrics


def test_export_kpis_to_blob_strips_empty_blob_name():
    data = {
        "loan_amount": [150000],
        "appraised_value": [300000],
        "borrower_income": [100000],
        "monthly_debt": [1800],
        "loan_status": ["current"],
        "interest_rate": [0.041],
        "principal_balance": [150000],
    }
    engine = LoanAnalyticsEngine(pd.DataFrame(data))
    exporter = StubExporter()

    result_path = engine.export_kpis_to_blob(exporter, blob_name="   ")

    assert result_path == "test-container/kpi-dashboard.json"
    assert exporter.received_blob_name is None


def test_export_kpis_to_blob_rejects_non_string_blob_name():
    engine = LoanAnalyticsEngine(
        pd.DataFrame(
            {
                "loan_amount": [100000],
                "appraised_value": [200000],
                "borrower_income": [120000],
                "monthly_debt": [2000],
                "loan_status": ["current"],
                "interest_rate": [0.05],
                "principal_balance": [100000],
            }
        )
    )

    with pytest.raises(TypeError):
        engine.export_kpis_to_blob(StubExporter(), blob_name=123)
