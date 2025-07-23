import streamlit as st
import json
from datetime import datetime
import os

def collect_user_info():
    st.title("📝 Personal Health Profile")
    st.markdown("Please provide your information to personalize your health forecast.")

    name = st.text_input("Name")
    age = st.number_input("Age", min_value=1, max_value=120, step=1)
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])

    conditions = st.multiselect(
        "Do you have any pre-existing health conditions?",
        ["Asthma", "COPD", "Heart Disease", "Diabetes", "Allergies", "None"]
    )

    submitted = st.button("Submit")

    if submitted:
        user_data = {
            "name": name,
            "age": age,
            "gender": gender,
            "conditions": conditions if conditions else ["None"],
            "timestamp": str(datetime.now())
        }

        os.makedirs("data", exist_ok=True)

        with open("data/user.json", "w") as f:
            json.dump(user_data, f, indent=4)

        all_data_file = "data/user_data.json"
        if os.path.exists(all_data_file):
            with open(all_data_file, "r") as f:
                all_users = json.load(f)
        else:
            all_users = []

        all_users.append(user_data)
        with open(all_data_file, "w") as f:
            json.dump(all_users, f, indent=4)

        st.success(f"User profile for {name} saved successfully!")
        return True

    return False
