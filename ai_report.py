import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()
PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY")

def generate_ai_health_report():
    # Load user data
    with open("data/user.json", "r") as user_file:
        user_data = json.load(user_file)

    # Load pollution and location data
    with open("data/result.json", "r") as result_file:
        result_data = json.load(result_file)

    pollution_data = result_data["pollution_data"]
    city = result_data["location"]["city"]
    timestamp = result_data["timestamp"]

    name = user_data["name"]
    age = user_data["age"]
    health_conditions = ", ".join(user_data["health_conditions"])
    smoker = user_data["smoker"]
    exercise = user_data["exercise"]

    prompt = f"""
    You are a certified environmental physician writing a personalized air pollution health impact report for a patient.

    ## Patient Info:
    - Name: {name}
    - Age: {age}
    - Existing Health Conditions: {health_conditions}
    - Smoking Status: {'Smoker' if smoker else 'Non-smoker'}
    - Exercise Habit: {exercise}

    ## Environmental Exposure:
    The following pollution data was recorded in {city} at {timestamp}:

    - PM2.5: {pollution_data['PM2.5']} µg/m³
    - PM10: {pollution_data['PM10']} µg/m³
    - CO: {pollution_data['CO']} µg/m³
    - NO₂: {pollution_data['NO2']} µg/m³
    - O₃: {pollution_data['O3']} µg/m³

    ### Report Format:
    Write this in the style of a doctor's prescription including:
    1. **Health Risk Summary** based on age and conditions
    2. **Short-term symptoms** expected
    3. **Long-term health impacts** considering user profile
    4. **Recommended actions & treatments** (air purifiers, masks, etc.)
    5. Use bullets, tables, or simple charts where useful
    6. Provide comparisons to safe WHO levels
    7. Add a friendly but professional closing statement
    """

    url = "https://api.perplexity.ai/chat/completions"
    headers = {
        "Authorization": f"Bearer {PERPLEXITY_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "sonar-reasoning", 
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "stream": False
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        report = response.json()['choices'][0]['message']['content']
        print("✅ AI Health Report Generated:\n")
        print(report)
    else:
        raise Exception(f"❌ Failed to generate report: {response.status_code} - {response.text}")

# Run this script
if __name__ == "__main__":
    generate_ai_health_report()
