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
| Total Respiratory | 0.390 | [-4.197, 4.976] | 0.868 | 0.128 | [-0.305, 0.561] | 0.563 |
| Children (0--14) | 0.212 | [-2.603, 3.027] | 0.883 | 0.046 | [-0.229, 0.322] | 0.742 |
| Adults (15--59) | 0.111 | [-1.324, 1.545] | 0.880 | 0.072 | [-0.080, 0.225] | 0.352 |
| Elderly (60+) | 0.167 | [-1.534, 1.868] | 0.847 | 0.128 | [-0.060, 0.317] | 0.183 |
| Female | 0.107 | [-2.355, 2.569] | 0.932 | 0.013 | [-0.242, 0.268] | 0.919 |
| Male | 0.319 | [-2.432, 3.071] | 0.820 | 0.171 | [-0.099, 0.441] | 0.214 |

Note: No estimates reached statistical significance at alpha = 0.05, reflecting the dominance of heterogeneity over the average effect. ATE = Average Treatment Effect; CI = confidence interval. Treatment: PM2.5 > 15 ug/m3. Outcome: daily respiratory hospitalisations. N = 33,280 city-days across 27 capitals.

---

\newpage

## Appendix C: CLAN Analysis --- Full Quartile Profiles

The Classification Analysis (CLAN) sorts all city-day observations into quartiles of estimated CATE and reports the mean covariate profile of each quartile.

### Table C.1: CLAN --- Total Respiratory Admissions

| Quartile | CATE | Pop. Density | Fleet/1000 | % Female | DTR (C) | % North | % NE | % CO | % SE | % South |
|----------|------|-------------|------------|----------|---------|---------|------|------|------|---------|
| Q1 (lowest) | -1.944 | 3,211 | 671 | 52.4% | 6.59 | 29.5% | 36.6% | 8.1% | 15.2% | 10.5% |
| Q2 | -0.199 | 2,199 | 727 | 52.3% | 7.83 | 26.3% | 37.9% | 15.8% | 14.1% | 5.9% |
| Q3 | +0.658 | 2,197 | 719 | 52.3% | 8.12 | 30.0% | 30.4% | 17.5% | 11.1% | 11.1% |
| Q4 (highest) | +3.044 | 3,342 | 695 | 52.7% | 7.66 | 15.5% | 29.7% | 18.2% | 19.3% | 17.3% |

### Table C.2: CLAN --- Children (0--14 years)

| Quartile | CATE | Pop. Density | Fleet/1000 | % Female | DTR (C) | % North | % NE | % CO | % SE | % South |
|----------|------|-------------|------------|----------|---------|---------|------|------|------|---------|
| Q1 (lowest) | -1.254 | 2,811 | 677 | 52.3% | 7.03 | 32.0% | 32.6% | 13.4% | 14.5% | 7.5% |
| Q2 | -0.167 | 1,979 | 732 | 52.2% | 7.90 | 28.7% | 33.6% | 17.3% | 11.9% | 8.4% |
| Q3 | +0.395 | 2,279 | 717 | 52.2% | 7.93 | 29.3% | 29.6% | 18.8% | 11.2% | 11.0% |
| Q4 (highest) | +1.876 | 3,878 | 687 | 52.9% | 7.33 | 11.2% | 38.8% | 10.1% | 22.0% | 17.8% |

### Table C.3: CLAN --- Adults (15--59 years)

| Quartile | CATE | Pop. Density | Fleet/1000 | % Female | DTR (C) | % North | % NE | % CO | % SE | % South |
|----------|------|-------------|------------|----------|---------|---------|------|------|------|---------|
| Q1 (lowest) | -0.663 | 3,836 | 689 | 52.7% | 6.45 | 16.1% | 45.8% | 7.5% | 19.5% | 11.3% |
| Q2 | -0.047 | 2,045 | 712 | 52.1% | 7.68 | 36.1% | 28.8% | 14.7% | 11.4% | 9.0% |
| Q3 | +0.251 | 2,011 | 734 | 52.2% | 8.35 | 28.2% | 28.6% | 19.5% | 10.2% | 13.5% |
| Q4 (highest) | +0.902 | 3,058 | 678 | 52.6% | 7.70 | 20.9% | 31.6% | 18.0% | 18.6% | 11.0% |

### Table C.4: CLAN --- Elderly (60+ years)

