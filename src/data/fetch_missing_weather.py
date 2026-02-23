#!/usr/bin/env python3
"""
Fetch missing weather data from Open-Meteo Archive API for 10 capitals
that lack weather_history coverage in Clima360 for 2022-2025.

Fetches the same 19 daily variables as the existing weather_history table
and appends them to the raw parquet file.
"""

import sys
import time
import uuid
import logging
from pathlib import Path

import pandas as pd
import requests

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

logging.basicConfig(format="%(asctime)s %(name)s %(levelname)s %(message)s", level=logging.INFO)
logger = logging.getLogger("fetch_missing_weather")

# Coordinates for the 10 missing capitals
MISSING_CAPITALS = {
    "Boa Vista":     {"lat": 2.8195,   "lon": -60.6714},
    "Fortaleza":     {"lat": -3.7172,  "lon": -38.5433},
    "João Pessoa":   {"lat": -7.1195,  "lon": -34.8450},
    "Maceió":        {"lat": -9.6658,  "lon": -35.7353},
    "Palmas":        {"lat": -10.1689, "lon": -48.3317},
    "Porto Alegre":  {"lat": -30.0346, "lon": -51.2177},
    "Recife":        {"lat": -8.0476,  "lon": -34.8770},
    "São Luís":      {"lat": -2.5297,  "lon": -44.2825},
    "Teresina":      {"lat": -5.0892,  "lon": -42.8019},
    "Vitória":       {"lat": -20.3155, "lon": -40.3128},
}

# Open-Meteo variable mapping (API name -> our column name)
DAILY_VARS = [
    "temperature_2m_mean",
    "temperature_2m_max",
    "temperature_2m_min",
    "apparent_temperature_max",
    "apparent_temperature_min",
    "relative_humidity_2m_mean",
    "pressure_msl_mean",
    "wind_speed_10m_max",
    "wind_gusts_10m_max",
    "wind_direction_10m_dominant",
    "precipitation_sum",
    "rain_sum",
    "precipitation_hours",
    "shortwave_radiation_sum",
    "et0_fao_evapotranspiration",
    "daylight_duration",
    "uv_index_max",
]

RENAME_MAP = {
    "temperature_2m_mean": "temperature_mean",
    "temperature_2m_max": "temperature_max",
    "temperature_2m_min": "temperature_min",
    "relative_humidity_2m_mean": "relative_humidity_mean",
    "pressure_msl_mean": "pressure_mean",
    "wind_speed_10m_max": "wind_speed_max",
    "wind_gusts_10m_max": "wind_gusts_max",
    "wind_direction_10m_dominant": "wind_direction_dominant",
}

API_URL = "https://archive-api.open-meteo.com/v1/archive"
START_DATE = "2022-01-01"
END_DATE = "2025-12-31"


def fetch_city(city: str, lat: float, lon: float, max_retries: int = 5) -> pd.DataFrame:
    """Fetch daily weather for one city from Open-Meteo Archive API with retry."""
    params = {
        "latitude": lat,
        "longitude": lon,
        "start_date": START_DATE,
        "end_date": END_DATE,
        "daily": ",".join(DAILY_VARS),
        "timezone": "America/Sao_Paulo",
    }

    for attempt in range(1, max_retries + 1):
        logger.info("Fetching %s (%.4f, %.4f) [attempt %d]...", city, lat, lon, attempt)
        try:
            resp = requests.get(API_URL, params=params, timeout=120)
            if resp.status_code == 429 or resp.status_code >= 500:
                wait = 10 * attempt
                logger.warning("  Status %d, waiting %ds...", resp.status_code, wait)
                time.sleep(wait)
                continue
            resp.raise_for_status()
            data = resp.json()
            break
        except (requests.exceptions.JSONDecodeError, requests.exceptions.RequestException) as e:
            wait = 10 * attempt
            logger.warning("  Error: %s, waiting %ds...", e, wait)
            time.sleep(wait)
            if attempt == max_retries:
                raise

    daily = data["daily"]
    df = pd.DataFrame(daily)
    df.rename(columns={"time": "date"}, inplace=True)
    df.rename(columns=RENAME_MAP, inplace=True)

    df["city"] = city
    df["lat"] = data["latitude"]
    df["lon"] = data["longitude"]
    df["id"] = [str(uuid.uuid4()) for _ in range(len(df))]

    logger.info("  -> %d rows (%s to %s)", len(df), df["date"].iloc[0], df["date"].iloc[-1])
    return df


def main():
    raw_path = Path(__file__).resolve().parents[2] / "data" / "raw" / "weather_history.parquet"

    # Load existing
    existing = pd.read_parquet(raw_path)
    logger.info("Existing weather data: %d rows, %d cities", len(existing), existing["city"].nunique())

    # Fetch missing
    new_frames = []
    for city, coords in MISSING_CAPITALS.items():
        df = fetch_city(city, coords["lat"], coords["lon"])
        new_frames.append(df)
        time.sleep(5)  # rate limit courtesy

    new_data = pd.concat(new_frames, ignore_index=True)

    # Align columns to match existing
    for col in existing.columns:
        if col not in new_data.columns:
            new_data[col] = None
    new_data = new_data[existing.columns]

    # Append and save
    combined = pd.concat([existing, new_data], ignore_index=True)
    combined.to_parquet(raw_path, index=False)

    logger.info("Combined weather data: %d rows, %d cities",
                len(combined), combined["city"].nunique())
    logger.info("New cities added: %s", sorted(new_data["city"].unique()))
    logger.info("Saved to %s", raw_path)


if __name__ == "__main__":
    main()
