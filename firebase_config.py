import firebase_admin
from firebase_admin import credentials, firestore
import streamlit as st
import os
import json

def get_firebase_credential():
    try:
        # Try to load from Streamlit Cloud secrets
        firebase_config = {
            "type": st.secrets.firebase["type"],
            "project_id": st.secrets.firebase["project_id"],
            "private_key_id": st.secrets.firebase["private_key_id"],
            "private_key": st.secrets.firebase["private_key"],
            "client_email": st.secrets.firebase["client_email"],
            "client_id": st.secrets.firebase["client_id"],
            "auth_uri": st.secrets.firebase["auth_uri"],
            "token_uri": st.secrets.firebase["token_uri"],
            "auth_provider_x509_cert_url": st.secrets.firebase["auth_provider_x509_cert_url"],
            "client_x509_cert_url": st.secrets.firebase["client_x509_cert_url"]
        }
        return credentials.Certificate(firebase_config)
    except Exception:
        # Fallback to local JSON file
        return credentials.Certificate("firebase_service_account.json")

# Initialize Firebase
if not firebase_admin._apps:
    cred = get_firebase_credential()
    firebase_admin.initialize_app(cred)

# Get Firestore DB
db = firestore.client()
