# Supplementary Material

**Who Suffers Most? Causal Machine Learning Reveals Heterogeneous Health Effects of Air Pollution Across Brazilian State Capitals**

Lucas Rover (ORCID: 0000-0001-6641-9224), Yara de Souza Tadano (ORCID: 0000-0002-3975-3419)

Graduate Program in Urban Environmental Sustainability (PPGSAU), Federal University of Technology -- Parana (UTFPR), Curitiba, PR, Brazil

---

\newpage

## Table of Contents

- Appendix A: Variable Definitions and Data Dictionary
- Appendix B: Average Treatment Effect Estimates (CF and DML)
- Appendix C: CLAN Analysis --- Full Quartile Profiles
- Appendix D: City-Level CATE Estimates
- Appendix E: SHAP Feature Importance
- Appendix F: Policy Counterfactuals
- Appendix G: Cost Estimation
- Appendix H: Sensitivity and Robustness Analyses
- Appendix I: Figures

---

\newpage

## Appendix A: Variable Definitions and Data Dictionary

### A.1 Treatment Variable

| Variable | Definition | Source |
|----------|-----------|--------|
| Treatment (binary) | 1 if daily PM2.5 > 15 ug/m3 (WHO AQG), 0 otherwise | CAMS/Copernicus |

### A.2 Outcome Variables

| Variable | Definition | Source |
|----------|-----------|--------|
| admissions | Total daily respiratory hospitalisations (ICD-10 J00--J99) | SIH/SUS DATASUS |
| admissions_age_0_14 | Respiratory admissions, age 0--14 years | SIH/SUS DATASUS |
| admissions_age_15_59 | Respiratory admissions, age 15--59 years | SIH/SUS DATASUS |
| admissions_age_60_plus | Respiratory admissions, age 60+ years | SIH/SUS DATASUS |
| admissions_female | Respiratory admissions, female | SIH/SUS DATASUS |
| admissions_male | Respiratory admissions, male | SIH/SUS DATASUS |

### A.3 Confounders (W)

| Variable | Definition | Source |
|----------|-----------|--------|
| temperature_2m_mean | Daily mean temperature at 2m (C) | ERA5/Open-Meteo |
| dtr | Diurnal temperature range: T_max - T_min (C) | ERA5/Open-Meteo |
| relative_humidity_2m_mean | Daily mean relative humidity (%) | ERA5/Open-Meteo |
| pressure_msl_mean | Mean sea-level pressure (hPa) | ERA5/Open-Meteo |
| wind_speed_10m_max | Maximum 10m wind speed (m/s) | ERA5/Open-Meteo |
| precipitation_sum | Total daily precipitation (mm) | ERA5/Open-Meteo |
| day_of_week | Day of week indicators (6 dummies) | Calendar |
| is_holiday | Public holiday indicator | Calendar |
| sin_annual, cos_annual | Fourier harmonics (annual cycle) | Derived |
| sin_semi, cos_semi | Fourier harmonics (semi-annual cycle) | Derived |
| time_trend | Linear time trend (days since start) | Derived |

### A.4 Effect Modifiers (X)

| Variable | Definition | Source |
|----------|-----------|--------|
| pop_density | Population / city area (inhabitants/km2) | IBGE Census 2022 |
| fleet_per_capita | Registered vehicles / population x 1000 | SENATRAN |
| pct_female | Female population / total population | IBGE Census 2022 |
| dtr | Diurnal temperature range (C) | ERA5/Open-Meteo |
| region_N, region_NE, region_CO, region_SE, region_S | Macro-region indicators | IBGE |

### A.5 Model Hyperparameters

| Parameter | Causal Forest | DML |
|-----------|--------------|-----|
| n_estimators | 2,000 | -- |
| min_samples_leaf | 20 | -- |
| honest | True | -- |
| discrete_treatment | True | True |
| cv (cross-fitting folds) | 5 | 5 |
| First-stage model (Y) | XGBoost (500 trees, depth 6, lr 0.05) | XGBoost (500 trees, depth 6, lr 0.05) |
| First-stage model (T) | XGBoost (500 trees, depth 6, lr 0.05) | XGBoost (500 trees, depth 6, lr 0.05) |
| Random seed | 42 | 42 |