| Quartile | CATE | Pop. Density | Fleet/1000 | % Female | DTR (C) | % North | % NE | % CO | % SE | % South |
|----------|------|-------------|------------|----------|---------|---------|------|------|------|---------|
| Q1 (lowest) | -0.727 | 3,218 | 687 | 52.5% | 6.66 | 22.6% | 38.1% | 8.9% | 14.9% | 15.5% |
| Q2 | -0.099 | 1,705 | 708 | 51.9% | 7.92 | 39.6% | 24.0% | 15.2% | 12.5% | 8.8% |
| Q3 | +0.263 | 1,889 | 715 | 52.1% | 8.07 | 31.1% | 30.6% | 18.2% | 10.9% | 9.2% |
| Q4 (highest) | +1.231 | 4,137 | 703 | 53.0% | 7.54 | 8.0% | 41.9% | 17.5% | 21.3% | 11.3% |

### Table C.5: CLAN --- Female

| Quartile | CATE | Pop. Density | Fleet/1000 | % Female | DTR (C) | % North | % NE | % CO | % SE | % South |
|----------|------|-------------|------------|----------|---------|---------|------|------|------|---------|
| Q1 (lowest) | -1.205 | 3,659 | 687 | 52.6% | 6.63 | 18.7% | 44.8% | 9.5% | 16.2% | 10.8% |
| Q2 | -0.150 | 1,965 | 710 | 52.2% | 7.86 | 31.2% | 31.4% | 16.7% | 12.5% | 8.3% |
| Q3 | +0.337 | 2,118 | 735 | 52.1% | 8.09 | 30.0% | 26.0% | 18.9% | 13.3% | 11.9% |
| Q4 (highest) | +1.446 | 3,206 | 681 | 52.6% | 7.61 | 21.4% | 32.5% | 14.5% | 17.6% | 13.9% |

### Table C.6: CLAN --- Male

| Quartile | CATE | Pop. Density | Fleet/1000 | % Female | DTR (C) | % North | % NE | % CO | % SE | % South |
|----------|------|-------------|------------|----------|---------|---------|------|------|------|---------|
| Q1 (lowest) | -1.099 | 2,720 | 655 | 52.3% | 6.47 | 34.7% | 32.8% | 8.6% | 14.8% | 9.0% |
| Q2 | -0.110 | 2,117 | 740 | 52.1% | 8.36 | 30.4% | 33.6% | 17.8% | 11.0% | 7.2% |
| Q3 | +0.488 | 2,337 | 714 | 52.4% | 7.77 | 26.9% | 33.2% | 16.4% | 11.5% | 12.0% |
| Q4 (highest) | +2.000 | 3,776 | 704 | 52.8% | 7.59 | 9.2% | 35.0% | 16.9% | 22.3% | 16.5% |

---

\newpage

## Appendix D: City-Level CATE Estimates

### Table D.1: Mean CATE by Capital (Total Respiratory Admissions)

| City | UF | Region | Mean CATE | Median CATE | SD | N obs | Mean daily admissions |
|------|----|---------|-----------|-----------|----|-------|----------------------|
| Sao Paulo | SP | SE | **+3.126** | +4.452 | 4.886 | 1,247 | 150.5 |
| Brasilia | DF | CO | +2.090 | +1.635 | 2.199 | 1,247 | 54.6 |
| Porto Alegre | RS | S | +1.469 | +1.403 | 1.981 | 1,241 | 41.5 |
| Salvador | BA | NE | +1.382 | +0.937 | 2.423 | 1,246 | 29.9 |
| Campo Grande | MS | CO | +1.152 | +1.093 | 1.027 | 1,237 | 14.6 |
| Aracaju | SE | NE | +0.895 | +0.784 | 1.226 | 1,245 | 13.3 |
| Maceio | AL | NE | +0.822 | +0.393 | 1.495 | 1,245 | 11.6 |
| Rio de Janeiro | RJ | SE | +0.775 | +0.709 | 1.063 | 1,247 | 43.4 |
| Florianopolis | SC | S | +0.743 | +0.861 | 1.332 | 1,241 | 14.5 |
| Belem | PA | N | +0.726 | +0.790 | 2.331 | 1,231 | 24.4 |
| Fortaleza | CE | NE | +0.536 | +0.123 | 3.597 | 1,246 | 45.7 |
| Natal | RN | NE | +0.422 | +0.256 | 1.550 | 1,244 | 13.3 |
| Goiania | GO | CO | +0.326 | +0.339 | 0.774 | 1,247 | 21.2 |
| Porto Velho | RO | N | +0.257 | +0.258 | 0.633 | 1,215 | 6.4 |
| Rio Branco | AC | N | +0.241 | +0.275 | 0.379 | 1,199 | 5.0 |
| Palmas | TO | N | +0.178 | +0.149 | 0.552 | 1,163 | 4.9 |
| Macapa | AP | N | +0.142 | +0.518 | 1.517 | 1,232 | 7.0 |
| Belo Horizonte | MG | SE | +0.060 | +0.119 | 2.582 | 1,246 | 47.2 |
| Teresina | PI | NE | +0.051 | +0.028 | 0.436 | 1,245 | 14.1 |
| Joao Pessoa | PB | NE | -0.282 | -0.002 | 1.402 | 1,243 | 19.0 |
| Recife | PE | NE | -0.364 | -0.600 | 1.727 | 1,246 | 52.3 |
| Vitoria | ES | SE | -0.389 | -0.366 | 0.577 | 1,221 | 6.3 |
| Curitiba | PR | S | -0.461 | -0.295 | 2.386 | 1,245 | 44.4 |
| Manaus | AM | N | -0.551 | -1.048 | 1.997 | 1,234 | 31.1 |
| Cuiaba | MT | CO | -0.555 | -0.425 | 1.062 | 1,232 | 8.9 |
| Sao Luis | MA | NE | -0.949 | -0.862 | 1.012 | 1,244 | 17.3 |
| Boa Vista | RR | N | **-1.525** | -1.915 | 1.420 | 1,151 | 10.9 |

