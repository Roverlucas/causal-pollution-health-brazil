# Methods Specification

> **Project:** Causal Pollution-Health Brazil (CPH-BR-2026)
> **Authors:** Lucas Rover, Yara de Souza Tadano
> **Version:** 1.0 (2026-02-22)
> **Status:** Pre-analysis specification (locked before data analysis)
> **Target:** The Lancet Planetary Health

---

## 2.1 Study Design and Setting

### Design

We conduct a multi-city ecological time-series study with causal machine learning inference. The unit of analysis is the city-day: a unique combination of state capital and calendar date, with health outcomes further stratified by age group (0--14, 15--59, 60+ years) and sex (male, female). This design exploits day-to-day variation in air pollution exposure within cities, conditional on meteorological and temporal confounders, to estimate heterogeneous causal effects on respiratory hospitalizations.

### Setting

The study encompasses all 27 Brazilian state capitals, spanning five macro-regions and four climate zones (equatorial, tropical, semi-arid, and subtropical). Together these capitals represent approximately 53.2 million inhabitants (26% of the national population) and concentrate the majority of Brazil's ground-level air quality monitoring infrastructure.

### Study Population

The 27 state capitals, with populations from IBGE Census 2022, are listed below by macro-region:

#### Norte (7 capitals)

| Capital | State (UF) | Population (2022) | Latitude | Longitude |
|---------|------------|-------------------|----------|-----------|
| Manaus | AM | 2,255,903 | -3.119 | -60.022 |
| Belem | PA | 1,393,399 | -1.456 | -48.490 |
| Porto Velho | RO | 548,952 | -8.761 | -63.900 |
| Macapa | AP | 522,357 | 0.035 | -51.069 |
| Boa Vista | RR | 436,591 | 2.824 | -60.676 |
| Rio Branco | AC | 413,418 | -9.975 | -67.825 |
| Palmas | TO | 313,349 | -10.169 | -48.332 |

#### Nordeste (9 capitals)

| Capital | State (UF) | Population (2022) | Latitude | Longitude |
|---------|------------|-------------------|----------|-----------|
| Salvador | BA | 2,900,319 | -12.971 | -38.501 |
| Fortaleza | CE | 2,703,391 | -3.717 | -38.543 |
| Recife | PE | 1,488,920 | -8.048 | -34.877 |
| Sao Luis | MA | 1,037,775 | -2.531 | -44.307 |
| Maceio | AL | 1,025,360 | -9.666 | -35.735 |
| Campo Grande* | -- | -- | -- | -- |
| Teresina | PI | 866,300 | -5.089 | -42.802 |
| Joao Pessoa | PB | 833,932 | -7.120 | -34.845 |
| Natal | RN | 751,300 | -5.795 | -35.211 |
| Aracaju | SE | 602,757 | -10.947 | -37.073 |

#### Centro-Oeste (4 capitals)

| Capital | State (UF) | Population (2022) | Latitude | Longitude |
|---------|------------|-------------------|----------|-----------|
| Brasilia | DF | 2,817,068 | -15.794 | -47.882 |
| Goiania | GO | 1,437,237 | -16.687 | -49.265 |
| Campo Grande | MS | 898,092 | -20.470 | -54.620 |
| Cuiaba | MT | 676,468 | -15.601 | -56.098 |

#### Sudeste (4 capitals)

| Capital | State (UF) | Population (2022) | Latitude | Longitude |
|---------|------------|-------------------|----------|-----------|
| Sao Paulo | SP | 11,451,999 | -23.551 | -46.633 |
| Rio de Janeiro | RJ | 6,211,423 | -22.907 | -43.173 |
| Belo Horizonte | MG | 2,315,560 | -19.917 | -43.935 |
| Vitoria | ES | 336,261 | -20.316 | -40.313 |

#### Sul (3 capitals)

| Capital | State (UF) | Population (2022) | Latitude | Longitude |
|---------|------------|-------------------|----------|-----------|
| Curitiba | PR | 1,948,626 | -25.428 | -49.273 |
| Porto Alegre | RS | 1,332,570 | -30.035 | -51.218 |
| Florianopolis | SC | 537,213 | -27.595 | -48.548 |

**Total study population:** approximately 53.2 million inhabitants across 27 capitals.

### Study Period

January 1, 2022 through December 31, 2025 (1,461 days). This window is determined by the intersection of all five data sources: air quality data from CAMS/Copernicus is available only from January 2022, while hospitalization data from SIH/SUS extends through December 2025. The four-year period provides sufficient temporal depth for seasonal adjustment while capturing critical events including the 2024 wildfire season and the implementation of CONAMA Resolution 506/2024.

### Data Platform

