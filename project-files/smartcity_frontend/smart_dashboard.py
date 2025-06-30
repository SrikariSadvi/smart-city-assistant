import streamlit as st
from streamlit_lottie import st_lottie
import requests

@st.cache_data
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

st.set_page_config(page_title="Smart City Assistant", layout="wide")

lottie_city = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_w51pcehl.json")

st.title("🌆 Welcome to the Smart City Assistant Dashboard")
st.markdown("Your AI-powered solution for a greener, smarter, and citizen-friendly urban future 🚀")

col1, col2 = st.columns([1, 2])
with col1:
    if lottie_city:
        st_lottie(lottie_city, height=300, key="city")
    else:
        st.error("❌ Failed to load city animation.")

with col2:
    st.markdown("""
    ### 🔍 What you can do here:
    - 🧠 **AI Chat Assistant** for all your smart city questions
    - 🌱 **Eco Tips** for sustainable living
    - 📜 **Policy Search** for quick summaries
    - 📊 **Dashboard** showing key insights
    - ⚠️ **Anomaly Detection** in city KPIs
    - 📮 **Feedback Form** to voice your concerns
    - 📈 **Forecasting** for future trends

    ---
    🕹️ Use the sidebar to navigate between features!
    """)

st.markdown("---")
st.caption("Built with ❤️ by your team using Streamlit and IBM Granite AI")
