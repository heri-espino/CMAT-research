# Paper 2.1 — status and roadmap

**Branch:** `paper/paper2.1-visit-frequency`  
**Created from Paper 2:** 2026-09-20  
**Stage:** design and analysis specification

## Current scientific idea

Paper 2.1 starts from a concise state-of-the-art review and treats the known 0-versus-1+ attendance association as a benchmark. Its substantive focus is the structure of outcomes **among CMAT users**, with attendance frequency resolved as finely as the data support.

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

### M1 — State of the art — NEXT

- [ ] review the selected mathematics-support literature specifically for visit-frequency grouping and repeated attendance;
- [ ] extract how prior studies define 0, 1, repeated, and high-frequency attendance;
- [ ] identify evidence about non-engagement, self-selection, and repeated use;
- [ ] identify whether any study formally tests equivalence or saturation/plateau patterns;
- [ ] draft a dense state-of-the-art section ending in the Paper 2.1 research gap;
- [ ] add further literature only when it materially informs frequency grouping, repeated attendance, or outcome interpretation.

### M2 — Support audit and final visit grouping

- [ ] generate exact positive-visit counts with instructor-period support;
- [ ] quantify within-instructor-period overlap among positive groups;
- [ ] apply the outcome-blind grouping rule;
- [ ] freeze the final exact-plus-tail grouping before inspecting pairwise outcomes;
- [ ] record the grouping decision in a machine-readable/Markdown decision note.

Current candidate only: `1 / 2 / 3 / 4 / 5 / 6 / 7+`.

### M3 — Dual-outcome inference

- [ ] reproduce 0 vs 1+ benchmark for PASS and continuous Z;
- [ ] run user-only omnibus model for continuous Z;
- [ ] run user-only omnibus model for PASS probability;
- [ ] estimate all positive-group pairwise contrasts;
- [ ] apply Holm adjustment separately by outcome family;
- [ ] extract adjacent contrasts explicitly;
- [ ] run instructor-level clustering sensitivity;
- [ ] retain numeric-only continuous complete-case sensitivity.

### M4 — Equivalence and visual synthesis

- [ ] decide whether defensible equivalence margins exist before testing;
- [ ] if yes, freeze margins and run equivalence tests;
- [ ] produce continuous-Z pairwise heatmap;
- [ ] produce pass-probability pairwise heatmap;
- [ ] optionally produce zero-inclusive supplementary heatmaps;
- [ ] fit an exploratory smooth/spline among users without using it to choose the categorical cut;
- [ ] write a synthesis classifying the observed structure as plateau/gradual/separated/irregular only to the extent supported by uncertainty.

### M5 — Entrance-exam extension — WAITING ON DATA

- [ ] inherit and complete the entrance-exam intake audit from Paper 2;
- [ ] assess coverage among the Paper 2.1 positive-frequency groups;
- [ ] rerun the principal models with observed baseline preparation if the score is usable;
- [ ] compare the frequency structure before and after baseline adjustment.

### M6 — Paper 2.1 manuscript

- [ ] replace the inherited Paper 2 manuscript with a Paper 2.1-specific manuscript only after M2–M4 stabilize;
- [ ] begin with the dense state-of-the-art section;
- [ ] keep 0 vs 1+ as a short benchmark rather than the main result;
- [ ] make the pairwise frequency structure and dual-outcome comparison the central Results section;
- [ ] integrate the two heatmaps;
- [ ] write a compact conclusion about what can and cannot be distinguished among attendance frequencies;
- [ ] preserve observational/non-causal language.

## Immediate next task

Implement M2 first: exact-count support by instructor-period and the outcome-blind grouping decision. Do **not** inspect pairwise grades/pass rates while choosing the tail cut.

The inherited Paper 2 LaTeX manuscript currently remains in this branch as a baseline/provenance artifact; it is not yet the Paper 2.1 manuscript.