---

\newpage

## Appendix B: Average Treatment Effect Estimates

### Table B.1: Causal Forest vs Double Machine Learning --- Full Comparison

| Outcome | CF ATE | CF 95% CI | CF p-value | DML ATE | DML 95% CI | DML p-value |
|---------|--------|-----------|------------|---------|------------|-------------|
| Total Respiratory | 0.599 | [-3.670, 4.869] | 0.783 | **0.716** | **[0.083, 1.350]** | **0.027** |
| Children (0--14) | 0.253 | [-2.511, 3.017] | 0.858 | 0.328 | [-0.072, 0.728] | 0.108 |
| Adults (15--59) | 0.231 | [-1.301, 1.763] | 0.767 | **0.264** | **[0.033, 0.494]** | **0.025** |
| Elderly (60+) | 0.207 | [-1.411, 1.824] | 0.802 | 0.210 | [-0.023, 0.443] | 0.077 |
| Female | 0.193 | [-2.166, 2.552] | 0.873 | 0.258 | [-0.082, 0.598] | 0.137 |
| Male | 0.372 | [-2.220, 2.965] | 0.778 | **0.418** | **[0.006, 0.830]** | **0.047** |

Note: Bold indicates statistical significance at alpha = 0.05. ATE = Average Treatment Effect; CI = confidence interval. Treatment: PM2.5 > 15 ug/m3. Outcome: daily respiratory hospitalisations.

---

\newpage

## Appendix C: CLAN Analysis --- Full Quartile Profiles

The Classification Analysis (CLAN) sorts all city-day observations into quartiles of estimated CATE and reports the mean covariate profile of each quartile.

### Table C.1: CLAN --- Total Respiratory Admissions

| Quartile | CATE | Pop. Density | Fleet/1000 | % Female | DTR (C) | % North | % NE | % CO | % SE | % South |
|----------|------|-------------|------------|----------|---------|---------|------|------|------|---------|
| Q1 (lowest) | -1.558 | 2,564 | 710 | 52.2% | 7.36 | 30.4% | 17.7% | 24.0% | 16.0% | 12.0% |
| Q2 | +0.010 | 1,653 | 719 | 52.0% | 8.10 | 39.2% | 15.0% | 28.4% | 8.9% | 8.5% |
| Q3 | +0.937 | 2,030 | 710 | 52.0% | 8.17 | 34.6% | 14.8% | 24.3% | 14.7% | 11.6% |
| Q4 (highest) | +3.009 | 3,779 | 729 | 52.6% | 7.92 | 12.0% | 23.5% | 17.6% | 31.6% | 15.3% |

### Table C.2: CLAN --- Children (0--14 years)

| Quartile | CATE | Pop. Density | Fleet/1000 | % Female | DTR (C) | % North | % NE | % CO | % SE | % South |
|----------|------|-------------|------------|----------|---------|---------|------|------|------|---------|
| Q1 (lowest) | -1.187 | 2,369 | 693 | 52.1% | 7.75 | 33.0% | 15.7% | 27.6% | 15.7% | 8.0% |
| Q2 | -0.086 | 1,863 | 742 | 52.0% | 8.25 | 31.2% | 14.7% | 33.8% | 10.8% | 9.5% |
| Q3 | +0.452 | 1,978 | 716 | 52.0% | 8.21 | 40.1% | 13.0% | 20.2% | 14.1% | 12.6% |
| Q4 (highest) | +1.834 | 3,816 | 717 | 52.6% | 7.34 | 11.9% | 27.6% | 12.8% | 30.5% | 17.3% |

### Table C.3: CLAN --- Adults (15--59 years)

