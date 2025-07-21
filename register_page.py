# register_page.py
import streamlit as st
from firebase_admin import firestore

def register_page():
    st.subheader("Register Page")

    db = firestore.client()

    email = st.text_input("Email", key="register_email")
    username = st.text_input("Username", key="register_username")
    password = st.text_input("Password", type="password", key="register_password")

    if st.button("Register", key="register_button"):
        users_ref = db.collection("users")
        query = users_ref.where("email", "==", email).get()

        if query:
            st.error("Email already exists!")
        else:
            users_ref.add({
                "email": email,
                "username": username,
                "password": password
            })
            st.success("User registered successfully!")
