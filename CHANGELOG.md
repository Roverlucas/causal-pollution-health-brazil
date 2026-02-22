# Changelog

All notable changes to this project are documented in this file.

## [1.0.0] - 2026-02-22

### Added

- **Data pipeline**: extraction from Clima360 Supabase (5 tables, 301,731 records) and processing into analytical panel (21,035 city-days, 17 capitals, 114 features)
- **Causal Forest models**: 6 Honest Causal Forest models (total + 3 age groups + 2 sex) with 2,000 trees, honest splitting, discrete treatment
- **DML models**: 6 Double Machine Learning models with 5-fold cross-fitting and XGBoost nuisance functions
- **SHAP analysis**: KernelSHAP decomposition of CATE heterogeneity across 9 effect modifiers
- **Policy counterfactuals**: prevented admissions and cost savings under 4 air quality thresholds (WHO 15, CONAMA 25/35, pre-2024 50 ug/m3)
- **Sensitivity analyses**: placebo test (t+7), leave-one-city-out jackknife (17 iterations), omitted variable bias analysis, threshold sensitivity
- **Visualizations**: 14 publication-quality PDF figures (maps, forest plots, SHAP beeswarm/dependence, policy curves)
- **Manuscript**: complete Lancet Planetary Health format manuscript with all real results (313 lines, 38 references)
- **Documentation**: evidence matrix (35 papers), methods specification, project charter, storytelling architecture
- **Makefile**: reproducible `make all` pipeline

### Key results

- DML ATE: 0.72 additional admissions/city-day [0.08, 1.35], p=0.027
- CATE range: -6.43 to +9.38 (16-fold heterogeneity)
- Top drivers: DTR (0.594), pop. density (0.457), fleet/capita (0.292)
- 3,834 prevented admissions under WHO compliance (0.58%)
- R$7.47M cost savings
- Placebo: p=0.82 (passed); OVB robustness: 0.826; Jackknife CV: 0.22

## [0.1.0] - 2026-02-21

### Added

- Initial project structure and Paper Factory pipeline configuration
- Project charter with research questions, hypotheses, and methodology
- 16 agent workflow definitions
- Storytelling narrative architecture