All data are extracted from the Clima360 Brasil platform (https://github.com/Roverlucas/clima-360-brasil), a purpose-built data integration system that merges five national and international sources into a unified, quality-controlled database with daily granularity across all 27 capitals.

---

## 2.2 Data Sources

### 2.2.1 Meteorological Data (Weather)

| Attribute | Detail |
|-----------|--------|
| **Provider** | Open-Meteo Archive API |
| **Source model** | ERA5/ERA5-Land reanalysis (ECMWF) |
| **Table** | `weather_history` |
| **Temporal coverage** | 2015-01-01 to 2026-02-07 (analysis window: 2022--2025) |
| **Spatial coverage** | 24/27 capitals with complete records (3 capitals with partial data backfilled from ERA5-Land nearest-grid) |
| **Granularity** | Daily |
| **Total records** | 63,963 (full database); approximately 35,000 within analysis window |

**Variables (19):**

| Variable | Unit | Description |
|----------|------|-------------|
| `temperature_max` | degrees C | Daily maximum temperature |
| `temperature_min` | degrees C | Daily minimum temperature |
| `temperature_mean` | degrees C | Daily mean temperature |
| `apparent_temperature_max` | degrees C | Maximum apparent temperature (heat index) |
| `apparent_temperature_min` | degrees C | Minimum apparent temperature (wind chill) |
| `precipitation_sum` | mm | Total daily precipitation |
| `rain_sum` | mm | Total daily rainfall (excluding snow) |
| `precipitation_hours` | hours | Hours with precipitation > 0.1 mm |
| `wind_speed_max` | km/h | Maximum 10m wind speed |
| `wind_gusts_max` | km/h | Maximum wind gust speed |
| `wind_direction_dominant` | degrees | Dominant wind direction |
| `relative_humidity_mean` | % | Mean relative humidity |
| `pressure_mean` | hPa | Mean sea-level pressure |
| `shortwave_radiation_sum` | MJ/m2 | Cumulative shortwave radiation |
| `et0_fao_evapotranspiration` | mm | FAO reference evapotranspiration |
| `uv_index_max` | index | Maximum UV index |
| `sunrise` | timestamp | Sunrise time |
| `sunset` | timestamp | Sunset time |
| `daylight_duration` | seconds | Duration of daylight |

**Quality control:** Records with fewer than 18 of 24 hourly observations contributing to the daily aggregate are flagged. Open-Meteo Archive API uses ERA5 reanalysis data, which undergoes quality control at ECMWF including automated checks for internal consistency, temporal continuity, and spatial coherence. For the 3 capitals with gaps (Porto Alegre, Teresina, Vitoria), we use ERA5-Land nearest-gridpoint data interpolated to municipal centroid coordinates.

### 2.2.2 Air Quality Data

| Attribute | Detail |
|-----------|--------|
| **Provider** | Copernicus Atmosphere Monitoring Service (CAMS), accessed via Open-Meteo Air Quality API |
| **Source model** | CAMS global reanalysis (EAC4) and near-real-time forecasts |
| **Table** | `air_quality_history` |
| **Temporal coverage** | 2022-01-01 to 2026-02-11 (analysis window: 2022--2025) |
| **Spatial coverage** | 27/27 capitals (100% complete) |
| **Granularity** | Daily (aggregated from hourly CAMS output) |
| **Total records** | 40,581 |

**Variables (7 pollutants + AQI):**

| Variable | Unit | Description |
|----------|------|-------------|
| `pm25` | micrograms/m3 | Particulate matter < 2.5 micrometers (daily mean) |
| `pm10` | micrograms/m3 | Particulate matter < 10 micrometers (daily mean) |
| `o3` | micrograms/m3 | Ozone (daily mean) |
| `no2` | micrograms/m3 | Nitrogen dioxide (daily mean) |
| `so2` | micrograms/m3 | Sulfur dioxide (daily mean) |
| `co` | micrograms/m3 | Carbon monoxide (daily mean) |
| `aqi` | US EPA index | Air Quality Index (computed from PM2.5 per US EPA standard) |
| `dominant_pollutant` | categorical | Pollutant with highest relative concentration |

**Quality control:** Each daily record is classified as `good` (>=12 hours of hourly data contributing) or `partial` (<12 hours). Primary analyses use only `good`-quality days; sensitivity analyses include `partial` days. CAMS reanalysis has been validated against ground-based monitors globally, with PM2.5 showing correlation r=0.7--0.9 depending on region. In Brazil, validation against CETESB (Sao Paulo) monitors shows mean bias of -2.1 micrograms/m3 for PM2.5.

**Limitations:** CAMS data are modeled reanalysis, not direct ground measurements. Spatial resolution is approximately 40 km, which may introduce exposure misclassification. This is addressed in sensitivity analyses (Section 2.9).

### 2.2.3 Hospitalization Data (Health Outcomes)

| Attribute | Detail |
|-----------|--------|
| **Provider** | Hospital Information System of the Unified Health System (SIH/SUS), Ministry of Health, Brazil |
| **Data system** | DATASUS, accessed via PySUS pipeline |
| **Table** | `health_hospitalizations` |
| **Temporal coverage** | 2014-03-26 to 2025-12-31 (analysis window: 2022--2025) |
| **Spatial coverage** | 27/27 capitals |
| **Granularity** | Daily, stratified by ICD category, age group, and sex |
| **Total records** | 196,369 |
| **Total admissions** | 6.16 million (all categories) |
| **Total deaths** | 526,000 |
| **Total cost** | R$ 18.59 billion |

**Variables:**

| Variable | Type | Description |
|----------|------|-------------|
| `admissions` | count | Total Hospitalization Authorization Forms (AIH) approved |
| `deaths` | count | In-hospital deaths |
| `total_cost` | BRL | Total hospitalization cost (SIH/SUS reimbursement) |
| `admissions_male` / `admissions_female` | count | Admissions by sex |
| `admissions_age_0_14` | count | Admissions, age 0--14 years |
| `admissions_age_15_59` | count | Admissions, age 15--59 years |
| `admissions_age_60_plus` | count | Admissions, age 60+ years |
| `deaths_male` / `deaths_female` | count | Deaths by sex |
| `deaths_age_0_14` / `deaths_age_15_59` / `deaths_age_60_plus` | count | Deaths by age group |
| `cid_category` | categorical | `respiratory` (ICD-10 J00--J99) or `cardiovascular` (ICD-10 I00--I99) |

**ICD-10 codes for respiratory outcomes:** J00--J99, encompassing acute upper respiratory infections (J00--J06), influenza and pneumonia (J09--J18), other acute lower respiratory infections (J20--J22), chronic lower respiratory diseases (J40--J47), and other diseases of the respiratory system (J60--J99).

**Quality control:** SIH/SUS data undergo retroactive revisions as late claims are processed. The Clima360 Data Vintage Tracking system (`health_revision_log` table) monitors weekly revisions and computes stability metrics. Data aged less than 6 months are flagged as potentially incomplete. For the analysis window (2022--2025), data from 2025 are restricted to records aged >= 6 months at the time of extraction (extraction date: February 2026). Revision rates for data aged > 6 months are below 2% for admissions counts, based on audit data.

**Coverage:** SIH/SUS covers approximately 75% of all hospitalizations in Brazil (the remainder occur in the private sector). Coverage is higher in northern and northeastern capitals (>85%) and lower in southeastern capitals with larger private healthcare markets (~65% in Sao Paulo). This differential coverage is addressed as a limitation.

### 2.2.4 Demographic Data

| Attribute | Detail |
|-----------|--------|
| **Provider** | IBGE (Brazilian Institute of Geography and Statistics), SIDRA system |
| **Table** | `demographics_history` |
| **Temporal coverage** | 1970--2025 (analysis window uses 2022 Census and annual estimates) |
| **Spatial coverage** | 27/27 capitals |
| **Granularity** | Annual |
| **Total records** | 430 |

**Variables (11):**

| Variable | Unit | Description |
|----------|------|-------------|
| `population` | count | Total population |
| `pop_male` | count | Male population |
| `pop_female` | count | Female population |
| `pop_0_14` | count | Population aged 0--14 years |
| `pop_15_59` | count | Population aged 15--59 years |
| `pop_60_plus` | count | Population aged 60+ years |
| `pop_urban` | count | Urban population |
| `pop_rural` | count | Rural population |
| `density` | inhabitants/km2 | Population density |
| `growth_rate` | % per year | Annual population growth rate |
| `source` | text | Data source identifier |

**Quality:** Based on the 2022 Population Census, the most recent complete enumeration of the Brazilian population. Inter-censal years (2023--2025) use IBGE official projections. Age-group breakdowns enable computation of rates per 100,000 by stratum.

### 2.2.5 Vehicle Fleet Data

| Attribute | Detail |
|-----------|--------|
| **Provider** | SENATRAN (National Secretariat of Transit), Ministry of Transport |
| **Table** | `fleet_history` |
| **Temporal coverage** | 2010--2023 |
| **Spatial coverage** | 27/27 capitals |
| **Granularity** | Annual (monthly snapshots, using December of each year) |
| **Total records** | 108 |

**Variables (9):**

| Variable | Unit | Description |
|----------|------|-------------|
| `fleet_total` | count | Total registered vehicles |
| `fleet_automobile` | count | Passenger cars |
| `fleet_motorcycle` | count | Motorcycles |
| `fleet_truck` | count | Trucks and heavy vehicles |
| `fleet_bus` | count | Buses |
| `fleet_utility` | count | Utility vehicles (SUVs, vans) |
| `fleet_tractor` | count | Tractors |
| `fleet_trailer` | count | Trailers and semi-trailers |
| `fleet_other` | count | Other vehicle categories |

**Derived variable:** `fleet_per_capita` = `fleet_total` / `population` (matched by city and year). For analysis years 2024--2025, fleet data are forward-filled from the 2023 value, as SENATRAN publication has a 1--2 year lag. This is justified because fleet growth rates in Brazilian capitals averaged 3.2% per year (2018--2023), introducing at most a 6% underestimate that is nearly constant across cities.

---

## 2.3 Variable Definitions

### 2.3.1 Treatment Variable

| Variable | Name | Definition | Threshold | Source |
|----------|------|------------|-----------|--------|
| **Primary** | `pm25_exceed` | Binary indicator: 1 if daily mean PM2.5 > 15 micrograms/m3, 0 otherwise | 15 micrograms/m3 (WHO AQG 2021, 24-hour guideline) | `air_quality_history.pm25` |
| Secondary | `o3_exceed` | Binary indicator: 1 if daily mean O3 > 100 micrograms/m3, 0 otherwise | 100 micrograms/m3 (WHO AQG 2021, 8-hour guideline) | `air_quality_history.o3` |
| Sensitivity | `pm25_continuous` | Continuous daily mean PM2.5 (micrograms/m3) | N/A (dose-response) | `air_quality_history.pm25` |

**Rationale for primary threshold:** The WHO 2021 Air Quality Guidelines recommend a 24-hour PM2.5 guideline of 15 micrograms/m3, below which health effects are considered minimal. Brazil's CONAMA Resolution 506/2024 sets an intermediate target of 25 micrograms/m3, which is less protective. The WHO threshold is used as the primary treatment definition to maximize policy relevance; alternative thresholds (25, 35, 50 micrograms/m3) are examined in sensitivity analyses.

### 2.3.2 Outcome Variables

All outcomes are daily counts of respiratory hospitalizations (ICD-10 J00--J99) by stratum:

| Variable | Definition | Denominator for rate |
|----------|-----------|---------------------|
| `resp_total` | Total respiratory admissions on day *t* in city *c* | Total population |
| `resp_0_14` | Respiratory admissions, age 0--14 years | Population 0--14 |
| `resp_15_59` | Respiratory admissions, age 15--59 years | Population 15--59 |
| `resp_60plus` | Respiratory admissions, age 60+ years | Population 60+ |
| `resp_male` | Respiratory admissions, male | Male population |
| `resp_female` | Respiratory admissions, female | Female population |

**Primary outcome:** `resp_total` (total daily respiratory hospitalizations).
**Secondary outcomes:** Age-stratified (`resp_0_14`, `resp_15_59`, `resp_60plus`) and sex-stratified (`resp_male`, `resp_female`).

### 2.3.3 Confounders (W)

Confounders are variables that plausibly cause both the treatment (pollution level) and the outcome (hospitalizations). They must be adjusted for to achieve conditional ignorability.

| Variable | Definition | Type | Lag | Source |
|----------|-----------|------|-----|--------|
| `temp_mean` | Daily mean temperature (degrees C) | Continuous | 0 | `weather_history` |
| `temp_dtr` | Diurnal temperature range: T_max - T_min (degrees C) | Continuous | 0 | Derived from `weather_history` |
| `humidity_mean` | Relative humidity, daily mean (%) | Continuous | 0 | `weather_history` |
| `pressure_mean` | Sea-level pressure, daily mean (hPa) | Continuous | 0 | `weather_history` |
| `wind_speed_max` | Maximum wind speed (km/h) | Continuous | 0 | `weather_history` |
| `precip_sum` | Total daily precipitation (mm) | Continuous | 0 | `weather_history` |
| `dow` | Day of week (1=Monday, ..., 7=Sunday) | Categorical (6 dummies) | -- | Derived |
| `holiday` | National or state holiday indicator (0/1) | Binary | -- | Derived (manual list) |
| `sin_annual` | sin(2 * pi * day_of_year / 365.25) | Continuous | -- | Derived |
| `cos_annual` | cos(2 * pi * day_of_year / 365.25) | Continuous | -- | Derived |
| `sin_semi` | sin(4 * pi * day_of_year / 365.25) | Continuous | -- | Derived |
| `cos_semi` | cos(4 * pi * day_of_year / 365.25) | Continuous | -- | Derived |
| `trend` | Linear time trend (integer: day number from study start) | Continuous | -- | Derived |

**Justification for confounder set:**
- **Temperature and DTR:** Temperature directly affects both pollutant concentrations (through atmospheric stability, photochemistry) and respiratory health (cold stress, heat stress). DTR captures within-day thermal stress, which is independently associated with respiratory morbidity.
- **Humidity:** Affects particle hygroscopic growth (increasing PM2.5 mass) and respiratory mucosa function.
- **Pressure:** Proxy for synoptic meteorological patterns (inversions, frontal passages) that simultaneously trap pollutants and trigger respiratory episodes.
- **Wind speed:** Higher wind dilutes pollutants; also affects pollen dispersion and windchill.
- **Precipitation:** Wet scavenging removes particles; also affects outdoor activity patterns.
- **Day of week and holidays:** Hospital admission patterns vary systematically by weekday (elective admissions concentrated Monday--Friday; emergency admissions more uniform). Pollution also varies by weekday (traffic patterns).
- **Fourier harmonics:** Capture annual and semi-annual seasonal cycles in both pollution (dry season, biomass burning) and respiratory disease (winter viral epidemics, dry-season allergies).
- **Linear trend:** Accounts for long-term secular trends in both health system capacity and pollution control measures (PROCONVE fleet renewal).

### 2.3.4 Effect Modifiers (X)

Effect modifiers are variables along which the causal effect may differ. These define the heterogeneity dimensions of interest and are inputs to the causal forest for CATE estimation.

| Variable | Definition | Type | Source |
|----------|-----------|------|--------|
| `age_group` | 0--14, 15--59, 60+ | Categorical (3 levels) | `health_hospitalizations` |
| `sex` | Male, Female | Binary | `health_hospitalizations` |
| `city` | Capital identifier (27 levels) | Categorical | -- |
| `region` | Macro-region: N, NE, CO, SE, S | Categorical (5 levels) | `capitals.ts` |
| `fleet_per_capita` | Fleet total / population | Continuous (or terciles) | `fleet_history` + `demographics_history` |
| `pop_density` | Population / area (inhabitants/km2) | Continuous (or terciles) | `demographics_history` |
| `dtr_quantile` | Tercile of diurnal temperature range (low/medium/high) | Ordinal (3 levels) | Derived from `weather_history` |
| `pct_elderly` | Proportion of population aged 60+ (%) | Continuous | `demographics_history` |

---

## 2.4 Causal Framework

### 2.4.1 Directed Acyclic Graph (DAG)

The causal structure is represented by the following DAG:

```
                    ┌──────────────────────────────────┐
                    │     Unmeasured Confounders (U)    │
                    │  (indoor exposure, smoking prev., │
                    │   healthcare access, SES)         │
                    └────────────┬─────────┬───────────┘
                                 │         │
                                 v         v
┌─────────────────┐    ┌────────────────┐    ┌────────────────────┐
│   Weather (W)   │───>│  PM2.5 > 15    │───>│  Respiratory       │
│  temp, humidity, │    │  (Treatment A) │    │  Hospitalizations  │
│  pressure, wind, │    └────────────────┘    │  (Outcome Y)       │
│  precipitation   │             ^            └────────────────────┘
└───────┬─────────┘             │                      ^
        │                       │                      │
        │             ┌─────────┴──────┐               │
        └────────────>│  Temporal       │──────────────┘
                      │  Confounders    │
                      │ (season, trend, │
                      │  DOW, holiday)  │
                      └────────────────┘

Effect Modifiers (X): age, sex, city, region, fleet/capita, pop_density, DTR, pct_elderly
    - Modify the A → Y edge (treatment effect heterogeneity)
    - Do NOT confound the A → Y relationship
```

### Causal Paths

1. **Direct causal path (target):** PM2.5 exceedance (A) --> Respiratory hospitalizations (Y). This is the causal effect of interest.

2. **Confounded paths (blocked by conditioning on W):**
   - Weather (W) --> PM2.5 (A) and Weather (W) --> Y. Temperature inversions increase pollution and cold stress increases respiratory disease. Blocked by conditioning on temperature, humidity, pressure, wind, precipitation.
   - Season --> A and Season --> Y. Dry season increases pollution and winter increases respiratory infections. Blocked by Fourier harmonics.
   - Day of week --> A and Day of week --> Y. Traffic patterns affect pollution; hospital admission patterns vary by weekday. Blocked by DOW dummies.
   - Trend --> A and Trend --> Y. Fleet renewal reduces pollution; health system capacity changes affect admissions. Blocked by linear trend.

3. **Effect modification paths (not blocked, intentionally estimated):**
   - Age modifies A --> Y: biological susceptibility (immature/aged respiratory systems).
   - Fleet density modifies A --> Y: proxy for emission source intensity and chronic exposure.
   - DTR modifies A --> Y: synergistic effect of thermal stress and pollution.
   - Region modifies A --> Y: captures unmeasured structural differences (climate zone, healthcare capacity, urbanization).

4. **Unmeasured confounders (U):**
   - Individual-level exposures (indoor air, smoking, occupational), socioeconomic status, healthcare access. These are addressed via sensitivity analysis (Rosenbaum bounds, Section 2.9.4).

### 2.4.2 Identification Assumption: Conditional Ignorability

**Formal statement:** Given the observed confounders W = (temperature, DTR, humidity, pressure, wind speed, precipitation, day of week, holiday, Fourier harmonics, linear trend), the treatment assignment A (PM2.5 exceedance) is independent of potential outcomes:

    Y(1), Y(0) ⊥ A | W

**Interpretation:** Conditional on weather conditions and temporal factors on day *t*, whether PM2.5 exceeds 15 micrograms/m3 is as good as randomly assigned with respect to respiratory hospitalizations. That is, there are no unobserved common causes of both pollution exceedance and hospitalizations that are not already captured in W.

**Justification:** Day-to-day variation in PM2.5 conditional on meteorology is driven by stochastic processes: traffic volume fluctuations, industrial activity variation, distant biomass burning plume transport, and atmospheric mixing-layer dynamics. These factors are plausibly unrelated to individuals' daily health-seeking behavior or respiratory vulnerability, once we condition on weather (which affects both pollutant dispersion and respiratory health) and temporal patterns (which capture seasonal and secular trends). This assumption has been invoked in prior causal inference studies of air pollution, including Deryugina et al. (2019) in the American Economic Review and Bondy et al. (2020) in the Journal of the European Economic Association.

**Threats to identification:** The primary threat is omitted variable bias from unmeasured confounders that jointly affect pollution and health beyond what weather and temporal variables capture. Examples include: (a) viral epidemic onset that increases both healthcare demand and indoor crowding (reducing outdoor activity and potentially outdoor pollution exposure); (b) wildfire events that simultaneously elevate PM2.5 and cause panic-driven emergency visits for non-respiratory complaints that displace respiratory admissions. We address these threats through sensitivity analysis (Rosenbaum bounds, placebo tests, alternative specifications).

### 2.4.3 Positivity Requirement

The positivity (overlap) assumption requires that for every combination of confounders W, there is a positive probability of both treatment states:

    0 < P(A=1 | W=w) < 1 for all w in the support of W

**Verification plan:**
1. Estimate the propensity score e(W) = P(A=1 | W) using XGBoost.
2. Inspect the distribution of propensity scores: verify that no observations have e(W) < 0.01 or e(W) > 0.99.
3. If positivity violations are detected, apply trimming (discard observations outside [0.01, 0.99]) and report the fraction trimmed.
4. Assess overlap visually via histograms of propensity scores by treatment status.

---

## 2.5 Honest Causal Forests

### 2.5.1 Algorithm Overview

We estimate heterogeneous treatment effects using Honest Causal Forests, as developed by Athey, Tibshirani, and Wager (2019). The causal forest is an ensemble of causal trees, each of which partitions the covariate space to maximize treatment effect heterogeneity rather than prediction accuracy.

### 2.5.2 Honesty via Sample Splitting

The defining feature of Honest Causal Forests is the separation of the data used for building the tree structure from the data used for estimating treatment effects within each leaf:

1. **Subsampling:** For each tree, draw a subsample of size *s* from the full dataset without replacement.
2. **Splitting:** Randomly assign half of the subsample (the "splitting sample", I) to determine the tree partition. The splitting criterion maximizes the variance of the estimated treatment effects across child nodes.
3. **Estimation:** Use the other half (the "estimation sample", J) to compute within-leaf treatment effects. This separation ensures that the same data are never used for both choosing where to split and estimating the effect, which provides valid asymptotic confidence intervals.

### 2.5.3 CATE Estimation

For each observation *i* with covariates X_i, the Conditional Average Treatment Effect (CATE) is:

    tau(x) = E[Y(1) - Y(0) | X = x]

The causal forest estimates tau(x) as a weighted average of treatment effect estimates across all trees, where weights are determined by the frequency with which observation *i* falls into the same leaf as the target point *x*. This produces an adaptive, locally-weighted estimator that can capture complex, non-linear heterogeneity patterns without parametric assumptions.

### 2.5.4 Hyperparameters

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| Number of trees (`n_estimators`) | 2,000 | Sufficient for stable estimates; diminishing returns beyond 1,000 per simulation studies |
| Minimum leaf size (`min_leaf_size`) | 20 | Ensures sufficient observations in each leaf for estimation; balances bias-variance |
| Subsample fraction (`subsample_ratio`) | 0.5 | Standard choice; entire subsample split equally between I and J |
| Maximum depth | None (grown to minimum leaf size) | Allows flexible heterogeneity detection |
| Number of confounders drawn at each split | sqrt(p) where p = number of confounders | Standard random forest convention |
| Honesty | True | Required for valid inference |
| Criterion | Heterogeneity (variance of treatment effects) | Maximizes CATE heterogeneity detection |

Hyperparameters will be selected via out-of-bag (OOB) honest estimation error, following the procedure in Athey and Wager (2019). The final model uses the hyperparameter combination that minimizes OOB mean squared error of the CATE estimate.

### 2.5.5 Aggregation: ATE, GATE, and CLAN

**Average Treatment Effect (ATE):**

    ATE = (1/N) * sum_{i=1}^{N} tau_hat(X_i)

The forest-based ATE is computed as the simple average of all individual CATE estimates. Confidence intervals are obtained via the asymptotic normal approximation with honest variance estimates.

**Group Average Treatment Effects (GATE):**

For each subgroup defined by an effect modifier (e.g., age 60+, high-fleet cities), the GATE is:

    GATE_g = (1/N_g) * sum_{i in g} tau_hat(X_i)

We report GATEs for all pre-specified subgroups: 3 age groups, 2 sex categories, 5 regions, 3 fleet density terciles, 3 DTR terciles, and 3 population density terciles.

**Classification Analysis of CATE (CLAN):**

Following Chernozhukov et al. (2018b), we sort observations by their estimated CATE and divide them into quantile-based groups (quintiles). For each group, we compute the mean and confidence interval of the CATE, as well as the mean values of all effect modifiers. This reveals which observable characteristics distinguish the most-affected from the least-affected subpopulations.

### 2.5.6 Best Linear Projection

To decompose the sources of heterogeneity, we compute the Best Linear Projection (BLP) of CATE on the effect modifiers X:

    tau_hat(X_i) = alpha_0 + alpha_1 * age_60plus_i + alpha_2 * fleet_per_capita_i + ... + epsilon_i

The BLP coefficients alpha_k indicate the marginal contribution of each modifier to treatment effect heterogeneity, with standard errors computed via heteroskedasticity-consistent sandwich estimators. This provides a parsimonious summary of which factors most strongly predict differential vulnerability.

### 2.5.7 Calibration Test for Heterogeneity

We apply the calibration test from Chernozhukov et al. (2018b) to assess whether the estimated CATEs contain genuine signal:

- **Test 1 (mean forest prediction):** Tests whether the mean of the CATE estimates is significantly different from zero (i.e., is there an average effect?).
- **Test 2 (differential forest prediction):** Tests whether individuals with higher estimated CATEs indeed experience larger treatment effects (i.e., is the estimated heterogeneity real?). This is the critical test: a significant coefficient on the heterogeneity term confirms that the forest is detecting real variation in treatment effects, not noise.

**Decision rule:** If Test 2 yields p < 0.05, we conclude that treatment effect heterogeneity is statistically significant and proceed with subgroup analyses. If p >= 0.05, we report the ATE only and note the absence of detectable heterogeneity.

### 2.5.8 Software

**Implementation:** `econml.dml.CausalForestDML` from the EconML package (Microsoft Research), version >= 0.15. This implementation combines the Honest Causal Forest with Double Machine Learning for the first-stage nuisance parameter estimation (see Section 2.6), providing doubly-robust CATE estimates.

---

## 2.6 Double Machine Learning (DML)

### 2.6.1 Motivation and Framework

Double Machine Learning, introduced by Chernozhukov et al. (2018), provides a framework for estimating treatment effects using machine learning for nuisance parameter estimation while retaining root-N consistent and asymptotically normal inference for the causal parameter of interest. The key innovation is the Neyman-orthogonal score function, which makes the causal estimate robust to first-stage estimation errors.

### 2.6.2 Neyman-Orthogonal Score

The partially linear model is:

    Y = tau * A + g(W) + epsilon       (outcome equation)
    A = m(W) + nu                       (treatment equation)

where g(W) = E[Y | W] (outcome nuisance function), m(W) = E[A | W] (propensity score), and tau is the ATE. The Neyman-orthogonal moment condition is:

    psi(tau) = (Y - g(W) - tau * (A - m(W))) * (A - m(W)) = 0

This score is orthogonal to perturbations in the nuisance functions g and m, meaning that even if the first-stage ML estimators converge at slower-than-parametric rates, the final estimate of tau converges at the parametric root-N rate.

### 2.6.3 Cross-Fitting

To avoid overfitting bias, we use K-fold cross-fitting:

1. Randomly partition the data into K=5 folds of approximately equal size.
2. For each fold k:
   a. Train the outcome model g_hat(W) and the propensity model m_hat(W) on the other K-1 folds.
   b. Predict g_hat(W_i) and m_hat(W_i) for observations in fold k.
3. Compute the DML estimate of tau using the cross-fitted residuals across all observations.

This procedure ensures that no observation's outcome or treatment is predicted using a model trained on that same observation, eliminating overfitting bias while allowing the full sample to contribute to the final estimate.

### 2.6.4 First-Stage Models

Both first-stage nuisance functions are estimated using XGBoost (Extreme Gradient Boosting):

**Propensity model (treatment):**

| Parameter | Value |
|-----------|-------|
| Objective | Binary logistic (`binary:logistic`) |
| Number of trees | 500 |
| Max depth | 6 |
| Learning rate | 0.05 |
| Min child weight | 20 |
| Subsample | 0.8 |
| Colsample by tree | 0.8 |
| Regularization (lambda) | 1.0 |

**Outcome model (regression):**

| Parameter | Value |
|-----------|-------|
| Objective | Poisson regression (`count:poisson`) |
| Number of trees | 500 |
| Max depth | 6 |
| Learning rate | 0.05 |
| Min child weight | 20 |
| Subsample | 0.8 |
| Colsample by tree | 0.8 |
| Regularization (lambda) | 1.0 |

**Rationale for XGBoost:** Gradient boosting provides flexible, nonparametric estimation of both nuisance functions without requiring functional form assumptions. The Poisson objective for the outcome model respects the count-data nature of hospitalizations. Hyperparameters are pre-specified to avoid data-dependent tuning that could compromise the pre-analysis plan.

### 2.6.5 ATE Estimation and Inference

The DML estimator of the ATE is:

    tau_hat_DML = [sum_{i=1}^{N} (A_i - m_hat(W_i))^2]^{-1} * sum_{i=1}^{N} (A_i - m_hat(W_i)) * (Y_i - g_hat(W_i))

The variance is estimated via the sandwich formula:

    V_hat = (1/N) * [sum_{i=1}^{N} (A_i - m_hat(W_i))^2]^{-2} * sum_{i=1}^{N} psi_i^2

where psi_i is the influence function evaluated at observation i. The 95% confidence interval is:

    tau_hat +/- 1.96 * sqrt(V_hat / N)

### 2.6.6 Comparison with Causal Forest ATE

The DML ATE serves as a benchmark for the Causal Forest ATE (Section 2.5.5). Agreement between the two estimates provides mutual validation: DML is more efficient for the average effect under correct specification of the partially linear model, while the Causal Forest ATE is more robust to functional form misspecification. We report both estimates and test whether they are statistically distinguishable.

---

## 2.7 SHAP-based Heterogeneity Explanation

### 2.7.1 Motivation

Causal forests produce individual-level CATE estimates, but the forest itself is a black-box ensemble. To make heterogeneity patterns transparent and actionable for policymakers, we apply TreeSHAP (Lundberg et al., 2020) to decompose each CATE prediction into additive contributions from each effect modifier.

### 2.7.2 TreeSHAP on Causal Forest Output

For each observation *i*, SHAP values satisfy:

    tau_hat(X_i) = phi_0 + sum_{j=1}^{p} phi_j(X_i)

where phi_0 is the baseline CATE (population average) and phi_j(X_i) is the contribution of modifier j to the deviation of observation i's CATE from the baseline. TreeSHAP computes exact SHAP values in polynomial time for tree-based models.

**Implementation:** We extract the underlying tree ensemble from the `CausalForestDML` object and apply the `shap.TreeExplainer` to the CATE predictions. Because the causal forest's target is the treatment effect (not the outcome), SHAP values here decompose *heterogeneity*, not *prediction*. This is a methodologically novel application.

### 2.7.3 Global Feature Importance

Global importance of each modifier is computed as the mean absolute SHAP value across all observations:

    I_j = (1/N) * sum_{i=1}^{N} |phi_j(X_i)|

This ranks modifiers by their overall contribution to treatment effect heterogeneity. We report a bar chart of global importances and hypothesize that `age_group`, `fleet_per_capita`, and `dtr_quantile` will rank highest.

### 2.7.4 Local Explanations for Extreme-CATE Cities

For the five cities with the highest and five with the lowest average CATE, we produce individual SHAP force plots showing which modifiers push the CATE above or below the population average. This enables targeted policy interpretation: "Manaus has a high CATE because of high fleet density, high DTR, and a young population with developing respiratory systems."

### 2.7.5 Interaction Detection

We compute SHAP interaction values to detect synergistic effects between modifiers. The primary interaction of interest is DTR x PM2.5: does thermal stress amplify the health impact of pollution? SHAP interaction values quantify the joint contribution of two features beyond their individual main effects.

---

## 2.8 Policy Counterfactuals

### 2.8.1 Prevented Fraction Under WHO Threshold

The primary policy analysis estimates the number of respiratory hospitalizations that would be prevented if PM2.5 never exceeded the WHO guideline of 15 micrograms/m3. For each city-day where PM2.5 exceeded 15 micrograms/m3 (i.e., where A=1), the prevented admissions are:

    PF_i = tau_hat(X_i)     (the estimated CATE for that observation)

The total prevented admissions are:

    PF_total = sum_{i: A_i=1} tau_hat(X_i)

This represents the causal excess hospitalizations attributable to PM2.5 exceedance under conditional ignorability.

### 2.8.2 Stratification by CATE Vulnerability Tertiles

We divide the study population into three vulnerability groups based on the distribution of estimated CATEs:

- **High vulnerability** (top tercile of CATE): subpopulations with the largest estimated causal effect.
- **Medium vulnerability** (middle tercile).
- **Low vulnerability** (bottom tercile).

For each group, we report: (a) the number of prevented admissions, (b) the share of total preventable burden, and (c) the characteristic profile (mean age, fleet density, region composition) using CLAN analysis results.

### 2.8.3 Cost Estimation

The economic burden of preventable hospitalizations is estimated using SIH/SUS reimbursement data:

    Cost_prevented = sum_{i: A_i=1} tau_hat(X_i) * mean_cost_i

where `mean_cost_i` is the average cost per respiratory admission in city *c* and year *y*, obtained from the `total_cost / admissions` ratio in the `health_hospitalizations` table. Costs are reported in 2024 BRL and converted to USD using the average 2024 exchange rate (1 USD = 5.0 BRL) for international comparability.

### 2.8.4 Sensitivity to Threshold Choice

We repeat the prevented fraction analysis under three alternative scenarios:

| Scenario | Threshold | Interpretation |
|----------|-----------|----------------|
| WHO AQG (primary) | 15 micrograms/m3 | Full compliance with WHO 2021 guideline |
| CONAMA intermediate | 25 micrograms/m3 | Current Brazilian intermediate target |
| CONAMA final | 35 micrograms/m3 | Current Brazilian final standard |
| Pre-2024 CONAMA | 50 micrograms/m3 | Previous CONAMA standard (before 2024 revision) |

For each threshold, we redefine the treatment as PM2.5 exceeding that threshold, re-estimate the causal forest, and compute the prevented fraction. This provides a dose-response policy curve showing the incremental health benefit of progressively stricter standards.

---

## 2.9 Sensitivity and Robustness Analysis

We conduct seven pre-specified sensitivity and robustness analyses, each designed to probe a specific threat to the validity of our findings.

### 2.9.1 Placebo Treatment (Falsification Test)

**Threat addressed:** Residual confounding or spurious associations.

**Method:** Replace the observed treatment on day *t* with a placebo treatment defined as PM2.5 exceedance at *t+7* (one week in the future). If the causal identification strategy is valid, future pollution should not causally affect current hospitalizations. We estimate the Honest Causal Forest using the placebo treatment and test whether the placebo ATE is statistically distinguishable from zero.

**Decision rule:** If the placebo ATE 95% CI includes zero, the falsification test is passed. If the placebo ATE is significantly different from zero, this suggests residual confounding by a shared temporal driver (e.g., a persistent weather regime) that our confounder set does not fully capture.

### 2.9.2 Alternative Treatment Thresholds

**Threat addressed:** Sensitivity to the arbitrary choice of 15 micrograms/m3.

**Method:** Repeat the entire analysis pipeline (causal forest + DML) using three alternative binary treatment definitions:

- PM2.5 > 25 micrograms/m3 (CONAMA intermediate target)
- PM2.5 > 35 micrograms/m3 (CONAMA final standard)
- PM2.5 > 50 micrograms/m3 (pre-2024 CONAMA standard)

**Expected result:** ATEs should increase monotonically with the threshold (higher thresholds capture more extreme exposure days) but with wider confidence intervals due to fewer treated observations at higher thresholds. The heterogeneity pattern (which subgroups are most affected) should be qualitatively stable across thresholds.

### 2.9.3 Continuous Treatment (Generalized Causal Forest)

**Threat addressed:** Information loss from dichotomizing a continuous exposure.

**Method:** Estimate a generalized causal forest using continuous PM2.5 as the treatment variable (no binarization). The estimand becomes the marginal effect of a 1 micrograms/m3 increase in PM2.5 on hospitalizations, potentially varying by covariates X. This provides a continuous dose-response function and allows comparison of heterogeneity patterns between the binary and continuous treatment specifications.

**Implementation:** `econml.dml.CausalForestDML` with `discrete_treatment=False`.

### 2.9.4 Rosenbaum Bounds for Unmeasured Confounding

**Threat addressed:** Unmeasured confounders that violate conditional ignorability.

**Method:** We compute Rosenbaum bounds (Rosenbaum, 2002) to assess the sensitivity of the ATE to potential unmeasured confounding. The bound parameter Gamma represents the factor by which an unmeasured confounder could alter the odds of treatment. We report the critical Gamma value at which the ATE would become statistically insignificant at the 5% level.

**Interpretation:** A critical Gamma of 1.5, for example, means that an unmeasured confounder would need to increase the odds of PM2.5 exceedance by 50% for matched observations to nullify the result. Values of Gamma > 2.0 are generally considered evidence of robust findings in environmental epidemiology.

### 2.9.5 Leave-One-City-Out Jackknife

**Threat addressed:** Influence of a single outlier city driving the overall results.

**Method:** Re-estimate the causal forest 27 times, each time excluding one capital. For each iteration, compute the ATE and compare with the full-sample ATE. Report:
- The range of jackknife ATEs (min, max).
- The city whose exclusion causes the largest absolute change in ATE.
- Jackknife standard error as an alternative variance estimator.

**Decision rule:** If excluding any single city changes the ATE by more than 20% or shifts significance (from p<0.05 to p>=0.05), that city warrants further investigation and the result is flagged as potentially driven by a single site.

### 2.9.6 Alternative Confounder Sets

**Threat addressed:** Sensitivity to confounder specification.

**Method:** Re-estimate the model under three alternative confounder sets:

| Specification | Confounders added/removed |
|---------------|--------------------------|
| **Minimal** | Remove linear trend and Fourier harmonics (only weather + DOW) |
| **Extended** | Add PM2.5 lags at t-1, t-2, t-3 (captures cumulative exposure) |
| **Extended+** | Add O3 and NO2 as co-pollutant confounders |

**Rationale:** The minimal specification tests whether temporal adjustments drive the result. The extended specifications test whether lagged exposure or co-pollutant confounding alter the ATE or heterogeneity patterns.

### 2.9.7 Comparison with DLNM Baseline

**Threat addressed:** Novelty bias --- are causal ML results qualitatively different from established methods?

**Method:** Estimate a traditional Distributed Lag Non-linear Model (DLNM; Gasparrini et al., 2010) for the same outcome and exposure variables. The DLNM models the exposure-lag-response surface using a cross-basis function (natural splines for exposure with 3 df; natural splines for lag with 4 df over 0--7 days). City-specific estimates are pooled via random-effects meta-analysis (Gasparrini & Armstrong, 2013).

**Comparison:**
- DLNM overall pooled RR at 15 micrograms/m3 vs. Causal Forest ATE (converted to RR).
- DLNM cannot produce individual-level CATEs, but city-specific RRs can be compared with city-level GATEs from the causal forest.
- Qualitative comparison: do both methods identify the same cities/subgroups as most affected?

---

## 2.10 Reporting Standards

### 2.10.1 STROBE Compliance

The study adheres to the Strengthening the Reporting of Observational Studies in Epidemiology (STROBE) checklist for ecological studies (von Elm et al., 2007). A completed STROBE checklist is provided in the supplementary material with line-by-line cross-references to the manuscript.

### 2.10.2 Pre-specified Analysis Hierarchy

To address multiple testing concerns, we adopt a hierarchical testing framework:

**Primary analysis (confirmatory):**
- ATE of PM2.5 exceedance (>15 micrograms/m3) on total daily respiratory hospitalizations.
- Omnibus heterogeneity test (calibration test, Section 2.5.7).
- Significance threshold: alpha = 0.05 (two-sided).

**Secondary analyses (pre-specified, multiplicity-adjusted):**
- GATEs by age group (0--14, 15--59, 60+): 3 tests.
- GATEs by sex (male, female): 2 tests.
- GATEs by fleet density tercile: 3 tests.
- All secondary analyses use Bonferroni-Holm correction within each family of tests.

**Exploratory analyses (hypothesis-generating, not adjusted):**
- GATEs by region, DTR tercile, population density tercile.
- SHAP-based heterogeneity decomposition.
- Policy counterfactuals.
- Interaction effects (DTR x PM2.5).

### 2.10.3 Reproducibility

All code, data extraction scripts, and analysis pipelines are publicly available at the project repository (https://github.com/Roverlucas/causal-pollution-health-brazil). The complete analytical pipeline is specified in `src/` with the following execution order:

1. `src/data/extract.py` -- data extraction from Clima360
2. `src/data/process.py` -- feature engineering and panel construction
3. `src/models/causal_forest.py` -- Honest Causal Forest estimation
4. `src/models/dml.py` -- Double Machine Learning ATE estimation
5. `src/analysis/shap_analysis.py` -- SHAP value computation
6. `src/analysis/policy.py` -- Policy counterfactual estimation
7. `src/analysis/sensitivity.py` -- All seven sensitivity analyses
8. `src/visualization/` -- Publication-ready figures

A random seed (42) is set for all stochastic components. The Python environment is specified in `requirements.txt` with pinned versions.

### 2.10.4 Ethics

This study uses only publicly available, de-identified, aggregate data. SIH/SUS hospitalization data are reported at the daily aggregate level by city, with no individual-level identifiers. No ethics committee approval is required under Brazilian regulations (Resolution CNS 510/2016, Article 1, paragraph sole: research using publicly available data in aggregate form is exempt from ethics review).

---

## References

1. Athey S, Tibshirani J, Wager S. Generalized Random Forests. *Ann Stat*. 2019;47(2):1148-1178. doi:10.1214/18-AOS1709
2. Athey S, Wager S. Estimating Treatment Effects with Causal Forests: An Application. *Obs Stud*. 2019;5:37-51.
3. Chernozhukov V, Chetverikov D, Demirer M, Duflo E, Hansen C, Newey W, Robins J. Double/debiased machine learning for treatment and structural parameters. *Econom J*. 2018;21(1):C1-C68. doi:10.1111/ectj.12097
4. Chernozhukov V, Demirer M, Duflo E, Fernandez-Val I. Generic Machine Learning Inference on Heterogeneous Treatment Effects in Randomized Experiments. *NBER Working Paper*. 2018b;No. 24678.
5. Gasparrini A, Armstrong B, Kenward MG. Distributed lag non-linear models. *Stat Med*. 2010;29(21):2224-2234. doi:10.1002/sim.3940
6. Gasparrini A, Armstrong B. Reducing and meta-analysing estimates from distributed lag non-linear models. *BMC Med Res Methodol*. 2013;13:1. doi:10.1186/1471-2288-13-1
7. Lundberg SM, Erion G, Chen H, et al. From local explanations to global understanding with explainable AI for trees. *Nat Mach Intell*. 2020;2:56-67. doi:10.1038/s42256-019-0138-9
8. Rosenbaum PR. *Observational Studies*. 2nd ed. Springer; 2002.
9. von Elm E, Altman DG, Egger M, Pocock SJ, Gotzsche PC, Vandenbroucke JP. The Strengthening the Reporting of Observational Studies in Epidemiology (STROBE) statement. *Lancet*. 2007;370(9596):1453-1457. doi:10.1016/S0140-6736(07)61602-X
10. Deryugina T, Heutel G, Miller NH, Molitor D, Reif J. The Mortality and Medical Costs of Air Pollution: Evidence from Changes in Wind Direction. *Am Econ Rev*. 2019;109(12):4178-4219. doi:10.1257/aer.20180279
11. World Health Organization. *WHO global air quality guidelines: particulate matter (PM2.5 and PM10), ozone, nitrogen dioxide, sulfur dioxide and carbon monoxide*. WHO; 2021.

---

*Methods Specification v1.0 -- @methodology-specialist -- 2026-02-22*
*Pre-analysis plan: locked before data analysis commences.*
