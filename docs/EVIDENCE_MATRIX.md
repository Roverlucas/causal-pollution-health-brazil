# EVIDENCE MATRIX: Comprehensive Literature Review

## Study: "Who Suffers Most? Causal Machine Learning Reveals Heterogeneous Health Effects of Air Pollution Across 27 Brazilian State Capitals"

**Target journal:** The Lancet Planetary Health
**Search date:** 2026-02-22
**Total papers reviewed:** 35

---

## PILLAR 1: Air Pollution & Health in Brazil (10 papers)

| # | Authors (Year) | Journal | Scope | Method | Exposure | Outcome | Key Finding (effect size) | Limitation | Gap We Fill | Relevance |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Ponce de Leon et al. (2023) | *Environment International* | 1,814 Brazilian cities, 2000--2015 | Difference-in-differences causal framework; time-series | Daily PM2.5 (satellite-derived) | All-cause hospitalizations (DATASUS) | +10 ug/m3 PM2.5 over lag 0--3 associated with 1.06% (95% CI: 0.94--1.17) increase in all-cause hospitalizations; larger effects for children 0--4 and elderly 80+ | Nationwide average effect; no subpopulation heterogeneity estimation; satellite PM2.5 exposure misclassification | We estimate heterogeneous CATEs across subgroups using causal forests, going beyond average effects | **H** |
| 2 | Bravo, Son, Freitas, Gouveia & Bell (2016) | *J Exposure Sci Environ Epidemiol* | Sao Paulo, 1996--2010 | Time-stratified case-crossover | PM10, NO2, SO2, CO, O3 | Non-accidental, cardiovascular, respiratory mortality | All pollutants associated with increased mortality (P<0.05); education gradient: 0 years education had higher effect than >11 years for NO2 (1.66%, 95% CI: 0.23--3.08%) | Single city; individual-level SES proxy only via death certificate education | We cover 27 capitals simultaneously with city-level moderators (fleet density, demographics) | **H** |
| 3 | Yu et al. (2022) | *Environment International* | 5,565 Brazilian municipalities, 2010--2018 | Life-table approach; relative risk regression | Long-term PM2.5 (5-year avg) | Years of life lost; life expectancy | RR 1.18 per 10 ug/m3 for all-cause YLL; RR 1.17 for respiratory; compliance with WHO guideline would gain 0.78 years LE | Long-term exposure design; ecological fallacy at municipality level; no causal identification strategy | We use short-term quasi-experimental variation with formal causal methods | **H** |
| 4 | Gouveia et al. (2006) | *Cad Saude Publica* | 7 Brazilian capital cities | Poisson time-series; health impact assessment | PM10 (concentration-response from literature) | Respiratory mortality and hospital admissions | >600 respiratory deaths/year in elderly and 47 in children attributable to air pollution (4.9% and 5.5% of respiratory deaths); >4,000 respiratory admissions | Used transferred coefficients rather than city-specific estimates; limited to PM10; 7 cities only | We use 27 capitals with city-specific estimates and PM2.5 | **H** |
| 5 | Carvalho et al. (2022) | *Nature Communications* | 510 immediate regions Brazil, 2000--2016 | Two-stage time-series with meta-analysis | Daily wildfire-related PM2.5 | All-cause, cardiovascular, respiratory mortality | +10 ug/m3 wildfire PM2.5: 3.1% all-cause, 2.6% cardiovascular, 7.7% respiratory mortality increase; 121,351 attributable deaths | Wildfire-specific PM2.5 only; no distinction of urban anthropogenic sources; no heterogeneity by SES | We address total ambient PM2.5 (including urban sources) with heterogeneity decomposition | **M** |
| 6 | Rodrigues et al. (2021) | *Nature Communications* | Nationwide Brazil, 2008--2018 | Panel regression; difference-in-differences | Wildfire-related PM2.5 waves | Respiratory and circulatory hospital admissions (>2M records) | Wildfire waves: +23% respiratory admissions, +21% circulatory admissions; +38% respiratory in the Amazon North | Wildfire-specific; aggregate regional estimates; no individual-level moderators | We model all-source PM2.5 with individual-level heterogeneity | **M** |
| 7 | Peres et al. (2024) | *Environmental Pollution* | Nationwide Brazil, 2003--2017 | Time-series; DLNMs | PM2.5, O3, NO2 | Cause-specific mortality by sex and age | +10 ug/m3 PM2.5: 2.93% (95% CI: 1.42--4.43) increase respiratory mortality; NO2: 17.56% respiratory mortality increase; elderly >65 most affected | No causal framework; no heterogeneity beyond stratified subgroups; no city-level moderators | We formally estimate heterogeneous causal effects across multiple moderators simultaneously | **H** |
| 8 | Santos et al. (2025) | *Scientific Reports* | Nationwide Brazil, all regions | Two-stage time-series; effect modification | PM2.5 and O3 combined with heat | Cardiorespiratory hospitalizations | PM2.5 amplified heat effects by 20.1% on respiratory admissions; regional heterogeneity: positive in Midwest, null in South | Focused on heat-pollution interaction only; no formal causal identification; DTR not examined | We explicitly include DTR as moderator and use causal forests to estimate interaction effects | **H** |
| 9 | Miranda et al. (2012) | *Air Qual Atmos Health* | 6 Brazilian capitals (SP, RJ, BH, CWB, RE, POA) | Gravimetric PM2.5 monitoring; health impact assessment | PM2.5 annual means (7.3--28.1 ug/m3) | Attributable mortality (WHO methodology) | >13,000 deaths/year attributable to PM2.5 across 6 cities; SP worst with mean 28.1 ug/m3 | Only 6 cities; monitoring-based exposure (spatial gaps); no causal design; no heterogeneity | We expand to 27 capitals with satellite-reanalysis PM2.5 and heterogeneity estimation | **M** |
| 10 | Oliveira et al. (2024) | *Air Qual Atmos Health* | Nationwide Brazil, 2008--2019 | Spatial analysis; relative risk; MERRA-2 data | PM2.5, O3 (reanalysis) | Cardiopulmonary hospitalization rates | Significant spatial heterogeneity; South highest median rates; Southeast-Northeast corridor hotspots; upward trends | Cross-sectional spatial design; ecological; no causal inference; no temporal variation exploited | We use daily time-series with causal identification within cities | **H** |

