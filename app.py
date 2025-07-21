import streamlit as st
from login_page import login_page
from register_page import register_page
from profile_page import profile_page
from home_page import home_page  # New home page

# Session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

def main():
    st.set_page_config(page_title="Health App", layout="centered")

    if not st.session_state.logged_in:
        tab = st.tabs(["Login", "Register"])
        with tab[0]:
            login_page()
        with tab[1]:
            register_page()
    else:
        tab = st.tabs(["Home", "Profile"])
        with tab[0]:
            home_page()
        with tab[1]:
            profile_page()

if __name__ == "__main__":
    main()
