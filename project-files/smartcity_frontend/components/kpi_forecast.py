import streamlit as st
import requests
import pandas as pd
import altair as alt

def kpi_forecast_ui():
    st.subheader("📊 KPI CSV Forecasting & Anomaly Detection")

    uploaded_file = st.file_uploader("Upload a KPI CSV file (with 'Date' and 'KPI_Value' columns)", type=["csv"])

    metric = st.selectbox("Select KPI Type", ["Energy Usage", "Water Usage", "Traffic Flow"])
    days = st.slider("Forecast for next days:", 1, 30, 7)

    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.dataframe(df)

        if st.button("Run Forecast & Anomaly Detection"):
            try:
                files = {"file": uploaded_file.getvalue()}
                res_forecast = requests.post("http://localhost:8000/upload_csv_forecast", files=files)
                res_anomaly = requests.post("http://localhost:8000/upload_csv_anomaly", files=files)

                if res_forecast.status_code == 200 and res_anomaly.status_code == 200:
                    forecast_result = res_forecast.json()["forecast"]
                    anomaly_result = res_anomaly.json()["anomalies"]

                    # 📈 Forecast Visualization
                    st.success("📈 Forecast Chart:")
                    forecast_df = pd.DataFrame(forecast_result)
                    forecast_df["date"] = pd.to_datetime(forecast_df["date"])

                    chart = alt.Chart(forecast_df).mark_line(point=True).encode(
                        x=alt.X("date:T", title="Date"),
                        y=alt.Y("predicted_kpi:Q", title="Predicted KPI"),
                        tooltip=["date:T", "predicted_kpi"]
                    ).properties(
                        title="Forecasted KPI Over Time"
                    )

                    st.altair_chart(chart, use_container_width=True)

                    # ⚠️ Anomaly Table
                    st.warning("⚠️ Detected Anomalies:")
                    if anomaly_result:
                        anomaly_df = pd.DataFrame(anomaly_result)
                        st.dataframe(anomaly_df)
                    else:
                        st.success("No anomalies detected.")
                else:
                    st.error("❌ Backend Error during forecast or anomaly detection.")
            except Exception as e:
                st.error(f"Error: {e}")
