#!/usr/bin/env python3
"""
Choropleth map of CATE by Brazilian state capital.

Downloads the IBGE state shapefile (UF level) and plots the mean CATE
for each capital, color-coded by effect magnitude.

Usage:
    python src/visualization/maps.py
"""

from __future__ import annotations

import json
import logging
import pickle
import sys
import time
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
import pandas as pd
import geopandas as gpd

# ---------------------------------------------------------------------------
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from src.utils.config import (
    PROCESSED_DIR,
    MODELS_DIR,
    FIGURES_DIR,
    RAW_DIR,
    RANDOM_SEED,
    ALL_CONFOUNDERS,
    HETEROGENEITY_MODERATORS,
    TREATMENT_PM25,
    OUTCOME_TOTAL,
    CAPITALS,
    LOG_FORMAT,
    LOG_DATE_FORMAT,
)

logging.basicConfig(format=LOG_FORMAT, datefmt=LOG_DATE_FORMAT, level=logging.INFO)
logger = logging.getLogger("maps")


# ---------------------------------------------------------------------------
# Download IBGE shapefile
# ---------------------------------------------------------------------------
IBGE_UF_URL = (
    "https://geoftp.ibge.gov.br/organizacao_do_territorio/"
    "malhas_territoriais/malhas_municipais/municipio_2022/Brasil/BR/"
    "BR_UF_2022.zip"
)

def get_brazil_shapefile() -> gpd.GeoDataFrame:
    """
    Load the IBGE UF-level shapefile.  Downloads once, caches locally.
    """
    cache_dir = RAW_DIR / "shapefiles"
    cache_dir.mkdir(parents=True, exist_ok=True)
    local_path = cache_dir / "BR_UF_2022.zip"

    if not local_path.exists():
        logger.info("Downloading IBGE shapefile from %s", IBGE_UF_URL)
        import requests
        resp = requests.get(IBGE_UF_URL, timeout=120)
        resp.raise_for_status()
        local_path.write_bytes(resp.content)
        logger.info("Saved shapefile to %s (%.1f MB)",
                     local_path, local_path.stat().st_size / 1e6)
    else:
        logger.info("Using cached shapefile %s", local_path)

    gdf = gpd.read_file(f"zip://{local_path}")
    logger.info("Shapefile loaded: %d features, CRS=%s", len(gdf), gdf.crs)
    return gdf


# ---------------------------------------------------------------------------
# Compute city-level mean CATE
# ---------------------------------------------------------------------------
def compute_city_cate() -> pd.DataFrame:
    """
    Load the causal forest and compute mean CATE per city.
    """
    model_path = MODELS_DIR / f"cf_{OUTCOME_TOTAL}" / "model.pkl"
    logger.info("Loading model from %s", model_path)
    with open(model_path, "rb") as f:
        cf = pickle.load(f)

    panel = pd.read_parquet(PROCESSED_DIR / "analysis_panel.parquet")

    available_moderators = [c for c in HETEROGENEITY_MODERATORS if c in panel.columns]
    available_confounders = [c for c in ALL_CONFOUNDERS if c in panel.columns]
    required = [OUTCOME_TOTAL, TREATMENT_PM25] + available_confounders + available_moderators
    subset = panel.dropna(subset=required).copy()

    X = subset[available_moderators].values.astype(np.float64)
    cate = cf.effect(X).ravel()
    subset["cate"] = cate

    city_cate = (
        subset
        .groupby("city")
        .agg(
            mean_cate=("cate", "mean"),
            median_cate=("cate", "median"),
            std_cate=("cate", "std"),
            n_obs=("cate", "size"),
            mean_admissions=(OUTCOME_TOTAL, "mean"),
        )
        .reset_index()
    )

    # Add UF for joining with shapefile
    city_to_uf = {city: meta["uf"] for city, meta in CAPITALS.items()}
    city_cate["uf"] = city_cate["city"].map(city_to_uf)
    city_cate["region"] = city_cate["city"].map(
        {city: meta["region"] for city, meta in CAPITALS.items()}
    )

    logger.info("City CATE summary:\n%s", city_cate.to_string())
    return city_cate


