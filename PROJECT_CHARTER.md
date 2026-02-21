# Project Charter — Causal Pollution-Health Brazil

## Metadata
- **Project Code:** CPH-BR-2026
- **Created:** 2026-02-21
- **Status:** Phase 0 — Kickoff
- **PI:** Lucas Rover (UTFPR)
- **Supervisor:** Dra. Yara de Souza Tadano
- **Pipeline:** Paper Factory v1.0 (Study Conductor)

---

## 1. Title

**"Who Suffers Most? Causal Machine Learning Reveals Heterogeneous Health Effects of Air Pollution Across 27 Brazilian State Capitals"**

### Working subtitle
*Honest Causal Forests and Double Machine Learning uncover which subpopulations bear disproportionate respiratory burden from PM2.5 and ozone exposure — evidence for targeted public health policy*

---

## 2. Research Question

**Primary:** Does the causal effect of short-term air pollution exposure (PM2.5, O3) on respiratory hospitalizations vary systematically across subpopulations defined by age group, sex, geographic region, fleet density, and population density in Brazilian state capitals?

**Secondary:**
- Which city-level and individual-level moderators explain the largest share of effect heterogeneity?
- Can SHAP-based explanations of causal heterogeneity inform priority-setting for targeted air quality alerts?
- How do current CONAMA standards compare to WHO guidelines in terms of preventable hospitalizations across vulnerability strata?

---

## 3. Thesis Statement

Air pollution does not affect everyone equally. While traditional epidemiological studies estimate a single population-average effect, the reality is that children, elderly, and residents of high-fleet-density capitals may face 2-5× higher causal risk. By applying Honest Causal Forests and Double Machine Learning to the largest multi-city environmental health dataset in Brazil (27 capitals, 2022-2025), we demonstrate that effect heterogeneity is not noise — it is the signal that public policy has been missing.

---

## 4. Hypothesis

**H1 (Main):** The Conditional Average Treatment Effect (CATE) of PM2.5 exceedance (>15 µg/m³ WHO guideline) on daily respiratory hospitalizations is significantly heterogeneous across subpopulations (p < 0.05 for omnibus heterogeneity test).

**H2:** Elderly (60+) and children (0-14) have CATE estimates ≥2× the population average.

**H3:** Capitals with fleet density >400 vehicles/1000 inhabitants show CATE ≥1.5× compared to low-fleet capitals (<200/1000).

**H4:** The interaction between thermal amplitude (DTR >10°C) and PM2.5 exceedance amplifies the CATE by ≥30%.

---

## 5. Data Sources (All Available in Clima360)

| Dataset | Source | Period | Granularity | Records |
|---------|--------|--------|-------------|---------|
| Weather | Open-Meteo Archive | 2015-2026 | Daily | 63,963 |
| Air Quality | CAMS/Copernicus | 2022-2026 | Daily | 40,581 |
| Hospitalizations | SIH/SUS DATASUS | 2014-2025 | Daily | 196,369 |
| Demographics | IBGE SIDRA | 1970-2025 | Annual | 430 |
| Fleet | SENATRAN | 2010-2023 | Annual | 108 |

**Analysis window:** 2022-2025 (intersection of all datasets)
**Cities:** 27 state capitals (complete coverage)

---

## 6. Methodology Overview

### Stage 1: Data Engineering
- Extract from Clima360 Supabase (all 7 tables)
- Merge daily climate + air quality + health by (city, date)
- Compute derived features: DTR, lagged exposures (0-7 days), moving averages, fleet/capita, pop density
- Quality filters: minimum 80% completeness per city-year

### Stage 2: Causal Identification
- **Treatment:** Binary indicator — PM2.5 > 15 µg/m³ (WHO AQG) or O3 > 100 µg/m³
- **Outcome:** Daily respiratory hospitalizations (CID J00-J99), by age group and sex
- **Confounders:** Temperature (mean, DTR), humidity, pressure, wind speed, precipitation, day of week, seasonality (Fourier), linear trend, holiday indicators
- **Assumption:** Conditional ignorability given weather confounders (pollution variation is quasi-random conditional on meteorology)

