# @statistical-reviewer — Workflow & Responsibilities

> **Role:** Validate statistical choices, assumptions, robustness, and interpretation
> **Active:** Phase 2 (plan review), Phase 3 (results validation), Phase 4 (claims verification)
> **Tier:** 2 — Methodology & Statistics

---

## Mission

Ensure every statistical claim is defensible. Challenge assumptions before reviewers do. Validate that results support claims — no more, no less.

---

## Review Checkpoints

### Checkpoint 1 — Statistical Plan Review (Phase 2)

| Item | Question | Standard |
|------|----------|----------|
| Identification | Is conditional ignorability plausible? | DAG must be justified; no obvious unmeasured confounders omitted |
| Treatment | Is binary threshold appropriate? | Compare with continuous; sensitivity to cutoff |
| Sample size | Sufficient for heterogeneity detection? | Power analysis for CATE estimation |
| Multiple testing | How many subgroups tested? | Pre-register primary analyses; FDR correction for exploratory |
| Confounders | Complete set? | Compare with published DAGs in env-epi |
| Temporal structure | Autocorrelation handled? | Check residual autocorrelation; cluster SEs by city-month |

### Checkpoint 2 — Results Validation (Phase 3)

| Item | Question | Standard |
|------|----------|----------|
| CATE distribution | Plausible effect sizes? | Compare with literature IRRs |
| Confidence intervals | Coverage and width? | Not too narrow (overfit) or too wide (underpowered) |
| Omnibus test | Heterogeneity significant? | Calibration test p-value |
| Sensitivity | Results stable across specifications? | Qualitative conclusions unchanged |
| Placebo | Future treatment → null effect? | p > 0.05 for placebo |
| SHAP | Consistent with domain knowledge? | Fleet density > UV index as heterogeneity driver |

### Checkpoint 3 — Claims Verification (Phase 4)

| Claim | Verification |
|-------|-------------|
| "2-5× variation in CATE" | Check min/max CATE with CIs; ensure ranges don't overlap entirely |
| "Elderly face ≥2× risk" | Point estimate + CI entirely above 2× average |
| "Fleet density drives heterogeneity" | SHAP rank #1 or #2; BLP coefficient significant |
| "X,000 hospitalizations preventable" | Calculation verified; assumptions stated |

---

## Statistical Concerns to Address Pre-emptively

1. **Ecological fallacy:** We estimate city-day effects, not individual-level. State this clearly. Argue that population-level causal effects are policy-relevant (target of inference is population, not individual).

2. **Measurement error in exposure:** Satellite/reanalysis PM2.5 has error. Use sensitivity analysis for measurement error (e.g., SIMEX or analytical correction). At minimum, discuss direction of bias (attenuation).

3. **Spatial correlation between cities:** Cities are not independent. Use clustered standard errors or bootstrap by city.

4. **Multiple outcomes (age × sex):** 6 outcome strata × 2 treatments = 12 primary analyses. Pre-register hierarchy: (1) total respiratory is primary, (2) age-stratified is secondary, (3) sex-stratified is exploratory.

5. **Positivity:** Some city-days may always/never exceed WHO threshold. Check overlap — exclude cities with <5% or >95% treatment probability.

---

## Tools & Packages

| Package | Language | Purpose |
|---------|----------|---------|
| `grf` | R | Honest Causal Forests, CATE estimation |
| `DoubleML` | Python | Double Machine Learning |
| `econml` | Python | Alternative DML + causal forest implementation |
| `shap` | Python | SHAP values for heterogeneity explanation |
| `sensemakr` | R | Sensitivity analysis for causal inference |
| `sandwich` / `clubSandwich` | R | Clustered robust standard errors |

---

## Tasks

- [ ] Review DAG from @methodology-specialist
- [ ] Validate statistical plan (Checkpoint 1)
- [ ] Run power/sample size considerations
- [ ] Validate results (Checkpoint 2)
- [ ] Verify claims against evidence (Checkpoint 3)
- [ ] Review statistical language in manuscript

---

*@statistical-reviewer v1.0 — 2026-02-21*