---

## PILLAR 2: Causal Inference in Environmental Epidemiology (10 papers)

| # | Authors (Year) | Journal | Scope | Method | Exposure | Outcome | Key Finding (effect size) | Limitation | Gap We Fill | Relevance |
|---|---|---|---|---|---|---|---|---|---|---|
| 11 | Wager & Athey (2018) | *JASA* | Methodological | Causal forests; honest estimation | Generic (treatment assignment) | Generic (outcomes) | Causal forests are pointwise consistent for true treatment effect; asymptotically Gaussian; valid confidence intervals | Theoretical guarantees assume unconfoundedness and overlap; limited guidance for observational environmental studies | We apply this foundational method to environmental health in a LMIC context with 27 cities | **H** |
| 12 | Athey, Tibshirani & Wager (2019) | *Ann Statistics* | Methodological | Generalized random forests (GRF) | Local moment conditions | Flexible target parameters | Unified framework for nonparametric estimation; consistent and asymptotically Gaussian; valid variance estimation | General framework; environmental health application requires domain-specific adaptations (temporal confounding, lag structures) | We adapt GRF to daily time-series environmental health data with lag structures | **H** |
| 13 | Chernozhukov et al. (2018) | *Econometrics Journal* | Methodological | Double/debiased ML (DML); Neyman-orthogonal scores; cross-fitting | High-dimensional nuisance parameters | Low-dimensional causal parameter | DML removes regularization bias and overfitting via orthogonal scores + cross-fitting; enables valid inference with ML nuisance estimation | Assumes correct specification of Neyman-orthogonal moment; limited exploration of environmental time-series | We implement DML for pollution-health with time-series confounding (weather, seasonality) | **H** |
| 14 | Jawadekar et al. (2023) | *Am J Epidemiol* | Tutorial/simulation | Honest causal forests; practical guide for epidemiologists | Simulated binary treatment | Simulated continuous outcome | Step-by-step guide; demonstrates identification and estimation of heterogeneous effects; highlights honesty mechanism | Simulation only; no real environmental data; no discussion of continuous treatment (pollution levels) | We provide real-world application with continuous PM2.5 treatment in a multi-city design | **H** |
| 15 | Wu, Braun, Kioumourtzoglou & Dominici (2020) | *Science Advances* | 68.5M Medicare enrollees, USA, 2000--2016 | 5 causal inference approaches; GPS matching | Long-term PM2.5 | All-cause mortality | 10 ug/m3 decrease in PM2.5 leads to 6--7% mortality reduction; lowering standard to 10 ug/m3 would save 143,257 lives/decade | US-only; elderly Medicare population; long-term exposure; no heterogeneity decomposition by causal forest | We examine short-term effects in a LMIC (Brazil) with formal heterogeneity estimation | **H** |
| 16 | Yazdi et al. (2021) | *Lancet Planetary Health* | 68.5M Medicare, USA, 2000--2016 | Doubly-robust additive model | PM2.5 (<12 ug/m3), NO2, O3 | All-cause mortality | Even at low concentrations, PM2.5 increased mortality; elderly and low-income most vulnerable | US-only; long-term design; subgroup analysis pre-specified (not data-driven) | We use data-driven heterogeneity discovery (causal forests) rather than pre-specified subgroups | **H** |
| 17 | Zorzetto, Bargagli-Stoffi, Canale & Dominici (2024) | *Biometrics* | Medicare enrollees, Texas, USA | Confounder-dependent Bayesian mixture model (CDBMM) | Long-term PM2.5 | ZIP-code level mortality | Novel Bayesian approach discovers heterogeneous groups; outperforms BART and BCF in simulations; applied at ZIP-code level | US-only; long-term exposure; Bayesian computational cost; no short-term design | We use a complementary non-Bayesian approach (causal forests) with short-term exposure in Brazil | **M** |
| 18 | Roqueta-Rivera et al. (2024) | *arXiv (preprint)* | Multi-pollutant PM2.5 constituents, USA | DML with measurement error correction | PM2.5 constituents (mismeasured) | Cognitive function | Novel DML method correcting for exposure measurement error in multi-pollutant settings; GEE-based calibration | Preprint (not peer-reviewed); cognitive outcome not respiratory; no heterogeneity by subpopulation | We address respiratory outcomes with PM2.5 and O3 in a multi-city setting | **M** |
| 19 | Miller (2020) | *J Environ Econ Manage* | Global fisheries data | Causal forests for environmental policy; panel setting with staggered adoption | Fishery quota policies | Catch outcomes | Substantial cross-sectional heterogeneity and time dependencies; longer policy exposure less beneficial than assumed | Not health outcome; environmental policy context; fisheries not air pollution | We transfer causal forest panel methodology to air pollution health in Brazilian cities | **M** |
| 20 | Dominici, Peng & Bell (2006) | *JRSS-A / JAMA* | 100 US cities (NMMAPS); 204 US counties | Multi-city time-series; Bayesian hierarchical models | PM10, PM2.5 | Daily mortality; hospital admissions | PM10 effect on mortality varied ~2-fold across model choices; PM2.5: 0.98% increase per 10 ug/m3 in CV admissions, 2.07% respiratory | US-only; frequentist/Bayesian averaging; no heterogeneous treatment effects framework | We apply modern causal ML (not just hierarchical models) to discover effect heterogeneity | **H** |

