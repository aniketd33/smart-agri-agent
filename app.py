import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
from utils.config import APP_NAME, APP_ICON
from utils.language import render_language_sidebar   # ← import karo

st.set_page_config(
    page_title=APP_NAME,
    page_icon=APP_ICON,
    layout="wide"
)

# ============================================
# LANGUAGE SIDEBAR — render karo
# T mein sari translations hain
# ============================================
T, lang_key = render_language_sidebar()

# ============================================
# MAIN UI
# ============================================
st.title(f"{APP_ICON} {APP_NAME}")
st.markdown(T["subtitle"])
st.markdown("---")

col1, col2, col3 = st.columns(3)
with col1:
    st.info(T["feat_crop"])
with col2:
    st.info(T["feat_disease"])
with col3:
    st.info(T["feat_weather"])

col4, col5 = st.columns(2)
with col4:
    st.info(T["feat_ai"])
with col5:
    st.info(T["feat_price"])

st.markdown("---")
st.caption(T["footer"])