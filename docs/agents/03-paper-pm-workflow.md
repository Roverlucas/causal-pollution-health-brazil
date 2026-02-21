# @paper-pm — Workflow & Responsibilities

> **Role:** Project manager — deadlines, versions, cadence, dependencies
> **Active:** All phases (parallel to study-conductor)
> **Tier:** 0 — Direction & Strategy

---

## Mission

Keep the project on track with realistic deadlines, clear dependencies, version control, and cadence. Prevent scope creep and stalls.

---

## Master Timeline

**Start date:** 2026-02-21
**Target submission:** 2026-04-07 (45 days)

| Phase | Start | End | Duration | Gate | Status |
|-------|-------|-----|----------|------|--------|
| 0 - Kickoff | Feb 21 | Feb 22 | 2d | Gate 0 | 🟡 In Progress |
| 1 - Scoping | Feb 23 | Mar 02 | 8d | Gate 1 | ⬜ Pending |
| 2 - Methodology | Mar 03 | Mar 09 | 7d | Gate 2 | ⬜ Pending |
| 3 - Execution | Mar 10 | Mar 22 | 13d | Gate 3 | ⬜ Pending |
| 4 - Writing | Mar 23 | Mar 30 | 8d | Gate 4 | ⬜ Pending |
| 5 - Submission | Mar 31 | Apr 05 | 6d | Gate 5 | ⬜ Pending |
| Buffer | Apr 06 | Apr 07 | 2d | — | ⬜ Buffer |

---

## Dependency Map

```
Phase 0 (Charter + Journals + Thesis)
  ↓
Phase 1 (Literature + Gap + Claims Map)
  ├── @literature-specialist: Evidence Matrix
  ├── @bibliometrics-specialist: Field mapping
  └── @scientific-storytelling: Claims Map v1
  ↓
Phase 2 (Methods + Stats Plan)
  ├── @methodology-specialist: Methods Spec [depends on Claims Map]
  ├── @statistical-reviewer: Stats Plan [depends on Methods Spec]
  └── @ethics-reproducibility: Reproducibility Plan
  ↓
Phase 3 (Execute + Analyze + Figures)
  ├── @technical-executor: Run causal forests [depends on Stats Plan]
  ├── @data-specialist: Analyze + validate [depends on execution results]
  └── @visual-impact-specialist: Figures [depends on analyzed results]
  ↓
Phase 4 (Write + Translate + Visual Abstract)
  ├── @multilingual-writer: Manuscript V1 [depends on figures + claims map v2]
  ├── @scientific-storytelling: Narrative review [parallel]
  └── @visual-impact-specialist: Graphical abstract [depends on key figures]
  ↓
Phase 5 (Format + Pack + QA)
  ├── @journal-formatter: Format for Journal A [depends on Manuscript V1]
  ├── @submission-specialist: Cover letter + pack [depends on formatted manuscript]
  └── @qa-board: Final QA [depends on all above]
```

---

## Version Control Protocol

| Version | Phase | Description |
|---------|-------|-------------|
| v0.1 | Phase 2 | Methods section draft |
| v0.2 | Phase 3 | Results + Figures draft |
| v0.3 | Phase 4 | Complete manuscript V1 |
| v0.4 | Phase 4 | Post-internal review |
| v1.0 | Phase 5 | Submission-ready |

**Rule:** Every version is a Git commit with tag. No file-name versioning.

---

## Cadence

- **Daily:** Study Conductor checks phase progress
- **Per gate:** Formal gate review with checklist + score
- **Blockers:** Escalate within 24h, resolve within 48h

---

## Tasks

- [x] Create master timeline
- [x] Map dependencies
- [x] Define version protocol
- [ ] Track phase completion dates (ongoing)
- [ ] Report stalls >2 days to study-conductor
- [ ] Update timeline if scope changes

---

*@paper-pm v1.0 — 2026-02-21*
