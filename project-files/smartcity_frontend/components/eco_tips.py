import streamlit as st
import requests

def eco_tips_ui():
    st.subheader("🌿 Generate an Eco-Friendly Tip")
    topic = st.text_input("Enter a topic (e.g., water, energy, transportation)")

    if st.button("Generate Tip"):
        if not topic.strip():
            st.warning("Please provide a topic to generate a tip.")
            return
        try:
            res = requests.get(f"http://localhost:8000/get-eco-tips?topic={topic}")
            if res.status_code == 200:
                st.success(res.json()["tip"])
            else:
                st.error(f"Error {res.status_code}: {res.json()['detail']}")
        except Exception as e:
            st.error(f"Tip generation failed: {e}")