import streamlit as st
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.language import render_language_sidebar
from modules.price_predictor import predict_price, get_price_trend, CROP_BASE_PRICES
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(page_title="Price Prediction", page_icon="📈", layout="wide")

T, lang_key = render_language_sidebar()

st.title(T["pp_title"])
st.markdown(T["pp_subtitle"])
st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    crop   = st.selectbox(T["pp_crop"],   list(CROP_BASE_PRICES.keys()))
    season = st.selectbox(T["pp_season"], ["Kharif", "Rabi", "Zaid"])

with col2:
    month = st.slider(T["pp_month"], 1, 12, datetime.now().month)
    year  = st.slider(T["pp_year"],  2024, 2027, 2025)

if st.button(T["pp_btn"], use_container_width=True):
    result = predict_price(crop, season, month, year)

    st.markdown("---")
    c1, c2, c3 = st.columns(3)
    c1.metric(T["pp_predicted"], f"₹{result['predicted_price']:,.0f}", T["pp_per_quintal"])
    c2.metric(T["pp_min"],       f"₹{result['min_expected']:,}")
    c3.metric(T["pp_max"],       f"₹{result['max_expected']:,}")

    st.markdown("---")
    st.subheader(f"{T['pp_trend'].split('—')[0]}— {crop} {T['pp_trend'].split('—')[1] if '—' in T['pp_trend'] else ''}")

    months_list, prices = get_price_trend(crop, season)
    month_names = ["Jan","Feb","Mar","Apr","May","Jun",
                   "Jul","Aug","Sep","Oct","Nov","Dec"]

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=month_names, y=prices,
        mode="lines+markers",
        name=T["pp_predicted"],
        line=dict(color="#00cc44", width=3),
        marker=dict(size=8)
    ))
    fig.add_hline(
        y=result["predicted_price"],
        line_dash="dash", line_color="orange",
        annotation_text=T["pp_selected_month"]
    )
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white"),
        yaxis_title=T["pp_yaxis"],
        xaxis_title=T["pp_xaxis"],
        height=400
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    st.subheader(T["pp_advice"])
    max_price  = max(prices)
    best_month = month_names[prices.index(max_price)]

    if result["predicted_price"] >= max_price * 0.95:
        st.success(T["pp_sell_now"])
    elif result["predicted_price"] >= max_price * 0.85:
        st.info(f"{T['pp_sell_decent']} **{best_month}** {T['pp_at']} ₹{max_price:,.0f}/Quintal.")
    else:
        st.warning(f"{T['pp_sell_wait']} **{best_month}** {T['pp_at']} ₹{max_price:,.0f}/Quintal.")