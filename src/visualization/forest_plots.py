#!/usr/bin/env python3
"""
Forest plot of CATE by subgroup.

Visualizes ATE / CATE estimates with confidence intervals for:
    - Total population
    - Age groups (0-14, 15-59, 60+)
    - Sex groups (female, male)
    - Vulnerability quartiles (CLAN)

Usage:
    python src/visualization/forest_plots.py
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
    MODELS_DIR,
    FIGURES_DIR,
    ALL_OUTCOMES,
    OUTCOME_TOTAL,
    LOG_FORMAT,
    LOG_DATE_FORMAT,
)

logging.basicConfig(format=LOG_FORMAT, datefmt=LOG_DATE_FORMAT, level=logging.INFO)
logger = logging.getLogger("forest_plots")


# ---------------------------------------------------------------------------
# Load ATE results for all outcomes
# ---------------------------------------------------------------------------
def load_ate_results() -> pd.DataFrame:
    """Load ATE results from all causal forest models."""
    records = []
    label_map = {
        "admissions": "Total Respiratory",
        "admissions_age_0_14": "Children (0-14)",
        "admissions_age_15_59": "Adults (15-59)",
        "admissions_age_60_plus": "Elderly (60+)",
        "admissions_female": "Female",
        "admissions_male": "Male",
    }

    for outcome in ALL_OUTCOMES:
        ate_path = MODELS_DIR / f"cf_{outcome}" / "ate.json"
        if not ate_path.exists():
            logger.warning("ATE file not found: %s", ate_path)
            continue
        with open(ate_path) as f:
            ate = json.load(f)
        records.append({
            "outcome": outcome,
            "label": label_map.get(outcome, outcome),
            "ate": ate["ate"],
            "ci_lower": ate["ci_lower"],
            "ci_upper": ate["ci_upper"],
            "pvalue": ate["pvalue"],
        })

    df = pd.DataFrame(records)
    logger.info("Loaded ATE results for %d outcomes", len(df))
    return df


def load_dml_results() -> pd.DataFrame:
    """Load DML ATE results for comparison."""
    records = []
    label_map = {
        "admissions": "Total Respiratory",
        "admissions_age_0_14": "Children (0-14)",
        "admissions_age_15_59": "Adults (15-59)",
        "admissions_age_60_plus": "Elderly (60+)",
        "admissions_female": "Female",
        "admissions_male": "Male",
    }

    for outcome in ALL_OUTCOMES:
        ate_path = MODELS_DIR / f"dml_{outcome}" / "ate.json"
        if not ate_path.exists():
            continue
        with open(ate_path) as f:
            ate = json.load(f)
        records.append({
            "outcome": outcome,
            "label": label_map.get(outcome, outcome),
            "ate": ate["ate"],
            "ci_lower": ate["ci_lower"],
            "ci_upper": ate["ci_upper"],
            "pvalue": ate["pvalue"],
        })

    return pd.DataFrame(records)


def load_clan_results() -> pd.DataFrame | None:
    """Load CLAN quartile results for total admissions."""
    clan_path = MODELS_DIR / f"cf_{OUTCOME_TOTAL}" / "clan.csv"
    if not clan_path.exists():
        logger.warning("CLAN file not found: %s", clan_path)
        return None
    clan = pd.read_csv(clan_path, index_col=0)
    return clan


# ---------------------------------------------------------------------------
# Forest plot: ATE by subgroup
# ---------------------------------------------------------------------------
def plot_subgroup_forest(ate_df: pd.DataFrame, dml_df: pd.DataFrame) -> None:
    """
    Forest plot with ATE and 95% CI for each subgroup.
    Shows both Causal Forest and LinearDML estimates side by side.
    """
    fig, ax = plt.subplots(figsize=(10, 7))

    n = len(ate_df)
    y_positions = np.arange(n)
    offset = 0.15

    # Causal Forest
    ax.errorbar(
        ate_df["ate"], y_positions + offset,
        xerr=[ate_df["ate"] - ate_df["ci_lower"],
              ate_df["ci_upper"] - ate_df["ate"]],
        fmt="o", color="#2166ac", markersize=8, capsize=4,
        label="Causal Forest", linewidth=1.5,
    )

    # DML (if available)
    if not dml_df.empty:
        # Match order
        dml_merged = pd.merge(
            ate_df[["outcome", "label"]], dml_df,
            on=["outcome", "label"], how="left", suffixes=("", "_dml"),
        )
        ax.errorbar(
            dml_merged["ate"], y_positions - offset,
            xerr=[dml_merged["ate"] - dml_merged["ci_lower"],
                  dml_merged["ci_upper"] - dml_merged["ate"]],
            fmt="s", color="#b2182b", markersize=7, capsize=4,
            label="Linear DML", linewidth=1.5,
        )

    ax.axvline(0, color="gray", linestyle="--", linewidth=0.8)
    ax.set_yticks(y_positions)
    ax.set_yticklabels(ate_df["label"], fontsize=10)
    ax.invert_yaxis()
    ax.set_xlabel("ATE (excess respiratory admissions per day)", fontsize=11)
    ax.set_title(
        "Average Treatment Effect of PM2.5 Exceedance (>15 ug/m3)\n"
        "on Respiratory Hospitalizations by Subgroup",
        fontsize=13, fontweight="bold",
    )
    ax.legend(loc="lower right", fontsize=10)

    # Add p-value annotations
    for i, row in ate_df.iterrows():
        sig = ""
        if row["pvalue"] < 0.001:
            sig = "***"
        elif row["pvalue"] < 0.01:
            sig = "**"
        elif row["pvalue"] < 0.05:
            sig = "*"
        if sig:
            ax.text(
                row["ci_upper"] + 0.02 * (ax.get_xlim()[1] - ax.get_xlim()[0]),
                y_positions[i] + offset,
                sig, fontsize=11, va="center", color="#2166ac",
            )

    plt.tight_layout()
    out_path = FIGURES_DIR / "forest_ate_subgroups.pdf"
    plt.savefig(out_path, dpi=300, bbox_inches="tight")
    plt.close()
    logger.info("Forest plot saved to %s", out_path)


# ---------------------------------------------------------------------------
# Forest plot: CLAN vulnerability quartiles
# ---------------------------------------------------------------------------
def plot_clan_forest(clan_df: pd.DataFrame) -> None:
    """Forest plot of mean CATE by vulnerability quartile."""
    if clan_df is None or "cate" not in clan_df.columns:
        logger.warning("No CLAN data available for plotting.")
        return

    fig, ax = plt.subplots(figsize=(8, 5))

    labels = clan_df.index.tolist()
    y_positions = np.arange(len(labels))
    cate_values = clan_df["cate"].values

    colors = ["#4575b4", "#91bfdb", "#fc8d59", "#d73027"]
    for i, (label, val) in enumerate(zip(labels, cate_values)):
        ax.barh(i, val, color=colors[i], edgecolor="black", linewidth=0.5, height=0.6)
        ax.text(
            val + 0.01 * (max(cate_values) - min(cate_values)),
            i, f"{val:.3f}",
            va="center", fontsize=10, fontweight="bold",
        )

    ax.axvline(0, color="gray", linestyle="--", linewidth=0.8)
    ax.set_yticks(y_positions)
    ax.set_yticklabels(labels, fontsize=10)
    ax.set_xlabel("Mean CATE (excess admissions/day)", fontsize=11)
    ax.set_title(
        "CLAN: Mean Treatment Effect by Vulnerability Quartile",
        fontsize=13, fontweight="bold",
    )
    ax.invert_yaxis()
    plt.tight_layout()

    out_path = FIGURES_DIR / "forest_clan_quartiles.pdf"
    plt.savefig(out_path, dpi=300, bbox_inches="tight")
    plt.close()
    logger.info("CLAN forest plot saved to %s", out_path)


# ---------------------------------------------------------------------------
# Comparison table: CF vs DML
# ---------------------------------------------------------------------------
def save_comparison_table(ate_df: pd.DataFrame, dml_df: pd.DataFrame) -> None:
    """Create a formatted comparison table."""
    if dml_df.empty:
        ate_df.to_csv(FIGURES_DIR.parent / "tables" / "ate_comparison.csv", index=False)
        return

    merged = pd.merge(
        ate_df, dml_df,
        on=["outcome", "label"],
        how="outer",
        suffixes=("_cf", "_dml"),
    )
    out_path = FIGURES_DIR.parent / "tables" / "ate_comparison.csv"
    merged.to_csv(out_path, index=False)
    logger.info("Comparison table saved to %s", out_path)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main() -> None:
    ate_df = load_ate_results()
    dml_df = load_dml_results()
    clan_df = load_clan_results()

    if ate_df.empty:
        logger.error("No ATE results found. Run causal_forest.py first.")
        return

    plot_subgroup_forest(ate_df, dml_df)
    plot_clan_forest(clan_df)
    save_comparison_table(ate_df, dml_df)

    logger.info("Forest plot visualization complete.")


if __name__ == "__main__":
    main()
