import streamlit as st
import requests
import pandas as pd
import altair as alt

def anomaly_checker_ui():
    st.subheader("⚠️ Anomaly Detection Tool")
    kpi_input = st.text_input("Enter KPI Data (comma separated)", placeholder="e.g., 100, 105, 110, 300, 115")

    if st.button("Check for Anomalies"):
        if not kpi_input:
            st.warning("Please enter some data.")
            return

        try:
            # Convert to list of floats
            kpi_values = [float(x.strip()) for x in kpi_input.split(",") if x.strip()]
            response = requests.post(
                "http://localhost:8000/check-anomalies",
                json={"data": kpi_values}
            )

            if response.status_code == 200:
                result = response.json()
                anomalies = result.get("anomalies", [])

                df = pd.DataFrame({"Index": list(range(len(kpi_values))), "Value": kpi_values})
                anomaly_df = pd.DataFrame(anomalies)

                # Line chart with red points for anomalies
                line = alt.Chart(df).mark_line().encode(
                    x="Index:Q",
                    y="Value:Q"
                )

                points = alt.Chart(anomaly_df).mark_circle(size=100, color="red").encode(
                    x="index:Q",
                    y="value:Q"
                )

                st.altair_chart(line + points, use_container_width=True)

                if anomalies:
                    st.error("🚨 Anomalies Detected:")
                    st.dataframe(anomaly_df)
                else:
                    st.success("✅ No anomalies found.")
            else:
                st.error("Backend error occurred while checking anomalies.")
        except Exception as e:
            st.error(f"Request failed: {e}")
