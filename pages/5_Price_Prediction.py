import streamlit as st
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules.price_predictor import predict_price, get_price_trend, CROP_BASE_PRICES
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(page_title="Price Prediction", page_icon="📈", layout="wide")

st.title("📈 Crop Price Prediction")
st.markdown("Predict crop prices before you sell — plan smarter!")
st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    crop   = st.selectbox("🌾 Select Crop",   list(CROP_BASE_PRICES.keys()))
    season = st.selectbox("📅 Select Season", ["Kharif", "Rabi", "Zaid"])

with col2:
    month = st.slider("📆 Month", 1, 12, datetime.now().month)
    year  = st.slider("📅 Year",  2024, 2027, 2025)

if st.button("🔍 Predict Price", use_container_width=True):
    result = predict_price(crop, season, month, year)

    st.markdown("---")
    c1, c2, c3 = st.columns(3)
    c1.metric("💰 Predicted Price", f"₹{result['predicted_price']:,.0f}", "per Quintal")
    c2.metric("📉 Min Expected",    f"₹{result['min_expected']:,}")
    c3.metric("📈 Max Expected",    f"₹{result['max_expected']:,}")

    # Price trend chart
    st.markdown("---")
    st.subheader(f"📊 {crop} Price Trend — All 12 Months")

    months_list, prices = get_price_trend(crop, season)
    month_names = ["Jan","Feb","Mar","Apr","May","Jun",
                   "Jul","Aug","Sep","Oct","Nov","Dec"]

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=month_names, y=prices,
        mode="lines+markers",
        name="Predicted Price",
        line=dict(color="#00cc44", width=3),
        marker=dict(size=8)
    ))
    fig.add_hline(
        y=result["predicted_price"],
        line_dash="dash", line_color="orange",
        annotation_text="Your Selected Month"
    )
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white"),
        yaxis_title="Price (₹/Quintal)",
        xaxis_title="Month",
        height=400
    )
    st.plotly_chart(fig, use_container_width=True)

    # Selling advice
    st.markdown("---")
    st.subheader("💡 Selling Advice")
    max_price  = max(prices)
    best_month = month_names[prices.index(max_price)]

    if result["predicted_price"] >= max_price * 0.95:
        st.success(f"✅ Great time to sell! Price is near peak this month.")
    elif result["predicted_price"] >= max_price * 0.85:
        st.info(f"📊 Decent price. Best month is **{best_month}** at ₹{max_price:,.0f}/Quintal.")
    else:
        st.warning(f"⏳ Consider waiting. Best price in **{best_month}** at ₹{max_price:,.0f}/Quintal.")
