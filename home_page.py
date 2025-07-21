import streamlit as st
import requests
from dotenv import load_dotenv
import os
def home_page():

    # Load environment variables
    load_dotenv()
    weather_api_key = os.getenv("OPENWEATHER_API_KEY")

    # App layout setup
    st.set_page_config(page_title="Weather & Pollution Dashboard", layout="wide")
    st.markdown("<h1 style='text-align: center;'>🌍 Weather & Air Quality Dashboard</h1>", unsafe_allow_html=True)
    st.markdown("---")

    # Functions
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

    # Get default location
    location_data = get_location_from_ip()
    default_city = location_data.get("city", "")
    default_coords = location_data.get("loc", "").split(',')
    default_lat, default_lon = default_coords if len(default_coords) == 2 else ("", "")

    # City input
    st.markdown("### 🔍 Enter City Name or use your current location")
    city = st.text_input("City", value=default_city, placeholder="e.g., Delhi, New York, Tokyo")

    # Get coordinates from city
    lat, lon, name, region, country = get_coords_from_city(city, weather_api_key)
    if not lat or not lon:
        st.error("❌ Location not found. Please enter a valid city.")
        st.stop()

    # Fetch weather and pollution data
    weather_data = get_weather(lat, lon, weather_api_key)
    pollution_data = get_pollution(lat, lon, weather_api_key)

    # Three-column layout
    col1, col2, col3 = st.columns(3)

    # --- Column 1: Location ---
    with col1:
        st.markdown("## 📍 Location")
        st.markdown(f"**City:** {name}")
        st.markdown(f"**Region:** {region or 'N/A'}")
        st.markdown(f"**Country:** {country}")
        st.markdown(f"**Coordinates:** `{lat}, {lon}`")

    # --- Column 2: Weather ---
    with col2:
        st.markdown("## 🌦 Weather")
        if "main" in weather_data:
            st.metric("Temperature", f"{weather_data['main']['temp']} °C")
            st.metric("Humidity", f"{weather_data['main']['humidity']} %")
            st.metric("Condition", weather_data['weather'][0]['main'])
        else:
            st.write("Weather data unavailable.")

    # --- Column 3: Pollution ---
        # --- Column 3: Pollution ---
    # --- Column 3: Pollution ---
    with col3:
        st.markdown("## 💨 Air Pollution")
        if "list" in pollution_data:
            pollutants = pollution_data['list'][0]['components']
    
            # Custom tooltip CSS
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
            </style>
            """, unsafe_allow_html=True)
    
            # Display with tooltip wrappers
            def pollutant_row(label, value, description):
                return f"""
                <div style="margin-bottom: 10px;">
                    <span class="tooltip">
                        <strong>{label}</strong>: {value} μg/m³
                        <span class="tooltiptext">{description}</span>
                    </span>
                </div>
                """
    
            st.markdown(pollutant_row("PM2.5", pollutants['pm2_5'], "Particulate Matter <2.5μm – Can penetrate lungs and cause health issues."), unsafe_allow_html=True)
            st.markdown(pollutant_row("PM10", pollutants['pm10'], "Particulate Matter <10μm – Can cause respiratory irritation."), unsafe_allow_html=True)
            st.markdown(pollutant_row("CO", pollutants['co'], "Carbon Monoxide – Reduces oxygen delivery to organs and tissues."), unsafe_allow_html=True)
            st.markdown(pollutant_row("NO₂", pollutants['no2'], "Nitrogen Dioxide – Linked to lung inflammation and infections."), unsafe_allow_html=True)
            st.markdown(pollutant_row("O₃", pollutants['o3'], "Ozone – Aggravates asthma and affects lung function."), unsafe_allow_html=True)
    
        else:
            st.write("Air quality data unavailable.")
    
            st.markdown("## 💨 Air Pollution")
            if "list" in pollution_data:
                pollutants = pollution_data['list'][0]['components']
                
                st.markdown(f"""
                    **<abbr title='Particulate Matter less than 2.5 micrometers in diameter'>PM2.5</abbr>**: {pollutants['pm2_5']} μg/m³  
                    **<abbr title='Particulate Matter less than 10 micrometers in diameter'>PM10</abbr>**: {pollutants['pm10']} μg/m³  
                    **<abbr title='Carbon Monoxide - a colorless, odorless toxic gas'>CO</abbr>**: {pollutants['co']} μg/m³  
                    **<abbr title='Nitrogen Dioxide - harmful gas causing respiratory issues'>NO₂</abbr>**: {pollutants['no2']} μg/m³  
                    **<abbr title='Ozone - ground-level ozone contributes to smog and respiratory problems'>O₃</abbr>**: {pollutants['o3']} μg/m³  
                """, unsafe_allow_html=True)
            else:
                st.write("Air quality data unavailable.")
    
            st.markdown("## 💨 Air Pollution")
            if "list" in pollution_data:
                pollutants = pollution_data['list'][0]['components']
                st.markdown(f"""
                **PM2.5**: {pollutants['pm2_5']} μg/m³ 
                :information_source:[Particulate Matter <2.5μm]\n
                **PM10**: {pollutants['pm10']} μg/m³ 
                :information_source:[Particulate Matter <10μm]\n
                **CO**: {pollutants['co']} μg/m³ 
                :information_source:[Carbon Monoxide]\n
                **NO₂**: {pollutants['no2']} μg/m³ 
                :information_source:[Nitrogen Dioxide]\n
                **O₃**: {pollutants['o3']} μg/m³ 
                :information_source:[Ozone]
                """)
            else:
                st.write("Air quality data unavailable.")
    
    # Styling tip: Add footer or background styles using `st.markdown` and HTML/CSS if desired.
