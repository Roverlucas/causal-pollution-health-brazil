#!/usr/bin/env python3
"""
Policy counterfactual visualizations.

Creates:
    1. Bar chart of prevented admissions by city
    2. Stacked bar chart of prevented fraction by vulnerability quartile
    3. Threshold dose-response curve
    4. Cost savings summary figure

Usage:
    python src/visualization/policy_plots.py
"""

from __future__ import annotations

import json
import logging
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# ---------------------------------------------------------------------------
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from src.utils.config import (
    TABLES_DIR,
    REPORTS_DIR,
    FIGURES_DIR,
    CAPITALS,
    LOG_FORMAT,
    LOG_DATE_FORMAT,
)

logging.basicConfig(format=LOG_FORMAT, datefmt=LOG_DATE_FORMAT, level=logging.INFO)
logger = logging.getLogger("policy_plots")


# ---------------------------------------------------------------------------
# Load policy data
# ---------------------------------------------------------------------------
def load_city_prevented() -> pd.DataFrame | None:
    path = TABLES_DIR / "policy_city_prevented.csv"
    if not path.exists():
        logger.warning("City prevented data not found: %s", path)
        return None
    return pd.read_csv(path)


def load_stratified() -> pd.DataFrame | None:
    path = TABLES_DIR / "policy_stratified.csv"
    if not path.exists():
        return None
    return pd.read_csv(path)


def load_thresholds() -> pd.DataFrame | None:
    path = TABLES_DIR / "policy_thresholds.csv"
    if not path.exists():
        return None
    return pd.read_csv(path)


def load_cost() -> dict | None:
    path = REPORTS_DIR / "cost_estimation.json"
    if not path.exists():
        return None
    return json.loads(path.read_text())


# ---------------------------------------------------------------------------
# 1. City-level prevented admissions
# ---------------------------------------------------------------------------
def plot_city_prevented(df: pd.DataFrame) -> None:
    """Horizontal bar chart of prevented admissions by city."""
    df = df.sort_values("prevented_pct", ascending=True)

    # Color by region
    city_to_region = {city: meta["region"] for city, meta in CAPITALS.items()}
    df["region"] = df["city"].map(city_to_region)
    region_colors = {"N": "#1b9e77", "NE": "#d95f02", "CO": "#7570b3",
                     "SE": "#e7298a", "S": "#66a61e"}
    colors = [region_colors.get(r, "#999999") for r in df["region"]]

    fig, ax = plt.subplots(figsize=(10, 9))
    bars = ax.barh(df["city"], df["prevented_pct"], color=colors,
                    edgecolor="black", linewidth=0.3)

    ax.set_xlabel("Prevented Respiratory Admissions (%)", fontsize=11)
    ax.set_title(
        "Percentage of Respiratory Admissions Preventable\n"
        "Under WHO PM2.5 Guideline (15 ug/m3) Compliance",
        fontsize=13, fontweight="bold",
    )

    # Legend for regions
    for region, color in region_colors.items():
        ax.barh([], [], color=color, label=region)
    ax.legend(title="Region", loc="lower right", fontsize=9)

    # Annotate values
    for i, (_, row) in enumerate(df.iterrows()):
        ax.text(
            row["prevented_pct"] + 0.2, i,
            f"{row['prevented_pct']:.1f}% ({row['prevented_admissions']:.0f})",
            va="center", fontsize=7,
        )

    plt.tight_layout()
    out_path = FIGURES_DIR / "policy_city_prevented.pdf"
    plt.savefig(out_path, dpi=300, bbox_inches="tight")
    plt.close()
    logger.info("City prevented plot saved to %s", out_path)


# ---------------------------------------------------------------------------
# 2. Stratified by vulnerability quartile
# ---------------------------------------------------------------------------
def plot_stratified(df: pd.DataFrame) -> None:
    """Bar chart of prevented fraction by CATE vulnerability quartile."""
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    # Left: prevented admissions
    colors = ["#4575b4", "#91bfdb", "#fc8d59", "#d73027"]
    axes[0].bar(
        df["vuln_quartile"], df["prevented_admissions"],
        color=colors, edgecolor="black", linewidth=0.5,
    )
    axes[0].set_ylabel("Prevented Admissions", fontsize=11)
    axes[0].set_title("Absolute Prevented Admissions", fontsize=12, fontweight="bold")
    axes[0].tick_params(axis="x", rotation=30)

    # Right: prevented percentage
    axes[1].bar(
        df["vuln_quartile"], df["prevented_pct"],
        color=colors, edgecolor="black", linewidth=0.5,
    )
    axes[1].set_ylabel("Prevented (%)", fontsize=11)
    axes[1].set_title("Relative Prevented Fraction", fontsize=12, fontweight="bold")
    axes[1].tick_params(axis="x", rotation=30)

    plt.suptitle(
        "Policy Impact by Vulnerability Quartile\n"
        "(Under WHO PM2.5 Compliance)",
        fontsize=13, fontweight="bold",
    )
    plt.tight_layout()

    out_path = FIGURES_DIR / "policy_stratified_quartiles.pdf"
    plt.savefig(out_path, dpi=300, bbox_inches="tight")
    plt.close()
    logger.info("Stratified plot saved to %s", out_path)


