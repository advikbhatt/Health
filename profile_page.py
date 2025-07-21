from firebase_config import db
import streamlit as st

def profile_page():
    st.title("User Profile")

    # Example: Fetch all users from Firestore collection 'users'
    users = db.collection('users').stream()

    for user in users:
        user_data = user.to_dict()
        st.write(f"Name: {user_data.get('name')}")
        st.write(f"Email: {user_data.get('email')}")
        st.markdown("---")
