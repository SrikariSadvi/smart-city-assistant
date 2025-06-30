import os
from fpdf import FPDF
from datetime import datetime
import streamlit as st

def generate_pdf_report(city_name, kpi_data, report_text):
    """
    Generate a PDF report from the given KPI data and sustainability report.
    """
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Title
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, f"Sustainability Report - {city_name}", ln=True, align="C")

    # Date
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 10, f"Date: {datetime.now().strftime('%Y-%m-%d')}", ln=True)

    # KPI Section
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Key Performance Indicators (KPIs):", ln=True)

    pdf.set_font("Arial", "", 12)
    for line in kpi_data.split("\n"):
        if ":" in line:
            kpi, value = line.split(":", 1)
            pdf.cell(0, 10, f"{kpi.strip()}: {value.strip()}", ln=True)

    pdf.ln(5)

    # Report Section
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Sustainability Report:", ln=True)

    pdf.set_font("Arial", "", 12)
    for line in report_text.split("\n"):
        pdf.multi_cell(0, 10, line)

    # Save to temp file
    output_path = "temp_report.pdf"
    pdf.output(output_path)

    return output_path


def report_generator_ui():
    st.header("📝 Generate Your City Sustainability Report")

    city_name = st.text_input("Enter your city name")
    kpi_data = st.text_area("Paste your KPI values (format: KPI: Value)", height=200)

    if st.button("Generate Report"):
        if not city_name or not kpi_data.strip():
            st.warning("Please provide both city name and KPI data.")
            return

        # Simulate AI report generation (or call your Watsonx backend)
        report_text = f"Based on the KPIs provided, here is a mock sustainability report for {city_name}.\n\n"

        for line in kpi_data.strip().split("\n"):
            if ":" in line:
                kpi, value = line.split(":", 1)
                report_text += f"- {kpi.strip()} is currently at {value.strip()}, which is being monitored.\n"

        st.success("✅ Report Generated Successfully!")

        st.markdown("### 📄 Sustainability Report")
        st.text(report_text)

        # Offer downloads
        st.download_button(
            label="📥 Download .md",
            data=report_text,
            file_name=f"{city_name}_sustainability_report.md",
            mime="text/markdown"
        )

        pdf_path = generate_pdf_report(city_name, kpi_data, report_text)
        with open(pdf_path, "rb") as pdf_file:
            st.download_button(
                label="📄 Download .pdf",
                data=pdf_file,
                file_name=f"{city_name}_sustainability_report.pdf",
                mime="application/pdf"
            )

        # Clean up temp file
        os.remove(pdf_path)
