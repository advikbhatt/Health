import firebase_admin
from firebase_admin import credentials, firestore
import streamlit as st

firebase_config = st.secrets["firebase"]

cred = credentials.Certificate(firebase_config)
firebase_admin.initialize_app(cred)

db = firestore.client()
