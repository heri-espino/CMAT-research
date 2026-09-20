# Paper 2.1 — status and roadmap

**Branch:** `paper/paper2.1-visit-frequency`  
**Created from Paper 2:** 2026-09-20  
**Stage:** full manuscript draft + remaining pre-submission robustness

## Current scientific idea

Paper 2.1 starts from a dense state-of-the-art review and treats the known 0-versus-1+ attendance association as a benchmark. Its substantive focus is the structure of outcomes **among CMAT users**, with attendance frequency resolved as finely as the data support.

Two principal outcome families will be analysed in parallel:

1. PASS versus non-PASS, with non-PASS = numeric <7.5 or BA/BV/RT;
2. continuous imputed final grade standardised within instructor-period group.

The current `4+` top-code is not binding on this branch.

## Milestones

### M0 — Branch and scientific contract — COMPLETE

- [x] create `paper/paper2.1-visit-frequency` from current Paper 2;
- [x] separate Paper 2.1 scope from Paper 2;
- [x] define dual principal outcomes;
- [x] document outcome-blind upper-frequency grouping principle;
- [x] document pairwise, heatmap, and equivalence strategy.

### M1 — State of the art — DRAFTED

- [x] review the selected mathematics-support literature specifically for visit-frequency grouping and repeated attendance;
- [x] extract how prior studies define 0, 1, repeated, and high-frequency attendance;
- [x] identify evidence about non-engagement, self-selection, and repeated use;
- [ ] identify whether any study formally tests equivalence or saturation/plateau patterns;
- [x] draft a dense state-of-the-art section ending in the Paper 2.1 research gap;
- [ ] perform a final literature audit before submission and add only sources that materially inform frequency grouping, repeated attendance, outcome composition, or interpretation;
- [x] cite Gokhool & Lawson (2026) only for abstract-supported claims and record the access limitation in `paper/LITERATURE_ACCESS_NOTES.md`.

### M2 — Support audit and final visit grouping — COMPLETE

- [x] generate exact positive-visit counts with instructor-period support;
- [x] quantify within-instructor-period overlap among positive groups;
- [x] compare candidate top-codes using the pair-overlap frontier;
- [x] freeze the final grouping before inspecting Paper 2.1 outcomes;
- [x] record the decision in `paper/VISIT_GROUPING_DECISION.md` and `paper/visit_grouping_spec.json`.

**Primary:** `1 / 2 / 3 / 4 / 5 / 6+`.

**Exploratory sensitivity:** `1 / 2 / 3 / 4 / 5 / 6 / 7+`.

### M3 — Dual-outcome and distributional inference

- [x] document the three-layer outcome framework in `paper/OUTCOME_FRAMEWORK.md`;
- [x] document the administrative-withdrawal attendance context and manuscript guardrail in `paper/ADMINISTRATIVE_OUTCOME_NOTE.md`;
- [x] implement the reproducible Paper 2.1 outcome runner;
- [x] verify the current controlled-data run in CI;
- [x] reproduce 0 vs 1+ benchmark for PASS and continuous Z;
- [x] run user-only omnibus model for continuous Z;
- [x] run user-only omnibus model for PASS probability;
- [x] estimate all positive-group pairwise contrasts;
- [x] apply Holm adjustment separately by outcome family;
- [x] flag adjacent contrasts explicitly in the pairwise outputs;
- [x] implement instructor-level clustering sensitivity through the shared cmat_analysis API;
- [ ] review the canonical instructor-level clustering outputs and decide whether they belong in the manuscript or supplement;
- [x] retain numeric-only continuous complete-case sensitivity;
- [x] implement PASS / numeric grade <7.5 / BV-RT / BA composition by frequency;
- [x] implement exact BV / RT / BA composition tables;
- [x] implement non-PASS administrative-vs-numeric benchmark and frequency models;
- [x] implement narrower non-PASS BV/RT-vs-numeric models;
- [x] implement imputed and complete-case Z-score quantile profiles;
- [x] verify and interpret the academic-management outputs from controlled-data CI, including BV-specific and RT-specific contrasts.

### M4 — Equivalence and visual synthesis

- [ ] decide whether defensible equivalence margins exist before testing;
- [ ] if yes, freeze margins and run equivalence tests;
- [x] produce continuous-Z pairwise heatmap;
- [x] produce pass-probability pairwise heatmap;
- [ ] optionally produce zero-inclusive supplementary heatmaps;
- [ ] fit an exploratory smooth/spline among users without using it to choose the categorical cut;
- [ ] write a synthesis classifying the observed structure as plateau/gradual/separated/irregular only to the extent supported by uncertainty.

### M5 — Entrance-exam extension — WAITING ON DATA

- [ ] inherit and complete the entrance-exam intake audit from Paper 2;
- [ ] assess coverage among the Paper 2.1 positive-frequency groups;
- [ ] rerun the principal models with observed baseline preparation if the score is usable;
- [ ] compare the frequency structure before and after baseline adjustment.

### M6 — Paper 2.1 manuscript — FULL DRAFT COMPLETE

- [x] replace the inherited Paper 2 manuscript with a Paper 2.1-specific manuscript;
- [x] begin with the dense state-of-the-art section;
- [x] keep 0 vs 1+ as a short benchmark rather than the main result;
- [x] make the pairwise frequency structure, performance margin, and academic-management margin the central Results section;
- [x] integrate the two heatmaps;
- [x] write a compact conclusion about what can and cannot be distinguished among attendance frequencies;
- [x] preserve observational/non-causal language.

## Shared-library status

Paper 2.1 reusable methods are upstream on `main` in **cmat-analysis 0.3.0** and documented through Sphinx and the generated function index. The paper runners are downstream consumers; future methodological improvements should be made in `main/cmat_analysis` first whenever they are reusable across education studies.

## Immediate next task

Treat `paper/sections/01.tex`--`04.tex` as the current Paper 2.1 manuscript draft. Immediate pre-submission priorities are: (1) instructor-level clustering sensitivity; (2) entrance-exam sensitivity if usable; (3) verify historical institutional rules for BV/RT/BA before making GPA/transcript claims; (4) resolve the ethics/data-use statement; (5) decide whether defensible equivalence margins exist; and (6) final referee-style literature/numbers audit. Do not change the frozen `1/2/3/4/5/6+` grouping in response to outcome significance.
