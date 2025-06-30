import streamlit as st
import pandas as pd
from components.city_kpi_data import get_kpis_for_city
import plotly.express as px

st.set_page_config(page_title="Smart City Dashboard", layout="wide")
st.title("🏙️ Smart City KPI Dashboard")

city_options = ["Pune", "Hyderabad", "Chennai", "Delhi", "Bangalore", "Other"]
selected = st.selectbox("Select a City", city_options)

if selected == "Other":
    custom_city = st.text_input("Enter your city name:")
    st.info("Please input KPI values manually for custom city.")

    air_quality = st.number_input("Air Quality Index", min_value=0)
    renewable = st.text_input("Renewable Energy Usage (e.g., 65%)")
    recycling = st.text_input("Waste Recycling Rate (e.g., 40%)")
    water = st.number_input("Water Conservation Score", min_value=0)
    energy = st.number_input("Energy Efficiency Score", min_value=0)
    green = st.text_input("Green Space Coverage (e.g., 20%)")

    if custom_city:
        kpis = {
            "Air Quality Index": air_quality,
            "Renewable Energy Usage": renewable,
            "Waste Recycling Rate": recycling,
            "Water Conservation Score": water,
            "Energy Efficiency Score": energy,
            "Green Space Coverage": green
        }
        city = custom_city
    else:
        st.stop()
else:
    city = selected
    kpis = get_kpis_for_city(city)

# Display KPIs
if kpis:
    st.subheader(f"KPI Overview for {city}")
    col1, col2, col3 = st.columns(3)
    col1.metric("Air Quality Index", kpis["Air Quality Index"])
    col2.metric("Renewable Energy Usage", kpis["Renewable Energy Usage"])
    col3.metric("Waste Recycling Rate", kpis["Waste Recycling Rate"])

    col4, col5, col6 = st.columns(3)
    col4.metric("Water Conservation Score", kpis["Water Conservation Score"])
    col5.metric("Energy Efficiency Score", kpis["Energy Efficiency Score"])
    col6.metric("Green Space Coverage", kpis["Green Space Coverage"])

    # Convert KPI data for chart
    numeric_kpis = {
        "Air Quality Index": float(kpis["Air Quality Index"]),
        "Water Conservation Score": float(kpis["Water Conservation Score"]),
        "Energy Efficiency Score": float(kpis["Energy Efficiency Score"])
    }

    # Handle % values
    for k in ["Renewable Energy Usage", "Waste Recycling Rate", "Green Space Coverage"]:
        try:
            numeric_kpis[k] = float(kpis[k].replace("%", ""))
        except:
            numeric_kpis[k] = 0

    # Chart
    df = pd.DataFrame(numeric_kpis.items(), columns=["KPI", "Value"])
    st.subheader("📊 KPI Trends")
    fig = px.bar(df, x="KPI", y="Value", title=f"KPI Overview for {city}", color="KPI", text="Value")
    st.plotly_chart(fig, use_container_width=True)

else:
    st.warning("No KPI data available.")
