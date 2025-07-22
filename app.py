import streamlit as st
from home_page import home_page 

def main():
    st.set_page_config(page_title="Health App", layout="centered")
    home_page()

if __name__ == "__main__":
    main()
