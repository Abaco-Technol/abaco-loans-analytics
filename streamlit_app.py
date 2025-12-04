import io
from typing import Iterable, Tuple

import pandas as pd
import plotly.express as px
import streamlit as st

from src.analytics_metrics import (
    calculate_quality_score,
    portfolio_kpis,
    project_growth,
    standardize_numeric,
)

REQUIRED_COLUMNS: Tuple[str, ...] = (
    "loan_amount",
    "appraised_value",
    "borrower_income",
    "monthly_debt",
    "loan_status",
    "interest_rate",
    "principal_balance",
)


def load_csv(upload) -> pd.DataFrame | None:
    if upload is None:
        return None
    try:
        return pd.read_csv(upload)
    except Exception:
        upload.seek(0)
        buffer = io.StringIO(upload.getvalue().decode("utf-8"))
        return pd.read_csv(buffer)


def normalize_dataset(df: pd.DataFrame) -> pd.DataFrame:
    normalized = df.copy()
    for column in REQUIRED_COLUMNS:
        if column in normalized.columns:
            normalized[column] = standardize_numeric(normalized[column])
    return normalized


def display_metrics(metrics: dict[str, float]) -> None:
    st.subheader("Portfolio KPIs")
    cols = st.columns(len(metrics))
    for col, (label, value) in zip(cols, metrics.items()):
        col.metric(label.replace("_", " ").title(), f"{value:.2f}")


def plot_growth(current_yield: float, target_yield: float, current_volume: float, target_volume: float) -> None:
    projection = project_growth(
        current_yield=current_yield,
        target_yield=target_yield,
        current_loan_volume=current_volume,
        target_loan_volume=target_volume,
    )
    fig = px.line(projection, x="month", y=["yield", "loan_volume"], markers=True)
    fig.update_layout(margin=dict(l=20, r=20, t=40, b=20))
    st.plotly_chart(fig, use_container_width=True)


def app_body(df: pd.DataFrame) -> None:
    st.write("Uploaded rows:", len(df))

    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing:
        st.error(f"Missing required columns: {', '.join(missing)}")
        return

    normalized = normalize_dataset(df)
    quality = calculate_quality_score(normalized)
    st.caption(f"Data quality score: {quality}/100")

    metrics, enriched = portfolio_kpis(normalized)
    display_metrics(metrics)

    st.subheader("Enriched sample")
    st.dataframe(enriched.head(20))

    st.subheader("Growth projection")
    col1, col2, col3, col4 = st.columns(4)
    current_yield = col1.number_input("Current yield", min_value=0.0, value=metrics["portfolio_yield"])
    target_yield = col2.number_input("Target yield", min_value=0.0, value=max(metrics["portfolio_yield"], 1.0))
    current_volume = col3.number_input("Current loan volume", min_value=0.0, value=100000.0)
    target_volume = col4.number_input("Target loan volume", min_value=0.0, value=150000.0)
    plot_growth(current_yield, target_yield, current_volume, target_volume)


def main() -> None:
    st.set_page_config(page_title="Abaco Loan Analytics", layout="wide")
    st.title("Abaco Loan Analytics Dashboard")
    st.write(
        "Upload a CSV with loan portfolio data to view KPIs, data quality, and growth projections."
    )

    upload = st.file_uploader("Upload CSV", type=["csv"])
    data = load_csv(upload)

    if data is None:
        st.info("Waiting for a CSV with columns: " + ", ".join(REQUIRED_COLUMNS))
        return

    app_body(data)


if __name__ == "__main__":
    main()
