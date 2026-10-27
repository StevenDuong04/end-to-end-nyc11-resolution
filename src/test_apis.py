import requests
import pandas as pd
from pathlib import Path

RAW = Path(__file__).resolve().parent.parent / "data" / "raw"
RAW.mkdir(parents=True, exist_ok=True)

# --- NYC 311 (Socrata) ---
url_311 = "https://data.cityofnewyork.us/resource/erm2-nwe9.json"
params_311 = {
    "$where": "created_date between '2025-01-01T00:00:00' and '2025-01-07T23:59:59'",
    "$limit": 500,
    "$order": "created_date",
}
r = requests.get(url_311, params=params_311, timeout=60)
print("311 status:", r.status_code)
r.raise_for_status()
df311 = pd.DataFrame(r.json())
df311.to_csv(RAW / "311_test.csv", index=False)
print("311 shape:", df311.shape)
print(df311.columns.tolist())

# --- Open-Meteo historical weather (NYC) ---
url_w = "https://archive-api.open-meteo.com/v1/archive"
params_w = {
    "latitude": 40.7128,
    "longitude": -74.0060,
    "start_date": "2025-01-01",
    "end_date": "2025-01-07",
    "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum,snowfall_sum,wind_speed_10m_max",
    "timezone": "America/New_York",
}
r = requests.get(url_w, params=params_w, timeout=60)
print("Weather status:", r.status_code)
r.raise_for_status()
dfw = pd.DataFrame(r.json()["daily"])
dfw.to_csv(RAW / "weather_test.csv", index=False)
print("Weather shape:", dfw.shape)
print(dfw.head())