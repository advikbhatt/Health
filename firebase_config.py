import firebase_admin
from firebase_admin import credentials, firestore

# Check if Firebase app is already initialized
if not firebase_admin._apps:
    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred)

# Initialize Firestore client
db = firestore.client()
