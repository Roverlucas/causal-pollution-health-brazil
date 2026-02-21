# Scientific Storytelling — Narrative Architecture

> **Agent:** @scientific-storytelling
> **Phase:** 0-1 (Foundation narrative, refined at each gate)
> **Goal:** Transform rigorous causal inference into a compelling, publishable story that resonates with editors, reviewers, and policymakers

---

## 1. The Opening Hook (Abstract + Introduction §1)

### The Human Story

> *In September 2024, Manaus registered PM2.5 levels 11 times above WHO guidelines as unprecedented wildfires engulfed the Amazon. In the same month, São Paulo — 2,700 km away — saw its worst air quality in a decade. Emergency rooms across Brazil overflowed with respiratory patients. But here is what the headlines missed: not everyone was equally at risk.*

**The Provocation:** Brazil enacted its National Air Quality Policy (Law 14,850/2024) and updated CONAMA standards — yet these standards set a single threshold for all citizens. A 4-year-old in Manaus with developing lungs. A 75-year-old in Cuiabá with COPD. A bus driver in São Paulo exposed 8 hours daily. The law treats them as the same person. They are not.

### The Knowledge Gap (§1.2)

- **What we know:** Air pollution causes respiratory disease. This is established beyond doubt (GBD 2019: 4.2M deaths/year globally; 326k in Brazil 2019-2021).
- **What we assume:** The effect is roughly uniform — "X% increase in hospitalizations per 10 µg/m³ PM2.5" — the population-average paradigm.
- **What we don't know:** *Who suffers most, where, and why?* Traditional epidemiological methods (Poisson regression, case-crossover, GAM) estimate one number for everyone. They cannot tell policymakers which subpopulations need priority protection.
- **Why this matters now:** Brazil just redesigned its air quality governance (CONAMA 506/2024, MonitoAr system). This is the window to embed heterogeneity-aware evidence into policy before standards solidify for the next decade.

### The Promise (§1.3)

We introduce **causal machine learning** — specifically, Honest Causal Forests (Athey & Wager, 2019) and Double Machine Learning (Chernozhukov et al., 2018) — to environmental health epidemiology in Brazil. For the first time, we move from *"pollution is harmful"* to *"pollution is THIS harmful for THIS person in THIS city, and here is why."*

---

## 2. The Context Architecture (Introduction §2 + Related Work)

### Layer 1: The Brazilian Paradox
- Brazil is the world's 5th-largest country by area and population
- Vehicle fleet reached 124 million in 2024 (4th largest globally)
- PROCONVE reduced per-vehicle emissions by 98% — yet fleet grew so fast that net health gains are uncertain
- Only 11 of 26 states have continuous air quality monitoring
- The country spans tropical, semi-arid, subtropical, and equatorial climates — one-size-fits-all thresholds are scientifically untenable

### Layer 2: The Methodological Plateau
- 20+ years of GAM/GLM/case-crossover studies in São Paulo (ESCALA study now 15 years old)
- Nearly zero studies covering all 27 capitals simultaneously
- Zero applications of causal ML in Brazilian environmental health
- The AJE published a practical guide for causal forests in epidemiology (2023) — but nobody has applied it in the global south

### Layer 3: The Policy Window
- Law 14,850/2024 created the National Air Quality Policy
- CONAMA 506/2024 updated emission standards (criticized by Lancet Planetary Health as "not justified in terms of human health")
- MonitoAr system approved but implementation incomplete
- Evidence gap: regulators lack subpopulation-specific dose-response data to set differentiated alerts

### Layer 4: The Data Revolution
- Clima360 Brasil platform integrates 5 data sources across 27 capitals (daily granularity)
- SIH/SUS provides 6.16M hospitalizations with age, sex, cost, and ICD stratification
- This data infrastructure did not exist 5 years ago — the study is only possible now

---

## 3. The Contribution Narrative (§1.4 + Discussion)

### What We Bring (5 Pillars)

**Pillar 1 — FROM ASSOCIATION TO CAUSATION**
> "For two decades, Brazilian environmental epidemiology has documented associations. We take the next step: causal identification under explicit assumptions, with rigorous sensitivity analysis."

- Conditional ignorability given rich meteorological confounders
- Robustness: placebo treatments, pre-treatment falsification tests, Rosenbaum bounds

**Pillar 2 — FROM AVERAGE TO HETEROGENEOUS**
> "The average masks the extreme. A population-average relative risk of 1.05 may hide a subgroup at RR 1.25 and another at RR 0.98. We reveal the distribution of harm."

- CATE estimates by age, sex, city, fleet density, thermal amplitude
- CLAN analysis identifies the "most affected" and "least affected" subgroups
- Policy implication: differentiated alert thresholds

**Pillar 3 — FROM 6 CITIES TO 27 CAPITALS**
> "Previous multi-city studies covered 2-6 Brazilian cities. We cover all 27 state capitals — from Boa Vista (equatorial, 400K pop) to São Paulo (subtropical, 11.5M pop) — for the first time."

- Geographic and climatic heterogeneity as a feature, not a limitation
- Meta-regression reveals structural moderators of effect heterogeneity

**Pillar 4 — FROM BLACK-BOX TO EXPLAINABLE**
> "Machine learning without explanation is science without communication. Every causal estimate is accompanied by SHAP attribution — making heterogeneity transparent and actionable."

- SHAP values on Causal Forest outputs (novel methodological contribution)
- Vulnerability maps readable by non-technical policymakers
- Dashboard-ready outputs integrated with Clima360

