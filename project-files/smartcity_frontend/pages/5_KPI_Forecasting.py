import streamlit as st
from components.kpi_forecast import kpi_forecast_ui  # ✅ match the actual file name

st.title("📊 KPI Forecast & Anomaly Checker")
kpi_forecast_ui()
