import streamlit as st
import requests
from dotenv import load_dotenv
import os
import json
from datetime import datetime
from generate_report import generate_ai_health_report


def home_page():
    # Load env variables
    load_dotenv()
    weather_api_key = st.secrets["OPENWEATHER_API_KEY"]

    st.set_page_config(page_title="Weather & Pollution Dashboard", layout="wide")
    st.markdown("<h1 style='text-align: center;'>🌍 Weather & Air Quality Dashboard</h1>", unsafe_allow_html=True)
    st.markdown("---")

    def get_location_from_ip():
        return requests.get("https://ipinfo.io/json").json()

    def get_coords_from_city(city, api_key):
        geocode_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={api_key}"
        response = requests.get(geocode_url).json()
        if response:
            return response[0]["lat"], response[0]["lon"], response[0]["name"], response[0].get("state", ""), response[0]["country"]
        return None, None, None, None, None

    def get_weather(lat, lon, api_key):
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"
        return requests.get(url).json()

    def get_pollution(lat, lon, api_key):
        url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={api_key}"
        return requests.get(url).json()

    # Load default location
    location_data = get_location_from_ip()
    default_city = location_data.get("city", "")
    default_coords = location_data.get("loc", "").split(',')
    default_lat, default_lon = default_coords if len(default_coords) == 2 else ("", "")

    st.markdown("### 🔍 Enter City Name or use your current location")
    city = st.text_input("City", value=default_city, placeholder="e.g., Delhi, Tokyo")

    lat, lon, name, region, country = get_coords_from_city(city, weather_api_key)
    if not lat or not lon:
        st.error("❌ Location not found. Please enter a valid city.")
        st.stop()

    weather_data = get_weather(lat, lon, weather_api_key)
    pollution_data = get_pollution(lat, lon, weather_api_key)

    pollutants = {}
    if "list" in pollution_data:
        pollutants = pollution_data["list"][0]["components"]

    # ─────────── Display UI ───────────
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("## 📍 Location")
        st.markdown(f"**City:** {name}")
        st.markdown(f"**Region:** {region or 'N/A'}")
        st.markdown(f"**Country:** {country}")
        st.markdown(f"**Coordinates:** `{lat}, {lon}`")

    with col2:
        st.markdown("## 🌦 Weather")
        if "main" in weather_data:
            st.metric("Temperature", f"{weather_data['main']['temp']} °C")
            st.metric("Humidity", f"{weather_data['main']['humidity']} %")
            st.metric("Condition", weather_data['weather'][0]['main'])
        else:
            st.write("Weather data unavailable.")

    with col3:
        st.markdown("## 💨 Air Pollution")
        if pollutants:
            result_report = {
                "location": {
                    "city": city,
                    "latitude": lat,
                    "longitude": lon,
                    "region": region,
                    "country": country
                },
                "pollution_data": {
                    "PM2.5": pollutants.get("pm2_5"),
                    "PM10": pollutants.get("pm10"),
                    "CO": pollutants.get("co"),
                    "NO2": pollutants.get("no2"),
                    "O3": pollutants.get("o3")
                },
                "timestamp": datetime.now().isoformat()
            }

            os.makedirs("data", exist_ok=True)

            with open("data/result.json", "w") as f:
                json.dump(result_report, f, indent=4)

            # Update users list
            data_path = "data/data.json"
            if os.path.exists(data_path):
                with open(data_path, "r") as f:
                    all_users = json.load(f)
            else:
                all_users = []

            user_exists = any(user["city"].lower() == city.lower() and
                              user["latitude"] == lat and user["longitude"] == lon
                              for user in all_users)

            if not user_exists:
                all_users.append({
                    "city": city,
                    "latitude": lat,
                    "longitude": lon,
                    "region": region,
                    "country": country,
                    "joined_at": datetime.now().isoformat()
                })

            with open(data_path, "w") as f:
                json.dump(all_users, f, indent=4)

            def pollutant_row(label, value, description):
                return f"""
                    <div style="margin-bottom: 10px;">
                        <span class="tooltip">
                            <strong>{label}</strong>: {value} μg/m³
                            <span class="tooltiptext">{description}</span>
                        </span>
                    </div>
                """

            st.markdown("""
                <style>
                .tooltip {
                    position: relative;
                    display: inline-block;
                    border-bottom: 1px dotted #ccc;
                    cursor: help;
                }
                .tooltip .tooltiptext {
                    visibility: hidden;
                    width: 240px;
                    background-color: #1c1c1c;
                    color: #fff;
                    text-align: left;
                    border-radius: 6px;
                    padding: 8px;
                    position: absolute;
                    z-index: 1;
                    bottom: 125%; 
                    left: 50%;
                    margin-left: -120px;
                    opacity: 0;
                    transition: opacity 0.3s;
                    font-size: 0.85rem;
                }
                .tooltip:hover .tooltiptext {
                    visibility: visible;
                    opacity: 1;
                }
               


                .report-container {
                    border: 2px solid #ccc;
                    padding: 20px;
                    border-radius: 15px;
                    background-color: #f9f9f9;
                    font-family: 'Segoe UI', sans-serif;
                }
                .download-button {
                    float: right;
                    margin-top: -40px;
                }
                 </style>

            """, unsafe_allow_html=True)

            st.markdown(pollutant_row("PM2.5", pollutants['pm2_5'], "Particulate Matter <2.5μm – Can penetrate lungs and cause health issues."), unsafe_allow_html=True)
            st.markdown(pollutant_row("PM10", pollutants['pm10'], "Particulate Matter <10μm – Can cause respiratory irritation."), unsafe_allow_html=True)
            st.markdown(pollutant_row("CO", pollutants['co'], "Carbon Monoxide – Reduces oxygen delivery to organs and tissues."), unsafe_allow_html=True)
            st.markdown(pollutant_row("NO₂", pollutants['no2'], "Nitrogen Dioxide – Linked to lung inflammation and infections."), unsafe_allow_html=True)
            st.markdown(pollutant_row("O₃", pollutants['o3'], "Ozone – Aggravates asthma and affects lung function."), unsafe_allow_html=True)
        else:
            st.warning("Air quality data unavailable for this location.")


    st.title("🏥 Health Impact Dashboard")
    with st.expander("🧠 AI Health Forecast Report (Generated using Perplexity AI)", expanded=True):
        with st.spinner("Generating AI health impact report... Please wait."):
            try:
                ai_report = generate_ai_health_report()
                st.download_button("📥 Download Report", ai_report, file_name="Health_Report.txt")
                st.markdown(ai_report, unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Failed to generate AI report: {e}")