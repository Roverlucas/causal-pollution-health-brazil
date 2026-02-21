# @visual-impact-specialist — Workflow & Responsibilities

> **Role:** Create high-impact figures, visual abstracts, and diagrams
> **Active:** Phase 3 (figures), Phase 4 (visual abstract, polish)
> **Tier:** 3 — Technical, Data & Figures

---

## Mission

Every figure must tell one story, be immediately understandable, and be publication-ready at 300 DPI. Figures are the first thing editors and reviewers see — they must be compelling.

---

## Figure Plan (5 main + 1 graphical abstract)

### Figure 1 — The Heterogeneity Map (HERO FIGURE)
- **Type:** Choropleth map of Brazil with 27 capital dots
- **Encoding:** Dot color = CATE magnitude (diverging colorscale); dot size = CI width (smaller = more precise)
- **Annotations:** Top 3 and bottom 3 capitals labeled
- **Message:** "The same pollutant causes vastly different health impacts depending on where you live"
- **Specs:** Full page width, 300 DPI, PDF vector
- **Tools:** `geopandas` + `matplotlib` with IBGE shapefiles

### Figure 2 — The Vulnerability Forest Plot
- **Type:** Horizontal forest plot with point estimates + 95% CIs
- **Groups:** Age (0-14, 15-59, 60+), Sex (M/F), Fleet density (tertiles), DTR (tertiles), Region (5)
- **Reference line:** Overall ATE (dashed)
- **Color coding:** Red (above average), blue (below average)
- **Message:** "Elderly in high-fleet cities face 2-5× the average effect"
- **Specs:** Single column, clean, minimal

### Figure 3 — SHAP Beeswarm
- **Type:** SHAP beeswarm plot for CATE heterogeneity
- **Features:** Top 8-10 moderators ranked by importance
- **Color:** Feature value (low=blue, high=red)
- **Message:** "Fleet density and age group are the strongest drivers of who suffers most"
- **Specs:** Single column, SHAP library default with refinements

### Figure 4 — Policy Counterfactual
- **Type:** Grouped bar chart
- **Groups:** WHO scenario vs CONAMA current, split by vulnerability tertile
- **Y-axis:** Hospitalizations preventable per year
- **Annotations:** Total numbers, cost savings
- **Message:** "Adopting WHO standards would prevent X,000 hospitalizations, concentrated in the most vulnerable groups"
- **Specs:** Full width, clean, no 3D

### Figure 5 — Methodological Pipeline
- **Type:** Flow diagram (horizontal)
- **Steps:** Data Sources → Integration → Causal Identification → Estimation → Explanation → Policy
- **Icons:** Database, merge, DAG, tree, SHAP, policy shield
- **Message:** "Transparent, reproducible, end-to-end"
- **Specs:** Full width, vector, clean minimalist design

### Graphical Abstract
- **Type:** Infographic (~18×9 cm)
- **Elements:** Mini-map (Fig 1), key numbers (N cities, N hospitalizations, max CATE ratio), policy takeaway arrow
- **Message:** One image = entire paper story
- **Required for:** Environment International (mandatory), useful for all journals

---

## Design Standards

| Parameter | Standard |
|-----------|----------|
| Resolution | 300 DPI minimum (600 for line art) |
| Format | PDF (vector) for journal; PNG for presentations |
| Colors | Colorblind-safe palette (viridis, cividis, or custom diverging) |
| Fonts | Helvetica/Arial, 8-10pt for labels |
| Borders | No box around figures (clean style) |
| Legends | Inside figure when possible, not separate |
| White space | Generous — no cramming |
| Journal compliance | Check specific journal figure guidelines before final |

---

## Tasks

- [ ] Source IBGE shapefiles for Brazil map
- [ ] Design colorscale and layout for Figure 1
- [ ] Generate Figures 1-5 from @technical-executor outputs
- [ ] Design Graphical Abstract
- [ ] Test all figures for colorblind accessibility
- [ ] Export at journal-required resolution and format
- [ ] Review figure captions with @multilingual-writer

---

*@visual-impact-specialist v1.0 — 2026-02-21*
