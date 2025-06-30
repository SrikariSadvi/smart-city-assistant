import streamlit as st
import requests

def policy_summarizer_ui():
    st.subheader("📄 Policy Document Summarizer")
    text = st.text_area("Paste the policy document below")

    if st.button("Summarize"):
        if not text.strip():
            st.warning("Please provide some text to summarize.")
            return
        try:
            response = requests.post(
                    "http://localhost:8000/summarize-policy",
                    json={"text": text}
)

            if response.status_code == 200:
                st.info(response.json()["summary"])
            else:
                st.error(f"Error {response.status_code}: {response.json()['detail']}")
        except Exception as e:
            st.error(f"Summarization failed: {e}")