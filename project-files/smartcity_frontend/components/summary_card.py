import streamlit as st

def summary_card(title: str, value: str, icon: str = "", color: str = "#4CAF50"):
    st.markdown(
        f"""
        <div style='
            background-color: {color};
            padding: 1.2rem;
            border-radius: 12px;
            box-shadow: 2px 2px 12px rgba(0, 0, 0, 0.1);
            margin-bottom: 1rem;
        '>
            <h5 style='color: white; margin-bottom: 0.5rem;'>{icon} {title}</h5>
            <h2 style='color: white; margin: 0;'>{value}</h2>
        </div>
        """,
        unsafe_allow_html=True
    )