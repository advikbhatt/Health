import os
import json
import requests

PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY")

def generate_ai_health_report():
    with open("data/result.json", "r") as file:
        result_data = json.load(file)

    with open("data/user.json", "r") as user_file:
        user_data = json.load(user_file)

    pollution_data = result_data["pollution_data"]
    city = result_data["location"]["city"]
    timestamp = result_data["timestamp"]

    name = user_data["name"]
    age = user_data["age"]
    gender = user_data["gender"]
    conditions = ", ".join(user_data["conditions"]) if user_data["conditions"] else "None"
    location = user_data["location"]

    prompt = f"""
    You are a certified environmental health expert preparing a personalized air quality health report.

    👤 Patient Name: {name}
    📍 Location: {location}
    🎂 Age: {age} | Gender: {gender}
    🩺 Pre-existing Conditions: {conditions}

    📊 Pollution Data (from {city} at {timestamp}):
    - PM2.5: {pollution_data['PM2.5']} µg/m³  
    - PM10: {pollution_data['PM10']} µg/m³  
    - CO: {pollution_data['CO']} µg/m³  
    - NO2: {pollution_data['NO2']} µg/m³  
    - O3: {pollution_data['O3']} µg/m³

    Generate a medical-style report including:
    1. Short- and long-term health risks based on age and conditions
    2. Visual indicators or bullet charts if needed
    3. Specific precautions the user should follow
    4. Color-coded health risk level (Low, Moderate, High)
    5. Professional medical-style tone

    Return in a well-structured format for patient understanding.
    """

    url = "https://api.perplexity.ai/chat/completions"
    headers = {
        "Authorization": f"Bearer {PERPLEXITY_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "sonar-reasoning",
        "messages": [{"role": "user", "content": prompt}],
        "stream": False
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        ai_report = response.json()['choices'][0]['message']['content']
        return ai_report
    else:
        raise Exception(f"Failed to generate report: {response.status_code} - {response.text}")
