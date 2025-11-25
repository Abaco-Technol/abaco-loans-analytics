"""Unified Streamlit bootstrap that centralizes configuration and styling."""
from __future__ import annotations

import streamlit as st

from streamlit_app.app import render_dashboard
from streamlit_app.config import theme

st.set_page_config(
    page_title=theme.PAGE_TITLE,
    page_icon=theme.PAGE_ICON,
    layout=theme.LAYOUT,
    initial_sidebar_state=theme.INITIAL_SIDEBAR_STATE,
)
st.markdown(theme.CUSTOM_CSS, unsafe_allow_html=True)

render_dashboard()