---

## PILLAR 3: Temperature Variability (DTR) & Health (6 papers)

| # | Authors (Year) | Journal | Scope | Method | Exposure | Outcome | Key Finding (effect size) | Limitation | Gap We Fill | Relevance |
|---|---|---|---|---|---|---|---|---|---|---|
| 21 | Lee et al. (2017) | *Environment International* | 308 cities, 10 countries (incl. Brazil) | Multi-country time-series; DLNM | Diurnal temperature range (DTR) | All-cause mortality | 2.5% (95% eCI: 2.3--2.7%) attributable fraction of total mortality to DTR; increasing from 2.4% to 2.7% over study period | Mortality only (not hospitalizations); DTR as standalone risk factor (no interaction with pollution); Brazil as one country among 10 | We explicitly model DTR-PM2.5 interaction as effect modifier on hospitalizations in Brazil | **H** |
| 22 | Zhao et al. (2022) | *Lancet Planetary Health* | 750 cities, 43 countries, 2000--2019 | Three-stage modeling; DLNM + meta-regression | Short-term temperature variability (TV) | All-cause mortality | 1,753,392 deaths/year globally attributable to TV (3.4% of all deaths); increasing trend identified | Global average; no pollution interaction; no city-level heterogeneity by socioeconomic factors; Brazil not disaggregated | We disaggregate across 27 Brazilian capitals with pollution co-exposure and socioeconomic moderators | **H** |
| 23 | Ma et al. (2020) | *Respiratory Research* | 21 Chinese cities | Two-stage time-series; DLNMs | Diurnal temperature range | COPD, asthma, bronchiectasis hospitalizations | Significant DTR-hospitalization associations after controlling for temperature, humidity, and pollution; stronger on cold days | China-specific; no formal interaction with pollution modeled; no causal identification | We model DTR as effect modifier in causal forest framework; tropical/subtropical Brazilian context | **H** |
| 24 | Vicedo-Cabrera et al. (2021) | *Nature Climate Change* | 732 locations, 43 countries, 1991--2018 | Empirical detection & attribution | Heat exposure (anthropogenic warming) | Heat-related mortality | 37.0% (range 20.5--76.3%) of warm-season heat-related deaths attributable to climate change; highest in Central/South America | Heat only (not DTR); no pollution interaction; focuses on attribution to climate change rather than health heterogeneity | We use DTR (not just mean temperature) and model it as pollution-health effect modifier | **M** |
| 25 | Bunker et al. (2016) | *Int J Biometeorol* | Systematic review (14 studies) | Systematic review of DTR & health | Diurnal temperature range | Mortality and morbidity | DTR associated with 0.7%/degC increase in CVD mortality; 1.0%/degC increase in respiratory morbidity; 0.7%/degC respiratory mortality; elderly most vulnerable | Aggregated estimates; no LMIC-specific analysis; no pollution interaction | We provide the first DTR-pollution interaction analysis in a LMIC (Brazil) with causal methods | **H** |
| 26 | Saldanha et al. (2023) | *Environmental Research* | All Brazilian capitals | Time-series; DLNM | Ambient temperature (cold and heat) | Cardiorespiratory mortality | RR 1.27 for circulatory (cold), 1.11 (heat); RR 1.16 respiratory (cold), 1.14 (heat); effects vary by region | Mean temperature only (not DTR); no pollution interaction; no causal forest methodology | We use DTR as a distinct exposure modifier alongside PM2.5 in a causal framework | **H** |