| Quartile | CATE | Pop. Density | Fleet/1000 | % Female | DTR (C) | % North | % NE | % CO | % SE | % South |
|----------|------|-------------|------------|----------|---------|---------|------|------|------|---------|
| Q1 (lowest) | -0.564 | 3,181 | 725 | 52.4% | 6.97 | 22.6% | 25.8% | 15.2% | 22.3% | 14.2% |
| Q2 | +0.017 | 1,778 | 716 | 51.9% | 8.17 | 39.1% | 13.9% | 26.0% | 10.5% | 10.5% |
| Q3 | +0.365 | 1,812 | 703 | 52.0% | 8.19 | 36.0% | 12.2% | 29.1% | 11.7% | 10.8% |
| Q4 (highest) | +1.109 | 3,257 | 724 | 52.5% | 8.22 | 18.5% | 19.1% | 24.1% | 26.6% | 11.7% |

### Table C.4: CLAN --- Elderly (60+ years)

| Quartile | CATE | Pop. Density | Fleet/1000 | % Female | DTR (C) | % North | % NE | % CO | % SE | % South |
|----------|------|-------------|------------|----------|---------|---------|------|------|------|---------|
| Q1 (lowest) | -0.822 | 2,969 | 702 | 52.4% | 6.85 | 26.9% | 23.3% | 13.5% | 17.9% | 18.4% |
| Q2 | -0.012 | 1,418 | 708 | 51.8% | 8.44 | 42.9% | 10.9% | 27.2% | 7.9% | 11.1% |
| Q3 | +0.396 | 1,875 | 727 | 51.9% | 8.29 | 32.0% | 12.7% | 31.7% | 12.7% | 10.9% |
| Q4 (highest) | +1.266 | 3,767 | 732 | 52.7% | 7.97 | 14.3% | 24.2% | 21.9% | 32.7% | 6.9% |

### Table C.5: CLAN --- Female

| Quartile | CATE | Pop. Density | Fleet/1000 | % Female | DTR (C) | % North | % NE | % CO | % SE | % South |
|----------|------|-------------|------------|----------|---------|---------|------|------|------|---------|
| Q1 (lowest) | -0.976 | 3,220 | 750 | 52.4% | 7.38 | 15.7% | 23.4% | 21.0% | 23.4% | 16.4% |
| Q2 | -0.074 | 1,712 | 720 | 51.9% | 8.61 | 41.0% | 8.7% | 29.0% | 13.2% | 8.1% |
| Q3 | +0.388 | 1,710 | 718 | 51.9% | 8.39 | 38.3% | 12.0% | 28.4% | 8.6% | 12.6% |
| Q4 (highest) | +1.434 | 3,385 | 681 | 52.5% | 7.17 | 21.1% | 26.9% | 16.0% | 25.9% | 10.1% |

### Table C.6: CLAN --- Male

| Quartile | CATE | Pop. Density | Fleet/1000 | % Female | DTR (C) | % North | % NE | % CO | % SE | % South |
|----------|------|-------------|------------|----------|---------|---------|------|------|------|---------|
| Q1 (lowest) | -1.130 | 2,316 | 651 | 52.2% | 6.82 | 37.9% | 21.8% | 20.0% | 10.4% | 10.0% |
| Q2 | -0.039 | 1,691 | 743 | 51.8% | 8.57 | 36.5% | 14.0% | 32.2% | 9.0% | 8.3% |
| Q3 | +0.586 | 2,000 | 728 | 52.0% | 8.10 | 35.1% | 11.1% | 22.4% | 16.7% | 14.7% |
| Q4 (highest) | +2.075 | 4,018 | 745 | 52.7% | 8.06 | 6.8% | 24.2% | 19.8% | 34.9% | 14.3% |

---

\newpage

## Appendix D: City-Level CATE Estimates

### Table D.1: Mean CATE by Capital (Total Respiratory Admissions)

