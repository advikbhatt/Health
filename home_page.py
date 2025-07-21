# home.py
import streamlit as st

def home_page():
    st.title("Welcome to Home Page")

    if "user_data" in st.session_state:
        user = st.session_state.user_data
        st.write(f"Welcome, {user['username']}!")
        st.write(f"Email: {user['email']}")
    else:
        st.warning("You must login first")
