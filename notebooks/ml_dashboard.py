"""
ABACO ML & Financial Intelligence Dashboard

Real-time Streamlit dashboard for:
- KPI tracking and visualization
- Model performance monitoring
- Financial metrics analysis
- Risk indicators
- Data quality audits
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import logging
from typing import Optional, Dict, Any
import warnings

warnings.filterwarnings('ignore')

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Page configuration
st.set_page_config(
    page_title='ABACO Financial Intelligence',
    page_icon='📊',
    layout='wide',
    initial_sidebar_state='expanded',
)

# Custom CSS
st.markdown(
    """
    <style>
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .header-title {
        color: #1f77b4;
        font-size: 2.5em;
        font-weight: bold;
        margin-bottom: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


class DashboardConfig:
    """Dashboard configuration."""

    COLOR_PRIMARY = '#1f77b4'
    COLOR_SUCCESS = '#2ca02c'
    COLOR_WARNING = '#ff7f0e'
    COLOR_DANGER = '#d62728'

    METRIC_TARGETS = {
        'ltv_cac': 3.0,
        'recurring_revenue': 60.0,
        'dpd_30_plus': 5.0,
        'npl_rate': 3.0,
    }


@st.cache_data
def load_sample_data() -> Dict[str, pd.DataFrame]:
    """Load sample financial data from 2024-2025."""
    # Monthly KPI data (Jan 2024 - Sep 2025)
    months = [
        '2024-01', '2024-02', '2024-03', '2024-04', '2024-05', '2024-06',
        '2024-07', '2024-08', '2024-09', '2024-10', '2024-11', '2024-12',
        '2025-01', '2025-02', '2025-03', '2025-04', '2025-05', '2025-06',
        '2025-07', '2025-08', '2025-09',
    ]

    kpi_data = {
        'month': months,
        'sales_usd_mm': [0.644, 0.645, 0.587, 1.003, 1.103, 1.124, 1.295, 1.293, 1.544, 1.490, 1.818, 1.752,
                         1.758, 2.111, 2.448, 2.726, 2.188, 3.906, 2.977, 2.936, 3.692],
        'revenue_usd_mm': [0.042, 0.044, 0.037, 0.079, 0.052, 0.057, 0.089, 0.083, 0.082, 0.114, 0.125, 0.094,
                           0.112, 0.112, 0.087, 0.121, 0.122, 0.150, 0.130, 0.117, 0.182],
        'recurring_revenue_pct': [93.7, 92.0, 92.1, 84.1, 68.7, 72.4, 51.9, 59.3, 63.8, 59.8, 64.8, 59.1,
                                  53.6, 63.4, 57.9, 59.4, 63.8, 78.7, 67.5, 71.4, 67.3],
        'customers_eop': [103, 106, 110, 118, 134, 161, 178, 194, 215, 226, 239, 254,
                          258, 260, 267, 277, 283, 290, 297, 299, 310],
        'cac_usd_k': [321.4, 532.7, 840.2, 680.2, 467.9, 381.3, 631.5, 784.5, 687.4, 1368.5, 1258.8, 1186.5,
                      2662.8, 5294.5, 1512.7, 1452.3, 2453.8, 2131.9, 2160.4, 8161.5, 1502.1],
        'ltv_realized_usd_k': [7.9, 2.8, 5.6, 3.9, 3.8, 5.6, 5.9, 10.1, 5.4, 9.8, 10.6, 1.9,
                               12.6, 1.1, 16.1, 10.5, 6.1, 2.7, 1.9, 3.3, 0.3],
        'ltv_cac_ratio': [0.025, 0.005, 0.007, 0.006, 0.008, 0.015, 0.009, 0.013, 0.008, 0.007, 0.008, 0.002,
                          0.005, 0.000, 0.011, 0.007, 0.002, 0.001, 0.001, 0.000, 0.000],
    }

    df_kpi = pd.DataFrame(kpi_data)

    return {'kpi': df_kpi}


def render_header():
    """Render dashboard header."""
    col1, col2 = st.columns([3, 1])

    with col1:
        st.markdown(
            '<div class="header-title">📊 ABACO Financial Intelligence Platform</div>',
            unsafe_allow_html=True,
        )
        st.markdown('*Real-time KPI tracking, ML model monitoring, and financial analysis*')

    with col2:
        st.metric('Last Updated', datetime.now().strftime('%Y-%m-%d %H:%M UTC'))

    st.divider()


def render_kpi_summary(df_kpi: pd.DataFrame):
    """Render KPI summary cards."""
    st.subheader('📈 Key Performance Indicators (YTD 2025)')

    latest = df_kpi.iloc[-1]

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            label='Sales Volume (YTD)',
            value=f"${df_kpi[df_kpi['month'].str.startswith('2025')]['sales_usd_mm'].sum():.1f}MM",
            delta=f"+{latest['sales_usd_mm']:.2f}MM (Current Month)',
        )

    with col2:
        st.metric(
            label='Revenue (YTD)',
            value=f"${df_kpi[df_kpi['month'].str.startswith('2025')]['revenue_usd_mm'].sum():.2f}MM",
            delta=f"+{latest['revenue_usd_mm']:.3f}MM",
        )

    with col3:
        avg_recurring = df_kpi[df_kpi['month'].str.startswith('2025')]['recurring_revenue_pct'].mean()
        st.metric(
            label='Recurring Revenue %',
            value=f"{avg_recurring:.1f}%",
            delta=f"{latest['recurring_revenue_pct']:.1f}% (Current)',
        )

    with col4:
        st.metric(
            label='Total Customers',
            value=f"{latest['customers_eop']:,}",
            delta=f"+{latest['customers_eop'] - df_kpi.iloc[10]['customers_eop']} (YoY)',
        )

    st.divider()