Note: Sorted by mean CATE (descending). Bold indicates highest and lowest values. All 27 state capitals included.

---

\newpage

## Appendix E: SHAP Feature Importance

### Table E.1: Mean Absolute SHAP Values for CATE Heterogeneity (Total Respiratory Admissions)

| Rank | Feature | Mean |SHAP| | Description |
|------|---------|----------------|-------------|
| 1 | pop_density | 0.676 | Population density (inhabitants/km2) |
| 2 | dtr | 0.608 | Diurnal temperature range (C) |
| 3 | pct_female | 0.371 | Proportion female in population |
| 4 | fleet_per_capita | 0.291 | Vehicles per 1,000 inhabitants |
| 5 | region_CO | 0.059 | Central-West region indicator |
| 6 | region_NE | 0.037 | Northeast region indicator |
| 7 | region_S | 0.033 | South region indicator |
| 8 | region_SE | 0.026 | Southeast region indicator |
| 9 | region_N | 0.016 | North region indicator |

Note: SHAP values decompose heterogeneity in Conditional Average Treatment Effects, not outcome prediction. Higher values indicate greater contribution to CATE variation across observations.

---

\newpage

## Appendix F: Policy Counterfactuals

### Table F.1: Prevented Admissions by City Under WHO Compliance (PM2.5 <= 15 ug/m3)

| City | Total admissions | Treated days | Prevented admissions | Mean CATE | Prevented (%) |
|------|-----------------|-------------|---------------------|-----------|---------------|
| Sao Paulo | 187,646 | 864 | 2,860.8 | +3.126 | 1.52% |
| Rio de Janeiro | 54,132 | 862 | 710.6 | +0.775 | 1.31% |
| Porto Alegre | 51,476 | 236 | 341.5 | +1.469 | 0.66% |
| Belo Horizonte | 58,791 | 177 | 224.5 | +0.060 | 0.38% |
| Curitiba | 55,219 | 147 | 157.0 | -0.461 | 0.28% |
| Rio Branco | 5,975 | 286 | 119.8 | +0.241 | 2.01% |
| Brasilia | 68,030 | 40 | 93.0 | +2.090 | 0.14% |
| Campo Grande | 18,030 | 87 | 75.5 | +1.152 | 0.42% |
| Florianopolis | 18,049 | 61 | 44.1 | +0.743 | 0.24% |
| Goiania | 26,479 | 86 | 38.9 | +0.326 | 0.15% |
| Palmas | 5,737 | 117 | 38.7 | +0.178 | 0.67% |
| Salvador | 37,235 | 13 | 26.3 | +1.382 | 0.07% |
| Natal | 16,487 | 20 | 14.0 | +0.422 | 0.08% |
| Macapa | 8,568 | 18 | 12.4 | +0.142 | 0.15% |
| Maceio | 14,504 | 6 | 3.1 | +0.822 | 0.02% |
| Aracaju | 16,572 | 1 | -1.0 | +0.895 | -0.01% |
| Teresina | 17,608 | 96 | -2.3 | +0.051 | -0.01% |
| Belem | 29,976 | 42 | -4.1 | +0.726 | -0.01% |
| Cuiaba | 10,923 | 161 | -28.2 | -0.555 | -0.26% |
| Porto Velho | 7,818 | 365 | -27.3 | +0.257 | -0.35% |
| Fortaleza | 56,908 | 50 | -30.8 | +0.536 | -0.05% |
| Joao Pessoa | 23,623 | 55 | -33.3 | -0.282 | -0.14% |
| Recife | 65,112 | 68 | -37.2 | -0.364 | -0.06% |
| Sao Luis | 21,545 | 38 | -21.8 | -0.949 | -0.10% |
| Vitoria | 7,730 | 175 | -38.8 | -0.389 | -0.50% |
| Boa Vista | 12,550 | 78 | -119.8 | -1.525 | -0.95% |
| Manaus | 38,391 | 355 | -248.2 | -0.551 | -0.65% |
| **Total** | **935,114** | **4,504** | **4,167.6** | -- | **0.45%** |