**Pillar 5 — FROM EVIDENCE TO ACTION**
> "We don't stop at estimation. We translate heterogeneous effects into policy counterfactuals: how many hospitalizations would each capital prevent by adopting WHO vs. current CONAMA standards, stratified by vulnerability?"

- Prevented Fraction under intervention scenarios
- Cost-benefit by subgroup (using SIH/SUS cost data)
- Input for MonitoAr alert calibration

---

## 4. The Narrative Arc (Full Paper Flow)

```
HOOK        →  "Not everyone breathes the same risk"
             ↓
CONTEXT     →  Brazil's air quality crisis × policy window × data revolution
             ↓
GAP         →  Average effects hide heterogeneity; no causal ML in Brazil
             ↓
PROMISE     →  First causal heterogeneity map across 27 capitals
             ↓
METHOD      →  Honest Causal Forests + DML + SHAP (rigorous, transparent)
             ↓
RESULTS     →  [Dramatic heterogeneity revealed: 2-5× variation in CATE]
             ↓
MEANING     →  [Children and elderly in high-fleet cities bear disproportionate burden]
             ↓
ACTION      →  WHO adoption would prevent X,000 hospitalizations, concentrated in Y groups
             ↓
IMPACT      →  Evidence for differentiated air quality alerts + CONAMA revision
             ↓
LEGACY      →  Methodological template exportable to any LMIC with DATASUS-equivalent data
```

---

## 5. Key Phrases & Framing

### Power phrases for the manuscript:

- "Heterogeneity is not noise — it is the signal public policy has been missing"
- "From population averages to personalized environmental risk"
- "The average relative risk is a statistical fiction that protects no one optimally"
- "Brazil's unique combination of continental-scale data, climatic diversity, and universal health system creates an unparalleled natural laboratory"
- "Causal forests do not predict — they explain *for whom* and *why*"
- "The cost of treating everyone equally is that the most vulnerable pay the highest price"

### Framing rules:

| Instead of... | Say... |
|---------------|--------|
| "We used machine learning" | "We applied causal machine learning for valid statistical inference" |
| "We predicted hospitalizations" | "We estimated heterogeneous causal effects on hospitalizations" |
| "Results show correlation" | "Causal estimates under conditional ignorability reveal..." |
| "Big data analysis" | "Integration of five national data systems across 27 capitals" |
| "AI for health" | "Transparent causal inference with explainable attribution" |

---

## 6. Visual Storytelling Plan

### Figure 1 — The Heterogeneity Reveal (Hero Figure)
**Type:** Geospatial CATE map of Brazil's 27 capitals
**Message:** "Effect varies 2-5× across cities" — visual impact for editor's first impression
**Design:** Choropleth + dot overlay (dot size = confidence interval width)

### Figure 2 — Who Suffers Most?
**Type:** Forest plot of CATE by subgroup (age × sex × fleet density tertile)
**Message:** Clear ranking of vulnerability — elderly in high-fleet cities at top

### Figure 3 — The SHAP Explanation
**Type:** Beeswarm SHAP plot showing which moderators drive heterogeneity
**Message:** "Fleet density and age are the top drivers of who suffers most"

### Figure 4 — Policy Counterfactual
**Type:** Stacked bar chart — preventable hospitalizations under WHO vs CONAMA by city group
**Message:** "Adopting WHO standards would prevent X,000 hospitalizations, with Y% concentrated in the most vulnerable groups"

### Figure 5 — Methodological Pipeline
**Type:** Flow diagram — data integration → causal identification → forest estimation → SHAP → policy
**Message:** "Reproducible, transparent, end-to-end causal pipeline"

### Visual Abstract (Graphical Abstract)
**Type:** Infographic combining Figure 1 (map), key numbers, and policy takeaway
**Message:** One image that tells the whole story for social media and journal landing page

---

## 7. Impact Narrative

### Academic Impact
- First causal ML application in environmental health in Latin America
- Methodological template for any country with hospitalization + pollution data
- Advances the "heterogeneous treatment effects in environmental epidemiology" frontier
- Citable by the WHO AQG evidence review for next revision

### Policy Impact
- Direct input for CONAMA standard revision (currently criticized as inadequate)
- Evidence base for MonitoAr's alert calibration by subpopulation
- Cost-benefit data for state-level Emission Control Plans
- Framework for environmental justice: identifying who bears disproportionate burden

### Societal Impact
- Makes invisible inequity visible: same air, different risk
- Translates to operational alert systems (Clima360 integration)
- Media-friendly narrative: "Who breathes the worst air in Brazil — and who pays the highest health cost?"

---

## 8. Anticipated Reviewer Concerns & Pre-emptive Responses

| Concern | Pre-emptive Strategy |
|---------|---------------------|
| "Causal claims too strong for observational data" | Explicit assumptions stated; sensitivity analysis (Rosenbaum bounds); multiple robustness checks |
| "Satellite/reanalysis PM2.5 ≠ ground monitors" | Acknowledge measurement error; cite validation studies; show results robust to error-in-variable corrections |
| "SUS-only data misses private hospitalizations" | ~75% of Brazil depends on SUS; discuss direction of bias; show SUS coverage varies by city and adjust |
| "Short time window (2022-2025)" | Strength is spatial breadth (27 cities); temporal limitation honestly acknowledged |
| "Causal forests are a black box" | SHAP integration makes every estimate explainable; compare with traditional DLNM |
| "Why not individual-level data?" | Ecological design acknowledged; strength is complete population coverage; discuss ecological fallacy mitigation |

---

*@scientific-storytelling v1.0 — Last updated: 2026-02-21*
*"The best science tells a story that cannot be ignored."*