| City | UF | Region | Mean CATE | Median CATE | SD | N obs | Mean daily admissions |
|------|----|---------|-----------|-----------|----|-------|----------------------|
| Sao Paulo | SP | SE | **+2.577** | +3.291 | 3.582 | 1,247 | 150.5 |
| Brasilia | DF | CO | +1.381 | +1.115 | 2.033 | 1,247 | 54.6 |
| Salvador | BA | NE | +1.127 | +0.566 | 2.498 | 1,246 | 29.9 |
| Rio de Janeiro | RJ | SE | +0.909 | +0.957 | 1.135 | 1,247 | 43.4 |
| Campo Grande | MS | CO | +0.820 | +0.747 | 1.015 | 1,237 | 14.6 |
| Florianopolis | SC | S | +0.693 | +0.739 | 1.253 | 1,241 | 14.5 |
| Aracaju | SE | NE | +0.692 | +0.767 | 1.845 | 1,245 | 13.3 |
| Natal | RN | NE | +0.656 | +0.696 | 1.727 | 1,244 | 13.3 |
| Belo Horizonte | MG | SE | +0.568 | +0.797 | 2.183 | 1,246 | 47.2 |
| Porto Velho | RO | N | +0.443 | +0.425 | 0.622 | 1,215 | 6.4 |
| Curitiba | PR | S | +0.334 | +0.599 | 2.427 | 1,245 | 44.4 |
| Belem | PA | N | +0.320 | +0.216 | 1.515 | 1,231 | 24.4 |
| Rio Branco | AC | N | +0.300 | +0.280 | 0.500 | 1,199 | 5.0 |
| Goiania | GO | CO | +0.146 | +0.082 | 0.875 | 1,247 | 21.2 |
| Macapa | AP | N | +0.002 | +0.216 | 1.192 | 1,232 | 7.0 |
| Manaus | AM | N | **-0.395** | -0.548 | 1.907 | 1,234 | 31.1 |
| Cuiaba | MT | CO | **-0.428** | -0.307 | 0.976 | 1,232 | 8.9 |

Note: Sorted by mean CATE (descending). Bold indicates highest and lowest values.

---

\newpage

## Appendix E: SHAP Feature Importance

### Table E.1: Mean Absolute SHAP Values for CATE Heterogeneity (Total Respiratory Admissions)

| Rank | Feature | Mean |SHAP| | Description |
|------|---------|----------------|-------------|
| 1 | dtr | 0.594 | Diurnal temperature range (C) |
| 2 | pop_density | 0.457 | Population density (inhabitants/km2) |
| 3 | fleet_per_capita | 0.292 | Vehicles per 1,000 inhabitants |
| 4 | pct_female | 0.265 | Proportion female in population |
| 5 | region_CO | 0.045 | Central-West region indicator |
| 6 | region_NE | 0.025 | Northeast region indicator |
| 7 | region_N | 0.024 | North region indicator |
| 8 | region_S | 0.023 | South region indicator |
| 9 | region_SE | 0.021 | Southeast region indicator |

Note: SHAP values decompose heterogeneity in Conditional Average Treatment Effects, not outcome prediction. Higher values indicate greater contribution to CATE variation across observations.

---

\newpage

## Appendix F: Policy Counterfactuals

### Table F.1: Prevented Admissions by City Under WHO Compliance (PM2.5 <= 15 ug/m3)

| City | Total admissions | Treated days | Prevented admissions | Mean CATE | Prevented (%) |
|------|-----------------|-------------|---------------------|-----------|---------------|
| Sao Paulo | 187,646 | 864 | 2,268.5 | +2.577 | 1.21% |
| Rio de Janeiro | 54,132 | 862 | 840.1 | +0.909 | 1.55% |
| Belo Horizonte | 58,791 | 177 | 286.4 | +0.568 | 0.49% |
| Curitiba | 55,219 | 147 | 249.6 | +0.334 | 0.45% |
| Rio Branco | 5,975 | 286 | 170.1 | +0.300 | 2.85% |
| Porto Velho | 7,818 | 365 | 63.9 | +0.443 | 0.82% |
| Brasilia | 68,030 | 40 | 54.0 | +1.381 | 0.08% |
| Florianopolis | 18,049 | 61 | 48.1 | +0.693 | 0.27% |
| Campo Grande | 18,030 | 87 | 42.6 | +0.820 | 0.24% |
| Salvador | 37,235 | 13 | 27.7 | +1.127 | 0.07% |
| Natal | 16,487 | 20 | 14.4 | +0.656 | 0.09% |
| Macapa | 8,568 | 18 | 10.0 | +0.002 | 0.12% |
| Goiania | 26,479 | 86 | 9.9 | +0.146 | 0.04% |
| Aracaju | 16,572 | 1 | -0.6 | +0.692 | -0.00% |
| Belem | 29,976 | 42 | -15.5 | +0.320 | -0.05% |
| Cuiaba | 10,923 | 161 | -27.6 | -0.428 | -0.25% |
| Manaus | 38,391 | 355 | -208.1 | -0.395 | -0.54% |
| **Total** | **658,321** | **3,585** | **3,833.7** | -- | **0.58%** |

