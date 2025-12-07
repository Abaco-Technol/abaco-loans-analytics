import sys
from pathlib import Path
import unittest

import numpy as np
import pandas as pd

# Ensure the analytics engine is importable when running from repo root
ENGINE_PATH = Path(__file__).resolve().parents[1] / "src"
if str(ENGINE_PATH) not in sys.path:
    sys.path.append(str(ENGINE_PATH))

from enterprise_analytics_engine import LoanAnalyticsEngine  # noqa: E402


class LoanAnalyticsEngineTests(unittest.TestCase):
    def setUp(self):
        self.sample_data = pd.DataFrame(
            {
                "loan_amount": [100_000, 200_000, 150_000],
                "appraised_value": [125_000, 250_000, 100_000],
                "borrower_income": [120_000, 90_000, 0],
                "monthly_debt": [1_200, 1_500, 1_000],
                "loan_status": [
                    "current",
                    "30-59 days past due",
                    "current",
                ],
                "interest_rate": [0.05, 0.06, 0.07],
                "principal_balance": [95_000, 190_000, 140_000],
            }
        )

        self.engine = LoanAnalyticsEngine(self.sample_data)

    def test_missing_columns_raise_value_error(self):
        with self.assertRaises(ValueError):
            LoanAnalyticsEngine(pd.DataFrame({"loan_amount": [100_000]}))

    def test_compute_loan_to_value(self):
        ltv = self.engine.compute_loan_to_value()
        expected = pd.Series([80.0, 80.0, 150.0])
        pd.testing.assert_series_equal(ltv.reset_index(drop=True), expected)

    def test_compute_debt_to_income_handles_zero_income(self):
        dti = self.engine.compute_debt_to_income()
        expected = np.array([12.0, 20.0, np.nan])
        pd.testing.assert_series_equal(pd.Series(dti), pd.Series(expected), check_dtype=False)

    def test_compute_delinquency_rate(self):
        delinquency_rate = self.engine.compute_delinquency_rate()
        self.assertAlmostEqual(delinquency_rate, 33.3333, places=3)

    def test_compute_portfolio_yield(self):
        portfolio_yield = self.engine.compute_portfolio_yield()
        self.assertAlmostEqual(portfolio_yield, 6.1058, places=3)

    def test_run_full_analysis_calculates_means(self):
        results = self.engine.run_full_analysis()
        self.assertIn("portfolio_delinquency_rate_percent", results)
        self.assertIn("portfolio_yield_percent", results)
        self.assertIn("average_ltv_ratio_percent", results)
        self.assertIn("average_dti_ratio_percent", results)

        self.assertAlmostEqual(results["portfolio_yield_percent"], 6.1058, places=3)
        self.assertAlmostEqual(results["average_ltv_ratio_percent"], 103.3333, places=3)
        self.assertAlmostEqual(results["average_dti_ratio_percent"], 16.0, places=1)


if __name__ == "__main__":
    unittest.main()
