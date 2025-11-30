"""
ABACO Financial Intelligence Engine

Comprehensive financial analysis, KPI calculation, and data processing utilities
for factoring and working capital solutions platform.

KPIs Tracked:
- Revenue (interest + fees + other income)
- Recurring Revenue %
- Sales Volume (disbursements)
- Customer Acquisition Cost (CAC)
- Lifetime Value (LTV)
- LTV/CAC Ratio
- Days Past Due (DPD) at 30/60/90+ days
- Net Interest Margin After Losses (NIMAL)
- Non-Performing Loans (NPL) Rate
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional, Any
import logging
from dataclasses import dataclass, asdict
from enum import Enum
import warnings

warnings.filterwarnings('ignore')

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)
logger = logging.getLogger(__name__)


class ClientType(Enum):
    """Customer classification based on activity."""

    NEW = 'New'
    RECURRING = 'Recurring'
    RECOVERED = 'Recovered'
    INACTIVE = 'Inactive'


class LoanStatus(Enum):
    """Loan status classifications."""

    ACTIVE = 'Active'
    PAID_OFF = 'Paid Off'
    DEFAULTED = 'Defaulted'
    DELINQUENT = 'Delinquent'


@dataclass
class MonthlyKPIs:
    """Monthly KPI snapshot."""

    month: str
    sales_usd_mm: float
    revenue_usd_mm: float
    recurring_revenue_pct: float
    customers_eop: int
    sales_expenses_usd_k: float
    new_customers: int
    cac_usd_k: float
    ltv_realized_usd_k: float
    ltv_cac_ratio: float
    dpd_30_plus_pct: float
    npl_rate_pct: float


@dataclass
class FinancialMetrics:
    """Annual/period financial metrics."""

    period: str
    total_sales_usd_mm: float
    total_revenue_usd_mm: float
    avg_recurring_revenue_pct: float
    customers_eop: int
    avg_cac_usd_k: float
    avg_ltv_usd_k: float
    avg_ltv_cac: float
    portfolio_yield_pct: float
    fee_income_pct: float


class FinancialDataGenerator:
    """Generate and validate financial data from loan tape."""

    @staticmethod
    def calculate_monthly_revenue(
        interest_payments: float,
        fee_payments: float,
        other_payments: float,
    ) -> float:
        """Calculate total revenue (excludes principal and taxes)."""
        return interest_payments + fee_payments + other_payments

    @staticmethod
    def calculate_recurring_revenue_pct(
        interest_payments: float, total_revenue: float
    ) -> float:
        """Calculate recurring revenue as % of total (interest/total)."""
        if total_revenue == 0:
            return 0.0
        return (interest_payments / total_revenue) * 100

    @staticmethod
    def calculate_disbursement_volume(disbursements: List[float]) -> float:
        """Sum monthly disbursements in USD MM."""
        return sum(disbursements) if disbursements else 0.0

    @staticmethod
    def classify_customer_type(
        loan_count: int,
        days_since_active: int,
        inactivity_threshold: int = 90,
    ) -> ClientType:
        """Classify customer as New, Recurring, Recovered, or Inactive."""
        if loan_count == 0:
            return ClientType.INACTIVE
        elif loan_count == 1:
            return ClientType.NEW
        elif days_since_active <= inactivity_threshold:
            return ClientType.RECURRING
        else:
            return ClientType.RECOVERED


class FinancialAnalyzer:
    """Comprehensive financial analysis engine for ABACO platform."""

    def __init__(self):
        """Initialize analyzer."""
        self.monthly_data: List[Dict[str, Any]] = []
        self.kpis: List[MonthlyKPIs] = []

    def calculate_cac(
        self,
        total_sales_expense_usd: float,
        new_customers: int,
    ) -> float:
        """
        Calculate Customer Acquisition Cost.

        CAC = Total Sales Expenses (USD) / New Customers Acquired
        Returns USD in thousands
        """
        if new_customers == 0:
            logger.warning('No new customers in period for CAC calculation')
            return 0.0

        cac_usd = total_sales_expense_usd / new_customers
        return cac_usd / 1000  # Convert to thousands

    def calculate_ltv(
        self,
        total_revenue_per_customer_usd: float,
        gross_margin_pct: float = 100.0,
    ) -> float:
        """
        Calculate Lifetime Value (realized).

        LTV = Total Revenue Per Customer × Gross Margin %
        Returns USD in thousands
        Realized LTV calculated from observed cash-in up to data cutoff
        """
        ltv_usd = total_revenue_per_customer_usd * (gross_margin_pct / 100)
        return ltv_usd / 1000  # Convert to thousands

    def calculate_ltv_cac_ratio(self, ltv_usd_k: float, cac_usd_k: float) -> float:
        """Calculate LTV/CAC efficiency ratio (higher is better, target > 3x)."""
        if cac_usd_k == 0:
            logger.warning('CAC is 0, LTV/CAC ratio set to 0')
            return 0.0
        return ltv_usd_k / cac_usd_k

    def calculate_dpd_metrics(
        self,
        loans_dpd_30_plus: int,
        loans_dpd_60_plus: int,
        loans_dpd_90_plus: int,
        total_active_loans: int,
    ) -> Dict[str, float]:
        """Calculate Days Past Due delinquency rates."""
        return {
            'dpd_30_pct': (loans_dpd_30_plus / total_active_loans * 100)
            if total_active_loans > 0
            else 0.0,
            'dpd_60_pct': (loans_dpd_60_plus / total_active_loans * 100)
            if total_active_loans > 0
            else 0.0,
            'dpd_90_pct': (loans_dpd_90_plus / total_active_loans * 100)
            if total_active_loans > 0
            else 0.0,
        }

    def calculate_npl_rate(
        self,
        non_performing_loans: int,
        total_active_loans: int,
    ) -> float:
        """
        Calculate Non-Performing Loans rate.

        NPL Rate = Non-Performing Loans / Total Active Loans × 100
        """
        if total_active_loans == 0:
            return 0.0
        return (non_performing_loans / total_active_loans) * 100

    def calculate_portfolio_yield(
        self,
        total_interest_income: float,
        avg_portfolio_balance: float,
        periods: int = 12,
    ) -> float:
        """
        Calculate portfolio yield (annualized).

        Yield % = (Total Interest Income / Avg Portfolio Balance) / Periods × 100
        """
        if avg_portfolio_balance == 0:
            return 0.0
        return (total_interest_income / avg_portfolio_balance / periods) * 100

    def generate_monthly_kpi_report(
        self, df: pd.DataFrame, period_column: str = 'month'
    ) -> List[MonthlyKPIs]:
        """
        Generate monthly KPI report from loan tape data.

        Expected DataFrame columns:
        - month: YYYY-MM format
        - disbursement_amount: USD
        - interest_payment: USD
        - fee_payment: USD
        - other_payment: USD
        - sales_expense: USD
        - new_customers_count: integer
        - active_loans: integer
        - dpd_30_plus: integer
        - customer_id: string (for unique count)
        """
        logger.info('Generating monthly KPI report...')
        kpi_list: List[MonthlyKPIs] = []

        for month in df[period_column].unique():
            month_data = df[df[period_column] == month]

            # Revenue metrics
            total_revenue = self.calculate_monthly_revenue(
                interest_payments=month_data['interest_payment'].sum(),
                fee_payments=month_data['fee_payment'].sum(),
                other_payments=month_data['other_payment'].sum(),
            )

            recurring_rev_pct = self.calculate_recurring_revenue_pct(
                interest_payments=month_data['interest_payment'].sum(),
                total_revenue=total_revenue,
            )

            # Sales metrics
            sales_usd_mm = month_data['disbursement_amount'].sum() / 1_000_000

            # Customer metrics
            unique_customers = month_data['customer_id'].nunique()
            new_customers = month_data['new_customers_count'].sum()

            # Unit economics
            cac_usd_k = self.calculate_cac(
                total_sales_expense_usd=month_data['sales_expense'].sum(),
                new_customers=new_customers if new_customers > 0 else 1,
            )

            # Assume avg LTV realized per customer
            revenue_per_customer = total_revenue / unique_customers if unique_customers > 0 else 0
            ltv_usd_k = self.calculate_ltv(revenue_per_customer)
            ltv_cac = self.calculate_ltv_cac_ratio(ltv_usd_k, cac_usd_k)

            # Risk metrics
            dpd_metrics = self.calculate_dpd_metrics(
                loans_dpd_30_plus=month_data['dpd_30_plus'].sum(),
                loans_dpd_60_plus=month_data['dpd_60_plus'].sum() if 'dpd_60_plus' in month_data.columns else 0,
                loans_dpd_90_plus=month_data['dpd_90_plus'].sum() if 'dpd_90_plus' in month_data.columns else 0,
                total_active_loans=month_data['active_loans'].sum(),
            )

            kpi = MonthlyKPIs(
                month=month,
                sales_usd_mm=sales_usd_mm,
                revenue_usd_mm=total_revenue / 1_000_000,
                recurring_revenue_pct=recurring_rev_pct,
                customers_eop=unique_customers,
                sales_expenses_usd_k=month_data['sales_expense'].sum() / 1_000,
                new_customers=new_customers,
                cac_usd_k=cac_usd_k,
                ltv_realized_usd_k=ltv_usd_k,
                ltv_cac_ratio=ltv_cac,
                dpd_30_plus_pct=dpd_metrics['dpd_30_pct'],
                npl_rate_pct=self.calculate_npl_rate(
                    month_data['defaulted_loans'].sum() if 'defaulted_loans' in month_data.columns else 0,
                    month_data['active_loans'].sum(),
                ),
            )

            kpi_list.append(kpi)
            logger.info(f'Generated KPI for {month}: Revenue=${kpi.revenue_usd_mm:.2f}MM, CAC=${cac_usd_k:.1f}k')

        self.kpis = kpi_list
        return kpi_list

    def generate_annual_summary(
        self, kpi_list: List[MonthlyKPIs], year: str
    ) -> FinancialMetrics:
        """Generate annual financial summary from monthly KPIs."""
        if not kpi_list:
            logger.warning(f'No KPIs available for {year}')
            return FinancialMetrics(
                period=year,
                total_sales_usd_mm=0.0,
                total_revenue_usd_mm=0.0,
                avg_recurring_revenue_pct=0.0,
                customers_eop=0,
                avg_cac_usd_k=0.0,
                avg_ltv_usd_k=0.0,
                avg_ltv_cac=0.0,
                portfolio_yield_pct=0.0,
                fee_income_pct=0.0,
            )

        total_sales = sum(k.sales_usd_mm for k in kpi_list)
        total_revenue = sum(k.revenue_usd_mm for k in kpi_list)
        avg_recurring = np.mean([k.recurring_revenue_pct for k in kpi_list])
        last_month_customers = kpi_list[-1].customers_eop if kpi_list else 0
        avg_cac = np.mean([k.cac_usd_k for k in kpi_list if k.cac_usd_k > 0])
        avg_ltv = np.mean([k.ltv_realized_usd_k for k in kpi_list if k.ltv_realized_usd_k > 0])
        avg_ltv_cac = np.mean([k.ltv_cac_ratio for k in kpi_list if k.ltv_cac_ratio > 0])

        return FinancialMetrics(
            period=year,
            total_sales_usd_mm=total_sales,
            total_revenue_usd_mm=total_revenue,
            avg_recurring_revenue_pct=avg_recurring,
            customers_eop=last_month_customers,
            avg_cac_usd_k=avg_cac,
            avg_ltv_usd_k=avg_ltv,
            avg_ltv_cac=avg_ltv_cac,
            portfolio_yield_pct=(total_revenue / total_sales * 100) if total_sales > 0 else 0,
            fee_income_pct=100 - avg_recurring,
        )

    def validate_data_quality(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Validate data quality and return audit scores."""
        audit = {
            'total_records': len(df),
            'date_range': f"{df.index.min() if hasattr(df.index, 'min') else 'N/A'} to {df.index.max() if hasattr(df.index, 'max') else 'N/A'}",
            'missing_values': df.isnull().sum().to_dict(),
            'completeness_pct': ((len(df) - df.isnull().sum().sum()) / (len(df) * len(df.columns)) * 100) if len(df) > 0 else 0,
            'duplicate_records': df.duplicated().sum(),
            'data_types': df.dtypes.to_dict(),
        }
        logger.info(f'Data audit: {audit["completeness_pct"]:.1f}% complete, {audit["duplicate_records"]} duplicates')
        return audit


