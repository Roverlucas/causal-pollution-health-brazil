# @scientific-storytelling — Workflow & Responsibilities

> **Role:** Narrative architect — transforms science into a publishable story
> **Active:** Phase 0 (thesis), Phase 1 (gap + claims), Phase 4 (manuscript narrative), Phase 6 (reviewer adjustments)
> **Tier:** 0 — Direction & Strategy

---

## Mission

Craft a narrative arc so compelling that editors cannot desk-reject, reviewers want to champion, and policymakers want to cite. The story must be scientifically rigorous yet emotionally resonant.

---

## Deliverables by Phase

### Phase 0 — Thesis & Hook
- [x] Core thesis statement
- [x] Opening hook (human story + provocation)
- [x] Contribution framing (5 pillars)
- [x] Narrative arc (full paper flow)
- [x] Key phrases and framing rules
- [x] Visual storytelling plan
- [x] Impact narrative (academic + policy + societal)
- [x] Anticipated reviewer concerns with pre-emptive responses
- **Output:** `docs/STORYTELLING.md` ✅

### Phase 1 — Gap Narrative
- [ ] Refine gap statement based on systematic literature review
- [ ] Build Claims Map v1 (claim → evidence → figure → data)
- [ ] Validate gap with @literature-specialist findings
- **Output:** `docs/CLAIMS_MAP.md`

### Phase 4 — Manuscript Narrative
- [ ] Write Introduction draft (hook → context → gap → promise)
- [ ] Write Discussion draft (meaning → comparison → limitations → implications)
- [ ] Ensure narrative coherence across all sections
- [ ] Review figures for storytelling impact
- [ ] Draft graphical abstract concept
- **Output:** Sections of manuscript

### Phase 6 — Reviewer Response
- [ ] Adjust narrative if reviewers challenge framing
- [ ] Strengthen/weaken claims based on review feedback
- [ ] Maintain narrative integrity through revisions

---

## Claims Map (v1 — to be refined in Phase 1)

| # | Claim | Evidence Required | Figure/Table | Status |
|---|-------|-------------------|-------------|--------|
| C1 | Effect heterogeneity is statistically significant | Omnibus test p-value; CATE distribution | Fig 1 (map) + Fig 2 (forest plot) | Planned |
| C2 | Elderly (60+) face ≥2× higher causal risk | CATE by age group with CIs | Fig 2 (forest plot) | Planned |
| C3 | High-fleet cities amplify pollution-health effects | CATE by fleet density tertile | Fig 2 + SHAP | Planned |
| C4 | DTR modifies the pollution-health effect | Interaction CATE: high DTR × high PM2.5 | Fig 3 (SHAP) | Planned |
| C5 | WHO standards would prevent X,000 hospitalizations | Policy counterfactual calculation | Fig 4 (bar chart) | Planned |
| C6 | SHAP reveals fleet density and age as top heterogeneity drivers | SHAP importance ranking | Fig 3 (beeswarm) | Planned |
| C7 | Results are robust to sensitivity analyses | Rosenbaum bounds, placebo tests, alt specifications | Supplementary | Planned |

---

## Narrative Principles

1. **Lead with "why it matters"**, not "what we did"
2. **Specific numbers > vague statements** ("2.3× higher" beats "significantly higher")
3. **One story per figure** — each figure makes exactly one point
4. **The Discussion is not a summary** — it's where we say what the results *mean* for policy
5. **Limitations as strength** — "we acknowledge X, which means our estimates are conservative"
6. **The last paragraph must inspire action** — end with what should happen next, not what we found

---

*@scientific-storytelling v1.0 — 2026-02-21*
