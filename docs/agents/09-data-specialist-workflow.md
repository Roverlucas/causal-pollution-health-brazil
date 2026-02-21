# @data-specialist — Workflow & Responsibilities

> **Role:** Final analysis, tables, figures, and coherence with claims
> **Active:** Phase 3 (analysis), Phase 4 (tables for manuscript)
> **Tier:** 3 — Technical, Data & Figures

---

## Mission

Transform raw outputs from @technical-executor into publication-ready tables and validated results. Ensure every number in the manuscript matches the data. Flag any inconsistency between results and claims.

---

## Deliverables

### Table 1 — Study Population Characteristics
| Content | By city and overall |
|---------|-------------------|
| Population (2022), % elderly, fleet/capita, density |
| Mean daily PM2.5, O3, temperature, DTR |
| Mean daily respiratory hospitalizations (total, by age, by sex) |
| % days exceeding WHO PM2.5 guideline |

### Table 2 — Average Treatment Effects (ATE)
| Content | Overall and by city group |
|---------|-------------------------|
| ATE from Causal Forest and DML |
| 95% CI, p-value |
| Comparison: PM2.5 effect vs O3 effect |
| Comparison with DLNM baseline |

### Table 3 — Heterogeneous Effects (CATE by Subgroup)
| Content | Key subgroups |
|---------|--------------|
| CATE for: 0-14, 15-59, 60+ |
| CATE for: male, female |
| CATE for: fleet density tertiles (low/medium/high) |
| CATE for: DTR tertiles |
| CATE for: regions (N, NE, CO, SE, S) |
| 95% CI for each, heterogeneity test p-value |

### Table 4 — Policy Counterfactuals
| Content | WHO vs CONAMA scenarios |
|---------|------------------------|
| Hospitalizations preventable under WHO (15 µg/m³) |
| Stratified by vulnerability group |
| Cost savings (BRL) |

### Table 5 — Sensitivity Analysis Summary
| Content | All robustness tests |
|---------|---------------------|
| Placebo test results |
| Alternative threshold results |
| Leave-one-city-out range |
| Continuous treatment dose-response |

### Supplementary Tables
- S1: Complete city-level CATE estimates (27 rows)
- S2: Full SHAP feature importance rankings
- S3: DLNM comparison results
- S4: Data quality summary per city

---

## Quality Checks

- [ ] Every number in abstract matches a table/figure
- [ ] CIs don't conflict with p-values
- [ ] Percentages sum to 100% where applicable
- [ ] No rounding errors >0.1%
- [ ] City names consistent throughout
- [ ] Sample sizes in Table 1 match N in analyses
- [ ] Sensitivity results don't contradict main findings (or if they do, flag to @study-conductor)

---

## Tasks

- [ ] Build Table 1 from processed data
- [ ] Build Tables 2-5 from model outputs
- [ ] Build Supplementary Tables
- [ ] Cross-validate all numbers with @technical-executor outputs
- [ ] Check claim ↔ evidence coherence with @scientific-storytelling Claims Map
- [ ] Deliver final tables in LaTeX format for @multilingual-writer

---

*@data-specialist v1.0 — 2026-02-21*
