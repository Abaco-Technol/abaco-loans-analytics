from __future__ import annotations

from dataclasses import dataclass
from typing import List, Sequence

import numpy as np
import pandas as pd


@dataclass(frozen=True)
class LoanAnalyticsConfig:
    """Static configuration controlling portfolio KPI computations."""

    arrears_threshold: int = 90
    currency: str = "USD"


class LoanAnalyticsEngine:
    """Compute portfolio KPIs, risk metrics, and cashflow views for loan books."""

    required_columns: Sequence[str] = (
        "loan_id",
        "principal",
        "interest_rate",
        "term_months",
        "origination_date",
        "status",
        "outstanding_principal",
        "days_in_arrears",
        "charge_off_amount",
        "recoveries",
        "paid_principal",
    )

    def __init__(self, data: pd.DataFrame, config: LoanAnalyticsConfig | None = None):
        self.config = config or LoanAnalyticsConfig()
        self.data = self._prepare_data(data.copy())

    @classmethod
    def from_csv(cls, path: str, config: LoanAnalyticsConfig | None = None) -> "LoanAnalyticsEngine":
        frame = pd.read_csv(path)
        return cls(frame, config=config)

    def _prepare_data(self, frame: pd.DataFrame) -> pd.DataFrame:
        if missing := [
            col for col in self.required_columns if col not in frame.columns
        ]:
            raise ValueError(f"Missing required columns: {', '.join(sorted(missing))}")

        frame["origination_date"] = pd.to_datetime(
            frame["origination_date"], format="%Y-%m-%d", errors="coerce"
        )
        if frame["origination_date"].isna().any():
            raise ValueError("origination_date contains invalid or missing values")
        numeric_cols: List[str] = [
            "principal",
            "interest_rate",
            "term_months",
            "outstanding_principal",
            "days_in_arrears",
            "charge_off_amount",
            "recoveries",
            "paid_principal",
        ]
        # Validate 'principal' and 'interest_rate' strictly
        for col in ["principal", "interest_rate"]:
            frame[col] = pd.to_numeric(frame[col], errors="coerce")
            if frame[col].isna().any():
                raise ValueError(f"{col} contains invalid or missing values")
        # For other numeric columns, coerce invalids to 0
        for col in [
            "term_months",
            "outstanding_principal",
            "days_in_arrears",
            "charge_off_amount",
            "recoveries",
            "paid_principal",
        ]:
            frame[col] = pd.to_numeric(frame[col], errors="coerce").fillna(0)

        frame["status"] = frame["status"].fillna("").astype(str)
        frame["arrears_flag"] = (
            (frame["days_in_arrears"] >= self.config.arrears_threshold)
            | frame["status"].str.lower().eq("defaulted")
        )
        frame["origination_quarter"] = frame["origination_date"].dt.to_period("Q")
        # Exposure at Default (EAD) is set to the maximum of outstanding principal and charge-off amount.
        # This ensures that EAD reflects the highest possible exposure, as charge-off amounts may include
        # accrued interest or fees that exceed the principal. Using max captures the true risk exposure.
        frame["exposure_at_default"] = frame[["outstanding_principal", "charge_off_amount"]].max(axis=1)
        return frame

    def portfolio_kpis(self) -> dict:
        """
        Compute and return key performance indicators (KPIs) for the loan portfolio.

        Returns:
            dict: A dictionary with the following keys:
                - currency (str): The currency of the portfolio, as specified in config.
                - total_outstanding (float): Total outstanding principal across all loans.
                - total_principal (float): Total original principal across all loans.
                - weighted_interest_rate (float): Weighted average interest rate, using outstanding principal as weights if available, otherwise original principal.
                - non_performing_loan_ratio (float): Ratio of outstanding principal in non-performing loans (arrears or defaulted) to total outstanding principal.
                - default_rate (float): Fraction of loans currently in default status.
                - loss_given_default (float): Average loss given default, calculated as (charge_off_amount - recoveries) / exposure_at_default for defaulted loans.
                - prepayment_rate (float): Ratio of total paid principal to total original principal, indicating early repayments.
                - repayment_velocity (float): Average monthly principal repayment rate, as computed by _repayment_velocity().

        Calculation details:
            - Weighted interest rate: np.average(interest_rate, weights=outstanding_principal or principal)
            - Non-performing loan ratio: sum(outstanding_principal for loans in arrears or defaulted) / total_outstanding
            - Default rate: number of defaulted loans / total number of loans
            - Loss given default: see _loss_given_default() for details
            - Prepayment rate: sum(paid_principal) / sum(principal)
            - Repayment velocity: see _repayment_velocity() for details

        Returns NaN for metrics if required data is missing or zero.
        """
        portfolio = self.data
        total_outstanding = portfolio["outstanding_principal"].sum()
        total_principal = portfolio["principal"].sum()

        if total_outstanding > 0:
            weighted_rate = np.average(
                portfolio["interest_rate"], weights=portfolio["outstanding_principal"]
            )
        elif total_principal > 0:
            weighted_rate = np.average(portfolio["interest_rate"], weights=portfolio["principal"])
        else:
            weighted_rate = float("nan")

        default_mask = portfolio["status"].str.lower().eq("defaulted")
        defaults = portfolio[default_mask]
        npl_outstanding = portfolio.loc[portfolio["arrears_flag"], "outstanding_principal"].sum()
        npl_ratio = npl_outstanding / total_outstanding if total_outstanding else float("nan")
        default_rate = len(defaults) / len(portfolio) if len(portfolio) else float("nan")

        lgd = self._loss_given_default(defaults)
        prepayment_rate = (
            portfolio["paid_principal"].sum() / total_principal if total_principal else float("nan")
        )
        repayment_velocity = self._repayment_velocity(portfolio)

        return {
            "currency": self.config.currency,
            "total_outstanding": total_outstanding,
            "total_principal": total_principal,
            "weighted_interest_rate": weighted_rate,
            "non_performing_loan_ratio": npl_ratio,
            "default_rate": default_rate,
            "loss_given_default": lgd,
            "prepayment_rate": prepayment_rate,
            "repayment_velocity": repayment_velocity,
        }

    def _loss_given_default(self, defaults: pd.DataFrame) -> float:
        exposure = defaults["exposure_at_default"].sum()
        if not exposure:
            return float("nan")
        losses = (defaults["charge_off_amount"] - defaults["recoveries"]).clip(lower=0).sum()
        return losses / exposure

    def _repayment_velocity(self, portfolio: pd.DataFrame) -> float:
        active_terms = portfolio["term_months"].replace(0, np.nan)
        scheduled_principal = portfolio["principal"] / active_terms
        scheduled_principal = scheduled_principal.replace([np.inf, -np.inf], np.nan).fillna(0)
        scheduled_total = scheduled_principal.sum()
        if not scheduled_total:
            return float("nan")
        return portfolio["paid_principal"].sum() / scheduled_total

    def _portfolio_kpis_from_frame(self, frame: pd.DataFrame) -> dict:
        """
        Compute portfolio KPIs for a pre-prepared frame without re-running _prepare_data.

        This temporarily swaps out self.data so that we can reuse the logic inside
        portfolio_kpis without constructing a new LoanAnalyticsEngine per segment.
        """
        original_data = self.data
        try:
            # frame is a subset of self.data, which is already prepared, so we can
            # safely reuse the existing KPI logic without re-preparing.
            self.data = frame
            return self.portfolio_kpis()
        finally:
            self.data = original_data

    def segment_kpis(self, segment_by: List[str]) -> pd.DataFrame:
        """
        Compute portfolio KPIs for each segment defined by the given columns.

        This method groups the loan portfolio data by the specified `segment_by` columns,
        computes KPIs for each segment, and returns a DataFrame where each row represents
        a segment and its associated KPIs.

        Parameters
        ----------
        segment_by : List[str]
            List of column names to group by. Each unique combination of values in these
            columns defines a segment. Must contain at least one column, and all columns
            must exist in the data.

        Returns
        -------
        pd.DataFrame
            DataFrame with one row per segment. The columns include all `segment_by`
            columns, plus the computed KPI columns (e.g., "default_rate", "loss_given_default",
            "repayment_velocity", etc.).

        Constraints
        -----------
        - `segment_by` must be a non-empty list.
        - All columns in `segment_by` must exist in the portfolio data.

        Example
        -------
        >>> engine.segment_kpis(["country", "loan_type"])
        Returns a DataFrame like:
            country  loan_type  default_rate  loss_given_default  repayment_velocity  ...
            US       consumer   0.02          0.45               0.87                ...
            US       business   0.01          0.30               0.92                ...
            CA       consumer   0.03          0.50               0.80                ...
        """
        if not segment_by:
            raise ValueError("segment_by must contain at least one column")
        missing = [col for col in segment_by if col not in self.data.columns]
        if missing:
            raise ValueError(f"Segment columns not found: {', '.join(missing)}")

        grouped = self.data.groupby(segment_by)
        rows = []
        for keys, frame in grouped:
            metrics = self._portfolio_kpis_from_frame(frame.reset_index(drop=True))
            if not isinstance(keys, tuple):
                keys = (keys,)
            rows.append({**dict(zip(segment_by, keys)), **metrics})
        return pd.DataFrame(rows)

    def vintage_default_table(self) -> pd.DataFrame:
        grouped = self.data.groupby("origination_quarter")
        rows = []
        for vintage, frame in grouped:
            if frame.empty:
                continue
            defaults = frame[frame["status"].str.lower().eq("defaulted")]
            rate = len(defaults) / len(frame) if len(frame) else float("nan")
            coverage = frame["principal"].sum()
            rows.append({
                "origination_quarter": vintage,
                "default_rate": rate,
                "principal_at_origination": coverage,
            })
        return pd.DataFrame(rows).sort_values("origination_quarter").reset_index(drop=True)

    def cashflow_curve(self, freq: str = "M") -> pd.DataFrame:
        expanded = self.data.copy()
        expanded["period"] = expanded["origination_date"].dt.to_period(freq)
        grouped = expanded.groupby("period")
        curve = grouped.agg(
            principal_funded=("principal", "sum"),
            principal_repaid=("paid_principal", "sum"),
            outstanding=("outstanding_principal", "sum"),
        )
        curve["net_cashflow"] = curve["principal_repaid"] - curve["principal_funded"]
        curve["cumulative_cashflow"] = curve["net_cashflow"].cumsum()
        return curve.reset_index()

    def scorecard(self) -> pd.DataFrame:
        kpis = self.portfolio_kpis()
        return pd.DataFrame(
            {
                "metric": list(kpis.keys()),
                "value": list(kpis.values()),
            }
        )
