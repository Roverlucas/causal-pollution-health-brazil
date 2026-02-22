"""
Central configuration for the Causal Pollution-Health Brazil project.

All constants, paths, variable lists, thresholds, and Supabase credentials
are defined here so every module draws from a single source of truth.
"""

import os
from pathlib import Path

# ---------------------------------------------------------------------------
# Project paths
# ---------------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
INTERIM_DIR = DATA_DIR / "interim"
PROCESSED_DIR = DATA_DIR / "processed"
OUTPUTS_DIR = PROJECT_ROOT / "outputs"
FIGURES_DIR = OUTPUTS_DIR / "figures"
TABLES_DIR = OUTPUTS_DIR / "tables"
REPORTS_DIR = OUTPUTS_DIR / "reports"
MODELS_DIR = OUTPUTS_DIR / "models"

# Ensure output directories exist
for d in [RAW_DIR, INTERIM_DIR, PROCESSED_DIR, FIGURES_DIR, TABLES_DIR,
          REPORTS_DIR, MODELS_DIR]:
    d.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------------------
# Supabase credentials (public anon key embedded in the Clima360 frontend)
# ---------------------------------------------------------------------------
SUPABASE_URL = os.getenv(
    "SUPABASE_URL",
    "https://qqadrpjrbnzapmsmryym.supabase.co"
)
SUPABASE_ANON_KEY = os.getenv(
    "SUPABASE_ANON_KEY",
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"
    ".eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InFxYWRycGpyYm56YXBtc21yeXltIiwi"
    "cm9sZSI6ImFub24iLCJpYXQiOjE3NjUyOTY1MjksImV4cCI6MjA4MDg3MjUyOX0"
    ".jkZi_JS_jtzLSBBgE3PmMMUx5FHemLx1zY1aNkhchBI"
)

# ---------------------------------------------------------------------------
# Supabase table names
# ---------------------------------------------------------------------------
TABLES = {
    "weather":       "weather_history",
    "air_quality":   "air_quality_history",
    "health":        "health_hospitalizations",
    "demographics":  "demographics_history",
    "fleet":         "fleet_history",
}

# Select columns per table (to minimize transfer size)
TABLE_COLUMNS = {
    "weather_history": [
        "id", "city", "date", "lat", "lon",
        "temperature_mean", "temperature_max", "temperature_min",
        "apparent_temperature_max", "apparent_temperature_min",
        "relative_humidity_mean", "pressure_mean",
        "wind_speed_max", "wind_gusts_max", "wind_direction_dominant",
        "precipitation_sum", "rain_sum", "precipitation_hours",
        "shortwave_radiation_sum", "et0_fao_evapotranspiration",
        "daylight_duration", "uv_index_max",
    ],
    "air_quality_history": [
        "id", "city", "date", "lat", "lon",
        "pm25", "pm10", "o3", "no2", "so2", "co",
        "aqi", "dominant_pollutant", "data_quality",
        "source", "station_name",
    ],
    "health_hospitalizations": [
        "id", "city", "ibge_code", "date", "cid_category",
        "admissions", "admissions_age_0_14", "admissions_age_15_59",
        "admissions_age_60_plus", "admissions_female", "admissions_male",
        "deaths", "deaths_age_0_14", "deaths_age_15_59",
        "deaths_age_60_plus", "deaths_female", "deaths_male",
        "total_cost", "data_quality", "source",
    ],
    "demographics_history": [
        "id", "city", "ibge_code", "year",
        "population", "density", "growth_rate",
        "pop_0_14", "pop_15_59", "pop_60_plus",
        "pop_female", "pop_male", "pop_rural", "pop_urban",
        "source",
    ],
    "fleet_history": [
        "id", "city", "ibge_code", "year", "month",
        "fleet_total", "fleet_automobile", "fleet_motorcycle",
        "fleet_bus", "fleet_truck", "fleet_utility",
        "fleet_tractor", "fleet_trailer", "fleet_other",
    ],
}

# ---------------------------------------------------------------------------
# Analysis parameters
# ---------------------------------------------------------------------------
ANALYSIS_START = "2022-01-01"
ANALYSIS_END = "2025-12-31"
RANDOM_SEED = 42

# WHO air quality guideline thresholds
WHO_PM25_THRESHOLD = 15.0   # ug/m3, 24h mean
WHO_O3_THRESHOLD = 100.0    # ug/m3, 8h mean

# Alternative thresholds for sensitivity analysis
ALT_PM25_THRESHOLDS = [25.0, 35.0, 50.0]

# Lag structure for exposure variables
MAX_LAG_DAYS = 7
MOVING_AVG_WINDOWS = [7, 14]

# CID-10 respiratory codes (Chapter X: J00-J99)
CID_RESPIRATORY = "J"

# Fourier terms for seasonality control
FOURIER_PERIODS = [365.25, 365.25 / 2]  # annual and semi-annual