# ---------------------------------------------------------------------------
# 3. Threshold dose-response
# ---------------------------------------------------------------------------
def plot_threshold_response(df: pd.DataFrame) -> None:
    """Line plot of prevented fraction vs PM2.5 threshold."""
    fig, ax1 = plt.subplots(figsize=(8, 5))

    # Left axis: prevented %
    color1 = "#2166ac"
    ax1.plot(
        df["threshold_ugm3"], df["prevented_pct"],
        "o-", color=color1, markersize=8, linewidth=2,
    )
    ax1.set_xlabel("PM2.5 Threshold (ug/m3)", fontsize=11)
    ax1.set_ylabel("Prevented Admissions (%)", fontsize=11, color=color1)
    ax1.tick_params(axis="y", labelcolor=color1)

    # Right axis: exceedance days %
    ax2 = ax1.twinx()
    color2 = "#b2182b"
    ax2.plot(
        df["threshold_ugm3"], df["exceed_pct"],
        "s--", color=color2, markersize=7, linewidth=1.5,
    )
    ax2.set_ylabel("Exceedance Days (%)", fontsize=11, color=color2)
    ax2.tick_params(axis="y", labelcolor=color2)

    # Mark WHO threshold
    ax1.axvline(15, color="green", linestyle=":", linewidth=1.5, label="WHO (15)")
    ax1.legend(fontsize=9, loc="upper right")

    ax1.set_title(
        "Dose-Response: PM2.5 Threshold vs. Prevented Hospitalizations",
        fontsize=13, fontweight="bold",
    )
    fig.tight_layout()

    out_path = FIGURES_DIR / "policy_threshold_response.pdf"
    plt.savefig(out_path, dpi=300, bbox_inches="tight")
    plt.close()
    logger.info("Threshold response plot saved to %s", out_path)


# ---------------------------------------------------------------------------
# 4. Cost savings summary
# ---------------------------------------------------------------------------
def plot_cost_summary(cost: dict) -> None:
    """Summary infographic of financial savings."""
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5)
    ax.axis("off")

    # Title
    ax.text(5, 4.5, "Estimated Financial Impact of WHO PM2.5 Compliance",
            ha="center", va="center", fontsize=14, fontweight="bold")

    # Key metrics
    metrics = [
        ("Total Health Cost (2022-2025)",
         f"R$ {cost['total_cost_brl']:,.0f}"),
        ("Average Cost per Admission",
         f"R$ {cost['avg_cost_per_admission_brl']:,.2f}"),
        ("Prevented Admissions",
         f"{cost['prevented_admissions']:,.0f}"),
        ("Estimated Cost Savings",
         f"R$ {cost['saved_cost_brl']:,.0f} ({cost['saved_cost_pct']:.1f}%)"),
    ]

    for i, (label, value) in enumerate(metrics):
        y = 3.5 - i * 0.9
        ax.text(1, y, label, fontsize=11, va="center", color="#333333")
        ax.text(8, y, value, fontsize=12, va="center", fontweight="bold",
                color="#2166ac", ha="right")
        ax.axhline(y - 0.4, xmin=0.05, xmax=0.95, color="#e0e0e0", linewidth=0.5)

    plt.tight_layout()
    out_path = FIGURES_DIR / "policy_cost_summary.pdf"
    plt.savefig(out_path, dpi=300, bbox_inches="tight")
    plt.close()
    logger.info("Cost summary saved to %s", out_path)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main() -> None:
    city_df = load_city_prevented()
    if city_df is not None:
        plot_city_prevented(city_df)

    strat_df = load_stratified()
    if strat_df is not None:
        plot_stratified(strat_df)

    thresh_df = load_thresholds()
    if thresh_df is not None:
        plot_threshold_response(thresh_df)

    cost = load_cost()
    if cost is not None:
        plot_cost_summary(cost)

    logger.info("Policy visualization complete.")


if __name__ == "__main__":
    main()