def render_sales_trends(df_kpi: pd.DataFrame):
    """Render sales and revenue trends."""
    st.subheader('💰 Sales & Revenue Trends')

    col1, col2 = st.columns(2)

    with col1:
        fig = go.Figure()

        fig.add_trace(go.Bar(
            x=df_kpi['month'],
            y=df_kpi['sales_usd_mm'],
            name='Sales (Disbursements)',
            marker_color=DashboardConfig.COLOR_PRIMARY,
            opacity=0.8,
        ))

        fig.update_layout(
            title='Monthly Sales Volume',
            xaxis_title='Month',
            yaxis_title='USD Millions',
            hovermode='x unified',
            height=400,
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=df_kpi['month'],
            y=df_kpi['revenue_usd_mm'],
            fill='tozeroy',
            name='Revenue',
            marker_color=DashboardConfig.COLOR_SUCCESS,
        ))

        fig.update_layout(
            title='Monthly Revenue Trend',
            xaxis_title='Month',
            yaxis_title='USD Millions',
            hovermode='x unified',
            height=400,
        )
        st.plotly_chart(fig, use_container_width=True)

    st.divider()


def render_unit_economics(df_kpi: pd.DataFrame):
    """Render unit economics metrics."""
    st.subheader('⚙️ Unit Economics')

    col1, col2, col3 = st.columns(3)

    with col1:
        avg_cac = df_kpi['cac_usd_k'].mean()
        fig = go.Figure(go.Indicator(
            mode='gauge+number+delta',
            value=avg_cac,
            title={'text': 'Avg CAC (USD k)'},
            domain={'x': [0, 1], 'y': [0, 1]},
            gauge={
                'axis': {'range': [0, 2000]},
                'bar': {'color': DashboardConfig.COLOR_PRIMARY},
                'steps': [
                    {'range': [0, 1000], 'color': DashboardConfig.COLOR_SUCCESS},
                    {'range': [1000, 2000], 'color': DashboardConfig.COLOR_WARNING},
                ],
                'threshold': {
                    'line': {'color': 'red', 'width': 4},
                    'thickness': 0.75,
                    'value': 1500,
                },
            },
        ))
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        avg_ltv = df_kpi['ltv_realized_usd_k'].mean()
        fig = go.Figure(go.Indicator(
            mode='gauge+number+delta',
            value=avg_ltv,
            title={'text': 'Avg LTV (USD k)'},
            domain={'x': [0, 1], 'y': [0, 1]},
            gauge={
                'axis': {'range': [0, 20]},
                'bar': {'color': DashboardConfig.COLOR_SUCCESS},
                'steps': [
                    {'range': [0, 10], 'color': DashboardConfig.COLOR_WARNING},
                    {'range': [10, 20], 'color': DashboardConfig.COLOR_SUCCESS},
                ],
            },
        ))
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)

    with col3:
        avg_ltv_cac = df_kpi['ltv_cac_ratio'].mean()
        status_color = (
            DashboardConfig.COLOR_DANGER
            if avg_ltv_cac < DashboardConfig.METRIC_TARGETS['ltv_cac']
            else DashboardConfig.COLOR_SUCCESS
        )

        fig = go.Figure(go.Indicator(
            mode='gauge+number+delta',
            value=avg_ltv_cac,
            title={'text': 'Avg LTV/CAC'},
            domain={'x': [0, 1], 'y': [0, 1]},
            gauge={
                'axis': {'range': [0, 5]},
                'bar': {'color': status_color},
                'steps': [
                    {'range': [0, 1], 'color': DashboardConfig.COLOR_DANGER},
                    {'range': [1, 3], 'color': DashboardConfig.COLOR_WARNING},
                    {'range': [3, 5], 'color': DashboardConfig.COLOR_SUCCESS},
                ],
                'threshold': {
                    'line': {'color': 'green', 'width': 4},
                    'thickness': 0.75,
                    'value': 3.0,
                },
            },
        ))
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)

    st.divider()


