#!/usr/bin/env python3
"""
SHAP visualization plots.

Creates publication-quality SHAP figures:
    1. Beeswarm summary (if not already created by shap_analysis.py)
    2. Bar chart of global feature importance
    3. Waterfall plot for high-vulnerability vs low-vulnerability exemplars

Usage:
    python src/visualization/shap_plots.py
"""

from __future__ import annotations

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
    TABLES_DIR,
    OUTCOME_TOTAL,
    HETEROGENEITY_MODERATORS,
    LOG_FORMAT,
    LOG_DATE_FORMAT,
)

logging.basicConfig(format=LOG_FORMAT, datefmt=LOG_DATE_FORMAT, level=logging.INFO)
logger = logging.getLogger("shap_plots")


# ---------------------------------------------------------------------------
# Load SHAP data
# ---------------------------------------------------------------------------
def load_shap_data() -> tuple[np.ndarray, np.ndarray, list[str]] | None:
    """Load pre-computed SHAP values from parquet."""
    shap_path = MODELS_DIR / f"cf_{OUTCOME_TOTAL}" / "shap_values.parquet"
    if not shap_path.exists():
        logger.error("SHAP values not found: %s. Run shap_analysis.py first.", shap_path)
        return None

    df = pd.read_parquet(shap_path)
    # Columns: feature_names + shap_feature_names
    feature_names = [c for c in df.columns if not c.startswith("shap_")]
    shap_cols = [c for c in df.columns if c.startswith("shap_")]

    X = df[feature_names].values
    shap_values = df[shap_cols].values

    logger.info("Loaded SHAP data: %d samples x %d features", X.shape[0], X.shape[1])
    return shap_values, X, feature_names


def load_importance() -> pd.DataFrame | None:
    """Load feature importance table."""
    imp_path = TABLES_DIR / f"shap_importance_{OUTCOME_TOTAL}.csv"
    if not imp_path.exists():
        return None
    return pd.read_csv(imp_path)


# ---------------------------------------------------------------------------
# Bar chart of global importance
# ---------------------------------------------------------------------------
def plot_importance_bar(imp_df: pd.DataFrame) -> None:
    """Horizontal bar chart of mean |SHAP| values."""
    fig, ax = plt.subplots(figsize=(8, 5))

    imp_sorted = imp_df.sort_values("mean_abs_shap", ascending=True)
    colors = plt.cm.viridis(np.linspace(0.2, 0.9, len(imp_sorted)))

    ax.barh(
        imp_sorted["feature"],
        imp_sorted["mean_abs_shap"],
        color=colors,
        edgecolor="black",
        linewidth=0.5,
    )
    ax.set_xlabel("Mean |SHAP value|", fontsize=11)
    ax.set_title(
        "Feature Importance for CATE Heterogeneity\n(PM2.5 Exceedance on Respiratory Admissions)",
        fontsize=12, fontweight="bold",
    )
    plt.tight_layout()

    out_path = FIGURES_DIR / "shap_importance_bar.pdf"
    plt.savefig(out_path, dpi=300, bbox_inches="tight")
    plt.close()
    logger.info("Importance bar chart saved to %s", out_path)


# ---------------------------------------------------------------------------
# Beeswarm summary using raw SHAP values
# ---------------------------------------------------------------------------
def plot_beeswarm(shap_values: np.ndarray, X: np.ndarray, feature_names: list[str]) -> None:
    """Create a publication-quality beeswarm plot."""
    import shap as shap_lib

    fig, ax = plt.subplots(figsize=(10, 6))
    shap_lib.summary_plot(
        shap_values, X,
        feature_names=feature_names,
        show=False,
        plot_size=None,
    )
    plt.title(
        "SHAP Beeswarm: Drivers of CATE Heterogeneity",
        fontsize=12, fontweight="bold",
    )
    plt.tight_layout()
    out_path = FIGURES_DIR / "shap_beeswarm_publication.pdf"
    plt.savefig(out_path, dpi=300, bbox_inches="tight")
    plt.close()
    logger.info("Beeswarm plot saved to %s", out_path)


# ---------------------------------------------------------------------------
# Exemplar comparison: high vs low CATE
# ---------------------------------------------------------------------------
def plot_exemplar_comparison(
    shap_values: np.ndarray,
    X: np.ndarray,
    feature_names: list[str],
) -> None:
    """
    Bar chart comparing SHAP contributions for a high-CATE and
    low-CATE exemplar observation.
    """
    # Compute total SHAP contribution per observation
    total_shap = shap_values.sum(axis=1)
    high_idx = np.argmax(total_shap)
    low_idx = np.argmin(total_shap)

    fig, axes = plt.subplots(1, 2, figsize=(14, 5), sharey=True)

    for ax_i, (idx, title) in enumerate([(high_idx, "Highest CATE Exemplar"),
                                          (low_idx, "Lowest CATE Exemplar")]):
        vals = shap_values[idx]
        sort_idx = np.argsort(np.abs(vals))
        sorted_names = [feature_names[i] for i in sort_idx]
        sorted_vals = vals[sort_idx]

        colors = ["#d73027" if v > 0 else "#4575b4" for v in sorted_vals]
        axes[ax_i].barh(sorted_names, sorted_vals, color=colors, edgecolor="black", linewidth=0.3)
        axes[ax_i].axvline(0, color="gray", linestyle="--", linewidth=0.8)
        axes[ax_i].set_title(title, fontsize=11, fontweight="bold")
        axes[ax_i].set_xlabel("SHAP value", fontsize=10)

        # Annotate feature values
        for j, (name, sv) in enumerate(zip(sorted_names, sorted_vals)):
            feat_idx = feature_names.index(name)
            feat_val = X[idx, feat_idx]
            axes[ax_i].text(
                sv + 0.001 * np.sign(sv) if sv != 0 else 0.001,
                j, f"({feat_val:.1f})",
                va="center", fontsize=7, color="gray",
            )

    plt.suptitle(
        "SHAP Decomposition: High vs Low Vulnerability Observations",
        fontsize=13, fontweight="bold",
    )
    plt.tight_layout()

    out_path = FIGURES_DIR / "shap_exemplar_comparison.pdf"
    plt.savefig(out_path, dpi=300, bbox_inches="tight")
    plt.close()
    logger.info("Exemplar comparison saved to %s", out_path)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main() -> None:
    imp_df = load_importance()
    if imp_df is not None:
        plot_importance_bar(imp_df)
    else:
        logger.warning("Importance data not found, skipping bar chart.")

    data = load_shap_data()
    if data is not None:
        shap_values, X, feature_names = data
        plot_beeswarm(shap_values, X, feature_names)
        plot_exemplar_comparison(shap_values, X, feature_names)
    else:
        logger.warning("SHAP data not found, skipping beeswarm and exemplar plots.")

    logger.info("SHAP visualization complete.")


if __name__ == "__main__":
    main()