class DataProcessor:
    """Data processing and normalization utilities."""

    @staticmethod
    def normalize_column(df: pd.DataFrame, column: str, method: str = 'minmax') -> pd.Series:
        """
        Normalize column to 0-1 range.

        Methods: 'minmax' (Min-Max scaling) or 'zscore' (Standardization)
        """
        if method == 'minmax':
            return (df[column] - df[column].min()) / (df[column].max() - df[column].min())
        elif method == 'zscore':
            return (df[column] - df[column].mean()) / df[column].std()
        else:
            raise ValueError(f'Unknown normalization method: {method}')

    @staticmethod
    def handle_missing_values(
        df: pd.DataFrame, strategy: str = 'mean', columns: Optional[List[str]] = None
    ) -> pd.DataFrame:
        """
        Handle missing values.

        Strategies: 'mean', 'median', 'forward_fill', 'drop'
        """
        result = df.copy()

        if columns is None:
            columns = result.columns

        for col in columns:
            if result[col].isnull().sum() > 0:
                if strategy == 'mean':
                    result[col].fillna(result[col].mean(), inplace=True)
                elif strategy == 'median':
                    result[col].fillna(result[col].median(), inplace=True)
                elif strategy == 'forward_fill':
                    result[col].fillna(method='ffill', inplace=True)
                elif strategy == 'drop':
                    result = result.dropna(subset=[col])

        return result

    @staticmethod
    def aggregate_by_period(
        df: pd.DataFrame,
        date_column: str,
        period: str = 'M',
        agg_functions: Optional[Dict[str, str]] = None,
    ) -> pd.DataFrame:
        """
        Aggregate data by time period.

        Period: 'D' (day), 'M' (month), 'Q' (quarter), 'Y' (year)
        """
        if agg_functions is None:
            agg_functions = {col: 'sum' for col in df.select_dtypes(include=[np.number]).columns}

        df_copy = df.copy()
        df_copy[date_column] = pd.to_datetime(df_copy[date_column])
        return df_copy.groupby(pd.Grouper(key=date_column, freq=period)).agg(agg_functions)


