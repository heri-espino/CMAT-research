# Paper 2.1 — CMAT visit-frequency structure

This branch is the canonical exploratory/publication workspace for **Paper 2.1**, a denser extension of Paper 2 focused on the structure of academic outcomes across different frequencies of CMAT attendance among students who use the centre.

**Parent checkpoint:** created from `paper/paper2-mu-performance` at commit `1956ef4bfe6073c9b28881a9da34d14cd22239a8`.

Paper 2 remains the simpler attendance-versus-non-attendance manuscript. Paper 2.1 asks a broader question: after the large zero-versus-any-attendance separation, how do outcomes vary across positive attendance frequencies, and does attendance also relate to the composition of adverse outcomes, particularly voluntary withdrawal versus numeric failure?

Read in this order:

1. `PAPER_BRANCH.md`
2. `paper/docs/project/PROJECT_CONTEXT.md`
3. `paper/docs/analysis/ANALYSIS_PLAN.md`
4. `paper/docs/results/PRELIMINARY_RESULTS.md`
5. `paper/docs/interpretation/ACADEMIC_MANAGEMENT_HYPOTHESIS.md`
6. `literature_selected/ACCESS_NOTES.md`
7. `paper/docs/project/STATUS_AND_ROADMAP.md`
8. `paper/AI_HANDOFF.md`

## Branch layout

Paper 2.1-specific material is organised by function rather than kept as loose files:

```text
paper/
├── README.md
├── AI_HANDOFF.md
├── docs/
│   ├── project/
│   ├── analysis/
│   ├── results/
│   └── interpretation/
├── sections/
└── manuscript/build sources

literature_selected/   # paper-specific literature map and access notes
code/                  # thin Paper 2.1 orchestration
results/paper21/       # canonical aggregate tables and vector figures
submission/            # submission metadata and checklist
```

Generated manuscript PDFs are intentionally not tracked; the paper-build workflow uploads them as GitHub Actions artifacts.

## Scientific boundary

Paper 2.1 inherits from Paper 2:

- first eligible MU attempt in periods with CMAT coverage;
- period-wide CMAT attendance, irrespective of visit subject label;
- instructor × academic-period grading context;
- observational framing;
- institutional pass mark of 7.5;
- BA, BV, and RT as adverse/non-passing outcomes.

Paper 2.1 **does not inherit the 4+ top-code as a fixed scientific decision**. The upper visit grouping must be chosen using an outcome-blind support/precision rule documented before pairwise outcome comparisons are inspected.

## Main contribution

Paper 2.1 now has two linked contributions.

First, it separates **initial CMAT use** from **frequency among users**. The primary positive-attendance groups are outcome-blind `1 / 2 / 3 / 4 / 5 / 6+`, with `1 / 2 / 3 / 4 / 5 / 6 / 7+` as an exploratory sensitivity. The current controlled-data results show a large 0-versus-1+ association in both standardised performance and pass probability, but no robust multiplicity-adjusted separation among positive frequency groups.

Second, it distinguishes a **performance margin** from an **academic-management margin**. Non-PASS is decomposed into numeric failure and administrative outcomes, with BV, RT and BA preserved separately. The current adjusted zero-versus-any-attendance pattern is specifically concentrated in BV versus numeric failure; RT does not show the same contrast. This may be discussed as compatible with broader academic engagement or institutional navigation, but those mechanisms are not directly measured.

The manuscript analyses:

1. continuous instructor-period-standardised final performance;
2. PASS versus non-PASS;
3. the composition of PASS / numeric <7.5 / BV-RT / BA, with exact BV / RT / BA diagnostics;
4. conditional non-PASS management contrasts.

A numeric-only complete-case outcome is retained as a sensitivity, especially for interpreting how administrative outcomes affect the lower tail of the continuous outcome.

## Repository governance

This is a long-lived `paper/*` branch. Do not merge the whole branch into `main` or back into Paper 2. Reusable estimators or support diagnostics that belong across papers should be proposed for upstream integration into `cmat_analysis` and then brought back into this branch.

The user retains final scientific authority.
