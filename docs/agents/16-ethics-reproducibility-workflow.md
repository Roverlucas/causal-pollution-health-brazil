# @ethics-reproducibility — Workflow & Responsibilities

> **Role:** Ethics compliance, reproducibility, and open science
> **Active:** Phase 2 (plan), Phase 5 (final verification)
> **Tier:** TOOL — Quality & Compliance

---

## Mission

Ensure the study meets ethical standards and that every result is fully reproducible by an independent researcher with access to the same data.

---

## Ethics Assessment

### Study Classification
- **Type:** Ecological time-series study using publicly available, aggregate administrative data
- **Human subjects:** No individual-level data accessed
- **Data sources:** All public (DATASUS, IBGE, SENATRAN, Open-Meteo, CAMS)
- **Ethics approval:** Likely exempt (aggregate, public data) — verify with institutional rules
- **Informed consent:** Not applicable (no identifiable subjects)

### Ethics Statement for Manuscript
> "This study used publicly available, aggregate administrative data from the Brazilian Unified Health System (SIH/SUS), the Brazilian Institute of Geography and Statistics (IBGE), the National Traffic Secretariat (SENATRAN), and open meteorological/air quality APIs. No individual-level health records were accessed. The study was conducted in accordance with the Declaration of Helsinki. [Ethics committee exemption/approval: TBD]."

---

## Reproducibility Plan

### Code Repository
- **Platform:** GitHub (public upon submission)
- **URL:** https://github.com/Roverlucas/causal-pollution-health-brazil
- **License:** MIT (code) + CC-BY 4.0 (manuscript/figures)

### Reproducibility Requirements

| Component | Requirement | Implementation |
|-----------|------------|---------------|
| Code | Complete pipeline from raw data to all results | `src/` directory with Makefile |
| Dependencies | Exact versions locked | `pyproject.toml` with locked versions |
| Data | All raw data accessible or instructions to obtain | `data/raw/` or extraction scripts |
| Seeds | All random operations seeded | `config.py` with global seed |
| Environment | Reproducible Python environment | `uv` lockfile or `requirements.txt` |
| Documentation | Step-by-step instructions | `README.md` |
| Outputs | All figures and tables regenerable | `Makefile` targets |

### Data Availability Statement
> "All data used in this study are publicly available. Climate and air quality data were obtained from the Open-Meteo API (https://open-meteo.com). Hospitalization data are from the Brazilian Unified Health System (SIH/SUS) via DATASUS (https://datasus.saude.gov.br). Demographic data are from IBGE SIDRA (https://sidra.ibge.gov.br). Vehicle fleet data are from SENATRAN. The integrated dataset and analysis code are available at [GitHub URL]. The Clima360 Brasil platform (https://github.com/Roverlucas/clima-360-brasil) provides the data integration infrastructure."

---

## Open Science Checklist

- [ ] Pre-registration of primary hypotheses (optional but recommended — OSF)
- [ ] Code repository public before submission
- [ ] Data access instructions complete
- [ ] All figures reproducible from code
- [ ] No proprietary tools required (all open-source)
- [ ] Supplementary materials comprehensive
- [ ] STROBE adherence documented
- [ ] Conflict of interest declarations complete
- [ ] Author contributions (CRediT taxonomy) documented

---

## Tasks

- [ ] Verify ethics exemption with UTFPR institutional rules
- [ ] Write ethics statement for manuscript
- [ ] Write data availability statement
- [ ] Verify all data sources are publicly accessible
- [ ] Test full pipeline reproducibility (clean environment)
- [ ] Add license files to repository
- [ ] Prepare CRediT author contribution statement

---

*@ethics-reproducibility v1.0 — 2026-02-21*
