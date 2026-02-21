# Who Suffers Most? Causal Machine Learning Reveals Heterogeneous Health Effects of Air Pollution Across 27 Brazilian State Capitals

> Honest Causal Forests and Double Machine Learning uncover which subpopulations bear disproportionate respiratory burden from PM2.5 and ozone exposure — evidence for targeted public health policy.

---

## Overview

This repository contains the complete analytical pipeline, manuscript, and reproducibility artifacts for a study applying **causal machine learning** to estimate heterogeneous health effects of air pollution across all 27 Brazilian state capitals.

**Key innovation:** First application of Honest Causal Forests (Athey & Wager, 2019) and Double Machine Learning (Chernozhukov et al., 2018) to environmental health epidemiology in Latin America.

## Data Sources

| Source | Period | Granularity | Provider |
|--------|--------|-------------|----------|
| Climate (19 variables) | 2015-2026 | Daily | Open-Meteo |
| Air Quality (7 pollutants) | 2022-2026 | Daily | CAMS/Copernicus |
| Hospitalizations (respiratory + cardiovascular) | 2014-2025 | Daily | SIH/SUS DATASUS |
| Demographics (11 variables) | 1970-2025 | Annual | IBGE SIDRA |
| Vehicle Fleet (9 categories) | 2010-2023 | Annual | SENATRAN |

Data integrated via [Clima360 Brasil](https://github.com/Roverlucas/clima-360-brasil) platform.

## Methods

- **Honest Causal Forests** for heterogeneous treatment effect estimation
- **Double Machine Learning** for robust average treatment effects
- **SHAP values** for causal heterogeneity explanation
- **Policy counterfactuals** under WHO vs CONAMA scenarios
- Full sensitivity battery: placebo tests, Rosenbaum bounds, jackknife, alternative specifications

## Repository Structure

```
├── PROJECT_CHARTER.md           # Project charter and decision log
├── docs/
│   ├── STORYTELLING.md          # Narrative architecture
│   ├── agents/                  # Workflow for each Paper Factory agent (16 agents)
│   ├── gates/                   # Gate review reports
│   ├── decisions/               # Decision log entries
│   └── sessions/                # Session handoffs
├── src/
│   ├── data/                    # Data extraction and processing
│   ├── models/                  # Causal Forest, DML, baseline DLNM
│   ├── analysis/                # EDA, SHAP, policy counterfactuals, sensitivity
│   ├── visualization/           # Publication-ready figures
│   └── utils/                   # Configuration, helpers, logging
├── data/
│   ├── raw/                     # Raw extracted data
│   ├── processed/               # Analysis-ready panel
│   └── interim/                 # Intermediate files
├── outputs/
│   ├── figures/                 # Publication figures (PDF, 300 DPI)
│   ├── tables/                  # Results tables (CSV + LaTeX)
│   └── reports/                 # EDA and analysis reports
├── templates/                   # Document templates
├── tests/                       # Pipeline tests
└── notebooks/                   # Exploratory Jupyter notebooks
```

## Pipeline

```bash
# 1. Set up environment
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# 2. Extract data from Clima360
python src/data/extract.py

# 3. Process and engineer features
python src/data/process.py

# 4. Run causal analysis
python src/models/causal_forest.py
python src/models/dml.py

# 5. Generate SHAP explanations
python src/analysis/shap_analysis.py

# 6. Policy counterfactuals
python src/analysis/policy.py

# 7. Sensitivity analyses
python src/analysis/sensitivity.py

# 8. Generate figures
python src/visualization/maps.py
python src/visualization/forest_plots.py
python src/visualization/shap_plots.py
python src/visualization/policy_plots.py
```

## Target Journals

| Priority | Journal | IF |
|----------|---------|-----|
| A | The Lancet Planetary Health | 24.1 |
| B | Environmental Health Perspectives | 11.0 |
| C | Environment International | 11.8 |

## Authors

- Lucas Rover — UTFPR
- Dra. Yara de Souza Tadano — UTFPR (Supervisor)

## License

- Code: MIT License
- Manuscript and figures: CC-BY 4.0

## Acknowledgments

Data integration powered by [Clima360 Brasil](https://github.com/Roverlucas/clima-360-brasil).
Hospitalization data from [SIH/SUS DATASUS](https://datasus.saude.gov.br).
Managed by Paper Factory Squad (MMOS).
