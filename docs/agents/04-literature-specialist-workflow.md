# @literature-specialist — Workflow & Responsibilities

> **Role:** Systematic literature search, filtering, and evidence synthesis
> **Active:** Phase 1 (primary), Phase 4 (reference validation)
> **Tier:** 1 — Evidence & Scientific Base

---

## Mission

Build the definitive evidence base for this study: what exists, what's missing, and where our contribution sits in the landscape.

---

## Search Strategy

### Search Domains (5 pillars)

**Pillar 1: Air Pollution & Health in Brazil**
- Databases: PubMed, Scopus, Web of Science
- Keywords: ("air pollution" OR "PM2.5" OR "particulate matter" OR "ozone") AND ("hospitaliz*" OR "morbidity" OR "respiratory") AND ("Brazil" OR "Brazilian")
- Filter: 2018-2026, English/Portuguese
- Expected yield: ~200 papers → ~40 highly relevant

**Pillar 2: Causal Inference in Environmental Epidemiology**
- Keywords: ("causal forest*" OR "double machine learning" OR "causal inference" OR "heterogeneous treatment effect*") AND ("air pollution" OR "environmental" OR "climate")
- Expected yield: ~80 papers → ~20 methodological anchors

**Pillar 3: Temperature Variability (DTR) & Health**
- Keywords: ("diurnal temperature range" OR "thermal amplitude" OR "temperature variability") AND ("hospitaliz*" OR "mortality" OR "cardiovascular" OR "respiratory")
- Expected yield: ~60 papers → ~15 key refs

**Pillar 4: Machine Learning for Pollution-Health**
- Keywords: ("machine learning" OR "random forest" OR "XGBoost" OR "deep learning" OR "SHAP") AND ("air quality" OR "air pollution") AND ("health" OR "hospitaliz*")
- Expected yield: ~150 papers → ~25 method comparisons

**Pillar 5: Multi-City Studies in Brazil / Latin America**
- Keywords: ("multi-city" OR "multiple cities" OR "nationwide") AND ("air pollution" OR "air quality") AND ("Brazil" OR "Latin America")
- Expected yield: ~30 papers → ~10 benchmarks

---

## Deliverables

### Evidence Matrix (Phase 1)
A structured table of the top ~50 papers with:

| Column | Description |
|--------|-------------|
| Reference | Author, year, journal |
| Scope | Cities, country, sample size |
| Method | Statistical approach |
| Exposure | Pollutants, temperature metrics |
| Outcome | Health endpoint |
| Key finding | Main result with effect size |
| Limitation | Author-stated limitation |
| Gap | What they didn't do that we will |
| Relevance | Low / Medium / High for our study |

### Gap Synthesis Report (Phase 1)
Narrative summary organized by:
1. What is well-established (consensus)
2. What is emerging but uncertain (debate)
3. What is absent (gap we fill)

### Reference List (Phase 4)
- Validated BibTeX file with all cited works
- Cross-check: every claim in manuscript has ≥1 reference
- No orphan references (cited but not used in argument)

---

## Key References Already Identified

### Foundational
- Athey, Tibshirani & Wager (2019) — Generalized Random Forests
- Chernozhukov et al. (2018) — Double/Debiased Machine Learning
- Wen et al. (2023) — Practical guide for causal forests in epidemiology (AJE)

### Brazilian Context
- Menezes-Filho et al. (2025) — 326k pollution deaths in Brazil
- Lancet Planetary Health (2024) — CONAMA critique
- Ye et al. (2025) — Wildfire PM2.5 and respiratory hospitalizations
- Schwantes et al. (2025) — DTR meta-analysis

### Methodological
- ESCALA study (HEI) — Multi-city Latin America benchmark
- Gasparrini & Armstrong — DLNM framework
- Lundberg & Lee (2017) — SHAP values

---

## Tasks

- [ ] Execute systematic search (5 pillars)
- [ ] Screen titles/abstracts (target: 500 → 100)
- [ ] Full-text review of top 100
- [ ] Build Evidence Matrix (50 papers)
- [ ] Write Gap Synthesis Report
- [ ] Deliver to @scientific-storytelling for Claims Map refinement
- [ ] Generate BibTeX file
- [ ] Validate references in final manuscript (Phase 4)

---

*@literature-specialist v1.0 — 2026-02-21*
