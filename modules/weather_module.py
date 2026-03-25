import requests
from utils.config import OPENWEATHER_API_KEY

BASE_URL = "https://api.openweathermap.org/data/2.5"

def get_weather(city):
    try:
        url = f"{BASE_URL}/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"
        r   = requests.get(url)
        d   = r.json()

        if d.get("cod") != 200:
            return None, d.get("message", "City not found")

        return {
            "city":        d["name"],
            "country":     d["sys"]["country"],
            "temp":        d["main"]["temp"],
            "feels_like":  d["main"]["feels_like"],
            "humidity":    d["main"]["humidity"],
            "pressure":    d["main"]["pressure"],
            "description": d["weather"][0]["description"].title(),
            "icon":        d["weather"][0]["icon"],
            "wind_speed":  d["wind"]["speed"],
            "visibility":  d.get("visibility", 0) // 1000,
        }, None

    except Exception as e:
        return None, str(e)

def get_forecast(city):
    try:
        url = f"{BASE_URL}/forecast?q={city}&appid={OPENWEATHER_API_KEY}&units=metric&cnt=5"
        r   = requests.get(url)
        d   = r.json()

        if d.get("cod") != "200":
            return None

        forecast = []
        for item in d["list"]:
            forecast.append({
                "time":        item["dt_txt"],
                "temp":        item["main"]["temp"],
                "humidity":    item["main"]["humidity"],
                "description": item["weather"][0]["description"].title(),
                "icon":        item["weather"][0]["icon"],
            })
        return forecast

    except:
        return None

def get_farming_advice(weather):
    advice = []
    temp = weather["temp"]
    hum  = weather["humidity"]
    desc = weather["description"].lower()

    if "rain" in desc:
        advice.append("🌧️ Rain expected — avoid spraying pesticides today")
        advice.append("💧 Skip irrigation — natural rainfall is sufficient")
    if temp > 35:
        advice.append("🌡️ High temperature — irrigate crops in early morning or evening")
    if temp < 10:
        advice.append("❄️ Cold weather — protect sensitive crops from frost")
    if hum > 80:
        advice.append("💧 High humidity — watch out for fungal diseases")
    if hum < 30:
        advice.append("🏜️ Low humidity — increase irrigation frequency")
    if "clear" in desc:
        advice.append("☀️ Clear sky — good day for spraying and field work")

    if not advice:
        advice.append("✅ Weather is favorable for normal farming activities")

    return advice