#!/usr/bin/env python3
"""
Policy counterfactual analysis.

Estimates the number of respiratory hospitalizations that would be
prevented if PM2.5 never exceeded the WHO 24-hour guideline (15 ug/m3),
stratified by CATE vulnerability quartiles.

Also computes financial savings using the ``total_cost`` field from
DATASUS hospitalization records.

Usage:
    python src/analysis/policy.py
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

# ---------------------------------------------------------------------------
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from src.utils.config import (
    PROCESSED_DIR,
    MODELS_DIR,
    TABLES_DIR,
    REPORTS_DIR,
    RANDOM_SEED,
    ALL_CONFOUNDERS,
    HETEROGENEITY_MODERATORS,
    TREATMENT_PM25,
    OUTCOME_TOTAL,
    WHO_PM25_THRESHOLD,
    ALT_PM25_THRESHOLDS,
    BOOTSTRAP_N,
    LOG_FORMAT,
    LOG_DATE_FORMAT,
)

logging.basicConfig(format=LOG_FORMAT, datefmt=LOG_DATE_FORMAT, level=logging.INFO)
logger = logging.getLogger("policy")

np.random.seed(RANDOM_SEED)


# ---------------------------------------------------------------------------
# Load model and data
# ---------------------------------------------------------------------------
def load_model_and_panel() -> tuple:
    """Load the fitted CausalForestDML and the full panel."""
    model_path = MODELS_DIR / f"cf_{OUTCOME_TOTAL}" / "model.pkl"
    logger.info("Loading model from %s", model_path)
    with open(model_path, "rb") as f:
        cf = pickle.load(f)

    panel = pd.read_parquet(PROCESSED_DIR / "analysis_panel.parquet")

    # Build analysis subset
    available_moderators = [c for c in HETEROGENEITY_MODERATORS if c in panel.columns]
    available_confounders = [c for c in ALL_CONFOUNDERS if c in panel.columns]
    required = [OUTCOME_TOTAL, TREATMENT_PM25] + available_confounders + available_moderators
    subset = panel.dropna(subset=required).copy()

    X = subset[available_moderators].values.astype(np.float64)
    return cf, subset, X, available_moderators


# ---------------------------------------------------------------------------
# Prevented fraction analysis
# ---------------------------------------------------------------------------
def prevented_fraction(
    cf,
    subset: pd.DataFrame,
    X: np.ndarray,
) -> pd.DataFrame:
    """
    Estimate prevented hospitalizations under WHO compliance.

    For each city-day where PM2.5 > 15 (treatment=1), the CATE gives
    the causal excess admissions attributable to the exceedance.
    Summing these CATEs gives the total preventable admissions.
    """
    cate = cf.effect(X).ravel()
    treated = subset[TREATMENT_PM25].values == 1

    # Prevented admissions = sum of CATEs on treated days
    prevented = cate[treated].sum()
    total_admissions = subset[OUTCOME_TOTAL].values.sum()
    prevented_frac = prevented / total_admissions if total_admissions > 0 else 0

    logger.info(
        "Prevented fraction: %.0f / %.0f = %.2f%% of admissions",
        prevented, total_admissions, 100 * prevented_frac,
    )

    # Per-city breakdown
    subset_c = subset.copy()
    subset_c["cate"] = cate
    subset_c["treated"] = treated.astype(int)
    subset_c["prevented"] = subset_c["cate"] * subset_c["treated"]

    city_summary = (
        subset_c
        .groupby("city")
        .agg(
            total_admissions=(OUTCOME_TOTAL, "sum"),
            treated_days=("treated", "sum"),
            prevented_admissions=("prevented", "sum"),
            mean_cate=("cate", "mean"),
        )
        .reset_index()
    )
    city_summary["prevented_pct"] = (
        100 * city_summary["prevented_admissions"] / city_summary["total_admissions"]
    )
    city_summary = city_summary.sort_values("prevented_pct", ascending=False)
    logger.info("Per-city prevented fractions:\n%s", city_summary.to_string())

    return city_summary


# ---------------------------------------------------------------------------
# Stratified by CATE vulnerability
# ---------------------------------------------------------------------------
def stratified_policy(
    cf,
    subset: pd.DataFrame,
    X: np.ndarray,
) -> pd.DataFrame:
    """
    Stratify policy impact by CATE vulnerability quartile.
    """
    cate = cf.effect(X).ravel()
    treated = subset[TREATMENT_PM25].values == 1

    df = subset.copy()
    df["cate"] = cate
    df["treated"] = treated.astype(int)
    df["prevented"] = df["cate"] * df["treated"]

    # Vulnerability quartiles
    df["vuln_quartile"] = pd.qcut(
        df["cate"], 4,
        labels=["Q1 (least vulnerable)", "Q2", "Q3", "Q4 (most vulnerable)"],
    )

    strat = (
        df
        .groupby("vuln_quartile", observed=True)
        .agg(
            n_obs=("cate", "size"),
            total_admissions=(OUTCOME_TOTAL, "sum"),
            treated_days=("treated", "sum"),
            prevented_admissions=("prevented", "sum"),
            mean_cate=("cate", "mean"),
        )
        .reset_index()
    )
    strat["prevented_pct"] = (
        100 * strat["prevented_admissions"] / strat["total_admissions"]
    )
    logger.info("Stratified policy:\n%s", strat.to_string())
    return strat


# ---------------------------------------------------------------------------
# Cost estimation
# ---------------------------------------------------------------------------
def cost_estimation(
    cf,
    subset: pd.DataFrame,
    X: np.ndarray,
) -> dict:
    """
    Estimate financial savings from prevented hospitalizations.

    Uses average cost per admission from the health data and the
    prevented fraction from the causal model.
    """
    cate = cf.effect(X).ravel()
    treated = subset[TREATMENT_PM25].values == 1

    total_cost = subset["total_cost"].sum()
    total_admissions = subset[OUTCOME_TOTAL].sum()
    avg_cost_per_admission = total_cost / total_admissions if total_admissions > 0 else 0

    prevented_admissions = cate[treated].sum()
    saved_cost = prevented_admissions * avg_cost_per_admission

    result = {
        "total_cost_brl": float(total_cost),
        "total_admissions": int(total_admissions),
        "avg_cost_per_admission_brl": float(round(avg_cost_per_admission, 2)),
        "prevented_admissions": float(round(prevented_admissions, 1)),
        "saved_cost_brl": float(round(saved_cost, 2)),
        "saved_cost_pct": float(round(100 * saved_cost / total_cost, 2)) if total_cost > 0 else 0,
    }
    logger.info("Cost estimation: %s", json.dumps(result, indent=2))
    return result


# ---------------------------------------------------------------------------
# Bootstrap CI for prevented fraction
# ---------------------------------------------------------------------------
def bootstrap_prevented_fraction(
    cf,
    subset: pd.DataFrame,
    X: np.ndarray,
    n_bootstrap: int = BOOTSTRAP_N,
) -> dict:
    """Bootstrap 95% CI for the prevented fraction."""
    cate = cf.effect(X).ravel()
    treated = subset[TREATMENT_PM25].values == 1
    admissions = subset[OUTCOME_TOTAL].values

    n = len(cate)
    prevented_fracs = []

    for _ in range(n_bootstrap):
        idx = np.random.choice(n, n, replace=True)
        prev = cate[idx][treated[idx]].sum()
        total = admissions[idx].sum()
        if total > 0:
            prevented_fracs.append(prev / total)

    prevented_fracs = np.array(prevented_fracs)
    ci_lower = float(np.percentile(prevented_fracs, 2.5))
    ci_upper = float(np.percentile(prevented_fracs, 97.5))
    mean_frac = float(np.mean(prevented_fracs))

    result = {
        "mean_prevented_pct": round(100 * mean_frac, 2),
        "ci_lower_pct": round(100 * ci_lower, 2),
        "ci_upper_pct": round(100 * ci_upper, 2),
        "n_bootstrap": n_bootstrap,
    }
    logger.info("Bootstrap prevented fraction: %s", result)
    return result


# ---------------------------------------------------------------------------
# Alternative threshold analysis
# ---------------------------------------------------------------------------
def alternative_thresholds(
    cf,
    subset: pd.DataFrame,
    X: np.ndarray,
) -> pd.DataFrame:
    """
    Estimate prevented fraction under alternative PM2.5 thresholds.
    """
    cate = cf.effect(X).ravel()
    total_admissions = subset[OUTCOME_TOTAL].sum()
    results = []

    for thresh in [WHO_PM25_THRESHOLD] + ALT_PM25_THRESHOLDS:
        treated = (subset["pm25"].values > thresh).astype(int)
        prevented = cate[treated == 1].sum()
        n_exceed = treated.sum()
        results.append({
            "threshold_ugm3": thresh,
            "exceed_days": int(n_exceed),
            "exceed_pct": float(round(100 * n_exceed / len(subset), 2)),
            "prevented_admissions": float(round(prevented, 1)),
            "prevented_pct": float(round(100 * prevented / total_admissions, 2)) if total_admissions > 0 else 0,
        })

    df = pd.DataFrame(results)
    logger.info("Alternative thresholds:\n%s", df.to_string())
    return df


# ---------------------------------------------------------------------------
# Save
# ---------------------------------------------------------------------------
def save_all(
    city_summary: pd.DataFrame,
    stratified: pd.DataFrame,
    costs: dict,
    bootstrap: dict,
    thresholds: pd.DataFrame,
) -> None:
    """Persist all policy analysis results."""
    # City-level prevented fractions
    city_summary.to_csv(TABLES_DIR / "policy_city_prevented.csv", index=False)

    # Stratified by vulnerability
    stratified.to_csv(TABLES_DIR / "policy_stratified.csv", index=False)

    # Cost estimation
    cost_path = REPORTS_DIR / "cost_estimation.json"
    cost_path.write_text(json.dumps(costs, indent=2))

    # Bootstrap
    boot_path = REPORTS_DIR / "bootstrap_prevented.json"
    boot_path.write_text(json.dumps(bootstrap, indent=2))

    # Alternative thresholds
    thresholds.to_csv(TABLES_DIR / "policy_thresholds.csv", index=False)

    logger.info("All policy results saved.")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main() -> None:
    t0 = time.time()

    cf, subset, X, mod_names = load_model_and_panel()

    city_summary = prevented_fraction(cf, subset, X)
    stratified = stratified_policy(cf, subset, X)
    costs = cost_estimation(cf, subset, X)
    bootstrap = bootstrap_prevented_fraction(cf, subset, X)
    thresholds = alternative_thresholds(cf, subset, X)

    save_all(city_summary, stratified, costs, bootstrap, thresholds)

    elapsed = time.time() - t0
    logger.info("Policy analysis complete in %.1f s.", elapsed)


if __name__ == "__main__":
    main()
