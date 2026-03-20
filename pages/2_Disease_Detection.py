import streamlit as st
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PIL import Image

try:
    from modules.disease_detector import predict_disease
    DISEASE_MODEL_AVAILABLE = True
except Exception:
    DISEASE_MODEL_AVAILABLE = False

st.set_page_config(page_title="Disease Detection", page_icon="🔬", layout="wide")

st.title("🔬 Crop Disease Detection")
st.markdown("Upload a leaf image to detect disease using AI.")
st.markdown("---")

uploaded_file = st.file_uploader(
    "📸 Upload Leaf Image",
    type=["jpg", "jpeg", "png"],
    help="Upload a clear image of the affected leaf"
)

if uploaded_file:
    image = Image.open(uploaded_file)
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📷 Uploaded Image")
        st.image(image, use_column_width=True)

    with col2:
        st.subheader("🧠 AI Analysis")

        if not DISEASE_MODEL_AVAILABLE:
            st.warning("⚠️ Disease Detection is only available when running locally.")
            st.info("💡 Run locally with: `streamlit run app.py`")

        else:
            with st.spinner("Analyzing leaf..."):
                results = predict_disease(image)

            top = results[0]

            if "healthy" in top["disease"].lower():
                st.success("✅ Plant is **Healthy!**")
            else:
                st.error("⚠️ Disease Detected!")

            st.markdown(f"### 🌿 Plant: **{top['plant']}**")
            st.markdown(f"### 🦠 Disease: **{top['disease']}**")
            st.metric("Confidence", f"{top['confidence']}%")

            st.markdown("---")
            st.subheader("📊 Top 3 Predictions")
            for i, r in enumerate(results):
                st.progress(
                    int(r["confidence"]),
                    text=f"{i+1}. {r['plant']} — {r['disease']} ({r['confidence']}%)"
                )

            st.markdown("---")
            st.subheader("💊 Treatment Suggestions")

            treatments = {
                "Early_blight":       "Apply copper-based fungicide. Remove infected leaves.",
                "Late_blight":        "Use Mancozeb spray. Avoid overhead irrigation.",
                "Leaf_Mold":          "Improve ventilation. Apply fungicide weekly.",
                "Septoria_leaf_spot": "Remove infected leaves. Apply chlorothalonil.",
                "Bacterial_spot":     "Use copper spray. Avoid working in wet conditions.",
                "healthy":            "No treatment needed. Keep monitoring regularly.",
            }

            matched = False
            for key, tip in treatments.items():
                if key.lower().replace("_", " ") in top["disease"].lower():
                    st.info(f"💡 {tip}")
                    matched = True
                    break

            if not matched:
                st.info("💡 Consult your local agricultural extension officer for treatment.")