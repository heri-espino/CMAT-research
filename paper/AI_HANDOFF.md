# Paper 2.1 — scientific and editorial handoff

**Scope is final for the current drafting stage:** only two academic outcomes (Z and PASS), attendance-frequency levels, instructor–period fixed effects and degree controls, clustered Wald/omnibus tests and Holm adjustment by explicitly labelled family. Maintain the manuscript in `paper/sections/01.tex`–`04.tex` and the research memory in `notes/`.

## Required reading
1. `notes/README.md`, `notes/04_METODOLOGIA_HOLM.md`, `notes/05_RESULTADOS_Y_PROCEDENCIA.md`.
2. `paper/docs/analysis/VISIT_GROUPING_DECISION.md`, `paper/docs/results/PRELIMINARY_RESULTS.md`.
3. `literature_selected/READING_GUIDE.md`, `literature_selected/ACCESS_NOTES.md`.
4. `submission/METADATA.md`; `paper/README.md`.

## Inferential separation

The positive-only pre-outcome support grouping is `1/2/3/4/5/6+` (15 comparisons per outcome), with finer `1/2/3/4/5/6/7+` as a sensitivity (21). The zero-inclusive eight-level model (28) is a distinct specification. The full-grid PASS 7+ minus 1 result (+14.5 pp; Holm p=.0206) cannot be silently carried over to the positive-only analysis, where no pair remains Holm significant. Instructor-cluster 6+ minus 1 sensitivity is a separate result (+12.0 pp; Holm p=.0358).

Benchmark zero vs any attendance: +0.361 Z, +15.3 PASS percentage points. Both are observational adjusted associations, not causal effects or student-level before/after changes. No equivalence margin was fixed; absence of rejection is not equality. Clearly label the primary pooled 6+ group and later exploratory exact-six/7+ reporting choice.

## Production

Only the support and outcome runners should be invoked by `paper/paper_build_figures.py`. The public paper uses the three PDF dashboards for differences and Holm values. No secondary modelling is called or described in Methods/Results/Discussion.

Do not overwrite or falsify the older research history; separate research remains preserved in its own independent branch. Never place administrative microdata or student identifiers into GitHub. Update notes and claims matrix whenever a numerical result changes.

## Remaining blockers

Confirm historical CMAT hours, PPA eligibility and time span; audit model/tables and Holm families; obtain exact UDLAP ethics/data-use wording; verify journal policy and source access; compile and check the TEAMAT PDF. This rewrite has not re-estimated the institutional dataset.