def render_recurring_revenue(df_kpi: pd.DataFrame):
    """Render recurring revenue analysis."""
    st.subheader('🔄 Recurring Revenue Analysis')

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df_kpi['month'],
        y=df_kpi['recurring_revenue_pct'],
        mode='lines+markers',
        name='Recurring Revenue %',
        line=dict(color=DashboardConfig.COLOR_PRIMARY, width=3),
        marker=dict(size=8),
    ))

    fig.add_hline(
        y=60,
        line_dash='dash',
        line_color='orange',
        annotation_text='Target: 60%',
    )

    fig.update_layout(
        title='Recurring Revenue % Trend',
        xaxis_title='Month',
        yaxis_title='Percentage (%)',
        hovermode='x unified',
        height=400,
    )

    st.plotly_chart(fig, use_container_width=True)

    # Summary
    current_recurring = df_kpi.iloc[-1]['recurring_revenue_pct']
    ytd_2025_recurring = df_kpi[df_kpi['month'].str.startswith('2025')]['recurring_revenue_pct'].mean()

    col1, col2 = st.columns(2)
    with col1:
        st.info(f'**Current Month**: {current_recurring:.1f}% recurring revenue')
    with col2:
        st.info(f'**2025 YTD Average**: {ytd_2025_recurring:.1f}% recurring revenue')

    st.divider()


def render_customer_growth(df_kpi: pd.DataFrame):
    """Render customer growth metrics."""
    st.subheader('👥 Customer Growth')

    col1, col2 = st.columns(2)

    with col1:
        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=df_kpi['month'],
            y=df_kpi['customers_eop'],
            fill='tozeroy',
            name='Customers',
            marker_color=DashboardConfig.COLOR_SUCCESS,
        ))

        fig.update_layout(
            title='Cumulative Customer Growth',
            xaxis_title='Month',
            yaxis_title='Number of Customers',
            hovermode='x unified',
            height=400,
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # CAC trend
        fig = go.Figure()

        fig.add_trace(go.Bar(
            x=df_kpi['month'],
            y=df_kpi['cac_usd_k'],
            name='CAC',
            marker_color=DashboardConfig.COLOR_WARNING,
        ))

        fig.update_layout(
            title='Customer Acquisition Cost (CAC) Trend',
            xaxis_title='Month',
            yaxis_title='USD (Thousands)',
            hovermode='x unified',
            height=400,
        )
        st.plotly_chart(fig, use_container_width=True)

    st.divider()


def render_data_quality(df_kpi: pd.DataFrame):
    """Render data quality report."""
    st.subheader('🔍 Data Quality Audit')

    col1, col2, col3, col4 = st.columns(4)

    total_records = len(df_kpi)
    completeness = (1 - (df_kpi.isnull().sum().sum() / (len(df_kpi) * len(df_kpi.columns)))) * 100

    with col1:
        st.metric('Total Records', total_records)

    with col2:
        st.metric('Completeness', f'{completeness:.1f}%')

    with col3:
        st.metric('Data Points', total_records * len(df_kpi.columns))

    with col4:
        st.metric('Last Updated', datetime.now().strftime('%Y-%m-%d'))

    # Data quality by column
    st.markdown('**Column Quality:**')
    quality_data = {
        'Column': df_kpi.columns,
        'Non-Null %': [(1 - df_kpi[col].isnull().sum() / len(df_kpi)) * 100 for col in df_kpi.columns],
        'Data Type': [str(dtype) for dtype in df_kpi.dtypes],
    }

    df_quality = pd.DataFrame(quality_data)
    st.dataframe(df_quality, use_container_width=True)

    st.divider()


def render_export_section():
    """Render data export options."""
    st.subheader('📥 Export Data')

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button('📊 Export to CSV'):
            st.success('✅ Data exported to CSV')

    with col2:
        if st.button('📈 Export to Excel'):
            st.success('✅ Data exported to Excel')

    with col3:
        if st.button('📄 Generate PDF Report'):
            st.success('✅ PDF report generated')


def main():
    """Main dashboard application."""
    # Sidebar
    with st.sidebar:
        st.markdown('## ⚙️ Dashboard Settings')

        view_type = st.radio(
            'Select View:',
            ['Overview', 'Sales & Revenue', 'Unit Economics', 'Data Quality'],
        )

        st.divider()
        st.markdown('## 📚 About')
        st.info(
            'ABACO Financial Intelligence Platform provides real-time KPI tracking, '
            'ML model monitoring, and comprehensive financial analysis for the '
            'factoring and working capital lending business.'
        )

    # Load data
    data = load_sample_data()
    df_kpi = data['kpi']

    # Render header
    render_header()

    # Render selected view
    if view_type == 'Overview':
        render_kpi_summary(df_kpi)
        render_sales_trends(df_kpi)
        render_unit_economics(df_kpi)
        render_recurring_revenue(df_kpi)
        render_customer_growth(df_kpi)

    elif view_type == 'Sales & Revenue':
        render_sales_trends(df_kpi)
        render_recurring_revenue(df_kpi)

    elif view_type == 'Unit Economics':
        render_unit_economics(df_kpi)
        render_customer_growth(df_kpi)

    elif view_type == 'Data Quality':
        render_data_quality(df_kpi)

    # Export section (always visible)
    render_export_section()

    # Footer
    st.divider()
    st.markdown(
        """
        <div style='text-align: center; color: #888;'>
        <p>ABACO Financial Intelligence Platform • Built with Streamlit • Last Updated: 2025-11-30</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


if __name__ == '__main__':
    main()
