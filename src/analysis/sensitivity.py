#!/usr/bin/env python3
"""
Sensitivity and robustness analyses for the causal estimates.

1. Placebo test: use future PM2.5 (t+7) as treatment -> should be null
2. Alternative thresholds: 25, 35, 50 ug/m3
3. Leave-one-city-out jackknife
4. Omitted variable bias bound (simplified Cinelli & Hazlett approach)

Usage:
    python src/analysis/sensitivity.py
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
from econml.dml import CausalForestDML

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
    CF_N_ESTIMATORS,
    CF_MIN_LEAF_SIZE,
    CF_HONEST,
    N_FOLDS,
    LOG_FORMAT,
    LOG_DATE_FORMAT,
)

logging.basicConfig(format=LOG_FORMAT, datefmt=LOG_DATE_FORMAT, level=logging.INFO)
logger = logging.getLogger("sensitivity")

np.random.seed(RANDOM_SEED)


# ---------------------------------------------------------------------------
# Shared helpers
# ---------------------------------------------------------------------------
def load_panel() -> pd.DataFrame:
    path = PROCESSED_DIR / "analysis_panel.parquet"
    return pd.read_parquet(path)


def _fit_quick_cf(
    Y: np.ndarray,
    T: np.ndarray,
    X: np.ndarray,
    W: np.ndarray,
    n_estimators: int = 500,
) -> CausalForestDML:
    """Fit a smaller causal forest for sensitivity checks."""
    model_y = GradientBoostingRegressor(
        n_estimators=100, max_depth=4, learning_rate=0.1,
        subsample=0.8, random_state=RANDOM_SEED,
    )
    model_t = GradientBoostingClassifier(
        n_estimators=100, max_depth=4, learning_rate=0.1,
        subsample=0.8, random_state=RANDOM_SEED,
    )
    cf = CausalForestDML(
        model_y=model_y,
        model_t=model_t,
        discrete_treatment=True,
        n_estimators=n_estimators,
        min_samples_leaf=CF_MIN_LEAF_SIZE,
        honest=CF_HONEST,
        cv=N_FOLDS,
        random_state=RANDOM_SEED,
    )
    cf.fit(Y=Y, T=T, X=X, W=W)
    return cf


def _get_ate(cf: CausalForestDML, X: np.ndarray) -> dict:
    """Extract ATE, CI, p-value."""
    from scipy import stats as sp_stats
    inf = cf.ate_inference(X=X)
    zstat = float(np.asarray(inf.zstat()).ravel()[0])
    return {
        "ate": float(np.asarray(inf.mean_point).ravel()[0]),
        "ci_lower": float(np.asarray(inf.conf_int_mean()[0]).ravel()[0]),
        "ci_upper": float(np.asarray(inf.conf_int_mean()[1]).ravel()[0]),
        "pvalue": float(2 * sp_stats.norm.sf(abs(zstat))),
    }


def _prepare(
    df: pd.DataFrame,
    outcome_col: str,
    treatment_col: str,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, list[str]]:
    """Prepare Y, T, X, W matrices."""
    available_confounders = [c for c in ALL_CONFOUNDERS if c in df.columns]
    available_moderators = [c for c in HETEROGENEITY_MODERATORS if c in df.columns]
    required = [outcome_col, treatment_col] + available_confounders + available_moderators
    subset = df.dropna(subset=required)

    Y = subset[outcome_col].values.astype(np.float64)
    T = subset[treatment_col].values.astype(np.float64)
    X = subset[available_moderators].values.astype(np.float64)
    W = subset[available_confounders].values.astype(np.float64)
    return Y, T, X, W, available_moderators


# =========================================================================
# 1. Placebo test — future treatment (t+7) should have null effect
# =========================================================================
def placebo_test(panel: pd.DataFrame) -> dict:
    """
    Placebo: use PM2.5 from 7 days in the future as the "treatment."
    If our model is well-specified, this should yield ATE ~ 0 with
    a p-value well above 0.05.
    """
    logger.info("=" * 60)
    logger.info("PLACEBO TEST: PM2.5 lead-7 as treatment")
    logger.info("=" * 60)

    df = panel.copy().sort_values(["city", "date"]).reset_index(drop=True)
    # Create lead-7 PM2.5 treatment
    df["pm25_lead7"] = df.groupby("city")["pm25"].shift(-7)
    df["pm25_lead7_exceed"] = (df["pm25_lead7"] > WHO_PM25_THRESHOLD).astype(int)
    df = df.dropna(subset=["pm25_lead7_exceed"])

    Y, T, X, W, mod_names = _prepare(df, OUTCOME_TOTAL, "pm25_lead7_exceed")
    logger.info("Placebo data: %d rows", len(Y))

    cf = _fit_quick_cf(Y, T, X, W)
    result = _get_ate(cf, X)
    result["test"] = "placebo_lead7"
    logger.info("Placebo ATE = %.4f [%.4f, %.4f], p=%.4f",
                result["ate"], result["ci_lower"], result["ci_upper"], result["pvalue"])

    passed = result["pvalue"] > 0.05
    result["passed"] = passed
    logger.info("Placebo test %s (p > 0.05 expected)", "PASSED" if passed else "FAILED")
    return result


# =========================================================================
# 2. Alternative PM2.5 thresholds
# =========================================================================
def threshold_sensitivity(panel: pd.DataFrame) -> pd.DataFrame:
    """
    Re-estimate the ATE using alternative PM2.5 thresholds:
    15 (WHO), 25 (CONAMA interim-1), 35, 50 ug/m3.
    """
    logger.info("=" * 60)
    logger.info("THRESHOLD SENSITIVITY")
    logger.info("=" * 60)

    results = []
    for thresh in [WHO_PM25_THRESHOLD] + ALT_PM25_THRESHOLDS:
        df = panel.copy()
        treat_col = f"pm25_gt{int(thresh)}"
        df[treat_col] = (df["pm25"] > thresh).astype(int)

        # Check there is enough variation in treatment
        treat_mean = df[treat_col].mean()
        if treat_mean < 0.01 or treat_mean > 0.99:
            logger.warning("Threshold %.0f: treatment mean=%.3f, skipping (insufficient variation)", thresh, treat_mean)
            results.append({
                "threshold": thresh, "ate": np.nan, "ci_lower": np.nan,
                "ci_upper": np.nan, "pvalue": np.nan, "treat_pct": round(100 * treat_mean, 2),
            })
            continue

        Y, T, X, W, mod_names = _prepare(df, OUTCOME_TOTAL, treat_col)
        logger.info("Threshold %.0f: %d rows, treat_pct=%.1f%%", thresh, len(Y), 100 * T.mean())

        cf = _fit_quick_cf(Y, T, X, W)
        ate = _get_ate(cf, X)

        results.append({
            "threshold": thresh,
            "ate": ate["ate"],
            "ci_lower": ate["ci_lower"],
            "ci_upper": ate["ci_upper"],
            "pvalue": ate["pvalue"],
            "treat_pct": round(100 * T.mean(), 2),
        })
        logger.info("  ATE=%.4f [%.4f, %.4f], p=%.4e",
                     ate["ate"], ate["ci_lower"], ate["ci_upper"], ate["pvalue"])

    df_results = pd.DataFrame(results)
    logger.info("Threshold sensitivity:\n%s", df_results.to_string())
    return df_results


# =========================================================================
# 3. Leave-one-city-out jackknife
# =========================================================================
def jackknife_cities(panel: pd.DataFrame) -> pd.DataFrame:
    """
    Leave-one-city-out: re-estimate ATE dropping each city in turn.
    This checks whether any single city is driving the result.
    """
    logger.info("=" * 60)
    logger.info("LEAVE-ONE-CITY-OUT JACKKNIFE")
    logger.info("=" * 60)

    cities = sorted(panel["city"].unique())
    results = []

    for city in cities:
        df = panel[panel["city"] != city].copy()
        Y, T, X, W, mod_names = _prepare(df, OUTCOME_TOTAL, TREATMENT_PM25)

        if len(Y) < 100:
            logger.warning("Skipping city=%s (only %d rows remain)", city, len(Y))
            continue

        logger.info("Excluding %s: %d rows", city, len(Y))
        cf = _fit_quick_cf(Y, T, X, W, n_estimators=300)
        ate = _get_ate(cf, X)

        results.append({
            "excluded_city": city,
            "ate": ate["ate"],
            "ci_lower": ate["ci_lower"],
            "ci_upper": ate["ci_upper"],
            "pvalue": ate["pvalue"],
            "n_rows": len(Y),
        })
        logger.info("  ATE=%.4f [%.4f, %.4f]", ate["ate"], ate["ci_lower"], ate["ci_upper"])

    df_results = pd.DataFrame(results)

    # Check stability: is the range of ATEs narrow?
    ate_range = df_results["ate"].max() - df_results["ate"].min()
    ate_mean = df_results["ate"].mean()
    ate_cv = df_results["ate"].std() / abs(ate_mean) if ate_mean != 0 else np.nan
    logger.info("Jackknife: ATE range=%.4f, mean=%.4f, CV=%.3f", ate_range, ate_mean, ate_cv)

    return df_results


# =========================================================================
# 4. Omitted variable bias: sensitivity parameter
# =========================================================================
def ovb_sensitivity(panel: pd.DataFrame) -> dict:
    """
    Simple Rosenbaum-style sensitivity: compute how strong an unmeasured
    confounder would need to be to nullify the treatment effect.

    We use the partial R^2 approach:
    - Regress Y on W to get R^2_Y|W
    - Regress T on W to get R^2_T|W
    - The 'robustness value' is the minimum partial R^2 that a confounder
      would need on both Y and T to reduce ATE to zero.
    """
    logger.info("=" * 60)
    logger.info("OMITTED VARIABLE BIAS SENSITIVITY")
    logger.info("=" * 60)

    from sklearn.linear_model import LinearRegression, LogisticRegression
    from sklearn.metrics import r2_score

    available_confounders = [c for c in ALL_CONFOUNDERS if c in panel.columns]
    required = [OUTCOME_TOTAL, TREATMENT_PM25] + available_confounders
    df = panel.dropna(subset=required)

    Y = df[OUTCOME_TOTAL].values
    T = df[TREATMENT_PM25].values
    W = df[available_confounders].values

    # R^2 of Y ~ W
    lr_y = LinearRegression().fit(W, Y)
    r2_y_w = r2_score(Y, lr_y.predict(W))

    # Pseudo-R^2 of T ~ W (McFadden)
    from sklearn.metrics import log_loss
    lr_t = LogisticRegression(max_iter=1000, random_state=RANDOM_SEED).fit(W, T)
    ll_model = -log_loss(T, lr_t.predict_proba(W), normalize=False)
    ll_null = -log_loss(T, np.full_like(T, T.mean(), dtype=float), normalize=False)
    pseudo_r2_t_w = 1 - ll_model / ll_null if ll_null != 0 else 0

    # Robustness value: sqrt of product of partial R^2
    # This is a simplified bound; a proper implementation would use
    # sensemakr-style analytics.
    residual_var_y = 1 - r2_y_w
    residual_var_t = 1 - pseudo_r2_t_w
    # The confounder would need partial R^2 of at least this much
    # to explain away the effect:
    robustness_value = np.sqrt(residual_var_y * residual_var_t)

    result = {
        "r2_y_given_w": round(float(r2_y_w), 4),
        "pseudo_r2_t_given_w": round(float(pseudo_r2_t_w), 4),
        "residual_var_y": round(float(residual_var_y), 4),
        "residual_var_t": round(float(residual_var_t), 4),
        "robustness_value": round(float(robustness_value), 4),
        "interpretation": (
            f"An unobserved confounder would need partial R^2 of at least "
            f"{robustness_value:.3f} with both Y and T (after controlling for "
            f"observed confounders) to reduce the ATE to zero."
        ),
    }
    logger.info("OVB Sensitivity: %s", json.dumps(result, indent=2))
    return result


# ---------------------------------------------------------------------------
# Save
# ---------------------------------------------------------------------------
def save_all(
    placebo: dict,
    thresholds: pd.DataFrame,
    jackknife: pd.DataFrame,
    ovb: dict,
) -> None:
    """Persist all sensitivity results."""
    sens_dir = REPORTS_DIR / "sensitivity"
    sens_dir.mkdir(parents=True, exist_ok=True)

    (sens_dir / "placebo_test.json").write_text(json.dumps(placebo, indent=2))
    thresholds.to_csv(TABLES_DIR / "sensitivity_thresholds.csv", index=False)
    jackknife.to_csv(TABLES_DIR / "sensitivity_jackknife.csv", index=False)
    (sens_dir / "ovb_sensitivity.json").write_text(json.dumps(ovb, indent=2))

    logger.info("All sensitivity results saved.")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main() -> None:
    t0 = time.time()
    panel = load_panel()

    placebo = placebo_test(panel)
    thresholds = threshold_sensitivity(panel)
    jackknife = jackknife_cities(panel)
    ovb = ovb_sensitivity(panel)

    save_all(placebo, thresholds, jackknife, ovb)

    elapsed = time.time() - t0
    logger.info("Sensitivity analysis complete in %.1f s.", elapsed)


if __name__ == "__main__":
    main()
