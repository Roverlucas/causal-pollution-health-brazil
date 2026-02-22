#!/usr/bin/env python3
"""
Double Machine Learning (LinearDML) estimation as a comparison to the
Causal Forest.

Uses econml.dml.LinearDML with 5-fold cross-fitting and GradientBoosting
nuisance models to estimate the Average Treatment Effect (ATE) under
Neyman-orthogonal moment conditions.

Produces:
    - ATE with 95% CI for each outcome
    - Coefficient table (treatment effect on each outcome)

Usage:
    python src/models/dml.py
"""

from __future__ import annotations

import json
import logging
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor, GradientBoostingClassifier
from econml.dml import LinearDML

# ---------------------------------------------------------------------------
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from src.utils.config import (
    PROCESSED_DIR,
    MODELS_DIR,
    RANDOM_SEED,
    ALL_CONFOUNDERS,
    HETEROGENEITY_MODERATORS,
    TREATMENT_PM25,
    ALL_OUTCOMES,
    N_FOLDS,
    LOG_FORMAT,
    LOG_DATE_FORMAT,
)

logging.basicConfig(format=LOG_FORMAT, datefmt=LOG_DATE_FORMAT, level=logging.INFO)
logger = logging.getLogger("dml")

np.random.seed(RANDOM_SEED)


# ---------------------------------------------------------------------------
# Data preparation (shared logic with causal_forest.py)
# ---------------------------------------------------------------------------
def load_panel() -> pd.DataFrame:
    path = PROCESSED_DIR / "analysis_panel.parquet"
    logger.info("Loading %s", path)
    return pd.read_parquet(path)


def prepare_matrices(
    df: pd.DataFrame,
    outcome_col: str,
    treatment_col: str = TREATMENT_PM25,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, list[str], list[str]]:
    available_confounders = [c for c in ALL_CONFOUNDERS if c in df.columns]
    available_moderators = [c for c in HETEROGENEITY_MODERATORS if c in df.columns]
    required = [outcome_col, treatment_col] + available_confounders + available_moderators
    subset = df.dropna(subset=required)
    logger.info("After NaN drop: %d rows for outcome=%s", len(subset), outcome_col)

    Y = subset[outcome_col].values.astype(np.float64)
    T = subset[treatment_col].values.astype(np.float64)
    X = subset[available_moderators].values.astype(np.float64)
    W = subset[available_confounders].values.astype(np.float64)
    return Y, T, X, W, available_moderators, available_confounders


# ---------------------------------------------------------------------------
# LinearDML fitting
# ---------------------------------------------------------------------------
def fit_linear_dml(
    Y: np.ndarray,
    T: np.ndarray,
    X: np.ndarray,
    W: np.ndarray,
) -> LinearDML:
    """Fit LinearDML with GradientBoosting first-stage models."""
    logger.info("Fitting LinearDML (cv=%d) ...", N_FOLDS)

    model_y = GradientBoostingRegressor(
        n_estimators=200, max_depth=5, learning_rate=0.05,
        subsample=0.8, random_state=RANDOM_SEED,
    )
    model_t = GradientBoostingClassifier(
        n_estimators=200, max_depth=5, learning_rate=0.05,
        subsample=0.8, random_state=RANDOM_SEED,
    )

    dml = LinearDML(
        model_y=model_y,
        model_t=model_t,
        discrete_treatment=True,
        cv=N_FOLDS,
        random_state=RANDOM_SEED,
    )
    dml.fit(Y=Y, T=T, X=X, W=W)
    logger.info("LinearDML fit complete.")
    return dml


# ---------------------------------------------------------------------------
# Inference extraction
# ---------------------------------------------------------------------------
def extract_results(
    dml: LinearDML,
    X: np.ndarray,
    x_names: list[str],
) -> dict:
    """Extract ATE, coefficients, and confidence intervals."""
    # ATE
    ate_inf = dml.ate_inference(X=X)
    ate = float(np.asarray(ate_inf.mean_point).ravel()[0])
    ci_l = float(np.asarray(ate_inf.conf_int_mean()[0]).ravel()[0])
    ci_u = float(np.asarray(ate_inf.conf_int_mean()[1]).ravel()[0])
    # Use zstat to compute pvalue (two-sided)
    from scipy import stats as sp_stats
    zstat = float(np.asarray(ate_inf.zstat()).ravel()[0])
    pval = float(2 * sp_stats.norm.sf(abs(zstat)))

    logger.info("ATE = %.4f [%.4f, %.4f], p=%.4e", ate, ci_l, ci_u, pval)

    # Coefficient summary (marginal effect of each moderator on CATE)
    try:
        summary = dml.summary()
        logger.info("DML Summary:\n%s", summary)
    except Exception:
        summary = None

    # Coefficient table from const_marginal_effect
    try:
        coef_inf = dml.const_marginal_ate_inference(X=X)
        coefs = np.asarray(coef_inf.mean_point).ravel()
        coef_ci_l = np.asarray(coef_inf.conf_int_mean()[0]).ravel()
        coef_ci_u = np.asarray(coef_inf.conf_int_mean()[1]).ravel()
        coef_zstat = np.asarray(coef_inf.zstat()).ravel()
        coef_pvals = 2 * sp_stats.norm.sf(np.abs(coef_zstat))
        coef_df = pd.DataFrame({
            "moderator": x_names,
            "coefficient": coefs,
            "ci_lower": coef_ci_l,
            "ci_upper": coef_ci_u,
            "pvalue": coef_pvals,
        })
    except Exception as exc:
        logger.warning("Coefficient extraction failed: %s", exc)
        coef_df = pd.DataFrame()

    return {
        "ate": {"ate": ate, "ci_lower": ci_l, "ci_upper": ci_u, "pvalue": pval},
        "coefficients": coef_df,
    }


# ---------------------------------------------------------------------------
# Save
# ---------------------------------------------------------------------------
def save_results(outcome_name: str, results: dict) -> None:
    base = MODELS_DIR / f"dml_{outcome_name}"
    base.mkdir(parents=True, exist_ok=True)

    # ATE
    ate_path = base / "ate.json"
    ate_path.write_text(json.dumps(results["ate"], indent=2))
    logger.info("ATE saved to %s", ate_path)

    # Coefficients
    if not results["coefficients"].empty:
        coef_path = base / "coefficients.csv"
        results["coefficients"].to_csv(coef_path, index=False)
        logger.info("Coefficients saved to %s", coef_path)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main() -> None:
    t0 = time.time()
    panel = load_panel()

    all_results = {}
    for outcome in ALL_OUTCOMES:
        logger.info("=" * 70)
        logger.info("OUTCOME (DML): %s", outcome)
        logger.info("=" * 70)

        Y, T, X, W, x_names, w_names = prepare_matrices(panel, outcome)

        if len(Y) < 100:
            logger.warning("Insufficient data (%d rows) for %s — skipping.", len(Y), outcome)
            continue

        dml = fit_linear_dml(Y, T, X, W)
        results = extract_results(dml, X, x_names)
        save_results(outcome, results)

        all_results[outcome] = results["ate"]
        logger.info("Outcome '%s' done.\n", outcome)

    # Summary table across all outcomes
    summary_df = pd.DataFrame(all_results).T
    summary_df.index.name = "outcome"
    summary_path = MODELS_DIR / "dml_summary.csv"
    summary_df.to_csv(summary_path)
    logger.info("Summary table saved to %s\n%s", summary_path, summary_df.to_string())

    elapsed = time.time() - t0
    logger.info("All DML models complete in %.1f s.", elapsed)


if __name__ == "__main__":
    main()
