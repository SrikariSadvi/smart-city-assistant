import streamlit as st
import requests

def feedback_form_ui():
    st.subheader("📝 Citizen Feedback Form")
    name = st.text_input("Your Name")
    email = st.text_input("Your Email")
    message = st.text_area("Your Feedback / Message")

    if st.button("Submit Feedback"):
        if not name or not email or not message:
            st.warning("Please fill out all fields.")
        else:
            try:
                res = requests.post(
                    "http://localhost:8000/submit-feedback",
                    json={"name": name, "email": email, "message": message}
                )
                if res.status_code == 200:
                    st.success("✅ Thanks for your feedback!")
                else:
                    st.error("❌ Submission failed.")
            except Exception as e:
                st.error(f"Error: {e}")
