import streamlit as st
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules.weather_module import get_weather, get_forecast, get_farming_advice

st.set_page_config(page_title="Weather", page_icon="🌦️", layout="wide")

st.title("🌦️ Weather Forecast")
st.markdown("Get real-time weather and farming advice for your location.")
st.markdown("---")

city = st.text_input("🏙️ Enter City Name", placeholder="e.g. Pune, Mumbai, Nagpur")

if st.button("🔍 Get Weather", use_container_width=True):
    if city:
        with st.spinner("Fetching weather data..."):
            weather, error = get_weather(city)

        if error:
            st.error(f"❌ {error}")
        else:
            # Main weather card
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("🌡️ Temperature",  f"{weather['temp']}°C",    f"Feels {weather['feels_like']}°C")
            col2.metric("💧 Humidity",      f"{weather['humidity']}%")
            col3.metric("💨 Wind Speed",    f"{weather['wind_speed']} m/s")
            col4.metric("👁️ Visibility",    f"{weather['visibility']} km")

            st.info(f"📍 **{weather['city']}, {weather['country']}** — {weather['description']}")

            st.markdown("---")

            # Farming advice
            st.subheader("🌾 Farming Advice for Today")
            advice = get_farming_advice(weather)
            for a in advice:
                st.success(a)

            # Forecast
            st.markdown("---")
            st.subheader("📅 Next 5 Hours Forecast")
            forecast = get_forecast(city)
            if forecast:
                cols = st.columns(len(forecast))
                for i, f in enumerate(forecast):
                    with cols[i]:
                        st.markdown(f"**{f['time'][11:16]}**")
                        st.metric("Temp", f"{f['temp']}°C")
                        st.caption(f['description'])
    else:
        st.warning("Please enter a city name!")