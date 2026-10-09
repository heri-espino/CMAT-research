# Paper 2.1 — CMAT attendance frequency and Holm

**Publication branch:** `paper/paper2.1-visit-frequency`. This article studies recorded visit frequency and two final outcomes in Matemáticas Universitarias: instructor-period standardised grade Z and PASS. Its inference is limited to **fixed-effect adjusted Wald contrasts with Holm multiplicity correction** and directly relevant robustness analyses.

Read `notes/README.md` first, then `paper/docs/analysis/ANALYSIS_PLAN.md`, `paper/docs/analysis/VISIT_GROUPING_DECISION.md`, `paper/docs/results/PRELIMINARY_RESULTS.md`, `paper/sections/01.tex`–`04.tex` and `submission/METADATA.md`.

The primary outcome-blind support grouping for attendance among users was `1/2/3/4/5/6+`. The manuscript additionally reports the finer `0/1/2/3/4/5/6/7+` grid, without retroactively representing its tail split as a pre-outcome design choice. Inference among users (15 or 21 pairs) and inference including non-users (28 pairs) use distinct models and Holm families.

`code/run_paper21.py` conducts the attendance support audit, `code/run_paper21_outcomes.py` produces the relevant adjusted outcomes, `code/figures_paper21.py` generates Holm-only figures, and `paper/paper_build.py` produces the clean and commented TEAMAT drafts. The publication-facing results are the Holm aggregates under `results/paper21/tables/` and the three pairwise dashboard figures.

This is observational research; the effect of assigning a student a number of CMAT sessions is not identified. Non-significant contrasts do not establish equivalence.

Code and aggregate tables from other research directions are **not** part of this paper. Its compiled source and figures do not depend on those analyses. Shared reusable scientific methods belong to `main/cmat_analysis`; do not merge this entire paper branch into `main` or alter historical source provenance.

The compiled manuscript is not submission-ready until historical PPA/CMAT facts, statistical numbers, journal requirements and exact ethics/data-use wording are verified.