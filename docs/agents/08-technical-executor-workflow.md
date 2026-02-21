# @technical-executor — Workflow & Responsibilities

> **Role:** Execute pipelines, models, experiments, and reproductions
> **Active:** Phase 3 (primary)
> **Tier:** 3 — Technical, Data & Figures

---

## Mission

Build and execute the complete analytical pipeline: from raw data extraction to trained causal forests, DML estimates, SHAP explanations, and policy counterfactuals. Every step must be reproducible, documented, and version-controlled.

---

## Technical Stack

| Component | Tool | Version |
|-----------|------|---------|
| Language | Python | 3.11+ |
| Causal Forests | `econml` (Microsoft) | latest |
| Alternative CF | `grf` via `rpy2` or R script | latest |
| Double ML | `econml.dml.DML` | latest |
| SHAP | `shap` | latest |
| Data wrangling | `pandas`, `polars` | latest |
| ML first-stage | `xgboost`, `lightgbm` | latest |
| Visualization | `matplotlib`, `seaborn`, `plotly` | latest |
| Geospatial | `geopandas`, `folium` | latest |
| Statistics | `scipy`, `statsmodels` | latest |
| Database | `supabase-py` or direct PostgreSQL | latest |
| Environment | `uv` / `venv` | PEP 668 compliant |
| Notebooks | Jupyter | for exploration |
| Scripts | `.py` modules | for production pipeline |

---

## Pipeline Architecture

```
Step 1: DATA EXTRACTION
  └── Extract from Clima360 Supabase (5 tables)
  └── Output: data/raw/*.parquet

Step 2: DATA PROCESSING
  ├── Merge by (city, date)
  ├── Compute derived features (DTR, lags, moving averages, Fourier, fleet/capita)
  ├── Quality filters (completeness ≥80%)
  ├── Handle missing values (interpolation for weather, drop for health)
  └── Output: data/processed/analysis_panel.parquet

Step 3: EXPLORATORY ANALYSIS
  ├── Descriptive statistics by city and overall
  ├── Treatment distribution (% days above WHO threshold per city)
  ├── Positivity check (exclude cities with <5% or >95% treatment)
  ├── Confounder balance assessment
  └── Output: outputs/reports/eda_report.html

Step 4: CAUSAL FOREST ESTIMATION
  ├── Define Y (outcome), T (treatment), X (heterogeneity moderators), W (confounders)
  ├── Train Honest Causal Forest (econml.CausalForestDML)
  ├── Estimate CATE for each observation
  ├── CLAN analysis (most/least affected groups)
  ├── Best Linear Projection (BLP) on moderators
  ├── Calibration test for heterogeneity
  └── Output: outputs/models/causal_forest_*.pkl

Step 5: DOUBLE MACHINE LEARNING
  ├── DML with XGBoost first-stage models
  ├── 5-fold cross-fitting
  ├── ATE and CATE estimates
  ├── Compare with Causal Forest estimates
  └── Output: outputs/models/dml_*.pkl

Step 6: SHAP ANALYSIS
  ├── SHAP values on Causal Forest heterogeneity
  ├── Global feature importance (beeswarm)
  ├── Local explanations for extreme CATE cities
  ├── Interaction effects (DTR × PM2.5)
  └── Output: outputs/figures/shap_*.pdf

Step 7: POLICY COUNTERFACTUALS
  ├── Prevented fraction: WHO (15 µg/m³) vs CONAMA (current)
  ├── Stratify by vulnerability group (top/bottom CATE tercile)
  ├── Cost estimation using SIH/SUS unit costs
  └── Output: outputs/tables/policy_counterfactuals.csv

Step 8: SENSITIVITY ANALYSIS
  ├── Placebo test (future treatment)
  ├── Alternative thresholds (25, 35, 50 µg/m³)
  ├── Leave-one-city-out jackknife
  ├── Continuous treatment (generalized CF)
  ├── Comparison with DLNM baseline
  └── Output: outputs/tables/sensitivity_*.csv

Step 9: REPRODUCIBILITY PACKAGE
  ├── requirements.txt / pyproject.toml
  ├── Makefile or dvc pipeline
  ├── README with step-by-step instructions
  ├── Seed setting for all random operations
  └── Output: repo root
```

---

## File Structure

```
src/
├── data/
│   ├── extract.py          # Supabase extraction
│   ├── process.py          # Merge, clean, feature engineering
│   └── quality.py          # Quality checks and filters
├── models/
│   ├── causal_forest.py    # Honest Causal Forest pipeline
│   ├── dml.py              # Double Machine Learning pipeline
│   └── baseline_dlnm.py    # DLNM comparison (R via rpy2)
├── analysis/
│   ├── eda.py              # Exploratory data analysis
│   ├── shap_analysis.py    # SHAP for causal heterogeneity
│   ├── policy.py           # Policy counterfactuals
│   └── sensitivity.py      # All robustness tests
├── visualization/
│   ├── maps.py             # Geospatial CATE maps
│   ├── forest_plots.py     # Forest plots by subgroup
│   ├── shap_plots.py       # SHAP beeswarm and interaction
│   └── policy_plots.py     # Counterfactual bar charts
└── utils/
    ├── config.py           # Constants, paths, parameters
    ├── helpers.py           # Shared utilities
    └── logger.py           # Logging configuration
```

---

## Computational Requirements

| Step | Est. Time | Resources |
|------|-----------|-----------|
| Data extraction | 5 min | Network (Supabase API) |
| Data processing | 10 min | Local (pandas) |
| Causal Forest (27 cities × 6 outcomes) | 2-4 hours | 24GB RAM, M4 chip |
| DML (27 cities × 6 outcomes) | 1-2 hours | Same |
| SHAP | 30-60 min | Same |
| Sensitivity battery | 4-8 hours | Same |
| **Total** | **~12-16 hours** | Apple M4, 24GB |

---

## Tasks

- [ ] Set up Python environment with all dependencies
- [ ] Implement data extraction from Clima360 Supabase
- [ ] Implement data processing + feature engineering
- [ ] Implement Causal Forest pipeline
- [ ] Implement DML pipeline
- [ ] Implement SHAP analysis
- [ ] Implement policy counterfactuals
- [ ] Implement full sensitivity battery
- [ ] Run complete pipeline
- [ ] Generate all outputs for @data-specialist and @visual-impact-specialist
- [ ] Package reproducibility artifacts

---

*@technical-executor v1.0 — 2026-02-21*
