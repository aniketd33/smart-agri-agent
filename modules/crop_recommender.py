import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import joblib
import os

DATA_PATH = "data/datasets/agriculture_data.csv"
MODEL_DIR = "data/models"

def train_and_save_model():
    df = pd.read_csv(DATA_PATH)

    # Encoders
    le_season = LabelEncoder()
    le_soil = LabelEncoder()
    le_district = LabelEncoder()

    df['Season_enc']   = le_season.fit_transform(df['Season'])
    df['Soil_enc']     = le_soil.fit_transform(df['Soil_Type'])
    df['District_enc'] = le_district.fit_transform(df['District'])

    features = ['N', 'P', 'K', 'Soil_pH', 'Temperature',
                'Humidity', 'Rainfall', 'Season_enc', 'Soil_enc', 'District_enc']

    X = df[features]
    y = df['Crop']

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    acc = accuracy_score(y_test, model.predict(X_test))
    print(f"Model Accuracy: {acc:.4f}")

    # Save model + encoders
    os.makedirs(MODEL_DIR, exist_ok=True)
    joblib.dump(model,      f"{MODEL_DIR}/crop_model.pkl")
    joblib.dump(le_season,  f"{MODEL_DIR}/le_season.pkl")
    joblib.dump(le_soil,    f"{MODEL_DIR}/le_soil.pkl")
    joblib.dump(le_district,f"{MODEL_DIR}/le_district.pkl")

    print("✅ Model saved successfully!")
    return acc

def predict_crop(N, P, K, soil_ph, temperature, humidity, rainfall, season, soil_type, district):
    model       = joblib.load(f"{MODEL_DIR}/crop_model.pkl")
    le_season   = joblib.load(f"{MODEL_DIR}/le_season.pkl")
    le_soil     = joblib.load(f"{MODEL_DIR}/le_soil.pkl")
    le_district = joblib.load(f"{MODEL_DIR}/le_district.pkl")

    # Handle unseen labels safely
    def safe_encode(le, val):
        if val in le.classes_:
            return le.transform([val])[0]
        return 0  # default fallback

    input_data = pd.DataFrame([{
        'N':           N,
        'P':           P,
        'K':           K,
        'Soil_pH':     soil_ph,
        'Temperature': temperature,
        'Humidity':    humidity,
        'Rainfall':    rainfall,
        'Season_enc':  safe_encode(le_season, season),
        'Soil_enc':    safe_encode(le_soil, soil_type),
        'District_enc':safe_encode(le_district, district)
    }])

    prediction = model.predict(input_data)[0]
    proba      = model.predict_proba(input_data)[0]
    confidence = round(max(proba) * 100, 2)

    return prediction, confidence

def get_available_options():
    le_season   = joblib.load(f"{MODEL_DIR}/le_season.pkl")
    le_soil     = joblib.load(f"{MODEL_DIR}/le_soil.pkl")
    le_district = joblib.load(f"{MODEL_DIR}/le_district.pkl")

    return {
        "seasons":   list(le_season.classes_),
        "soils":     list(le_soil.classes_),
        "districts": list(le_district.classes_)
    }

if __name__ == "__main__":
    train_and_save_model()