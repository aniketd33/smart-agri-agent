import streamlit as st
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.language import render_language_sidebar
from modules.weather_module import get_weather, get_forecast, get_farming_advice

st.set_page_config(page_title="Weather", page_icon="🌦️", layout="wide")

T, lang_key = render_language_sidebar()

st.title(T["wt_title"])
st.markdown(T["wt_subtitle"])
st.markdown("---")

city = st.text_input(T["wt_city"], placeholder=T["wt_city_hint"])

if st.button(T["wt_btn"], use_container_width=True):
    if city:
        with st.spinner(T["wt_loading"]):
            weather, error = get_weather(city)

        if error:
            st.error(f"❌ {error}")
        else:
            col1, col2, col3, col4 = st.columns(4)
            col1.metric(T["wt_temp"],       f"{weather['temp']}°C",       f"{T['wt_feels']} {weather['feels_like']}°C")
            col2.metric(T["wt_humidity"],   f"{weather['humidity']}%")
            col3.metric(T["wt_wind"],       f"{weather['wind_speed']} m/s")
            col4.metric(T["wt_visibility"], f"{weather['visibility']} km")

            st.info(f"📍 **{weather['city']}, {weather['country']}** — {weather['description']}")
            st.markdown("---")

            st.subheader(T["wt_advice"])
            advice = get_farming_advice(weather)
            for a in advice:
                st.success(a)

            st.markdown("---")
            st.subheader(T["wt_forecast"])
            forecast = get_forecast(city)
            if forecast:
                cols = st.columns(len(forecast))
                for i, f in enumerate(forecast):
                    with cols[i]:
                        st.markdown(f"**{f['time'][11:16]}**")
                        st.metric(T["wt_temp_short"], f"{f['temp']}°C")
                        st.caption(f['description'])
    else:
        st.warning(T["wt_no_city"])