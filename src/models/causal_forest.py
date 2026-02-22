#!/usr/bin/env python3
"""
Causal Forest estimation using econml.dml.CausalForestDML.

Estimates the Conditional Average Treatment Effect (CATE) of PM2.5
exceedance on respiratory hospitalizations, with heterogeneity across
subpopulations defined by age, fleet density, population density, etc.

Produces:
    - ATE with 95% CI
    - CATE estimates for every observation
    - CLAN analysis (quartile-based classification)
    - Best Linear Projection of CATE on moderators
    - Model summaries saved to outputs/models/

Usage:
    python src/models/causal_forest.py
"""

from __future__ import annotations

import json
import logging
import pickle
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor, GradientBoostingClassifier
from econml.dml import CausalForestDML

# ---------------------------------------------------------------------------
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from src.utils.config import (
    PROCESSED_DIR,
    MODELS_DIR,
    TABLES_DIR,
    RANDOM_SEED,
    ALL_CONFOUNDERS,
    HETEROGENEITY_MODERATORS,
    TREATMENT_PM25,
    ALL_OUTCOMES,
    CF_N_ESTIMATORS,
    CF_MIN_LEAF_SIZE,
    CF_HONEST,
    N_FOLDS,
    LOG_FORMAT,
    LOG_DATE_FORMAT,
)

logging.basicConfig(format=LOG_FORMAT, datefmt=LOG_DATE_FORMAT, level=logging.INFO)
logger = logging.getLogger("causal_forest")

np.random.seed(RANDOM_SEED)


# ---------------------------------------------------------------------------
# Data preparation
# ---------------------------------------------------------------------------
def load_panel() -> pd.DataFrame:
    """Load the processed analysis panel."""
    path = PROCESSED_DIR / "analysis_panel.parquet"
    logger.info("Loading %s", path)
    df = pd.read_parquet(path)
    logger.info("Panel: %d rows x %d cols", len(df), len(df.columns))
    return df


def prepare_matrices(
    df: pd.DataFrame,
    outcome_col: str,
    treatment_col: str = TREATMENT_PM25,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, list[str], list[str]]:
    """
    Build Y, T, X, W matrices from the panel.

    Returns
    -------
    Y : outcome array (n,)
    T : treatment array (n,)
    X : heterogeneity moderators (n, p_x)
    W : confounders (n, p_w)
    x_names : moderator column names
    w_names : confounder column names
    """
    # Determine available columns
    available_confounders = [c for c in ALL_CONFOUNDERS if c in df.columns]
    available_moderators = [c for c in HETEROGENEITY_MODERATORS if c in df.columns]

    # Drop rows with NaN in any required column
    required = [outcome_col, treatment_col] + available_confounders + available_moderators
    subset = df.dropna(subset=required)
    logger.info("After dropping NaN in required columns: %d -> %d rows",
                len(df), len(subset))

    Y = subset[outcome_col].values.astype(np.float64)
    T = subset[treatment_col].values.astype(np.float64)
    X = subset[available_moderators].values.astype(np.float64)
    W = subset[available_confounders].values.astype(np.float64)

    return Y, T, X, W, available_moderators, available_confounders


# ---------------------------------------------------------------------------
# Causal Forest fitting
# ---------------------------------------------------------------------------
def fit_causal_forest(
    Y: np.ndarray,
    T: np.ndarray,
    X: np.ndarray,
    W: np.ndarray,
) -> CausalForestDML:
    """
    Fit an Honest Causal Forest via CausalForestDML.

    Uses GradientBoosting for both the outcome and treatment first-stage
    models (nuisance estimation), with 5-fold cross-fitting.
    """
    logger.info("Fitting CausalForestDML (n_estimators=%d, min_leaf=%d, honest=%s) ...",
                CF_N_ESTIMATORS, CF_MIN_LEAF_SIZE, CF_HONEST)

    model_y = GradientBoostingRegressor(
        n_estimators=200, max_depth=5, learning_rate=0.05,
        subsample=0.8, random_state=RANDOM_SEED,
    )
    model_t = GradientBoostingClassifier(
        n_estimators=200, max_depth=5, learning_rate=0.05,
        subsample=0.8, random_state=RANDOM_SEED,
    )

    cf = CausalForestDML(
        model_y=model_y,
        model_t=model_t,
        n_estimators=CF_N_ESTIMATORS,
        min_samples_leaf=CF_MIN_LEAF_SIZE,
        max_depth=None,
        honest=CF_HONEST,
        cv=N_FOLDS,
        random_state=RANDOM_SEED,
    )
    cf.fit(Y=Y, T=T, X=X, W=W)
    logger.info("CausalForestDML fit complete.")
    return cf


# ---------------------------------------------------------------------------
# Inference extraction
# ---------------------------------------------------------------------------
def extract_ate(cf: CausalForestDML, X: np.ndarray) -> dict:
    """Extract ATE and 95% confidence interval."""
    ate_inference = cf.ate_inference(X=X)
    ate = float(ate_inference.mean_point)
    ci_lower = float(ate_inference.conf_int_mean()[0][0])
    ci_upper = float(ate_inference.conf_int_mean()[1][0])
    pval = float(ate_inference.pvalue_mean()[0])
    logger.info("ATE = %.4f [%.4f, %.4f], p=%.4e", ate, ci_lower, ci_upper, pval)
    return {
        "ate": ate,
        "ci_lower": ci_lower,
        "ci_upper": ci_upper,
        "pvalue": pval,
    }