Note: Negative prevented admissions indicate cities where the CATE is negative, suggesting possible harvesting effects or unmeasured protective factors. Treated days = days PM2.5 exceeded 15 ug/m3. All 27 state capitals included.

### Table F.2: Prevented Admissions by CATE Vulnerability Quartile

| Quartile | N obs | Total admissions | Treated days | Prevented admissions | Mean CATE | Prevented (%) |
|----------|-------|-----------------|-------------|---------------------|-----------|---------------|
| Q1 (least vulnerable) | 8,321 | 261,686 | 948 | -2,022.5 | -1.944 | -0.77% |
| Q2 | 8,322 | 157,350 | 984 | -185.6 | -0.199 | -0.12% |
| Q3 | 8,318 | 174,713 | 1,173 | +742.6 | +0.658 | +0.43% |
| Q4 (most vulnerable) | 8,319 | 341,365 | 1,399 | +5,633.2 | +3.044 | +1.65% |

Note: The Q4 quartile alone accounts for 5,633 of the 4,168 net prevented admissions. The net total is lower because Q1 and Q2 show negative prevented admissions.

### Table F.3: Dose-Response Policy Curve --- Alternative Thresholds

| Threshold (ug/m3) | Exceedance days | Exceedance (%) | Prevented admissions | Prevented (%) |
|-------------------|----------------|----------------|---------------------|---------------|
| 15 (WHO AQG) | 4,504 | 13.53% | 4,167.6 | 0.45% |
| 25 (CONAMA intermediate) | 1,487 | 4.47% | 1,805.0 | 0.19% |
| 35 (CONAMA final) | 660 | 1.98% | 575.5 | 0.06% |
| 50 (pre-2024 standard) | 256 | 0.77% | 122.0 | 0.01% |

### Table F.4: Bootstrap Confidence Interval for Prevented Fraction

| Metric | Value |
|--------|-------|
| Mean prevented (%) | 0.44% |
| 95% CI lower | 0.41% |
| 95% CI upper | 0.48% |
| Bootstrap resamples | 1,000 |

---

\newpage

## Appendix G: Cost Estimation

### Table G.1: Economic Impact of WHO Compliance

| Metric | Value |
|--------|-------|
| Total SUS respiratory costs (study period) | R$ 1,815,748,569 |
| Total admissions | 935,114 |
| Mean cost per admission | R$ 1,941.74 |
| Prevented admissions (WHO scenario) | 4,167.6 |
| Saved costs | R$ 8,092,492 |
| Saved costs (% of total) | 0.45% |
| Saved costs (USD, approx.) | USD 1,619,000 |

Note: Costs based on SIH/SUS reimbursement data. USD conversion at approximate 2024 exchange rate of R$5.00/USD.

---

\newpage

## Appendix H: Sensitivity and Robustness Analyses

### Table H.1: Placebo Test (PM2.5 at t+7)

| Metric | Value |
|--------|-------|
| Test | Future PM2.5 (7-day lead) as placebo treatment |
| ATE | -0.534 |
| 95% CI | [-5.727, 4.660] |
| p-value | 0.840 |
| Result | **Passed** (null effect of future pollution on current admissions) |

### Table H.2: Leave-One-City-Out Jackknife