### Stage 3: Causal Forest Estimation
- **Honest Causal Forests** (Athey, Tibshirani & Wager, 2019): train/estimation sample split for valid inference
- **Double Machine Learning** (Chernozhukov et al., 2018): Neyman-orthogonal estimation with cross-fitting
- **Heterogeneity moderators:** age group, sex, city, region, fleet/capita, pop density, DTR quantile
- **Inference:** CLAN analysis (Classification Analysis of CATE), Best Linear Projection, calibration test

### Stage 4: Explainability & Policy Translation
- **SHAP values** on causal forest to identify which moderators drive heterogeneity
- **Vulnerability maps:** CATE by capital, visualized geographically
- **Policy counterfactuals:** hospitalizations preventable under WHO vs CONAMA standards, stratified by vulnerability group
- **Alert system prototype:** risk thresholds by subpopulation for compound events

---

## 7. Innovation & Contribution

| Dimension | Status Quo | Our Contribution |
|-----------|-----------|-----------------|
| **Method** | Associational (Poisson, GAM, case-crossover) | First causal ML study in Brazilian env. health |
| **Scope** | 2-6 cities max | All 27 state capitals |
| **Effect** | Population-average | Heterogeneous (CATE by subgroup) |
| **Explainability** | Black-box or none | SHAP on causal estimates |
| **Data** | Single-source | 5 integrated sources (Clima360) |
| **Policy** | Generic recommendations | Targeted, subgroup-specific thresholds |

---

## 8. Target Journals (A/B/C)

| Priority | Journal | IF (2024) | Fit |
|----------|---------|-----------|-----|
| **A** | The Lancet Planetary Health | 24.1 | Climate-health-policy, global south |
| **A** | Environmental Health Perspectives | 11.0 | Gold standard env-health, open access |
| **B** | American Journal of Epidemiology | 5.0 | Published causal forest guide (2023) |
| **B** | Environment International | 11.8 | Multi-city pollution-health |
| **C** | Science of the Total Environment | 8.2 | Broad environmental science |

---

## 9. Risks & Mitigations

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| Causal identification challenged | Medium | High | Robustness: DiD, placebo tests, sensitivity analysis (Rosenbaum bounds) |
| DATASUS quality (retroactive revisions) | Medium | Medium | Use Clima360 Data Vintage system; restrict to data aged >6 months |
| Air quality only from 2022 | High | Medium | Honest about temporal limitation; strength is spatial breadth |
| Desk reject at Lancet | Medium | Low | B/C journal pipeline ready |
| Computational cost of causal forests | Low | Low | Cloud compute; grf package is optimized |

---

## 10. Timeline (Target: 45 days)

| Phase | Duration | Gate | Key Deliverable |
|-------|----------|------|-----------------|
| 0 - Kickoff | Days 1-2 | Gate 0 | This charter + journal targets |
| 1 - Scoping | Days 3-10 | Gate 1 | Evidence matrix + claims map |
| 2 - Methodology | Days 11-17 | Gate 2 | Methods spec + statistical plan |
| 3 - Execution | Days 18-30 | Gate 3 | Results + figures |
| 4 - Writing | Days 31-38 | Gate 4 | Manuscript V1 |
| 5 - Submission | Days 39-43 | Gate 5 | Formatted + cover letter |
| Buffer | Days 44-45 | — | Final review |

---

## 11. Decision Log

| # | Date | Decision | Rationale |
|---|------|----------|-----------|
| D1 | 2026-02-21 | Selected Option 2 (Causal Forests) over 4 alternatives | Highest novelty (zero causal ML in BR env-health), strongest policy impact, all data available |
| D2 | 2026-02-21 | Target Lancet Planetary Health as Journal A | Perfect fit: climate-health-policy, global south focus, high IF |
| D3 | 2026-02-21 | Use Clima360 as integrated data platform | All 5 data sources already merged, quality-controlled, 27 capitals |
