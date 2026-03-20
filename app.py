import streamlit as st
from utils.config import APP_NAME, APP_ICON

st.set_page_config(
    page_title=APP_NAME,
    page_icon=APP_ICON,
    layout="wide"
)

st.title(f"{APP_ICON} {APP_NAME}")
st.markdown("### Your AI-powered farming assistant")

st.markdown("---")

col1, col2, col3 = st.columns(3)

with col1:
    st.info("🌱 **Crop Recommendation**\nGet crop suggestions based on your soil & location")
with col2:
    st.info("🔬 **Disease Detection**\nUpload a leaf photo to detect crop disease")
with col3:
    st.info("🌦️ **Weather Forecast**\nReal-time weather for your farm location")

col4, col5 = st.columns(2)
with col4:
    st.info("🤖 **AI Farm Assistant**\nChat with an AI trained on agriculture")
with col5:
    st.info("📈 **Price Prediction**\nForecast crop prices before you sell")

st.markdown("---")
st.caption("Use the sidebar to navigate between features.")