| Excluded city | ATE | 95% CI | p-value | N rows |
|--------------|-----|--------|---------|--------|
| Aracaju | 0.595 | [-4.795, 5.984] | 0.829 | 32,035 |
| Belo Horizonte | 0.653 | [-5.105, 6.411] | 0.824 | 32,034 |
| Belem | 0.475 | [-5.094, 6.043] | 0.867 | 32,049 |
| Boa Vista | 0.532 | [-5.233, 6.298] | 0.856 | 32,129 |
| Brasilia | 0.354 | [-4.986, 5.694] | 0.897 | 32,033 |
| Campo Grande | 0.592 | [-5.292, 6.477] | 0.844 | 32,043 |
| Cuiaba | 0.509 | [-4.962, 5.979] | 0.855 | 32,048 |
| Curitiba | 0.609 | [-4.588, 5.806] | 0.818 | 32,035 |
| Florianopolis | 0.357 | [-5.117, 5.830] | 0.898 | 32,039 |
| Fortaleza | 0.551 | [-4.580, 5.681] | 0.833 | 32,034 |
| Goiania | 0.418 | [-5.294, 6.130] | 0.886 | 32,033 |
| Joao Pessoa | 0.474 | [-4.974, 5.922] | 0.865 | 32,037 |
| Macapa | 0.534 | [-4.983, 6.050] | 0.850 | 32,048 |
| Maceio | 0.642 | [-4.916, 6.200] | 0.821 | 32,035 |
| Manaus | 0.545 | [-5.134, 6.224] | 0.851 | 32,046 |
| Natal | 0.479 | [-5.123, 6.081] | 0.867 | 32,036 |
| Palmas | 0.614 | [-4.857, 6.084] | 0.826 | 32,117 |
| Porto Alegre | 0.479 | [-4.809, 5.768] | 0.859 | 32,039 |
| Porto Velho | 0.643 | [-4.972, 6.258] | 0.823 | 32,065 |
| Recife | 0.540 | [-4.914, 5.993] | 0.846 | 32,034 |
| Rio Branco | 0.533 | [-5.022, 6.087] | 0.851 | 32,081 |
| Rio de Janeiro | 0.516 | [-5.198, 6.229] | 0.860 | 32,033 |
| Salvador | 0.616 | [-4.661, 5.892] | 0.819 | 32,034 |
| Sao Luis | 0.574 | [-4.897, 6.046] | 0.837 | 32,036 |
| Sao Paulo | **0.168** | [-4.132, 4.469] | 0.939 | 32,033 |
| Teresina | 0.553 | [-5.403, 6.509] | 0.856 | 32,035 |
| Vitoria | **0.646** | [-5.031, 6.324] | 0.823 | 32,059 |

| Summary statistic | Value |
|-------------------|-------|
| Minimum ATE | 0.168 (excl. Sao Paulo) |
| Maximum ATE | 0.653 (excl. Belo Horizonte) |
| Mean ATE | 0.526 |
| Coefficient of variation | 0.21 |

Note: Bold indicates minimum and maximum ATE values. No single city exclusion changes the direction of the main finding. All 27 capitals included in jackknife analysis.

### Table H.3: Threshold Sensitivity (Causal Forest ATE)

| Threshold (ug/m3) | ATE | 95% CI | p-value | Treatment prevalence |
|-------------------|-----|--------|---------|---------------------|
| 15 (primary) | 0.533 | [-4.602, 5.669] | 0.839 | 13.53% |
| 25 | 0.840 | [-14.721, 16.401] | 0.916 | 4.47% |
| 35 | 1.003 | [-21.622, 23.628] | 0.931 | 1.98% |
| 50 | -- | -- | -- | 0.77% (skipped, insufficient variation) |

Note: As the threshold increases, treatment prevalence decreases and confidence intervals widen substantially, reflecting reduced statistical power.

### Table H.4: Omitted Variable Bias Analysis

| Metric | Value |
|--------|-------|
| R2 of Y given W (observed confounders) | 0.1978 |
| Pseudo-R2 of T given W | 0.1040 |
| Residual variance of Y | 0.8022 |
| Residual variance of T | 0.8960 |
| **Robustness value** | **0.8478** |
| Interpretation | An unobserved confounder would need partial R2 of at least 0.848 with both Y and T (after controlling for observed confounders) to reduce the ATE to zero. |

Note: The robustness value of 0.848 indicates that any unobserved confounder would need to explain more variance than the entire set of observed confounders combined --- an implausibly strong requirement.

---

\newpage

## Appendix I: Figures

### Figure S1: CATE Map of Brazil

Geospatial map of estimated Conditional Average Treatment Effects (CATEs) across all 27 Brazilian state capitals. Colour represents CATE magnitude (blue = negative/low, red = high).

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

Bar chart showing prevented respiratory hospitalisations under WHO compliance for each of the 27 state capitals, sorted by magnitude.

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
