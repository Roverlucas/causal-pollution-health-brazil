# @methodology-specialist — Workflow & Responsibilities

> **Role:** Design the complete methodological framework with reproducibility
> **Active:** Phase 2 (primary), Phase 4 (methods section writing support)
> **Tier:** 2 — Methodology & Statistics

---

## Mission

Design a methodological framework so rigorous that reviewers cannot challenge the approach — only debate the findings. Every analytical choice must have a rationale, every assumption must be explicit, and every step must be reproducible.

---

## Study Design

### Type
Multi-city ecological time-series study with causal machine learning inference

### Unit of Analysis
City-day: (capital × date) with outcomes stratified by age group and sex

### Study Period
- **Analysis window:** January 1, 2022 — December 31, 2025 (4 years)
- **Rationale:** Intersection of all 5 data sources; air quality data starts 2022

### Study Population
All SUS hospitalizations for respiratory causes (ICD-10 J00-J99) in 27 Brazilian state capitals

---

## Causal Framework

### Directed Acyclic Graph (DAG)

```
Weather Confounders ──→ Pollution Exposure ──→ Hospitalizations
  (temp, humidity,     (PM2.5, O3)           (respiratory, by age/sex)
   pressure, wind,                ↑
   precipitation)         ↑       │
         │                │   Effect Modifiers
         └────────────────┘   (age, fleet/capita,
                              pop density, DTR, region)

Temporal Confounders ──→ Both exposure and outcome
  (seasonality, trend,
   day-of-week, holidays)
```

### Identification Strategy

**Assumption:** Conditional Ignorability (Unconfoundedness)
- Treatment: Binary — PM2.5 > 15 µg/m³ (WHO AQG daily guideline) on day *t*
- Conditional on weather confounders on day *t* and temporal confounders, pollution variation is quasi-random
- Biological rationale: day-to-day pollution spikes conditional on weather are driven by stochastic emission events, traffic patterns, and atmospheric dynamics — not by health-seeking behavior

### Robustness & Sensitivity

| Test | Purpose | Implementation |
|------|---------|---------------|
| Placebo treatment | Falsification | Future pollution (t+7) should not predict current hospitalizations |
| Alternative thresholds | Sensitivity | Test 25, 35, 50 µg/m³ cutoffs |
| Continuous treatment | Sensitivity | Dose-response via generalized causal forests |
| Rosenbaum bounds | Unmeasured confounding | How strong would a hidden confounder need to be to nullify results? |
| Leave-one-city-out | Stability | Jackknife by city to check no single capital drives results |
| Alternative confounders | Specification | Add/remove long-term trend, add pollution lags |
| Comparison with DLNM | Benchmark | Traditional distributed lag non-linear model for same data |

---

## Feature Engineering Specification

### Treatment Variables
| Variable | Definition | Source |
|----------|-----------|--------|
| `pm25_exceed` | 1 if PM2.5 > 15 µg/m³, 0 otherwise | air_quality_history |
| `o3_exceed` | 1 if O3 > 100 µg/m³, 0 otherwise | air_quality_history |
| `pm25_continuous` | PM2.5 daily mean (µg/m³) | air_quality_history |

### Outcome Variables
| Variable | Definition | Source |
|----------|-----------|--------|
| `resp_total` | Daily respiratory admissions (J00-J99) | health_hospitalizations |
| `resp_0_14` | Respiratory admissions age 0-14 | health_hospitalizations |
| `resp_15_59` | Respiratory admissions age 15-59 | health_hospitalizations |
| `resp_60plus` | Respiratory admissions age 60+ | health_hospitalizations |
| `resp_male` | Respiratory admissions, male | health_hospitalizations |
| `resp_female` | Respiratory admissions, female | health_hospitalizations |

### Confounders (W)
| Variable | Definition | Lags | Source |
|----------|-----------|------|--------|
| `temp_mean` | Daily mean temperature | 0 | weather_history |
| `temp_dtr` | Thermal amplitude (max-min) | 0 | weather_history (derived) |
| `humidity_mean` | Relative humidity mean | 0 | weather_history |
| `pressure_mean` | Sea-level pressure | 0 | weather_history |
| `wind_speed_max` | Max wind speed | 0 | weather_history |
| `precip_sum` | Precipitation total | 0 | weather_history |
| `dow` | Day of week (1-7) | — | derived |
| `holiday` | Binary holiday indicator | — | derived |
| `sin_annual` | sin(2πt/365.25) | — | derived |
| `cos_annual` | cos(2πt/365.25) | — | derived |
| `sin_semi` | sin(4πt/365.25) | — | derived |
| `cos_semi` | cos(4πt/365.25) | — | derived |
| `trend` | Linear time trend | — | derived |

### Effect Modifiers (X for heterogeneity)
| Variable | Definition | Source |
|----------|-----------|--------|
| `age_group` | 0-14, 15-59, 60+ | health_hospitalizations |
| `sex` | Male, Female | health_hospitalizations |
| `city` | Capital identifier | — |
| `region` | N, NE, CO, SE, S | capitals.ts |
| `fleet_per_capita` | Fleet total / population (annual) | fleet_history + demographics |
| `pop_density` | Population / area (annual) | demographics_history |
| `dtr_quantile` | DTR tercile (low/medium/high) | weather_history (derived) |
| `pct_elderly` | % pop 60+ (annual) | demographics_history |

---

## Methods Spec for Manuscript

### Section 2.1 — Study Design and Data
- Ecological multi-city time-series, 27 capitals, 2022-2025
- Five integrated data sources via Clima360 platform
- Outcome: daily respiratory hospitalizations (SIH/SUS, ICD-10 J00-J99)

### Section 2.2 — Causal Identification
- DAG presentation
- Conditional ignorability assumption with justification
- Treatment definition and rationale for WHO threshold

### Section 2.3 — Honest Causal Forests
- Algorithm description (Athey & Wager, 2019)
- Honesty: training/estimation sample split
- Hyperparameter selection via out-of-bag error
- CATE estimation and aggregation

### Section 2.4 — Double Machine Learning
- Neyman-orthogonal score function
- Cross-fitting (K=5 folds)
- First-stage models: XGBoost for both treatment and outcome

### Section 2.5 — Heterogeneity Analysis
- CLAN (Classification Analysis of CATE)
- Best Linear Projection of CATE on moderators
- SHAP values for heterogeneity explanation
- Calibration test for CATE reliability

### Section 2.6 — Sensitivity and Robustness
- Full battery of tests (see table above)

### Section 2.7 — Policy Counterfactuals
- Prevented fraction under WHO vs CONAMA scenarios
- Stratified by vulnerability group
- Cost estimation using SIH/SUS unit costs

---

## Tasks

- [ ] Finalize DAG with @statistical-reviewer
- [ ] Write complete Methods Specification document
- [ ] Define feature engineering pipeline code spec (for @technical-executor)
- [ ] Define robustness test battery
- [ ] Review Methods section draft in manuscript (Phase 4)
- [ ] Ensure STROBE compliance

---

*@methodology-specialist v1.0 — 2026-02-21*
