import streamlit as st
import requests
from components.report_generator import generate_pdf_report

st.set_page_config(page_title="Sustainability Report", layout="wide")
st.title("📄 Smart City Sustainability Report")

# ✅ City Input Field
city = st.text_input("Enter City Name", placeholder="e.g., Hyderabad")

# KPI Text Area
st.subheader("Enter City KPI Data")
kpi_data = st.text_area(
    "Paste your KPIs below",
    height=200,
    placeholder="Example:\nAir Quality Index: 42\nRenewable Energy Usage: 62%\nWaste Recycling Rate: 38%"
)

# Submit Button
if st.button("Generate Report"):
    if not city.strip() or not kpi_data.strip():
        st.warning("⚠️ Please enter both city and KPI data.")
    else:
        with st.spinner("Generating report..."):
            try:
                response = requests.post(
                    "http://127.0.0.1:8000/generate-report",
                    json={"city": city, "kpi_data": kpi_data}
                )
                if response.status_code == 200:
                    report = response.json()["report"]
                    st.success("✅ Report Generated Successfully!")

                    st.markdown("### 📝 Generated Report")
                    st.markdown(report)

                    st.download_button("📥 Download Report (Markdown)", report, file_name="sustainability_report.md")

                    pdf_filename = generate_pdf_report(city, kpi_data, report)

                    with open(pdf_filename, "rb") as f:
                        st.download_button(
                            "📄 Download Report (PDF)",
                            f,
                            file_name=pdf_filename,
                            mime="application/pdf"
                        )
                else:
                    st.error(f"❌ Failed to generate report: {response.text}")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
