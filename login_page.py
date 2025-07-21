import streamlit as st
from firebase_config import db

def login_page():
    st.markdown("### Login Page")
    username = st.text_input("Username or Email")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        # 🔒 Replace this logic with your Firestore query
        user_ref = db.collection("users").where(filter=("username", "==", username)).where(filter=("password", "==", password))
        result = user_ref.get()

        if result:
            st.success("Login successful!")
            st.session_state.logged_in = True  # ✅ Login state updated
            st.rerun()
        else:
            st.error("Invalid credentials!")
