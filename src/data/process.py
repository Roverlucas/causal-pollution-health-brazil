#!/usr/bin/env python3
"""
Process raw Parquet extracts into a single analysis-ready panel dataset.

Pipeline:
    1. Load raw tables (weather, air_quality, health, demographics, fleet)
    2. Filter to analysis window (2022-01-01 to 2025-12-31)
    3. Filter health to respiratory CID codes (J*)
    4. Merge weather + air_quality + health on (city, date)
    5. Merge annual demographics and fleet (interpolated to daily)
    6. Compute derived features (DTR, lags, moving averages, Fourier, etc.)
    7. Construct treatment indicators (PM2.5 and O3 WHO exceedances)
    8. Apply quality filters
    9. Save analysis_panel.parquet

Usage:
    python src/data/process.py
"""

from __future__ import annotations

import logging
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

# ---------------------------------------------------------------------------
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from src.utils.config import (
    RAW_DIR,
    PROCESSED_DIR,
    INTERIM_DIR,
    TABLES,
    ANALYSIS_START,
    ANALYSIS_END,
    WHO_PM25_THRESHOLD,
    WHO_O3_THRESHOLD,
    CID_RESPIRATORY,
    MAX_LAG_DAYS,
    MOVING_AVG_WINDOWS,
    FOURIER_PERIODS,
    CAPITALS,
    REGION_ORDER,
    LOG_FORMAT,
    LOG_DATE_FORMAT,
)

logging.basicConfig(format=LOG_FORMAT, datefmt=LOG_DATE_FORMAT, level=logging.INFO)
logger = logging.getLogger("process")


# =========================================================================
# 1. Load raw tables
# =========================================================================
def load_raw(table_key: str) -> pd.DataFrame:
    """Load a raw Parquet file."""
    table_name = TABLES[table_key]
    path = RAW_DIR / f"{table_name}.parquet"
    logger.info("Loading %s", path)
    df = pd.read_parquet(path)
    logger.info("  -> %d rows x %d cols", len(df), len(df.columns))
    return df


# =========================================================================
# 2-3. Pre-filter helper
# =========================================================================
def _parse_dates(df: pd.DataFrame, col: str = "date") -> pd.DataFrame:
    """Parse date column to datetime and filter to analysis window."""
    df = df.copy()
    df[col] = pd.to_datetime(df[col], errors="coerce")
    mask = (df[col] >= ANALYSIS_START) & (df[col] <= ANALYSIS_END)
    before = len(df)
    df = df.loc[mask].reset_index(drop=True)
    logger.info("  Date filter %s..%s: %d -> %d rows", ANALYSIS_START, ANALYSIS_END, before, len(df))
    return df


def _filter_respiratory(health: pd.DataFrame) -> pd.DataFrame:
    """Keep only respiratory hospitalization rows."""
    # cid_category uses descriptive names ("respiratory", "cardiovascular")
    mask = health["cid_category"].str.lower().str.contains("respiratory", na=False)
    before = len(health)
    health = health.loc[mask].reset_index(drop=True)
    logger.info("  Respiratory filter: %d -> %d rows", before, len(health))
    return health


# =========================================================================
# 4. Merge daily tables
# =========================================================================
def merge_daily(
    weather: pd.DataFrame,
    air_quality: pd.DataFrame,
    health: pd.DataFrame,
) -> pd.DataFrame:
    """
    Inner merge weather + air_quality + health on (city, date).

    Health is first aggregated by (city, date) across CID sub-categories
    to produce a single row per city-day with total respiratory admissions.
    """
    # Aggregate health to one row per city-date
    health_agg_cols = [
        "admissions", "admissions_age_0_14", "admissions_age_15_59",
        "admissions_age_60_plus", "admissions_female", "admissions_male",
        "deaths", "deaths_age_0_14", "deaths_age_15_59",
        "deaths_age_60_plus", "deaths_female", "deaths_male",
        "total_cost",
    ]
    health_grouped = (
        health
        .groupby(["city", "date", "ibge_code"], as_index=False)[health_agg_cols]
        .sum()
    )
    logger.info("Health aggregated to %d city-dates", len(health_grouped))

    # Merge weather + air quality
    daily = pd.merge(
        weather, air_quality,
        on=["city", "date"],
        how="inner",
        suffixes=("_wx", "_aq"),
    )
    logger.info("Weather + AQ merge: %d rows", len(daily))

    # Merge with health
    daily = pd.merge(
        daily, health_grouped,
        on=["city", "date"],
        how="inner",
    )
    logger.info("+ Health merge: %d rows", len(daily))
    return daily


