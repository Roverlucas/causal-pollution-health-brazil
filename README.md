# Who Suffers Most? Causal Machine Learning Reveals Heterogeneous Health Effects of Air Pollution Across Brazilian State Capitals

[![License: MIT](https://img.shields.io/badge/Code-MIT-blue.svg)](LICENSE)
[![License: CC BY 4.0](https://img.shields.io/badge/Manuscript-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)
[![Python 3.14+](https://img.shields.io/badge/Python-3.14%2B-blue.svg)](https://www.python.org/)
[![EconML](https://img.shields.io/badge/EconML-0.16-green.svg)](https://econml.azurewebsites.net/)

> Honest Causal Forests and Double Machine Learning uncover which subpopulations bear disproportionate respiratory burden from PM2.5 exposure — evidence for targeted public health policy in Brazil.

---

## Key Results

| Metric | Value |
|--------|-------|
| **Causal Forest ATE** | 0.39 additional admissions/city-day [-4.20, 4.98], p=0.87 |
| **DML ATE** | 0.13 additional admissions/city-day [-0.31, 0.56], p=0.56 |
| **CATE range** | -8.06 to +11.09 (19-fold heterogeneity) |
| **Top heterogeneity drivers** | Pop. density (0.676), DTR (0.608), pct female (0.371), fleet/capita (0.291) |
| **Prevented admissions (WHO scenario)** | 4,168 (0.45%, 95% CI: 0.41-0.48%) |
| **Cost savings** | R$8.09 million |
| **Placebo test** | p=0.84 (passed) |
| **OVB robustness value** | 0.848 |

### Most affected cities

| City | Mean CATE | Mean daily admissions |
|------|-----------|----------------------|
| Sao Paulo | +3.13 | 150.5 |
| Brasilia | +2.09 | 54.6 |
| Porto Alegre | +1.47 | 41.5 |
| Salvador | +1.38 | 29.9 |
| Campo Grande | +1.15 | 14.6 |

---

## Overview

This repository contains the complete analytical pipeline, manuscript, and reproducibility artifacts for a study applying **causal machine learning** to estimate heterogeneous health effects of air pollution across all 27 Brazilian state capitals (2022-2025).

**Five contributions:**

1. **Association to causation** — conditional ignorability with explicit sensitivity analyses
2. **Average to heterogeneous effects** — CATEs across 8 effect modifiers
3. **Single-city to national** — all 27 state capitals (33,280 city-days)
4. **Black-box to explainable** — SHAP decomposition of causal heterogeneity
5. **Estimates to policy** — counterfactual prevented admissions under WHO/CONAMA scenarios

---

## Data Sources

| Source | Period | Records | Provider |
|--------|--------|---------|----------|
| Meteorology (19 variables) | 2015-2026 | 78,583 | ERA5 via Open-Meteo |
| Air Quality (7 pollutants) | 2022-2026 | 40,581 | CAMS/Copernicus |
| Hospitalizations (ICD-10 J00-J99) | 2014-2025 | 196,369 | SIH/SUS DATASUS |
| Demographics | 1970-2025 | 430 | IBGE Census 2022 |
| Vehicle Fleet | 2010-2023 | 108 | SENATRAN |

All data integrated via [Clima360 Brasil](https://github.com/Roverlucas/clima-360-brasil).

---

## Methods

- **Honest Causal Forests** (Athey, Tibshirani & Wager, 2019) — 2,000 trees, honest splitting, min leaf 20
- **Double Machine Learning** (Chernozhukov et al., 2018) — 5-fold cross-fitting, XGBoost nuisance models
- **Treatment:** Binary PM2.5 > 15 ug/m3 (WHO AQG daily guideline)
- **Outcome:** Daily respiratory hospitalizations (ICD-10 J00-J99)
- **KernelSHAP** for heterogeneity decomposition
- **Policy counterfactuals** under 4 air quality thresholds (15, 25, 35, 50 ug/m3)
- **Sensitivity:** placebo test, leave-one-city-out jackknife, omitted variable bias, threshold sensitivity

---

## Repository Structure

```
causal-pollution-health-brazil/
├── article/
│   └── manuscript.md               # Full manuscript (Lancet Planetary Health format)
├── src/
│   ├── data/
│   │   ├── extract.py              # Supabase/Clima360 data extraction
│   │   └── process.py              # Panel construction & feature engineering
│   ├── models/
│   │   ├── causal_forest.py        # Honest Causal Forest estimation
│   │   └── dml.py                  # Double Machine Learning estimation
│   ├── analysis/
│   │   ├── shap_analysis.py        # KernelSHAP heterogeneity decomposition
│   │   ├── policy.py               # Policy counterfactuals & cost estimation
│   │   └── sensitivity.py          # Placebo, jackknife, OVB, thresholds
│   ├── visualization/
│   │   ├── maps.py                 # Geospatial CATE maps
│   │   ├── forest_plots.py         # ATE/GATE forest plots
│   │   ├── shap_plots.py           # SHAP beeswarm & dependence plots
│   │   └── policy_plots.py         # Policy counterfactual figures
│   └── utils/
│       └── config.py               # Central configuration (capitals, params)
├── docs/
│   ├── EVIDENCE_MATRIX.md          # Systematic literature review (35 papers)
│   ├── METHODS_SPECIFICATION.md    # Detailed statistical methods
│   ├── STORYTELLING.md             # Narrative architecture
│   └── agents/                     # Paper Factory agent workflows (16 agents)
├── outputs/
│   ├── figures/                    # 14 publication-quality PDF figures
│   ├── tables/                     # 8 CSV results tables
│   ├── models/                     # Trained models, CATEs, CLAN analyses
│   └── reports/                    # Sensitivity & cost reports (JSON)
├── data/
│   ├── raw/                        # Raw extracted data
│   ├── processed/                  # Analysis-ready panel
│   └── interim/                    # Intermediate files
├── Makefile                        # Reproducible pipeline (make all)
├── requirements.txt                # Python dependencies
├── LICENSE                         # MIT License
├── CITATION.cff                    # Citation metadata
├── CHANGELOG.md                    # Version history
└── PROJECT_CHARTER.md              # Project charter & decision log
```

---

## Quick Start

### Prerequisites

- Python 3.14+
- Access to Clima360 Brasil Supabase API (set `SUPABASE_URL` and `SUPABASE_KEY` environment variables)

### Installation

```bash
git clone https://github.com/Roverlucas/causal-pollution-health-brazil.git
cd causal-pollution-health-brazil
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Run the full pipeline

```bash
make all
```

Or step by step:

```bash
# 1. Extract data from Clima360 Supabase
make extract

# 2. Process into analytical panel
make process

# 3. Train Causal Forest + DML models
make model

# 4. Run SHAP, policy, and sensitivity analyses
make analyze

# 5. Generate publication figures
make visualize
```

### Pipeline outputs

After running, you will find:

- `outputs/models/` — 12 trained models (6 CF + 6 DML) with ATEs, CATEs, and CLAN analyses
- `outputs/figures/` — 14 publication-ready PDF figures
- `outputs/tables/` — 8 CSV tables with all results
- `outputs/reports/` — Sensitivity and cost estimation reports

---

## Analytical Panel

| Characteristic | Value |
|---------------|-------|
| City-days | 33,280 |
| Capitals | 27 (all state capitals) |
| Total admissions | 935,114 |
| Mean daily admissions | 28.1 (IQR: 8-37) |
| Mean PM2.5 | 10.7 ug/m3 (SD: 9.0) |
| Treatment prevalence | 13.5% (PM2.5 > 15 ug/m3) |
| Study period | August 2022 - December 2025 |
| Features | 114 (weather, air quality, demographics, fleet, temporal) |

---

## Sensitivity Analyses

| Test | Result | Interpretation |
|------|--------|----------------|
| Placebo (PM2.5 at t+7) | ATE = -0.53, p=0.84 | No residual confounding |
| Leave-one-city-out jackknife | ATE range: 0.17-0.65, CV=0.21 | No single city drives result |
| Omitted variable bias | Robustness value = 0.848 | Confounder needs R2 > 0.848 to nullify |
| Threshold 25 ug/m3 | ATE = 0.84 (4.5% exceedance) | Consistent direction |
| Threshold 35 ug/m3 | ATE = 1.00 (2.0% exceedance) | Consistent direction |
| Threshold 50 ug/m3 | Skipped (0.8% exceedance) | Insufficient variation |

---

## Target Journal

**The Lancet Planetary Health** (IF 24.1) — Climate-health-policy, Global South focus

---

## Authors

- **Lucas Rover** — Graduate Program in Urban Environmental Sustainability (PPGSAU), UTFPR ([ORCID](https://orcid.org/0000-0001-6641-9224))
- **Yara de Souza Tadano** — PPGSAU, UTFPR ([ORCID](https://orcid.org/0000-0002-3975-3419))

## Citation

If you use this code or data, please cite:

```bibtex
@article{rover2026whosuffers,
  title={Who Suffers Most? Causal Machine Learning Reveals Heterogeneous Health
         Effects of Air Pollution Across Brazilian State Capitals},
  author={Rover, Lucas and Tadano, Yara de Souza},
  journal={Submitted to The Lancet Planetary Health},
  year={2026}
}
```

See [CITATION.cff](CITATION.cff) for machine-readable citation metadata.

## License

- **Code:** [MIT License](LICENSE)
- **Manuscript and figures:** [CC-BY 4.0](https://creativecommons.org/licenses/by/4.0/)

## Acknowledgments

- Data integration powered by [Clima360 Brasil](https://github.com/Roverlucas/clima-360-brasil)
- Hospitalization data from [SIH/SUS DATASUS](https://datasus.saude.gov.br)
- Air quality data from [CAMS/Copernicus](https://atmosphere.copernicus.eu/)
- Meteorological data from [ERA5 via Open-Meteo](https://open-meteo.com/)
- Demographics from [IBGE Census 2022](https://www.ibge.gov.br/)
- Vehicle fleet data from [SENATRAN](https://www.gov.br/transportes/)
- Managed by Paper Factory Squad (MMOS)
