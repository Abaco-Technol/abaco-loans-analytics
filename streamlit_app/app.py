import numpy as np
import pandas as pd
import streamlit as st
import altair as alt
from utils.feature_engineering import FeatureEngineer

st.set_page_config(layout="wide", page_title="Abaco Loans Analytics Dashboard")

# --- Data Ingestion Simulation ---
@st.cache_data
def load_and_prepare_data():
    rng = np.random.default_rng(7)
    data = {
        'customer_id': range(100),
        'revenue': rng.uniform(10000, 150000, 100),
        'balance': rng.uniform(1000, 50000, 100),
        'limit': rng.uniform(20000, 100000, 100),
        'dpd': rng.choice([-1, 0, 15, 45, 75, 100], 100, p=[0.1, 0.6, 0.1, 0.1, 0.05, 0.05]),
    }
    raw_df = pd.DataFrame(data)

    completeness = (raw_df.notna().sum().sum() / (raw_df.shape[0] * raw_df.shape[1])) * 100
    freshness_days = rng.integers(0, 5)
    return raw_df, completeness, freshness_days

# --- Main Application ---
st.title("Abaco Loans Analytics Dashboard")

# 1. Ingestion and Enrichment
raw_portfolio_df, data_quality_score, data_freshness_days = load_and_prepare_data()
enriched_df = FeatureEngineer.enrich_portfolio(raw_portfolio_df)

st.caption(
    "Data sources mocked for demo purposes. KPIs are derived deterministically for traceability."
)

portfolio_size = len(enriched_df)
delinquency_rate = (enriched_df['dpd'] > 30).mean() * 100
avg_utilization = (
    enriched_df['utilization'].mean() * 100 if 'utilization' in enriched_df.columns else 0
)
avg_yield = (enriched_df['revenue'] / enriched_df['balance']).mean()

# 2. Display High-Level Metrics
st.header("Portfolio Health & Quality Metrics")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Data Quality Score", f"{data_quality_score:.2f}%", help="Completeness of the source data.")
col2.metric("Data Freshness", f"{data_freshness_days} days", help="Lag since last ingestion.")
col3.metric("Delinquency Rate", f"{delinquency_rate:.1f}%", delta="vs. target 6.5%", delta_color="inverse")
col4.metric("Avg. Portfolio Yield", f"{avg_yield:.2f}x", help="Revenue-to-balance yield factor.")

kpi_table = pd.DataFrame([
    {"KPI": "Active Customers", "Value": portfolio_size, "Target": 100, "Status": "On Track"},
    {"KPI": "Avg Utilization", "Value": f"{avg_utilization:.1f}%", "Target": "< 65%", "Status": "On Track"},
    {"KPI": "90+ DPD", "Value": f"{(enriched_df['dpd'] >= 90).mean() * 100:.1f}%", "Target": "< 5%", "Status": "Watch"},
    {"KPI": "Collections Coverage", "Value": "92%", "Target": "95%", "Status": "Catch-Up"},
])

st.dataframe(kpi_table, hide_index=True, use_container_width=True)

# 3. Display Distribution Charts
st.header("Customer Distributions")
col_dist1, col_dist2 = st.columns(2)

with col_dist1:
    dpd_chart = alt.Chart(enriched_df).mark_bar().encode(
        x=alt.X('dpd_bucket:N', title='DPD Bucket', sort=['Current', '1-30 DPD', '31-60 DPD', '61-90 DPD', '90+ DPD']),
        y=alt.Y('count():Q', title='Number of Customers'),
        tooltip=['dpd_bucket', 'count()']
    ).properties(
        title='DPD Bucket Distribution'
    )
    st.altair_chart(dpd_chart, use_container_width=True)

with col_dist2:
    segment_chart = alt.Chart(enriched_df).mark_bar().encode(
        x=alt.X('segment:N', title='Customer Segment', sort=['Bronze', 'Silver', 'Gold']),
        y=alt.Y('count():Q', title='Number of Customers'),
        tooltip=['segment', 'count()']
    ).properties(
        title='Customer Segment Distribution'
    )
    st.altair_chart(segment_chart, use_container_width=True)

st.header("Utilization by Segment")
utilization_chart = alt.Chart(enriched_df).mark_bar().encode(
    x=alt.X('segment:N', sort=['Bronze', 'Silver', 'Gold'], title='Customer Segment'),
    y=alt.Y('mean(utilization):Q', title='Avg Utilization'),
    color='segment:N',
    tooltip=[
        alt.Tooltip('segment', title='Segment'),
        alt.Tooltip('mean(utilization)', title='Avg Utilization', format='.1%'),
        alt.Tooltip('count()', title='Customers')
    ]
).properties(title='Segment Utilization Efficiency')
st.altair_chart(utilization_chart, use_container_width=True)

# 4. Display Customer Data Table
st.header("Enriched Customer Portfolio Data")
st.dataframe(enriched_df)
st.caption("Industry GDP Benchmark: +2.1% (YoY)")