# ---------------------------------------------------------------------------
# Plot: Choropleth CATE map
# ---------------------------------------------------------------------------
def plot_cate_map(city_cate: pd.DataFrame) -> None:
    """Create a choropleth map colored by mean CATE."""
    gdf = get_brazil_shapefile()

    # Join on UF abbreviation
    # The IBGE shapefile uses 'SIGLA_UF' for UF codes
    uf_col = None
    for candidate in ["SIGLA_UF", "SIGLA", "UF", "sigla_uf"]:
        if candidate in gdf.columns:
            uf_col = candidate
            break
    if uf_col is None:
        logger.warning("Could not find UF column in shapefile. Available: %s", list(gdf.columns))
        # Try the first likely candidate
        uf_col = gdf.columns[1]
        logger.info("Using column '%s' as UF identifier", uf_col)

    gdf = gdf.merge(
        city_cate[["uf", "mean_cate"]],
        left_on=uf_col, right_on="uf", how="left",
    )

    # Plot
    fig, ax = plt.subplots(1, 1, figsize=(10, 12))

    # Base map (all states in light gray)
    gdf.plot(
        ax=ax,
        color="#e0e0e0",
        edgecolor="white",
        linewidth=0.5,
    )

    # Overlay states with CATE data
    has_data = gdf["mean_cate"].notna()
    if has_data.any():
        vmin = gdf.loc[has_data, "mean_cate"].min()
        vmax = gdf.loc[has_data, "mean_cate"].max()
        # Diverging colormap centered at 0
        norm = mcolors.TwoSlopeNorm(vmin=vmin, vcenter=0, vmax=max(vmax, 0.01))

        gdf.loc[has_data].plot(
            ax=ax,
            column="mean_cate",
            cmap="RdYlBu_r",
            norm=norm,
            edgecolor="white",
            linewidth=0.5,
            legend=True,
            legend_kwds={
                "label": "Mean CATE (excess admissions/day)",
                "orientation": "horizontal",
                "shrink": 0.6,
                "pad": 0.02,
            },
        )

    # Annotate capital cities
    capital_coords = {}
    for city, meta in CAPITALS.items():
        # Use centroid of the UF polygon as approximate location
        uf_mask = gdf[uf_col] == meta["uf"]
        if uf_mask.any():
            centroid = gdf.loc[uf_mask].geometry.centroid.iloc[0]
            capital_coords[city] = (centroid.x, centroid.y)

    for city, (x, y) in capital_coords.items():
        cate_val = city_cate.loc[city_cate["city"] == city, "mean_cate"]
        if not cate_val.empty:
            label = f"{city}\n({cate_val.iloc[0]:.2f})"
            ax.annotate(
                label,
                xy=(x, y),
                fontsize=5,
                ha="center",
                va="center",
                fontweight="bold",
                bbox=dict(boxstyle="round,pad=0.15", facecolor="white",
                          edgecolor="gray", alpha=0.7),
            )

    ax.set_title(
        "Conditional Average Treatment Effect of PM2.5 Exceedance\n"
        "on Respiratory Hospitalizations by State Capital",
        fontsize=13, fontweight="bold",
    )
    ax.set_axis_off()
    plt.tight_layout()

    out_path = FIGURES_DIR / "cate_map_brazil.pdf"
    plt.savefig(out_path, dpi=300, bbox_inches="tight")
    plt.close()
    logger.info("CATE map saved to %s", out_path)

    # Also save as PNG for quick preview
    out_png = FIGURES_DIR / "cate_map_brazil.png"
    fig2, ax2 = plt.subplots(1, 1, figsize=(10, 12))
    gdf.plot(ax=ax2, color="#e0e0e0", edgecolor="white", linewidth=0.5)
    if has_data.any():
        gdf.loc[has_data].plot(
            ax=ax2, column="mean_cate", cmap="RdYlBu_r", norm=norm,
            edgecolor="white", linewidth=0.5, legend=True,
            legend_kwds={"label": "Mean CATE", "orientation": "horizontal",
                         "shrink": 0.6, "pad": 0.02},
        )
    ax2.set_axis_off()
    ax2.set_title("CATE of PM2.5 Exceedance on Respiratory Hospitalizations",
                   fontsize=13, fontweight="bold")
    plt.tight_layout()
    plt.savefig(out_png, dpi=150, bbox_inches="tight")
    plt.close()
    logger.info("CATE map PNG saved to %s", out_png)


# ---------------------------------------------------------------------------
# Plot: Capital-level scatter with region color
# ---------------------------------------------------------------------------
def plot_cate_scatter(city_cate: pd.DataFrame) -> None:
    """Scatter plot of mean CATE vs mean admissions, colored by region."""
    fig, ax = plt.subplots(figsize=(10, 7))
    region_colors = {"N": "#1b9e77", "NE": "#d95f02", "CO": "#7570b3",
                     "SE": "#e7298a", "S": "#66a61e"}

    for region, color in region_colors.items():
        mask = city_cate["region"] == region
        subset = city_cate[mask]
        ax.scatter(
            subset["mean_admissions"], subset["mean_cate"],
            c=color, label=region, s=80, alpha=0.8, edgecolors="black", linewidth=0.5,
        )
        for _, row in subset.iterrows():
            ax.annotate(
                row["city"], (row["mean_admissions"], row["mean_cate"]),
                fontsize=6, ha="left", va="bottom",
            )

    ax.axhline(0, color="gray", linestyle="--", linewidth=0.8)
    ax.set_xlabel("Mean Daily Respiratory Admissions", fontsize=11)
    ax.set_ylabel("Mean CATE (excess admissions/day)", fontsize=11)
    ax.set_title("CATE vs. Hospitalization Burden by Capital", fontsize=13, fontweight="bold")
    ax.legend(title="Region", fontsize=9)
    plt.tight_layout()

    out_path = FIGURES_DIR / "cate_scatter_capitals.pdf"
    plt.savefig(out_path, dpi=300, bbox_inches="tight")
    plt.close()
    logger.info("Scatter plot saved to %s", out_path)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main() -> None:
    t0 = time.time()

    city_cate = compute_city_cate()

    # Save city-level CATE table
    city_cate.to_csv(FIGURES_DIR.parent / "tables" / "city_cate_summary.csv", index=False)

    plot_cate_map(city_cate)
    plot_cate_scatter(city_cate)

    elapsed = time.time() - t0
    logger.info("Map visualization complete in %.1f s.", elapsed)


if __name__ == "__main__":
    main()