class ExportUtilities:
    """Export and reporting utilities."""

    @staticmethod
    def export_to_excel(
        data: Dict[str, pd.DataFrame],
        filename: str,
        include_summary: bool = True,
    ) -> None:
        """Export multiple DataFrames to Excel with multiple sheets."""
        try:
            with pd.ExcelWriter(filename, engine='openpyxl') as writer:
                for sheet_name, df in data.items():
                    df.to_excel(writer, sheet_name=sheet_name, index=True)

                if include_summary:
                    summary_data = {
                        'Sheet': list(data.keys()),
                        'Rows': [len(df) for df in data.values()],
                        'Columns': [len(df.columns) for df in data.values()],
                    }
                    summary_df = pd.DataFrame(summary_data)
                    summary_df.to_excel(writer, sheet_name='Summary', index=False)

            logger.info(f'Exported to {filename}')
        except Exception as e:
            logger.error(f'Export failed: {str(e)}')
            raise

    @staticmethod
    def export_kpis_to_csv(kpis: List[MonthlyKPIs], filename: str) -> None:
        """Export KPIs to CSV."""
        try:
            kpi_dicts = [asdict(kpi) for kpi in kpis]
            df = pd.DataFrame(kpi_dicts)
            df.to_csv(filename, index=False)
            logger.info(f'Exported {len(kpis)} KPIs to {filename}')
        except Exception as e:
            logger.error(f'KPI export failed: {str(e)}')
            raise

    @staticmethod
    def generate_text_report(metrics: FinancialMetrics) -> str:
        """Generate formatted text report."""
        return f"""
╔══════════════════════════════════════════════════════════════╗
║          ABACO FINANCIAL INTELLIGENCE REPORT                 ║
╚══════════════════════════════════════════════════════════════╝

Period: {metrics.period}

REVENUE & SALES
  Sales (Disbursements):     ${metrics.total_sales_usd_mm:,.2f}MM
  Revenue:                   ${metrics.total_revenue_usd_mm:,.2f}MM
  Recurring Revenue:         {metrics.avg_recurring_revenue_pct:.1f}%

GROWTH
  Customers (EoP):           {metrics.customers_eop:,}
  Portfolio Yield:           {metrics.portfolio_yield_pct:.2f}%
  Fee Income %:              {metrics.fee_income_pct:.1f}%

UNIT ECONOMICS
  Avg CAC:                   ${metrics.avg_cac_usd_k:,.1f}k
  Avg LTV (Realized):        ${metrics.avg_ltv_usd_k:,.1f}k
  LTV/CAC Ratio:             {metrics.avg_ltv_cac:.2f}x (Target: >3.0x)

════════════════════════════════════════════════════════════════
"""
