import streamlit as st
import sys
import os
import requests
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PIL import Image
from geopy.geocoders import Nominatim
from utils.language import render_language_sidebar   # ← import karo

try:
    from modules.disease_detector import predict_disease
    DISEASE_MODEL_AVAILABLE = True
except Exception:
    DISEASE_MODEL_AVAILABLE = False

st.set_page_config(page_title="Disease Detection", page_icon="🔬", layout="wide")

# ============================================
# LANGUAGE — ek line, sab kuch ready
# ============================================
T, lang_key = render_language_sidebar()

# ============================================
# TREATMENT DATA
# ============================================
TREATMENTS = {
    "early blight": {
        "en": "Apply copper-based fungicide. Remove infected leaves.",
        "hi": "तांबे आधारित फफूंदनाशक लगाएं। संक्रमित पत्तियां हटाएं।",
        "mr": "तांबे-आधारित बुरशीनाशक लावा. संक्रमित पाने काढा.",
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6a/Alternaria_solani_on_tomato_leaf.jpg/320px-Alternaria_solani_on_tomato_leaf.jpg",
    },
    "late blight": {
        "en": "Use Mancozeb spray. Avoid overhead irrigation.",
        "hi": "Mancozeb स्प्रे करें। ऊपर से सिंचाई से बचें।",
        "mr": "Mancozeb फवारणी करा. वरून पाणी देणे टाळा.",
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/38/Late_blight_on_potato_leaf.jpg/320px-Late_blight_on_potato_leaf.jpg",
    },
    "leaf mold": {
        "en": "Improve ventilation. Apply fungicide weekly.",
        "hi": "वायु संचार बढ़ाएं। साप्ताहिक फफूंदनाशक लगाएं।",
        "mr": "हवा खेळती करा. आठवड्यातून बुरशीनाशक लावा.",
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d1/Fulvia_fulva_on_tomato.jpg/320px-Fulvia_fulva_on_tomato.jpg",
    },
    "septoria leaf spot": {
        "en": "Remove infected leaves. Apply chlorothalonil.",
        "hi": "संक्रमित पत्तियां हटाएं। क्लोरोथालोनिल लगाएं।",
        "mr": "संक्रमित पाने काढा. क्लोरोथॅलोनिल लावा.",
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/52/Septoria_lycopersici_on_tomato.jpg/320px-Septoria_lycopersici_on_tomato.jpg",
    },
    "bacterial spot": {
        "en": "Use copper spray. Avoid working in wet conditions.",
        "hi": "कॉपर स्प्रे करें। गीली स्थिति में काम से बचें।",
        "mr": "कॉपर फवारणी करा. ओल्या परिस्थितीत काम टाळा.",
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b5/Bacterial_leaf_scorch.jpg/320px-Bacterial_leaf_scorch.jpg",
    },
    "black rot": {
        "en": "Remove infected leaves. Apply Bordeaux mixture.",
        "hi": "संक्रमित पत्तियां हटाएं। बोर्डो मिश्रण लगाएं।",
        "mr": "संक्रमित पाने काढा. बोर्डो मिश्रण लावा.",
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1e/Xanthomonas_campestris_pv._campestris_on_cabbage.jpg/320px-Xanthomonas_campestris_pv._campestris_on_cabbage.jpg",
    },
    "powdery mildew": {
        "en": "Apply sulfur-based fungicide. Improve air circulation.",
        "hi": "सल्फर आधारित फफूंदनाशक लगाएं। वायु प्रवाह बढ़ाएं।",
        "mr": "गंधक-आधारित बुरशीनाशक लावा. हवा खेळती करा.",
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5f/Powdery_mildew_on_tomato.jpg/320px-Powdery_mildew_on_tomato.jpg",
    },
    "healthy": {
        "en": "No treatment needed. Keep monitoring regularly.",
        "hi": "कोई उपचार जरूरी नहीं। नियमित निगरानी रखें।",
        "mr": "उपचाराची गरज नाही. नियमित देखरेख करा.",
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/41/Simple_leaf.jpg/320px-Simple_leaf.jpg",
    },
}

# ============================================
# FUNCTIONS
# ============================================
def get_treatment(disease, lang_key):
    for key, data in TREATMENTS.items():
        if key in disease.lower():
            return data["image"], data[lang_key]
    fallback = {
        "en": "Consult your local agricultural extension officer.",
        "hi": "अपने स्थानीय कृषि अधिकारी से सलाह लें।",
        "mr": "स्थानिक कृषी अधिकाऱ्यांशी सल्लामसलत करा.",
    }
    return None, fallback[lang_key]