# =========================================================================
# 5. Merge annual tables (demographics + fleet)
# =========================================================================
def _interpolate_annual_to_daily(
    annual_df: pd.DataFrame,
    daily_dates: pd.DataFrame,
    value_cols: list[str],
    time_col: str = "year",
) -> pd.DataFrame:
    """
    For each city, linearly interpolate annual values to daily resolution.

    Parameters
    ----------
    annual_df : DataFrame with city, year, and value columns.
    daily_dates : DataFrame with city, date (unique city-date pairs).
    value_cols : columns to interpolate.

    Returns
    -------
    DataFrame with city, date, and interpolated value columns.
    """
    daily_dates = daily_dates[["city", "date"]].drop_duplicates()
    daily_dates["year"] = daily_dates["date"].dt.year

    # Merge on year (floor) — gives the value at start of each year
    merged = pd.merge(daily_dates, annual_df[["city", time_col] + value_cols],
                       on=["city", time_col], how="left")

    # For rows with missing values, try year+1 / year-1 fallback
    # then forward-fill and back-fill within each city
    for col in value_cols:
        merged[col] = (
            merged.groupby("city")[col]
            .transform(lambda s: s.ffill().bfill())
        )

    return merged[["city", "date"] + value_cols]


def merge_annual(
    daily: pd.DataFrame,
    demographics: pd.DataFrame,
    fleet: pd.DataFrame,
) -> pd.DataFrame:
    """Attach annual demographics and fleet data to the daily panel."""
    # Demographics: one row per city-year
    demo_cols = [
        "population", "density", "pop_0_14", "pop_15_59", "pop_60_plus",
        "pop_female", "pop_male",
    ]
    demo_interp = _interpolate_annual_to_daily(
        demographics, daily, demo_cols, time_col="year"
    )
    daily = pd.merge(daily, demo_interp, on=["city", "date"], how="left")
    logger.info("+ Demographics merge: %d rows", len(daily))

    # Fleet: aggregate months to year-level (take max of monthly fleet_total)
    fleet_yearly = (
        fleet
        .groupby(["city", "year"], as_index=False)
        .agg({"fleet_total": "max", "fleet_automobile": "max",
               "fleet_motorcycle": "max", "fleet_bus": "max",
               "fleet_truck": "max"})
    )
    fleet_cols = ["fleet_total", "fleet_automobile", "fleet_motorcycle",
                  "fleet_bus", "fleet_truck"]
    fleet_interp = _interpolate_annual_to_daily(
        fleet_yearly, daily, fleet_cols, time_col="year"
    )
    daily = pd.merge(daily, fleet_interp, on=["city", "date"], how="left")
    logger.info("+ Fleet merge: %d rows", len(daily))

    return daily


# =========================================================================
# 6. Derived features
# =========================================================================
def add_derived_features(df: pd.DataFrame) -> pd.DataFrame:
    """Compute all derived features required for analysis."""
    df = df.copy()
    df = df.sort_values(["city", "date"]).reset_index(drop=True)

    # --- Diurnal temperature range ---
    df["dtr"] = df["temperature_max"] - df["temperature_min"]

    # --- Lagged exposures (within each city) ---
    for lag in range(1, MAX_LAG_DAYS + 1):
        for var in ["pm25", "o3", "temperature_mean"]:
            col_name = f"{var}_lag{lag}"
            df[col_name] = df.groupby("city")[var].shift(lag)

    # --- Moving averages ---
    for window in MOVING_AVG_WINDOWS:
        for var in ["pm25", "o3", "temperature_mean"]:
            col_name = f"{var}_ma{window}"
            df[col_name] = (
                df.groupby("city")[var]
                .transform(lambda s: s.rolling(window, min_periods=1).mean())
            )

    # --- Fourier terms for seasonality ---
    day_of_year = df["date"].dt.dayofyear
    for i, period in enumerate(FOURIER_PERIODS):
        suffix = "annual" if i == 0 else "semiannual"
        df[f"sin_{suffix}"] = np.sin(2 * np.pi * day_of_year / period)
        df[f"cos_{suffix}"] = np.cos(2 * np.pi * day_of_year / period)

    # --- Day of week dummies ---
    dow = df["date"].dt.dayofweek  # 0=Monday
    for d in range(1, 7):  # Monday is reference
        df[f"dow_{d}"] = (dow == d).astype(int)

    # --- Linear trend (days since start) ---
    start_date = pd.Timestamp(ANALYSIS_START)
    df["trend"] = (df["date"] - start_date).dt.days

    # --- Fleet per capita ---
    df["fleet_per_capita"] = np.where(
        df["population"].notna() & (df["population"] > 0),
        df["fleet_total"] / df["population"] * 1000,  # per 1000 inhabitants
        np.nan,
    )

    # --- Population density (computed from population / known city area) ---
    city_area = {city: meta["area_km2"] for city, meta in CAPITALS.items()}
    df["city_area_km2"] = df["city"].map(city_area)
    df["pop_density"] = np.where(
        df["population"].notna() & (df["population"] > 0) & df["city_area_km2"].notna(),
        df["population"] / df["city_area_km2"],
        np.nan,
    )

    # --- Percent female (proxy for demographic structure) ---
    df["pct_female"] = np.where(
        df["population"].notna() & (df["population"] > 0)
        & df["pop_female"].notna(),
        df["pop_female"] / df["population"],
        np.nan,
    )

    # --- Region dummies ---
    city_to_region = {city: meta["region"] for city, meta in CAPITALS.items()}
    df["region"] = df["city"].map(city_to_region)
    for r in REGION_ORDER:
        df[f"region_{r}"] = (df["region"] == r).astype(int)

    # --- UF mapping ---
    city_to_uf = {city: meta["uf"] for city, meta in CAPITALS.items()}
    df["uf"] = df["city"].map(city_to_uf)

    logger.info("Derived features added: %d columns total", len(df.columns))
    return df