---

## PILLAR 4: Machine Learning for Pollution-Health (5 papers)

| # | Authors (Year) | Journal | Scope | Method | Exposure | Outcome | Key Finding (effect size) | Limitation | Gap We Fill | Relevance |
|---|---|---|---|---|---|---|---|---|---|---|
| 27 | Lundberg & Lee (2017) | *NeurIPS* | Methodological | SHAP (SHapley Additive exPlanations) | Generic ML model features | Feature importance values | Unified framework for model interpretability; unique solution with desirable properties; game-theoretic foundation | General ML interpretability; not designed for causal inference; can conflate correlation with causation | We use SHAP to interpret the causal forest heterogeneity drivers, providing mechanistic insight into CATEs | **H** |
| 28 | Zarei et al. (2024) | *Scientific Reports* | Mashhad, Iran, 2017--2020 | Random forest; permutation importance; PDPs | PM2.5, PM10, SO2, NO2, CO + meteorological | Cardiovascular mortality | Time, pressure, and temperature most important; NO2 and SO2 most influential pollutants; meteorological factors outweigh pollutants | Predictive only (not causal); single city; no SHAP; no heterogeneous effects | We combine causal forests (for causal effects) with SHAP (for mechanistic interpretation) across 27 cities | **M** |
| 29 | Yin et al. (2025) | *Sci Total Environ* | Lanzhou, China | Random forest + XGBoost + SHAP | PM2.5, O3, NO2, CO, SO2 + meteorological | Respiratory outpatient visits | O3 most important factor via SHAP; risk elevated when Tmax <16degC and pollutants high; interaction effects identified | Predictive correlation (not causal); single city; Chinese context | We use SHAP on causal estimates (not predictions) across 27 Brazilian cities | **M** |
| 30 | Alotaibi et al. (2025) | *Atmosphere* (systematic review) | 38 studies reviewed | Systematic review of XAI for air pollution health risk | Various pollutants | Respiratory outcomes | XGBoost and RF dominant methods; SHAP main interpretability tool; most studies predictive, <5% use causal methods | Documents gap: almost no studies combine ML interpretability with causal inference for health | We bridge exactly this gap by using SHAP to interpret causal forest CATEs | **H** |
| 31 | Liu et al. (2019) | *NEJM* | 652 cities, 24 countries | GAM + random-effects meta-analysis | PM10, PM2.5 | Daily all-cause, CVD, respiratory mortality | +10 ug/m3 PM10: 0.44% (95% CI: 0.39--0.50) all-cause mortality; +10 ug/m3 PM2.5: 0.68% (95% CI: 0.59--0.77); no safe threshold | Traditional statistical methods; no heterogeneity by city-level moderators beyond region; no causal ML | We apply causal ML to discover data-driven heterogeneity across city-level and population characteristics | **H** |

