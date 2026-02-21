# @qa-board — Workflow & Responsibilities

> **Role:** Cross-cutting quality validation at each gate
> **Active:** All gate reviews
> **Tier:** TOOL — Quality & Compliance

---

## Mission

No claim without evidence. No number without source. No inconsistency between sections. The QA Board is the last line of defense before submission.

---

## Gate Review Checklists

### Gate 0 — Kickoff ✅
- [x] Project Charter complete with all sections
- [x] Research question clear, specific, and answerable
- [x] Hypothesis falsifiable with available data
- [x] Journal targets A/B/C with rationale
- [x] Timeline realistic with buffer
- [x] Risks identified with mitigations
- [x] Decision log initialized

### Gate 1 — Scoping (Phase 1)
- [ ] Evidence matrix with ≥30 relevant references
- [ ] Gap statement validated against literature
- [ ] Claims Map v1 complete (all claims have planned evidence)
- [ ] No major omission in related work
- [ ] Bibliometric positioning clear

### Gate 2 — Methodology (Phase 2)
- [ ] DAG complete and justified
- [ ] Identification strategy explicitly stated
- [ ] All variables defined with sources
- [ ] Robustness tests pre-registered
- [ ] Reproducibility plan in place
- [ ] STROBE checklist items addressed in design
- [ ] @statistical-reviewer approved statistical plan

### Gate 3 — Execution (Phase 3)
- [ ] Pipeline runs end-to-end without errors
- [ ] Results reproducible from raw data (re-run test)
- [ ] All sensitivity tests completed
- [ ] Figures publication-ready (300 DPI, colorblind-safe)
- [ ] Tables internally consistent (totals match, CIs consistent with p-values)
- [ ] Claims Map v2 updated with actual evidence
- [ ] No claim unsupported by results

### Gate 4 — Manuscript (Phase 4)
- [ ] All sections complete and coherent
- [ ] Word count within journal limit
- [ ] Abstract matches body content
- [ ] Every number in text matches tables/figures
- [ ] References complete and correctly formatted
- [ ] No orphan references
- [ ] No unsupported claims
- [ ] Narrative arc follows STORYTELLING.md
- [ ] Statistical language approved by @statistical-reviewer
- [ ] Acknowledgments and disclosures complete

### Gate 5 — Submission (Phase 5)
- [ ] Journal formatting 100% compliant
- [ ] Cover letter compelling and accurate
- [ ] STROBE checklist completed
- [ ] All supplementary materials prepared
- [ ] Data/code availability verified (GitHub repo public)
- [ ] All co-author approvals obtained
- [ ] Submission checklist from @submission-specialist complete
- [ ] Final proofread completed

---

## Cross-Cutting Checks

| Check | Applied At | Method |
|-------|-----------|--------|
| Claim ↔ Evidence coherence | Gates 3, 4, 5 | Cross-reference Claims Map with Results |
| Number consistency | Gates 3, 4, 5 | Abstract vs body vs tables vs figures |
| Reference validity | Gates 1, 4 | All refs exist, DOIs resolve, no retractions |
| Statistical language | Gate 4 | No causal overclaiming; appropriate hedging |
| Plagiarism | Gate 4 | Similarity check (optional: iThenticate) |
| Formatting | Gate 5 | Journal-specific checklist |

---

## Tasks

- [x] Complete Gate 0 review
- [ ] Execute Gate 1-5 reviews at each phase transition
- [ ] Flag any quality issues to @study-conductor
- [ ] Maintain running quality score

---

*@qa-board v1.0 — 2026-02-21*
