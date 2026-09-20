# Paper 2.1 — CMAT visit-frequency structure

This branch is the canonical exploratory/publication workspace for **Paper 2.1**, a denser extension of Paper 2 focused on the structure of academic outcomes across different frequencies of CMAT attendance among students who use the centre.

**Parent checkpoint:** created from `paper/paper2-mu-performance` at commit `1956ef4bfe6073c9b28881a9da34d14cd22239a8`.

Paper 2 remains the simpler attendance-versus-non-attendance manuscript. Paper 2.1 asks a broader question: after the large zero-versus-any-attendance separation, how do outcomes vary across positive attendance frequencies, and does attendance also relate to the composition of adverse outcomes, particularly voluntary withdrawal versus numeric failure?

Read in this order:

1. `PAPER_BRANCH.md`
2. `paper/PROJECT_CONTEXT.md`
3. `paper/ANALYSIS_PLAN.md`
4. `paper/PRELIMINARY_RESULTS.md`
5. `paper/ACADEMIC_MANAGEMENT_HYPOTHESIS.md`
6. `paper/LITERATURE_ACCESS_NOTES.md`
7. `paper/STATUS_AND_ROADMAP.md`
8. `paper/AI_HANDOFF.md`

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

The branch will investigate whether the familiar contrast between students with no recorded CMAT attendance and students who attend at least once is followed by:

- meaningful differences among positive attendance frequencies;
- plateaus in which adjacent visit counts are practically similar;
- a gradual pattern;
- or a more irregular relationship.

The analysis will be run in parallel for:

1. **binary academic success:** PASS versus non-PASS, where PASS means numeric grade >= 7.5 and non-PASS includes numeric grade < 7.5 plus BA, BV, and RT;
2. **continuous performance:** the Paper 2 imputed final-grade outcome standardised within instructor × academic-period group.

A numeric-only complete-case analysis may remain a robustness check, but it is not one of the two principal Paper 2.1 outcome families.

## Repository governance

This is a long-lived `paper/*` branch. Do not merge the whole branch into `main` or back into Paper 2. Reusable estimators or support diagnostics that belong across papers should be proposed for upstream integration into `cmat_analysis` and then brought back into this branch.

The user retains final scientific authority.