Note: Negative prevented admissions indicate cities where the CATE is negative, suggesting possible harvesting effects or unmeasured protective factors. Treated days = days PM2.5 exceeded 15 ug/m3.

### Table F.2: Prevented Admissions by CATE Vulnerability Quartile

| Quartile | N obs | Total admissions | Treated days | Prevented admissions | Mean CATE | Prevented (%) |
|----------|-------|-----------------|-------------|---------------------|-----------|---------------|
| Q1 (least vulnerable) | 5,260 | 172,613 | 786 | -1,339.5 | -1.558 | -0.78% |
| Q2 | 5,260 | 105,846 | 733 | +13.9 | +0.010 | +0.01% |
| Q3 | 5,257 | 128,783 | 861 | +809.6 | +0.937 | +0.63% |
| Q4 (most vulnerable) | 5,258 | 251,079 | 1,205 | +4,349.7 | +3.009 | +1.73% |

Note: The Q4 quartile alone accounts for 4,350 of the 3,834 net prevented admissions. The net total is lower because Q1 shows negative prevented admissions.

### Table F.3: Dose-Response Policy Curve --- Alternative Thresholds

| Threshold (ug/m3) | Exceedance days | Exceedance (%) | Prevented admissions | Prevented (%) |
|-------------------|----------------|----------------|---------------------|---------------|
| 15 (WHO AQG) | 3,585 | 17.04% | 3,833.7 | 0.58% |
| 25 (CONAMA intermediate) | 1,371 | 6.52% | 1,564.8 | 0.24% |
| 35 (CONAMA final) | 633 | 3.01% | 553.3 | 0.08% |
| 50 (pre-2024 standard) | 253 | 1.20% | 144.4 | 0.02% |

### Table F.4: Bootstrap Confidence Interval for Prevented Fraction

| Metric | Value |
|--------|-------|
| Mean prevented (%) | 0.58% |
| 95% CI lower | 0.54% |
| 95% CI upper | 0.62% |
| Bootstrap resamples | 1,000 |

---

\newpage

## Appendix G: Cost Estimation

### Table G.1: Economic Impact of WHO Compliance

| Metric | Value |
|--------|-------|
| Total SUS respiratory costs (study period) | R$ 1,282,441,262 |
| Total admissions | 658,321 |
| Mean cost per admission | R$ 1,948.05 |
| Prevented admissions (WHO scenario) | 3,833.7 |
| Saved costs | R$ 7,468,189 |
| Saved costs (% of total) | 0.58% |
| Saved costs (USD, approx.) | USD 1,494,000 |

Note: Costs based on SIH/SUS reimbursement data. USD conversion at approximate 2024 exchange rate of R$5.00/USD.

---

\newpage

## Appendix H: Sensitivity and Robustness Analyses

### Table H.1: Placebo Test (PM2.5 at t+7)

| Metric | Value |
|--------|-------|
| Test | Future PM2.5 (7-day lead) as placebo treatment |
| ATE | -0.540 |
| 95% CI | [-5.280, 4.200] |
| p-value | 0.823 |
| Result | **Passed** (null effect of future pollution on current admissions) |

