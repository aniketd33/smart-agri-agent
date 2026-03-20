import pandas as pd
import numpy as np
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.preprocessing import LabelEncoder
import joblib
import os
import json
from datetime import datetime

MODEL_DIR = "data/models"

CROP_BASE_PRICES = {
    "Rice":       {"base": 2200, "min": 1800, "max": 3500},
    "Wheat":      {"base": 2100, "min": 1800, "max": 2800},
    "Bajra":      {"base": 1800, "min": 1500, "max": 2500},
    "Jowar":      {"base": 2000, "min": 1700, "max": 2800},
    "Gram":       {"base": 4800, "min": 4000, "max": 6500},
    "Onion":      {"base": 1500, "min": 500,  "max": 5000},
    "Vegetables": {"base": 2000, "min": 800,  "max": 4000},
    "Fodder":     {"base": 600,  "min": 400,  "max": 1000},
}

SEASONAL_FACTORS = {
    "Kharif": {"Rice": 1.1, "Bajra": 1.05, "Jowar": 1.05, "Vegetables": 0.95},
    "Rabi":   {"Wheat": 1.1, "Gram": 1.08, "Onion": 1.15},
    "Zaid":   {"Vegetables": 1.2, "Fodder": 1.1},
}

def generate_price_data():
    rows = []
    crops = list(CROP_BASE_PRICES.keys())
    seasons = ["Kharif", "Rabi", "Zaid"]
    months  = list(range(1, 13))

    for _ in range(2000):
        crop    = np.random.choice(crops)
        season  = np.random.choice(seasons)
        month   = np.random.choice(months)
        year    = np.random.choice([2022, 2023, 2024])

        base    = CROP_BASE_PRICES[crop]["base"]
        factor  = SEASONAL_FACTORS.get(season, {}).get(crop, 1.0)
        noise   = np.random.uniform(0.85, 1.15)
        price   = base * factor * noise

        rows.append({
            "crop": crop, "season": season,
            "month": month, "year": year,
            "price": round(price, 2)
        })

    return pd.DataFrame(rows)

def train_price_model():
    df = generate_price_data()

    le_crop   = LabelEncoder()
    le_season = LabelEncoder()
    df["crop_enc"]   = le_crop.fit_transform(df["crop"])
    df["season_enc"] = le_season.fit_transform(df["season"])

    X = df[["crop_enc", "season_enc", "month", "year"]]
    y = df["price"]

    model = GradientBoostingRegressor(n_estimators=100, random_state=42)
    model.fit(X, y)

    os.makedirs(MODEL_DIR, exist_ok=True)
    joblib.dump(model,    f"{MODEL_DIR}/price_model.pkl")
    joblib.dump(le_crop,  f"{MODEL_DIR}/price_le_crop.pkl")
    joblib.dump(le_season,f"{MODEL_DIR}/price_le_season.pkl")
    print("✅ Price model saved!")

def predict_price(crop, season, month, year):
    model     = joblib.load(f"{MODEL_DIR}/price_model.pkl")
    le_crop   = joblib.load(f"{MODEL_DIR}/price_le_crop.pkl")
    le_season = joblib.load(f"{MODEL_DIR}/price_le_season.pkl")

    crop_enc   = le_crop.transform([crop])[0]
    season_enc = le_season.transform([season])[0]

    X = pd.DataFrame([{
        "crop_enc": crop_enc, "season_enc": season_enc,
        "month": month, "year": year
    }])

    price = model.predict(X)[0]
    info  = CROP_BASE_PRICES.get(crop, {"min": 0, "max": 9999})

    return {
        "predicted_price": round(price, 2),
        "min_expected":    info["min"],
        "max_expected":    info["max"],
        "unit":            "₹ per Quintal"
    }

def get_price_trend(crop, season):
    model     = joblib.load(f"{MODEL_DIR}/price_model.pkl")
    le_crop   = joblib.load(f"{MODEL_DIR}/price_le_crop.pkl")
    le_season = joblib.load(f"{MODEL_DIR}/price_le_season.pkl")

    crop_enc   = le_crop.transform([crop])[0]
    season_enc = le_season.transform([season])[0]

    months = list(range(1, 13))
    prices = []
    for m in months:
        X = pd.DataFrame([{
            "crop_enc": crop_enc, "season_enc": season_enc,
            "month": m, "year": 2025
        }])
        prices.append(round(model.predict(X)[0], 2))

    return months, prices

if __name__ == "__main__":
    train_price_model()