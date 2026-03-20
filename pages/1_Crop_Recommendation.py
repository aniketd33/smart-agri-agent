import streamlit as st
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules.crop_recommender import predict_crop, get_available_options

st.set_page_config(page_title="Crop Recommendation", page_icon="🌱", layout="wide")

st.title("🌱 Crop Recommendation")
st.markdown("Fill in your soil and location details to get the best crop suggestion.")
st.markdown("---")

# Load options
options = get_available_options()

# Layout
col1, col2 = st.columns(2)

with col1:
    st.subheader("📍 Location & Season")
    district = st.selectbox("District", options["districts"])
    season   = st.selectbox("Season", options["seasons"])
    soil     = st.selectbox("Soil Type", options["soils"])

with col2:
    st.subheader("🧪 Soil Parameters")
    N         = st.slider("Nitrogen (N)", 40, 90, 60)
    P         = st.slider("Phosphorus (P)", 25, 50, 37)
    K         = st.slider("Potassium (K)", 10, 60, 40)
    soil_ph   = st.slider("Soil pH", 5.0, 9.0, 7.0, step=0.1)

st.markdown("---")

col3, col4 = st.columns(2)
with col3:
    temperature = st.slider("🌡️ Temperature (°C)", 10, 45, 25)
    humidity    = st.slider("💧 Humidity (%)", 20, 90, 55)
with col4:
    rainfall    = st.slider("🌧️ Rainfall (mm)", 45, 145, 93)

st.markdown("---")

if st.button("🔍 Recommend Crop", use_container_width=True):
    with st.spinner("Analyzing your farm data..."):
        crop, confidence = predict_crop(
            N, P, K, soil_ph, temperature,
            humidity, rainfall, season, soil, district
        )

    st.success(f"### ✅ Recommended Crop: **{crop}**")
    st.metric(label="Model Confidence", value=f"{confidence}%")

    # Crop info cards
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
        st.subheader(f"{info['emoji']} About {crop}")
        c1, c2, c3 = st.columns(3)
        c1.metric("💧 Water Requirement", info["water"])
        c2.metric("📅 Best Season",       info["season"])
        c3.info(f"💡 **Tip:** {info['tip']}")