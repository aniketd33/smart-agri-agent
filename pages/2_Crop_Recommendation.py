import streamlit as st
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.language import render_language_sidebar
from modules.crop_recommender import predict_crop, get_available_options

st.set_page_config(page_title="Crop Recommendation", page_icon="🌱", layout="wide")

T, lang_key = render_language_sidebar()

st.title(T["cr_title"])
st.markdown(T["cr_subtitle"])
st.markdown("---")

options = get_available_options()

col1, col2 = st.columns(2)

with col1:
    st.subheader(T["cr_location"])
    district = st.selectbox(T["cr_district"], options["districts"])
    season   = st.selectbox(T["cr_season"],   options["seasons"])
    soil     = st.selectbox(T["cr_soil"],     options["soils"])

with col2:
    st.subheader(T["cr_soil_params"])
    N       = st.slider(T["cr_nitrogen"],   40,  90,  60)
    P       = st.slider(T["cr_phosphorus"], 25,  50,  37)
    K       = st.slider(T["cr_potassium"],  10,  60,  40)
    soil_ph = st.slider(T["cr_ph"],         5.0, 9.0, 7.0, step=0.1)

st.markdown("---")

col3, col4 = st.columns(2)
with col3:
    temperature = st.slider(T["cr_temp"],     10,  45,  25)
    humidity    = st.slider(T["cr_humidity"], 20,  90,  55)
with col4:
    rainfall    = st.slider(T["cr_rainfall"], 45, 145,  93)

st.markdown("---")

if st.button(T["cr_btn"], use_container_width=True):
    with st.spinner(T["cr_loading"]):
        crop, confidence = predict_crop(
            N, P, K, soil_ph, temperature,
            humidity, rainfall, season, soil, district
        )

    st.success(f"### {T['cr_result']}: **{crop}**")
    st.metric(label=T["cr_confidence"], value=f"{confidence}%")

    crop_info = {
        "Rice":       {"emoji": "🌾", "water": "High",   "season": "Kharif", "tip": "Requires flooded fields"},
        "Wheat":      {"emoji": "🌿", "water": "Medium", "season": "Rabi",   "tip": "Cool weather preferred"},
        "Bajra":      {"emoji": "🌱", "water": "Low",    "season": "Kharif", "tip": "Drought resistant"},
        "Jowar":      {"emoji": "🌾", "water": "Low",    "season": "Kharif", "tip": "Grows in dry conditions"},
        "Gram":       {"emoji": "🫘", "water": "Low",    "season": "Rabi",   "tip": "Nitrogen fixing crop"},
        "Onion":      {"emoji": "🧅", "water": "Medium", "season": "Rabi",   "tip": "Well-drained soil needed"},
        "Vegetables": {"emoji": "🥦", "water": "Medium", "season": "Zaid",   "tip": "Short duration crop"},
        "Fodder":     {"emoji": "🌿", "water": "Medium", "season": "Zaid",   "tip": "Good for livestock"},
    }

    if crop in crop_info:
        info = crop_info[crop]
        st.markdown("---")
        st.subheader(f"{info['emoji']} {crop} {T['cr_about']}")
        c1, c2, c3 = st.columns(3)
        c1.metric(T["cr_water"],       info["water"])
        c2.metric(T["cr_best_season"], info["season"])
        c3.info(f"💡 **{T['cr_tip']}:** {info['tip']}")