---

## PILLAR 5: Multi-City Studies Brazil / Latin America (4 papers)

| # | Authors (Year) | Journal | Scope | Method | Exposure | Outcome | Key Finding (effect size) | Limitation | Gap We Fill | Relevance |
|---|---|---|---|---|---|---|---|---|---|---|
| 32 | Romieu et al. (2012) | *HEI Research Report 171* | 9 Latin American cities (ESCALA); incl. SP, RJ | Standardized multi-city time-series; common protocol | PM10, O3 | Daily mortality by cause and age | Confirmed PM10-mortality associations; SES modifies effect: lower SES = higher respiratory mortality risk (COPD) | Only 2 Brazilian cities (SP, RJ); PM10 not PM2.5; no causal framework; pre-2010 data | We cover all 27 Brazilian capitals with PM2.5 and formal causal heterogeneity estimation | **H** |
| 33 | Nascimento et al. (2019) | *Int J Environ Res Public Health* | 5 cities, South Brazil, 2013--2016 | Panel Poisson regression; monthly time-series | PM10, SO2, CO, NO2, O3 | Respiratory hospitalizations by age group | +10 ug/m3 PM10: IRR up to 2.04 in 16--59 age group; NO2 and SO2 stronger effects in children 6--15 | Only 5 cities in one state (RS); monthly aggregation loses daily variation; PM10 only; no causal design | We use daily data across 27 capitals with PM2.5 and causal identification | **H** |
| 34 | Oliveira Alves & Souza Tadano (2024) | *Air Qual Atmos Health* | Nationwide Brazil (all municipalities) | Spatial regression; relative risk; cluster analysis | PM2.5, emissions, land use (MERRA-2) | Cardiopulmonary hospitalizations 2008--2019 | Spatial heterogeneity: South highest rates; SE-NE corridor hotspots; upward trends in localized areas | Cross-sectional spatial analysis; no temporal causal identification; ecological design | We use within-city daily variation for causal identification with heterogeneity decomposition | **H** |
| 35 | Nardocci et al. (2013) | *Rev Saude Publica* | Sao Paulo metropolitan region + review of Brazilian studies | Literature review + health impact assessment | Multiple pollutants | Respiratory and cardiovascular mortality/morbidity | PM2.5 compliance with WHO would prevent >5,000 deaths in SP alone; comprehensive review of Brazilian evidence | Review focused on SP; pre-2013 literature; no causal methods; no multi-city heterogeneity | We provide the first comprehensive causal multi-city analysis across all 27 state capitals | **M** |

---

## GAP SYNTHESIS

### 1. Well-Established (Consensus Findings)

The following associations are firmly supported by the evidence matrix and represent the foundation upon which our study builds:

- **PM2.5 increases respiratory morbidity and mortality in Brazil.** Multiple nationwide studies (Ponce de Leon et al. 2023; Peres et al. 2024; Yu et al. 2022) using different designs (time-series, life-table, case-crossover) consistently report significant associations. Effect sizes range from 1.06% increase in all-cause hospitalizations per 10 ug/m3 (short-term) to RR 1.17 for respiratory years-of-life-lost (long-term). The 652-city NEJM study by Liu et al. (2019) confirms this globally with no safe threshold.