### Table H.2: Leave-One-City-Out Jackknife

| Excluded city | ATE | 95% CI | p-value | N rows |
|--------------|-----|--------|---------|--------|
| Aracaju | 0.716 | [-4.241, 5.673] | 0.777 | 19,790 |
| Belo Horizonte | 0.654 | [-4.609, 5.918] | 0.808 | 19,789 |
| Belem | 0.687 | [-4.550, 5.923] | 0.797 | 19,804 |
| Brasilia | 0.623 | [-4.391, 5.636] | 0.808 | 19,788 |
| Campo Grande | 0.747 | [-4.672, 6.165] | 0.787 | 19,798 |
| Cuiaba | 0.859 | [-4.884, 6.602] | 0.769 | 19,803 |
| Curitiba | **0.970** | [-4.232, 6.172] | 0.715 | 19,790 |
| Florianopolis | 0.636 | [-4.770, 6.043] | 0.818 | 19,794 |
| Goiania | 0.672 | [-4.782, 6.126] | 0.809 | 19,788 |
| Macapa | 0.802 | [-4.583, 6.187] | 0.770 | 19,803 |
| Manaus | 0.803 | [-5.321, 6.927] | 0.797 | 19,801 |
| Natal | 0.450 | [-4.547, 5.448] | 0.860 | 19,791 |
| Porto Velho | 0.795 | [-4.528, 6.119] | 0.770 | 19,820 |
| Rio Branco | 0.710 | [-4.490, 5.910] | 0.789 | 19,836 |
| Rio de Janeiro | 0.822 | [-6.334, 7.979] | 0.822 | 19,788 |
| Salvador | 0.542 | [-4.561, 5.644] | 0.835 | 19,789 |
| Sao Paulo | **0.339** | [-3.598, 4.275] | 0.866 | 19,788 |

| Summary statistic | Value |
|-------------------|-------|
| Minimum ATE | 0.339 (excl. Sao Paulo) |
| Maximum ATE | 0.970 (excl. Curitiba) |
| Mean ATE | 0.696 |
| Coefficient of variation | 0.22 |

Note: Bold indicates minimum and maximum ATE values. No single city exclusion changes the direction of the main finding.

### Table H.3: Threshold Sensitivity (Causal Forest ATE)

| Threshold (ug/m3) | ATE | 95% CI | p-value | Treatment prevalence |
|-------------------|-----|--------|---------|---------------------|
| 15 (primary) | 0.625 | [-4.336, 5.587] | 0.805 | 17.04% |
| 25 | 0.375 | [-12.130, 12.880] | 0.953 | 6.52% |
| 35 | 0.423 | [-15.205, 16.050] | 0.958 | 3.01% |
| 50 | 1.717 | [-72.189, 75.623] | 0.964 | 1.20% |

Note: As the threshold increases, treatment prevalence decreases and confidence intervals widen substantially, reflecting reduced statistical power.

### Table H.4: Omitted Variable Bias Analysis

| Metric | Value |
|--------|-------|
| R2 of Y given W (observed confounders) | 0.2386 |
| Pseudo-R2 of T given W | 0.1037 |
| Residual variance of Y | 0.7614 |
| Residual variance of T | 0.8963 |
| **Robustness value** | **0.8261** |
| Interpretation | An unobserved confounder would need partial R2 of at least 0.826 with both Y and T (after controlling for observed confounders) to reduce the ATE to zero. |

Note: The robustness value of 0.826 indicates that any unobserved confounder would need to explain more variance than the entire set of observed confounders combined --- an implausibly strong requirement.

---

\newpage

## Appendix I: Figures

### Figure S1: CATE Map of Brazil

Geospatial map of estimated Conditional Average Treatment Effects (CATEs) across 17 Brazilian state capitals. Dot colour represents CATE magnitude (blue = negative/low, red = high); dot size represents confidence interval width.

![Figure S1: CATE Map of Brazil](../outputs/figures/cate_map_brazil.pdf){width=100%}

