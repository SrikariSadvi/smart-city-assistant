import streamlit as st
import requests

def chat_assistant():
    st.subheader("🤖 Chat with City Assistant")
    prompt = st.text_area("Ask something about your city or policies")

    if st.button("Ask"):
        if not prompt.strip():
            st.warning("Please enter a prompt before submitting.")
            return
        try:
            response = requests.post(
                "http://localhost:8000/ask-assistant",
                json={"prompt": prompt}
            )
            if response.status_code == 200:
                st.success(response.json()["response"])
            else:
                st.error(f"Error {response.status_code}: {response.json()['detail']}")
        except Exception as e:
            st.error(f"Request failed: {e}")