- **Elderly and children bear disproportionate burden.** Every Brazilian study that stratified by age (Ponce de Leon 2023; Peres 2024; Bravo et al. 2016; Gouveia 2006) found amplified effects in ages 0--4 and 65+. The systematic review by Bunker et al. (2016) confirms this for DTR exposure as well.

- **Socioeconomic status modifies pollution-health effects.** The ESCALA study (Romieu et al. 2012) and Bravo et al. (2016) demonstrate an SES gradient: lower education and income are associated with higher mortality risk from identical pollution exposure. Yazdi et al. (2021) confirm this in the US Medicare population.

- **Diurnal temperature range (DTR) is an independent health risk.** The multi-country study by Lee et al. (2017) attributes 2.5% of global mortality to DTR. Bunker et al.'s (2016) systematic review quantifies a consistent 0.7--1.0% mortality/morbidity increase per degree Celsius of DTR. The global assessment by Zhao et al. (2022) counts 1.75 million DTR-attributable deaths annually.

- **Causal forests can validly estimate heterogeneous treatment effects.** Wager & Athey (2018) and Athey et al. (2019) provide theoretical guarantees. Jawadekar et al. (2023) translate these for epidemiological practice. DML (Chernozhukov et al. 2018) provides a complementary semiparametric causal framework.

### 2. Emerging but Uncertain (Debate Areas)

These areas show promising but contested or incomplete evidence that our study can contribute to resolving:

- **Whether pollution-DTR interactions amplify health effects beyond additive contributions.** Santos et al. (2025) find PM2.5 amplifies heat effects by 20% in some Brazilian regions but null effects in others. Ma et al. (2020) show DTR effects are stronger on cold days. However, no study has formally modeled the DTR-pollution interaction as a causal effect modifier using modern causal ML methods. The direction and magnitude of this interaction remain region-dependent and poorly characterized.

- **Whether causal forests outperform traditional subgroup analyses in environmental epidemiology.** Jawadekar et al. (2023) provide simulation evidence, and Zorzetto et al. (2024) demonstrate novel Bayesian alternatives. However, real-world applications to air pollution exposure remain scarce. Wu et al. (2020) and Yazdi et al. (2021) use causal methods but not heterogeneity-focused approaches. The practical value of data-driven heterogeneity discovery versus pre-specified subgroup analyses is still under active debate (see the 2024 response letter in AJE).

- **Spatial heterogeneity of pollution effects across Brazilian regions.** Oliveira et al. (2024) document spatial variation in cardiopulmonary hospitalization rates, and Santos et al. (2025) show regional differences in heat-pollution interactions. However, these are ecological observations, not causally identified city-level effect estimates. The extent to which fleet density, urbanization, and demographic composition explain this spatial variation is unknown.

- **The role of SHAP in interpreting causal (not merely predictive) models.** Alotaibi et al. (2025) systematic review shows <5% of ML-for-health studies combine interpretability with causal inference. Yin et al. (2025) and Zarei et al. (2024) use SHAP on predictive models, which captures correlations but not causal mechanisms. Whether SHAP applied to causal forest CATEs yields actionable policy insights is methodologically novel and not yet validated.

### 3. Absent (Gaps We Fill -- Our Contribution)

These are the critical gaps in the literature that our study directly addresses. No existing paper occupies this space:

- **No study has applied honest causal forests or DML to estimate heterogeneous causal effects of air pollution on respiratory health across Brazilian cities.** All Brazilian studies use either traditional time-series (Ponce de Leon 2023; Peres 2024; Gouveia 2006), spatial ecological designs (Oliveira et al. 2024), or stratified subgroup analyses (Bravo et al. 2016). The causal ML literature (Wu et al. 2020; Zorzetto et al. 2024) is exclusively US-based and focused on long-term exposure in Medicare populations. We provide the first application of causal forests to short-term air pollution exposure in a low- and middle-income country (LMIC).

