# 🌾 Smart Agricultural Agent
### AI-Powered Farming Assistant for Indian Farmers

---

## 📌 Project Name

**Smart Agricultural Agent** — An intelligent, AI-driven web application that acts as a personal farming assistant for Indian farmers, helping them make data-driven decisions about crops, diseases, weather, and market prices — all in one place.

---

## ❗ Problem Statement

Indian agriculture faces several critical challenges:

- **Crop selection uncertainty** — Farmers lack access to scientific soil and climate-based crop recommendations, leading to poor yield.
- **Delayed disease detection** — Plant diseases are often identified too late, causing massive crop losses estimated at 20-30% annually.
- **No real-time weather guidance** — Farmers cannot easily translate weather data into actionable farming decisions.
- **Market price ignorance** — Farmers sell crops without knowing current or predicted market prices, resulting in financial losses.
- **Limited agricultural knowledge access** — Expert agricultural advice is not available to rural farmers in an affordable, accessible form.

> In India, over 58% of the rural population depends on agriculture, yet most farmers lack access to modern tools and expert knowledge to maximize their productivity and income.

---

## 💡 Solution

**Smart Agricultural Agent** is a unified AI platform that solves all these problems in one Streamlit web app:

| Problem | Our Solution |
|---|---|
| Crop selection uncertainty | ML-based Crop Recommendation (Random Forest) |
| Late disease detection | Deep Learning Disease Detector (MobileNetV2, 97.91% accuracy) |
| No weather guidance | Real-time Weather API + AI-generated farming advice |
| Market price ignorance | Crop Price Prediction with 12-month trend chart |
| No expert access | 24/7 AI Chat Assistant (LLaMA 3.3 70B via Groq) |

---

## 👨‍💻 My Role

This project was independently designed, developed, and deployed by **Aniket** as a Major Project submission.

**Responsibilities included:**
- Ideation and system architecture design
- Data collection and preprocessing (19,900 row custom Indian agriculture dataset)
- Training and evaluating ML models (Random Forest, MobileNetV2, Gradient Boosting)
- API integration (OpenWeatherMap, Groq)
- Full-stack development using Python and Streamlit
- Debugging, optimization, and deployment on Streamlit Cloud

---

## ✨ Features

### 1. 🤖 AI Farm Assistant (Chat)
- Powered by **LLaMA 3.3 70B** via Groq API
- Focused on Indian agriculture context
- Multi-turn conversations with full chat history
- Quick question buttons for common farming queries
- Covers: crops, soil, pest control, government schemes (PM-KISAN, Fasal Bima), irrigation

### 2. 🌱 Crop Recommendation
- Input: District, Season, Soil Type, NPK values, pH, Temperature, Humidity, Rainfall
- Output: Recommended crop + confidence score + crop info card
- Model: **Random Forest Classifier**
- Dataset: 19,900 records with real Indian district names

### 3. 🔬 Plant Disease Detection
- Upload any leaf image → instant disease diagnosis
- Model: **MobileNetV2** (Transfer Learning)
- Accuracy: **97.91%**
- Dataset: PlantVillage (~26,000 images, 23 classes)
- Output: Top 3 predictions + treatment suggestions

### 4. 🌦️ Weather Forecast
- Real-time weather for any Indian city
- AI-generated farming advice based on conditions
- 5-hour forecast display
- Powered by **OpenWeatherMap API**

### 5. 📈 Crop Price Prediction
- Predict price per quintal by crop, season, month, year
- 12-month price trend chart (Plotly)
- Smart selling advice with best month recommendation
- Model: **Gradient Boosting Regressor**

---

## 🏗️ System Architecture
<img width="1440" height="1948" alt="image" src="https://github.com/user-attachments/assets/39e6b1c6-5667-4fd8-92c0-6b1068b9d45d" />

---

## 🗂️ Project Structure

```
smart-agri-agent/
│
├── app.py                          # Main Streamlit dashboard
├── requirements.txt
├── .env                            # API keys (not pushed)
├── .gitignore
├── README.md
│
├── modules/
│   ├── crop_recommender.py
│   ├── disease_detector.py
│   ├── weather_module.py
│   ├── chat_agent.py
│   └── price_predictor.py
│
├── pages/
│   ├── 1_Crop_Recommendation.py
│   ├── 2_Disease_Detection.py
│   ├── 3_Weather.py
│   ├── 4_AI_Chat.py
│   └── 5_Price_Prediction.py
│
├── utils/
│   ├── config.py
│   └── location.py
│
└── data/
    ├── models/
    │   ├── crop_model.pkl
    │   ├── disease_model.keras
    │   ├── class_labels.json
    │   ├── price_model.pkl
    │   └── *.pkl (encoders)
    └── datasets/
        └── agriculture_data.csv
```

---

## 🧠 Model Performance

| Model | Algorithm | Performance |
|---|---|---|
| Crop Recommendation | Random Forest | 100% accuracy |
| Disease Detection | MobileNetV2 | 97.91% accuracy |
| Price Prediction | Gradient Boosting | R² > 0.95 |

---

## 📊 Datasets Used

| Dataset | Source | Size |
|---|---|---|
| Indian Crop Dataset | Custom / Field Data | 19,900 rows |
| PlantVillage | Kaggle | ~26,000 images, 23 classes |
| Crop Price Data | Synthetic (Agmarknet patterns) | 2,000 rows |

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Streamlit |
| ML / Deep Learning | Scikit-learn, TF-Keras, MobileNetV2 |
| AI Chat | Groq API (LLaMA 3.3 70B) |
| Weather | OpenWeatherMap API |
| Data Processing | Pandas, NumPy |
| Visualization | Plotly |
| Image Processing | Pillow (PIL) |
| Environment | Python 3.10, python-dotenv |

---

## ⚙️ Installation & Setup

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

### 4. Setup API keys — create `.env` file
```env
OPENWEATHER_API_KEY=your_openweathermap_key
GROQ_API_KEY=your_groq_key
```

Free API keys:
- OpenWeatherMap → https://openweathermap.org/api
- Groq → https://console.groq.com/keys

### 5. Train models
```bash
python modules/crop_recommender.py
python modules/price_predictor.py
python modules/disease_detector.py
```

### 6. Run the app
```bash
streamlit run app.py
```

Open → `http://localhost:8501`

---

## 🌐 Live Demo

🚀 **[Click here to try the app](https://share.streamlit.io/aniketd33/smart-agri-agent)**

---

## 🔮 Future Scope

- Hindi and Marathi language support for rural farmers
- SMS-based recommendations (no smartphone needed)
- Integration with real-time Mandi price APIs (Agmarknet)
- Satellite imagery based soil health analysis
- Mobile app version (Android)
- Government scheme eligibility checker

---

## 👨‍💻 Author
**Aniket Dombale**
aniketdombale329@gmail.com
GitHub: [@aniketd33](https://github.com/aniketd33)


---

> *"Technology should empower every farmer, not just the ones with internet."*