def extract_cate(
    cf: CausalForestDML,
    X: np.ndarray,
    x_names: list[str],
) -> pd.DataFrame:
    """Extract CATE for every observation."""
    cate = cf.effect(X=X)
    cate_inf = cf.effect_inference(X=X)
    ci_lower = cate_inf.conf_int()[0].ravel()
    ci_upper = cate_inf.conf_int()[1].ravel()

    df_cate = pd.DataFrame(X, columns=x_names)
    df_cate["cate"] = cate.ravel()
    df_cate["cate_ci_lower"] = ci_lower
    df_cate["cate_ci_upper"] = ci_upper
    logger.info("CATE: mean=%.4f, std=%.4f, range=[%.4f, %.4f]",
                df_cate["cate"].mean(), df_cate["cate"].std(),
                df_cate["cate"].min(), df_cate["cate"].max())
    return df_cate


def clan_analysis(df_cate: pd.DataFrame) -> pd.DataFrame:
    """
    CLAN: Classification Analysis of CATEs.
    Divide CATE into quartiles and compute mean moderator values per group.
    """
    df = df_cate.copy()
    df["cate_quartile"] = pd.qcut(df["cate"], 4, labels=["Q1 (lowest)", "Q2", "Q3", "Q4 (highest)"])
    moderator_cols = [c for c in df.columns if c not in
                      ["cate", "cate_ci_lower", "cate_ci_upper", "cate_quartile"]]
    clan = df.groupby("cate_quartile", observed=True)[moderator_cols + ["cate"]].mean()
    logger.info("CLAN analysis:\n%s", clan.to_string())
    return clan


def best_linear_projection(
    cf: CausalForestDML,
    X: np.ndarray,
    x_names: list[str],
) -> pd.DataFrame:
    """
    Best Linear Projection of CATE on moderators.
    Shows which moderators explain the most heterogeneity.
    """
    try:
        blp = cf.const_marginal_ate_inference(X=X)
        coefs = blp.mean_point.ravel()
        ci_l = blp.conf_int_mean()[0].ravel()
        ci_u = blp.conf_int_mean()[1].ravel()
        pvals = blp.pvalue_mean().ravel()

        blp_df = pd.DataFrame({
            "moderator": x_names,
            "coefficient": coefs,
            "ci_lower": ci_l,
            "ci_upper": ci_u,
            "pvalue": pvals,
        })
        blp_df = blp_df.sort_values("pvalue").reset_index(drop=True)
        logger.info("Best Linear Projection:\n%s", blp_df.to_string())
        return blp_df
    except Exception as exc:
        logger.warning("BLP extraction failed: %s", exc)
        return pd.DataFrame()


# ---------------------------------------------------------------------------
# Save results
# ---------------------------------------------------------------------------
def save_results(
    outcome_name: str,
    cf_model: CausalForestDML,
    ate_result: dict,
    df_cate: pd.DataFrame,
    clan_df: pd.DataFrame,
    blp_df: pd.DataFrame,
) -> None:
    """Persist all results to disk."""
    base = MODELS_DIR / f"cf_{outcome_name}"
    base.mkdir(parents=True, exist_ok=True)

    # ATE
    ate_path = base / "ate.json"
    ate_path.write_text(json.dumps(ate_result, indent=2))
    logger.info("ATE saved to %s", ate_path)

    # CATE
    cate_path = base / "cate.parquet"
    df_cate.to_parquet(cate_path, index=False)
    logger.info("CATE saved to %s", cate_path)

    # CLAN
    clan_path = base / "clan.csv"
    clan_df.to_csv(clan_path)
    logger.info("CLAN saved to %s", clan_path)

    # BLP
    if not blp_df.empty:
        blp_path = base / "blp.csv"
        blp_df.to_csv(blp_path, index=False)
        logger.info("BLP saved to %s", blp_path)

    # Pickle the model (for SHAP later)
    model_path = base / "model.pkl"
    with open(model_path, "wb") as f:
        pickle.dump(cf_model, f, protocol=pickle.HIGHEST_PROTOCOL)
    logger.info("Model saved to %s", model_path)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main() -> None:
    t0 = time.time()
    panel = load_panel()

    # Run for each outcome
    for outcome in ALL_OUTCOMES:
        logger.info("=" * 70)
        logger.info("OUTCOME: %s", outcome)
        logger.info("=" * 70)

        Y, T, X, W, x_names, w_names = prepare_matrices(panel, outcome)

        if len(Y) < 100:
            logger.warning("Insufficient data (%d rows) for %s — skipping.", len(Y), outcome)
            continue

        cf = fit_causal_forest(Y, T, X, W)
        ate = extract_ate(cf, X)
        df_cate = extract_cate(cf, X, x_names)
        clan_df = clan_analysis(df_cate)
        blp_df = best_linear_projection(cf, X, x_names)

        save_results(outcome, cf, ate, df_cate, clan_df, blp_df)
        logger.info("Outcome '%s' done.\n", outcome)

    elapsed = time.time() - t0
    logger.info("All causal forest models complete in %.1f s.", elapsed)


if __name__ == "__main__":
    main()
