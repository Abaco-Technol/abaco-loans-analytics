import pandas as pd
import streamlit as st

from src.analytics_metrics import portfolio_kpis, project_growth

st.set_page_config(page_title="Abaco Loan Analytics", page_icon="📊", layout="wide")


def load_sample_portfolio() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "loan_amount": [12000, 8000, 16000, 14000],
            "appraised_value": [15000, 10000, 20000, 18000],
            "monthly_debt": [500, 400, 300, 450],
            "borrower_income": [60000, 45000, 80000, 70000],
            "principal_balance": [10000, 5000, 15000, 12000],
            "interest_rate": [0.05, 0.07, 0.06, 0.065],
            "loan_status": ["current", "delinquent", "current", "current"],
        }
    )


def render_portfolio_overview(df: pd.DataFrame) -> None:
    metrics, enriched = portfolio_kpis(df)

    st.subheader("Portfolio KPIs")
    kpi_cols = st.columns(4)
    kpi_cols[0].metric("Delinquency rate", f"{metrics['delinquency_rate']:.2%}")
    kpi_cols[1].metric("Portfolio yield", f"{metrics['portfolio_yield']:.2%}")
    kpi_cols[2].metric("Average LTV", f"{metrics['average_ltv']:.2%}")
    kpi_cols[3].metric("Average DTI", f"{metrics['average_dti']:.2f}")

    st.dataframe(enriched, use_container_width=True)


st.title("Abaco Loan Analytics Cockpit")
st.write(
    "Track governed KPIs, growth trajectories, and risk posture for the lending portfolio with audit-ready calculations."
)

portfolio_data = load_sample_portfolio()
render_portfolio_overview(portfolio_data)

st.subheader("Growth trajectory")
growth_df = project_growth(1.0, 1.5, 100_000, 200_000)
st.line_chart(growth_df.set_index("date")[["loan_volume", "yield"]])
