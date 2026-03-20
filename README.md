# 🌾 Smart Agricultural Agent

An AI-powered farming assistant built with Python and Streamlit that helps Indian farmers make smarter decisions about crops, diseases, weather, and market prices.

---

## 🎯 Objectives

1. **AI Chat Assistant** — Provide farmers with instant answers to agriculture-related queries using a conversational AI powered by Groq (LLaMA 3.3 70B).

2. **Crop Recommendation** — Recommend the most suitable crop based on soil parameters (NPK, pH), location (district), season, and weather conditions using a trained Random Forest model.

3. **Crop Disease Detection** — Identify plant diseases from leaf images using a MobileNetV2 deep learning model trained on the PlantVillage dataset (23 disease classes, ~97% accuracy).

4. **Weather Forecast** — Display real-time weather data and generate actionable farming advice based on current conditions using the OpenWeatherMap API.

5. **Crop Price Prediction** — Predict crop prices per quintal based on crop type, season, month, and year using a Gradient Boosting Regressor model with 12-month trend visualization.

---

## 🚀 Features

| Feature | Technology |
|---|---|
| AI Chat | Groq API (LLaMA 3.3 70B) |
| Crop Recommendation | Random Forest (Scikit-learn) |
| Disease Detection | MobileNetV2 (TF-Keras) |
| Weather Forecast | OpenWeatherMap API |
| Price Prediction | Gradient Boosting Regressor |
| Frontend | Streamlit |

---

## 🗂️ Project Structure

```
smart-agri-agent/
├── app.py                        # Main Streamlit entry point
├── requirements.txt
├── .env                          # API keys (not pushed to GitHub)
├── modules/
│   ├── crop_recommender.py       # Crop recommendation ML model
│   ├── disease_detector.py       # Plant disease CNN model
│   ├── weather_module.py         # Weather API integration
│   ├── chat_agent.py             # AI chat using Groq
│   └── price_predictor.py        # Crop price prediction model
├── pages/
│   ├── 1_Crop_Recommendation.py
│   ├── 2_Disease_Detection.py
│   ├── 3_Weather.py
│   ├── 4_AI_Chat.py
│   └── 5_Price_Prediction.py
├── utils/
│   ├── config.py                 # API key loader
│   └── location.py
└── data/
    ├── models/                   # Trained .pkl and .keras files
    └── datasets/                 # CSV datasets
```

---

## ⚙️ Setup & Installation

### 1. Clone the repository
```bash
git clone https://github.com/aniketd33/smart-agri-agent.git
cd smart-agri-agent
```

### 2. Create virtual environment
```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Setup API keys
Create a `.env` file in the root directory:
```env
OPENWEATHER_API_KEY=your_openweathermap_key
GROQ_API_KEY=your_groq_key
```

Get your free API keys:
- OpenWeatherMap → https://openweathermap.org/api
- Groq → https://console.groq.com/keys

### 5. Train the models
```bash
python modules/crop_recommender.py
python modules/disease_detector.py
python modules/price_predictor.py
```

> **Note:** Disease detection model requires the PlantVillage dataset (`color/` folder) placed inside `data/datasets/`. Download from [Kaggle](https://www.kaggle.com/datasets/abdallahalidev/plantvillage-dataset).

### 6. Run the app
```bash
streamlit run app.py
```

Open `http://localhost:8501` in your browser.

---

## 📊 Dataset

| Dataset | Source | Records |
|---|---|---|
| Crop Recommendation | Custom Indian Agriculture Dataset | 19,900 rows |
| Disease Detection | PlantVillage Dataset | ~26,000 images, 23 classes |
| Price Prediction | Synthetic (based on real Mandi price patterns) | 2,000 rows |

---

## 🧠 Model Performance

| Model | Accuracy |
|---|---|
| Crop Recommendation (Random Forest) | 100% (seasonal patterns) |
| Disease Detection (MobileNetV2) | ~97.91% |
| Price Prediction (Gradient Boosting) | R² > 0.95 |

---

## 🌐 Deployment

Deployed on **Streamlit Cloud** → [Live Demo](https://share.streamlit.io)

---

## 📌 Requirements

- Python 3.10+
- Streamlit
- TensorFlow / TF-Keras
- Scikit-learn
- Groq Python SDK
- Plotly
- Pandas, NumPy
- Pillow
- python-dotenv

---

## 👨‍💻 Author

**Aniket** 
GitHub: [@aniketd33](https://github.com/aniketd33)

---

## 📄 License

This project is for educational purposes.
