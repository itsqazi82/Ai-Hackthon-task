import streamlit as st
import requests

# ================= CONFIG =================
API_KEY = "4fcad71e81a8087b4dc9c3291dc5a6ae"
GEO_URL = "http://api.openweathermap.org/geo/1.0/direct"
AIR_URL = "http://api.openweathermap.org/data/2.5/air_pollution"

st.set_page_config(
    page_title="Air Pollution Checker",
    page_icon="🌍",
    layout="centered"
)

# ================= STYLES =================
st.markdown("""
<style>
.card {
    padding: 20px;
    border-radius: 15px;
    background: linear-gradient(135deg, #1f4037, #99f2c8);
    color: black;
    font-size: 18px;
}
.result {
    font-size: 22px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# ================= FUNCTIONS =================
def get_air_quality_label(aqi):
    labels = {
        1: "Good 😊",
        2: "Fair 🙂",
        3: "Moderate 😐",
        4: "Poor 😷",
        5: "Very Poor ☠️"
    }
    return labels.get(aqi, "Unknown")

# ================= UI =================
st.title("🌍 Air Pollution Monitoring System")
st.write("Check real-time air pollution using your location")

city = st.text_input("Enter City Name", placeholder="e.g. Karachi, Lahore, London")

if st.button("Check Air Quality"):

    if city.strip() == "":
        st.warning("Please enter a city name.")
        st.stop()

    # ---------- Get Coordinates ----------
    geo_params = {
        "q": city,
        "limit": 1,
        "appid": API_KEY
    }

    geo_response = requests.get(GEO_URL, params=geo_params).json()

    # ✅ FIX: Proper response check
    if not isinstance(geo_response, list) or len(geo_response) == 0:
        st.error("❌ City not found OR API key not active.")
        st.stop()

    lat = geo_response[0]["lat"]
    lon = geo_response[0]["lon"]

    # ---------- Get Air Pollution Data ----------
    air_params = {
        "lat": lat,
        "lon": lon,
        "appid": API_KEY
    }

    air_data = requests.get(AIR_URL, params=air_params).json()

    # ✅ FIX: Safe air data check
    if "list" not in air_data or len(air_data["list"]) == 0:
        st.error("❌ Air pollution data not available.")
        st.stop()

    components = air_data["list"][0]["components"]
    aqi = air_data["list"][0]["main"]["aqi"]

    # ---------- Display Result ----------
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown(
        f"<div class='result'>Air Quality: {get_air_quality_label(aqi)}</div>",
        unsafe_allow_html=True
    )
    st.write(f"📍 Location: **{city.title()}**")
    st.write("---")

    st.write(f"🧪 **SO₂:** {components['so2']} µg/m³")
    st.write(f"🧪 **NO₂:** {components['no2']} µg/m³")
    st.write(f"🧪 **PM10:** {components['pm10']} µg/m³")
    st.write(f"🧪 **PM2.5:** {components['pm2_5']} µg/m³")
    st.write(f"🧪 **O₃:** {components['o3']} µg/m³")
    st.write(f"🧪 **CO:** {components['co']} µg/m³")

    st.markdown("</div>", unsafe_allow_html=True)
