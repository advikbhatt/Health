import streamlit as st
from home_page import home_page
from data_collect import collect_user_info

def main():
    st.set_page_config(page_title="Health App", layout="centered")

    if "user_submitted" not in st.session_state:
        st.session_state.user_submitted = False

    if not st.session_state.user_submitted:
        submitted = collect_user_info()
        if submitted:
            st.session_state.user_submitted = True
            st.rerun()
    else:
        home_page()

if __name__ == "__main__":
    main()