# =========================================================================
# 7. Treatment indicators
# =========================================================================
def add_treatments(df: pd.DataFrame) -> pd.DataFrame:
    """Add binary treatment indicators."""
    df = df.copy()
    df["pm25_exceed"] = (df["pm25"] > WHO_PM25_THRESHOLD).astype(int)
    df["o3_exceed"] = (df["o3"] > WHO_O3_THRESHOLD).astype(int)
    logger.info(
        "Treatment indicators: PM2.5>%.0f (%.1f%% exceed), O3>%.0f (%.1f%% exceed)",
        WHO_PM25_THRESHOLD,
        100 * df["pm25_exceed"].mean(),
        WHO_O3_THRESHOLD,
        100 * df["o3_exceed"].mean(),
    )
    return df


# =========================================================================
# 8. Quality filters
# =========================================================================
def apply_quality_filters(df: pd.DataFrame) -> pd.DataFrame:
    """
    Drop city-days with critical missing data.

    Rules:
        - PM2.5 must be non-null
        - Admissions (total) must be non-null
        - Temperature must be non-null
    """
    before = len(df)
    df = df.dropna(subset=["pm25", "admissions", "temperature_mean"])
    after = len(df)
    logger.info("Quality filter: %d -> %d rows (dropped %d)", before, after, before - after)

    # Log per-city summary
    city_counts = df.groupby("city").size()
    if len(city_counts) > 0:
        logger.info("Cities remaining: %d, days range: %d - %d",
                    len(city_counts), int(city_counts.min()), int(city_counts.max()))
    else:
        logger.warning("No rows remaining after quality filter!")
    return df.reset_index(drop=True)


# =========================================================================
# 9. Save
# =========================================================================
def save_panel(df: pd.DataFrame) -> Path:
    """Save the analysis panel to Parquet."""
    out_path = PROCESSED_DIR / "analysis_panel.parquet"
    df.to_parquet(out_path, index=False, engine="pyarrow")
    size_mb = out_path.stat().st_size / 1024 / 1024
    logger.info("Saved %s (%.2f MB, %d rows x %d cols)",
                out_path, size_mb, len(df), len(df.columns))

    # Also save a lightweight summary
    summary_path = INTERIM_DIR / "panel_summary.json"
    summary = {
        "n_rows": int(len(df)),
        "n_cols": int(len(df.columns)),
        "n_cities": int(df["city"].nunique()),
        "date_range": [str(df["date"].min().date()), str(df["date"].max().date())],
        "columns": list(df.columns),
        "pm25_exceed_pct": float(round(100 * df["pm25_exceed"].mean(), 2)),
        "o3_exceed_pct": float(round(100 * df["o3_exceed"].mean(), 2)),
        "mean_admissions": float(round(df["admissions"].mean(), 2)),
        "cities": sorted(df["city"].unique().tolist()),
    }
    import json
    summary_path.write_text(json.dumps(summary, indent=2, ensure_ascii=False))
    logger.info("Summary saved to %s", summary_path)

    return out_path


# =========================================================================
# Main
# =========================================================================
def main() -> None:
    t0 = time.time()

    # 1. Load
    weather = load_raw("weather")
    air_quality = load_raw("air_quality")
    health = load_raw("health")
    demographics = load_raw("demographics")
    fleet = load_raw("fleet")

    # 2-3. Date filter + respiratory filter
    weather = _parse_dates(weather)
    air_quality = _parse_dates(air_quality)
    health = _parse_dates(health)
    health = _filter_respiratory(health)

    # Demographics / fleet: filter years relevant to analysis
    demographics["year"] = demographics["year"].astype(int)
    fleet["year"] = fleet["year"].astype(int)
    start_year = int(ANALYSIS_START[:4]) - 1   # one year before for interpolation
    end_year = int(ANALYSIS_END[:4]) + 1
    demographics = demographics[
        (demographics["year"] >= start_year) & (demographics["year"] <= end_year)
    ].reset_index(drop=True)
    fleet = fleet[
        (fleet["year"] >= start_year) & (fleet["year"] <= end_year)
    ].reset_index(drop=True)

    # 4. Merge daily
    panel = merge_daily(weather, air_quality, health)

    # 5. Merge annual
    panel = merge_annual(panel, demographics, fleet)

    # 6. Derived features
    panel = add_derived_features(panel)

    # 7. Treatment indicators
    panel = add_treatments(panel)

    # 8. Quality filters
    panel = apply_quality_filters(panel)

    # 9. Save
    save_panel(panel)

    elapsed = time.time() - t0
    logger.info("Processing complete in %.1f s.", elapsed)


if __name__ == "__main__":
    main()
