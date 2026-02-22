#!/usr/bin/env python3
"""
SHAP analysis on the Causal Forest model.

Uses TreeExplainer to decompose CATE heterogeneity into feature
contributions, producing:
    - Global feature importance (mean |SHAP|)
    - SHAP values matrix
    - Beeswarm summary plot
    - Dependence plots for top features

Usage:
    python src/analysis/shap_analysis.py
"""

from __future__ import annotations

import logging
import pickle
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd
import shap

# ---------------------------------------------------------------------------
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from src.utils.config import (
    PROCESSED_DIR,
    MODELS_DIR,
    FIGURES_DIR,
    TABLES_DIR,
    RANDOM_SEED,
    ALL_CONFOUNDERS,
    HETEROGENEITY_MODERATORS,
    TREATMENT_PM25,
    OUTCOME_TOTAL,
    SHAP_MAX_SAMPLES,
    LOG_FORMAT,
    LOG_DATE_FORMAT,
)

logging.basicConfig(format=LOG_FORMAT, datefmt=LOG_DATE_FORMAT, level=logging.INFO)
logger = logging.getLogger("shap_analysis")

np.random.seed(RANDOM_SEED)


# ---------------------------------------------------------------------------
# Load model and data
# ---------------------------------------------------------------------------
def load_model_and_data(
    outcome: str = OUTCOME_TOTAL,
) -> tuple:
    """Load the fitted CausalForestDML and the matching data matrices."""
    model_path = MODELS_DIR / f"cf_{outcome}" / "model.pkl"
    logger.info("Loading model from %s", model_path)
    with open(model_path, "rb") as f:
        cf = pickle.load(f)

    panel = pd.read_parquet(PROCESSED_DIR / "analysis_panel.parquet")

    # Reproduce the same matrix construction
    available_moderators = [c for c in HETEROGENEITY_MODERATORS if c in panel.columns]
    available_confounders = [c for c in ALL_CONFOUNDERS if c in panel.columns]
    required = [outcome, TREATMENT_PM25] + available_confounders + available_moderators
    subset = panel.dropna(subset=required)

    X = subset[available_moderators].values.astype(np.float64)

    return cf, X, available_moderators


# ---------------------------------------------------------------------------
# SHAP computation
# ---------------------------------------------------------------------------
def compute_shap_values(
    cf,
    X: np.ndarray,
    feature_names: list[str],
) -> tuple[np.ndarray, np.ndarray]:
    """
    Compute SHAP values for the CATE predictions.

    The CausalForestDML.effect() produces CATE predictions.  We wrap
    this in a function and use KernelExplainer (or TreeExplainer on the
    underlying forest) to get SHAP values.

    For large datasets, we subsample to SHAP_MAX_SAMPLES.
    """
    n = X.shape[0]
    if n > SHAP_MAX_SAMPLES:
        logger.info("Subsampling from %d to %d for SHAP", n, SHAP_MAX_SAMPLES)
        idx = np.random.choice(n, SHAP_MAX_SAMPLES, replace=False)
        X_shap = X[idx]
    else:
        X_shap = X

    # Use the effect function as the prediction function
    def predict_cate(x):
        return cf.effect(x).ravel()

    # Background summary for KernelExplainer
    background = shap.kmeans(X_shap, min(50, len(X_shap)))
    explainer = shap.KernelExplainer(predict_cate, background)

    logger.info("Computing SHAP values for %d samples ...", len(X_shap))
    shap_values = explainer.shap_values(X_shap, nsamples=200)

    return shap_values, X_shap


def global_importance(
    shap_values: np.ndarray,
    feature_names: list[str],
) -> pd.DataFrame:
    """Compute mean absolute SHAP importance."""
    mean_abs = np.abs(shap_values).mean(axis=0)
    imp_df = pd.DataFrame({
        "feature": feature_names,
        "mean_abs_shap": mean_abs,
    }).sort_values("mean_abs_shap", ascending=False).reset_index(drop=True)
    logger.info("Global SHAP importance:\n%s", imp_df.to_string())
    return imp_df


# ---------------------------------------------------------------------------
# Save
# ---------------------------------------------------------------------------
def save_shap_results(
    shap_values: np.ndarray,
    X_shap: np.ndarray,
    feature_names: list[str],
    importance_df: pd.DataFrame,
    outcome: str,
) -> None:
    """Save SHAP values and importance table."""
    base = MODELS_DIR / f"cf_{outcome}"

    # SHAP values as parquet
    shap_df = pd.DataFrame(shap_values, columns=[f"shap_{f}" for f in feature_names])
    x_df = pd.DataFrame(X_shap, columns=feature_names)
    combined = pd.concat([x_df, shap_df], axis=1)
    shap_path = base / "shap_values.parquet"
    combined.to_parquet(shap_path, index=False)
    logger.info("SHAP values saved to %s", shap_path)

    # Importance table
    imp_path = TABLES_DIR / f"shap_importance_{outcome}.csv"
    importance_df.to_csv(imp_path, index=False)
    logger.info("Importance table saved to %s", imp_path)


# ---------------------------------------------------------------------------
# Plotting (saved to figures/)
# ---------------------------------------------------------------------------
def plot_beeswarm(
    shap_values: np.ndarray,
    X_shap: np.ndarray,
    feature_names: list[str],
    outcome: str,
) -> None:
    """Create and save a SHAP beeswarm summary plot."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(10, 6))
    shap.summary_plot(
        shap_values,
        X_shap,
        feature_names=feature_names,
        show=False,
        plot_size=None,
    )
    plt.title(f"SHAP Beeswarm — CATE of PM2.5 Exceedance on {outcome}", fontsize=12)
    plt.tight_layout()
    out_path = FIGURES_DIR / f"shap_beeswarm_{outcome}.pdf"
    plt.savefig(out_path, dpi=300, bbox_inches="tight")
    plt.close()
    logger.info("Beeswarm plot saved to %s", out_path)


def plot_dependence_top3(
    shap_values: np.ndarray,
    X_shap: np.ndarray,
    feature_names: list[str],
    importance_df: pd.DataFrame,
    outcome: str,
) -> None:
    """Create dependence plots for the top 3 features."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    top3 = importance_df["feature"].head(3).tolist()
    for feat in top3:
        idx = feature_names.index(feat)
        fig, ax = plt.subplots(figsize=(8, 5))
        shap.dependence_plot(
            idx,
            shap_values,
            X_shap,
            feature_names=feature_names,
            show=False,
            ax=ax,
        )
        ax.set_title(f"SHAP Dependence: {feat} ({outcome})", fontsize=12)
        plt.tight_layout()
        out_path = FIGURES_DIR / f"shap_dependence_{feat}_{outcome}.pdf"
        plt.savefig(out_path, dpi=300, bbox_inches="tight")
        plt.close()
        logger.info("Dependence plot saved to %s", out_path)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main() -> None:
    t0 = time.time()

    outcome = OUTCOME_TOTAL
    logger.info("Running SHAP analysis for outcome: %s", outcome)

    cf, X, feature_names = load_model_and_data(outcome)
    shap_values, X_shap = compute_shap_values(cf, X, feature_names)
    imp_df = global_importance(shap_values, feature_names)

    save_shap_results(shap_values, X_shap, feature_names, imp_df, outcome)
    plot_beeswarm(shap_values, X_shap, feature_names, outcome)
    plot_dependence_top3(shap_values, X_shap, feature_names, imp_df, outcome)

    elapsed = time.time() - t0
    logger.info("SHAP analysis complete in %.1f s.", elapsed)


if __name__ == "__main__":
    main()