\newpage

### Figure S2: CATE Scatter by Capital

Scatter plot of mean CATE vs mean daily admissions for each capital, coloured by macro-region.

![Figure S2: CATE Scatter by Capital](../outputs/figures/cate_scatter_capitals.pdf){width=100%}

\newpage

### Figure S3: Forest Plot --- ATE by Subgroup

Forest plot of Average Treatment Effects (CF and DML) for total, age-stratified, and sex-stratified outcomes. Diamond = point estimate; horizontal line = 95% confidence interval; vertical dashed line = null effect.

![Figure S3: Forest Plot — ATE by Subgroup](../outputs/figures/forest_ate_subgroups.pdf){width=100%}

\newpage

### Figure S4: Forest Plot --- CLAN Quartiles

Forest plot of Group Average Treatment Effects by CLAN quartile, showing the monotonic gradient from Q1 (lowest vulnerability) to Q4 (highest vulnerability).

![Figure S4: Forest Plot — CLAN Quartiles](../outputs/figures/forest_clan_quartiles.pdf){width=100%}

\newpage

### Figure S5: SHAP Beeswarm Plot

Beeswarm plot of SHAP values for all effect modifiers. Each point represents one city-day observation; horizontal position indicates the SHAP value (positive = higher CATE); colour indicates the feature value (blue = low, red = high).

![Figure S5: SHAP Beeswarm Plot](../outputs/figures/shap_beeswarm_admissions.pdf){width=100%}

\newpage

### Figure S6: SHAP Dependence --- DTR

SHAP dependence plot for diurnal temperature range (DTR), showing the non-linear relationship between DTR and its contribution to CATE heterogeneity.

![Figure S6: SHAP Dependence — DTR](../outputs/figures/shap_dependence_dtr_admissions.pdf){width=100%}

\newpage

### Figure S7: SHAP Dependence --- Population Density

SHAP dependence plot for population density, illustrating how densely populated cities show higher CATE contributions.

![Figure S7: SHAP Dependence — Population Density](../outputs/figures/shap_dependence_pop_density_admissions.pdf){width=100%}

\newpage

### Figure S8: SHAP Dependence --- Fleet per Capita

SHAP dependence plot for fleet per capita (vehicles per 1,000 inhabitants).

![Figure S8: SHAP Dependence — Fleet per Capita](../outputs/figures/shap_dependence_fleet_per_capita_admissions.pdf){width=100%}

\newpage

### Figure S9: Policy --- Prevented Admissions by City

Bar chart showing prevented respiratory hospitalisations under WHO compliance for each of the 17 capitals, sorted by magnitude.

![Figure S9: Prevented Admissions by City](../outputs/figures/policy_city_prevented.pdf){width=100%}

\newpage

### Figure S10: Policy --- Stratified by Vulnerability Quartile

Stacked bar chart showing the distribution of prevented admissions across CATE vulnerability quartiles under the WHO scenario.

![Figure S10: Stratified by Vulnerability Quartile](../outputs/figures/policy_stratified_quartiles.pdf){width=100%}

\newpage

### Figure S11: Policy --- Threshold Response Curve

Dose-response curve showing prevented admissions as a function of the PM2.5 threshold (15, 25, 35, 50 ug/m3), demonstrating diminishing returns at higher thresholds.

![Figure S11: Threshold Response Curve](../outputs/figures/policy_threshold_response.pdf){width=100%}

\newpage

### Figure S12: Policy --- Cost Summary

Bar chart of estimated cost savings (R$ millions) under WHO compliance, stratified by vulnerability group.

![Figure S12: Cost Summary](../outputs/figures/policy_cost_summary.pdf){width=100%}

---

\newpage

## Code Availability

The complete analytical pipeline, including data extraction, processing, causal estimation, SHAP analysis, policy counterfactuals, sensitivity analyses, and visualization code, is available at:

**https://github.com/Roverlucas/causal-pollution-health-brazil**

The pipeline can be reproduced with a single command: `make all`

---

*End of Supplementary Material*