# Cross-fitting folds
N_FOLDS = 5

# Causal forest parameters
CF_N_ESTIMATORS = 2000
CF_MIN_LEAF_SIZE = 20
CF_HONEST = True

# SHAP subsample for speed
SHAP_MAX_SAMPLES = 5000

# Bootstrap for inference
BOOTSTRAP_N = 1000

# ---------------------------------------------------------------------------
# Brazilian state capitals — reference table
# Maps city name (as stored in Supabase) to metadata.
# ---------------------------------------------------------------------------
CAPITALS = {
    "Aracaju":        {"uf": "SE", "ibge": "2800308", "region": "NE"},
    "Belém":          {"uf": "PA", "ibge": "1501402", "region": "N"},
    "Belo Horizonte": {"uf": "MG", "ibge": "3106200", "region": "SE"},
    "Boa Vista":      {"uf": "RR", "ibge": "1400100", "region": "N"},
    "Brasília":       {"uf": "DF", "ibge": "5300108", "region": "CO"},
    "Campo Grande":   {"uf": "MS", "ibge": "5002704", "region": "CO"},
    "Cuiabá":         {"uf": "MT", "ibge": "5103403", "region": "CO"},
    "Curitiba":       {"uf": "PR", "ibge": "4106902", "region": "S"},
    "Florianópolis":  {"uf": "SC", "ibge": "4205407", "region": "S"},
    "Fortaleza":      {"uf": "CE", "ibge": "2304400", "region": "NE"},
    "Goiânia":        {"uf": "GO", "ibge": "5208707", "region": "CO"},
    "João Pessoa":    {"uf": "PB", "ibge": "2507507", "region": "NE"},
    "Macapá":         {"uf": "AP", "ibge": "1600303", "region": "N"},
    "Maceió":         {"uf": "AL", "ibge": "2704302", "region": "NE"},
    "Manaus":         {"uf": "AM", "ibge": "1302603", "region": "N"},
    "Natal":          {"uf": "RN", "ibge": "2408102", "region": "NE"},
    "Palmas":         {"uf": "TO", "ibge": "1721000", "region": "N"},
    "Porto Alegre":   {"uf": "RS", "ibge": "4314902", "region": "S"},
    "Porto Velho":    {"uf": "RO", "ibge": "1100205", "region": "N"},
    "Recife":         {"uf": "PE", "ibge": "2611606", "region": "NE"},
    "Rio Branco":     {"uf": "AC", "ibge": "1200401", "region": "N"},
    "Rio de Janeiro": {"uf": "RJ", "ibge": "3304557", "region": "SE"},
    "Salvador":       {"uf": "BA", "ibge": "2927408", "region": "NE"},
    "São Luís":       {"uf": "MA", "ibge": "2111300", "region": "NE"},
    "São Paulo":      {"uf": "SP", "ibge": "3550308", "region": "SE"},
    "Teresina":       {"uf": "PI", "ibge": "2211001", "region": "NE"},
    "Vitória":        {"uf": "ES", "ibge": "3205309", "region": "SE"},
}

REGION_ORDER = ["N", "NE", "CO", "SE", "S"]

# ---------------------------------------------------------------------------
# Confounders (W), Moderators (X), Treatments (T), Outcomes (Y)
# These lists are referenced by model scripts for consistency.
# ---------------------------------------------------------------------------
WEATHER_CONFOUNDERS = [
    "temperature_mean", "dtr", "relative_humidity_mean",
    "pressure_mean", "wind_speed_max", "precipitation_sum",
]

TEMPORAL_CONFOUNDERS = [
    "sin_annual", "cos_annual", "sin_semiannual", "cos_semiannual",
    "dow_1", "dow_2", "dow_3", "dow_4", "dow_5", "dow_6",
    "trend",
]

ALL_CONFOUNDERS = WEATHER_CONFOUNDERS + TEMPORAL_CONFOUNDERS

HETEROGENEITY_MODERATORS = [
    "pop_density", "fleet_per_capita", "pct_elderly",
    "dtr", "region_N", "region_NE", "region_CO", "region_SE", "region_S",
]

TREATMENT_PM25 = "pm25_exceed"
TREATMENT_O3 = "o3_exceed"

OUTCOME_TOTAL = "admissions"
OUTCOME_AGE_GROUPS = [
    "admissions_age_0_14",
    "admissions_age_15_59",
    "admissions_age_60_plus",
]
OUTCOME_SEX_GROUPS = [
    "admissions_female",
    "admissions_male",
]
ALL_OUTCOMES = [OUTCOME_TOTAL] + OUTCOME_AGE_GROUPS + OUTCOME_SEX_GROUPS

# ---------------------------------------------------------------------------
# Logging format
# ---------------------------------------------------------------------------
LOG_FORMAT = "%(asctime)s | %(name)-24s | %(levelname)-7s | %(message)s"
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