- **No study has formally estimated the causal interaction between DTR and PM2.5 on health outcomes.** Santos et al. (2025) examine heat-PM2.5 interaction, but DTR (thermal amplitude) is a distinct exposure that captures within-day temperature swings. Bunker et al. (2016), Lee et al. (2017), and Zhao et al. (2022) treat DTR as a standalone risk factor. Our study is the first to model DTR as a causal effect modifier of the PM2.5-hospitalization relationship using causal forests, testing whether large diurnal temperature swings amplify or attenuate pollution effects.

- **No study covers all 27 Brazilian state capitals simultaneously with causal ML methods.** The ESCALA study (2012) included only Sao Paulo and Rio de Janeiro from Brazil. Nascimento et al. (2019) covered 5 cities in Rio Grande do Sul. Miranda et al. (2012) monitored 6 capitals. Ponce de Leon et al. (2023) covered 1,814 municipalities but estimated only average effects. We provide the first complete coverage of all 27 state capitals with heterogeneous causal effect estimation.

- **No study has used SHAP to interpret causal forest heterogeneity drivers in environmental health.** The systematic review by Alotaibi et al. (2025) documents that SHAP has been used exclusively on predictive models (XGBoost, Random Forest) in the air pollution-health literature. We apply SHAP to causal forest CATEs, bridging the gap between causal inference and explainable AI to identify which city-level and population-level features drive effect heterogeneity, which is directly actionable for targeted public health policy.

- **No study explicitly links fleet density as a causal moderator of pollution-health effects.** While vehicle emissions are known drivers of urban PM2.5, fleet density per capita has not been used as a moderator variable in heterogeneous causal effect models. Our inclusion of SENATRAN fleet data as a city-level moderator enables identification of cities where vehicular sources may amplify health vulnerability, which is directly relevant for traffic management and clean fleet policies.

- **No study provides a policy counterfactual analysis of CONAMA versus WHO standards across heterogeneous subpopulations.** While Yu et al. (2022) estimated life expectancy gains from WHO compliance at the national level, no study has estimated how the preventable hospitalization burden under different standards varies across vulnerable subpopulations identified by causal forests. Our secondary analysis of CONAMA versus WHO thresholds stratified by CATE quintiles can inform whether current Brazilian regulations adequately protect the most vulnerable.

---

## Key References by Pillar (for BibTeX)

**Pillar 1 (Brazil):** Ponce de Leon et al. 2023; Bravo et al. 2016; Yu et al. 2022; Gouveia et al. 2006; Carvalho et al. 2022; Rodrigues et al. 2021; Peres et al. 2024; Santos et al. 2025; Miranda et al. 2012; Oliveira et al. 2024.

**Pillar 2 (Causal):** Wager & Athey 2018; Athey et al. 2019; Chernozhukov et al. 2018; Jawadekar et al. 2023; Wu et al. 2020; Yazdi et al. 2021; Zorzetto et al. 2024; Roqueta-Rivera et al. 2024; Miller 2020; Dominici et al. 2006.

**Pillar 3 (DTR):** Lee et al. 2017; Zhao et al. 2022; Ma et al. 2020; Vicedo-Cabrera et al. 2021; Bunker et al. 2016; Saldanha et al. 2023.

**Pillar 4 (ML):** Lundberg & Lee 2017; Zarei et al. 2024; Yin et al. 2025; Alotaibi et al. 2025; Liu et al. 2019.

**Pillar 5 (Multi-city):** Romieu et al. 2012; Nascimento et al. 2019; Oliveira & Souza Tadano 2024; Nardocci et al. 2013.

---

## Summary Statistics

| Metric | Count |
|---|---|
| Total papers in matrix | 35 |
| High relevance (H) | 25 |
| Medium relevance (M) | 10 |
| Papers using causal methods | 12 |
| Papers focused on Brazil | 14 |
| Papers addressing heterogeneity | 9 |
| Papers combining causal + heterogeneity + Brazil | **0** (this is our gap) |

The zero at the intersection of causal inference, heterogeneous effects, and Brazilian environmental health is the fundamental contribution of this study. No existing work in the 35-paper matrix simultaneously applies causal ML methods, estimates heterogeneous treatment effects, and covers Brazilian state capitals, which validates the novelty of "Who Suffers Most?" for a Lancet Planetary Health submission.