def get_nearby_shops(city):
    try:
        geolocator = Nominatim(user_agent="agro_disease_app_v3")
        location = geolocator.geocode(city, timeout=10)
        if not location:
            return [], "City not found. Try a different name."

        lat, lon = location.latitude, location.longitude
        query = f"""
        [out:json][timeout:25];
        (
          node["shop"="agrarian"](around:10000,{lat},{lon});
          node["shop"="garden_centre"](around:10000,{lat},{lon});
          node["name"~"agro|krishi|kisan|farm|nursery",i](around:10000,{lat},{lon});
        );
        out body 6;
        """
        response = requests.post(
            "https://overpass-api.de/api/interpreter",
            data={"data": query},
            timeout=30,
        )
        if response.status_code != 200 or not response.text.strip():
            return [], "API not responding. Try again later."
        return response.json().get("elements", []), None

    except requests.exceptions.Timeout:
        return [], "Request timed out. Try again."
    except Exception as e:
        return [], f"Error: {str(e)}"

# ============================================
# MAIN UI
# ============================================
st.title(T["dd_title"])
st.markdown(T["dd_subtitle"])
st.markdown("---")

uploaded_file = st.file_uploader(
    T["dd_upload"],
    type=["jpg", "jpeg", "png"],
    help="Upload a clear image of the affected leaf"
)

if uploaded_file:
    image = Image.open(uploaded_file)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader(T["dd_uploaded"])
        st.image(image, use_column_width=True)

    with col2:
        st.subheader(T["dd_analysis"])

        if not DISEASE_MODEL_AVAILABLE:
            st.warning(T["dd_local_only"])
            st.info(T["dd_run_local"])

        else:
            with st.spinner("Analyzing..."):
                results = predict_disease(image)

            top = results[0]

            if "healthy" in top["disease"].lower():
                st.success(T["dd_healthy"])
            else:
                st.error(T["dd_diseased"])

            st.markdown(f"### {T['dd_plant']}: **{top['plant']}**")
            st.markdown(f"### {T['dd_disease']}: **{top['disease']}**")
            st.metric(T["dd_confidence"], f"{top['confidence']}%")

            st.markdown("---")
            st.subheader(T["dd_top3"])
            for i, r in enumerate(results):
                st.progress(
                    int(r["confidence"]),
                    text=f"{i+1}. {r['plant']} — {r['disease']} ({r['confidence']}%)"
                )

    if DISEASE_MODEL_AVAILABLE:
        # Treatment Section
        st.markdown("---")
        st.subheader(T["dd_treatment"])

        treat_img_url, tip = get_treatment(top["disease"], lang_key)

        t1, t2 = st.columns([1, 2])
        with t1:
            if treat_img_url:
                try:
                    st.image(treat_img_url,
                             caption=f"{top['plant']} — {top['disease']}",
                             use_column_width=True)
                except:
                    st.info(T["dd_treat_err"])
            else:
                st.info(T["dd_treat_err"])

        with t2:
            st.info(f"💡 {tip}")
            st.markdown("---")
            st.markdown(f"""
| {T['dd_detail']} | {T['dd_info']} |
|---|---|
| {T['dd_plant']} | {top['plant']} |
| {T['dd_disease']} | {top['disease']} |
| {T['dd_confidence']} | {top['confidence']}% |
            """)

        # Nearby Shops Section
        st.markdown("---")
        st.subheader(T["dd_shops"])

        city = st.text_input(
            T["dd_city"],
            value="Pune",
            placeholder="e.g. Pune, Nashik, Nagpur"
        )

        if st.button(T["dd_search"]):
            with st.spinner("Searching..."):
                shops, error = get_nearby_shops(city)

            if error:
                st.error(f"❌ {error}")
                st.info(T["dd_google_tip"])
            elif shops:
                st.success(f"✅ {len(shops)} {T['dd_found']}")
                for shop in shops:
                    tags  = shop.get("tags", {})
                    name  = tags.get("name", "Agro Shop")
                    addr  = tags.get("addr:street", tags.get("addr:full", ""))
                    phone = tags.get("phone", tags.get("contact:phone", ""))
                    lat_s = shop.get("lat", "")
                    lon_s = shop.get("lon", "")

                    with st.container(border=True):
                        s1, s2 = st.columns([3, 1])
                        with s1:
                            st.markdown(f"**🏪 {name}**")
                            if addr:  st.markdown(f"📍 {addr}")
                            if phone: st.markdown(f"📞 {phone}")
                        with s2:
                            maps_url = (
                                f"https://www.google.com/maps?q={lat_s},{lon_s}"
                                if lat_s and lon_s else
                                f"https://www.google.com/maps/search/{name}+{city}"
                            )
                            st.link_button(T["dd_maps"], maps_url)
            else:
                st.warning(f"⚠️ {T['dd_no_shops']}")
                st.info(T["dd_google_tip"])