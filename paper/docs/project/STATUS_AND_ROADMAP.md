# Paper 2.1 — status and roadmap (2026-10-09)

**Current scope:** a manuscript of attendance-frequency comparisons in Z and PASS, with Wald tests and Holm-adjusted multiplicity. Four LaTeX manuscript sections have been refocused to match this scope, and the figure/build pipeline regenerates only three contrast dashboards.

## Completed analytical work, previously verified

- First eligible MU cohort, N=6,627 in 190 instructor-period groups; 1,234 CMAT users.
- Support-based, outcome-blind decision to pool 6+ positive frequencies.
- Benchmark any versus no visits, Z +0.361 SD and PASS +15.3 percentage points.
- User-only omnibus and Holm-adjusted 15 contrasts per outcome, plus 21-contrast high-tail sensitivity.
- Full zero-inclusive 28-contrast exploratory displays in Z and PASS.
- Instructor-level clustering sensitivity, preserving fixed effects.
- Numeric complete-case Z sensitivity, observed-data analysis limits.

See `paper/docs/results/PRELIMINARY_RESULTS.md` and `notes/05_RESULTADOS_Y_PROCEDENCIA.md`. These are retained earlier results, not newly executed on 2026-10-09.

## Work to complete before publication

1. Check manuscript numbers against all canonical aggregate CSV files and outcome/group definitions.
2. Check p-values, confidence intervals, multiplicity families and descriptive vs adjusted values in all three figures.
3. Verify historical PPA, CMAT operating context and institutional grade/withdrawal codes.
4. Include exact institutional ethics/data-use wording and investigate comparable entrance-examination measures if available.
5. Review bibliography, limited-access sources and current TEAMAT instructions.
6. Compile clean/commented PDFs, inspect rendering and run referee-style scientific review.

The main inferential strategy remains Holm. Do not replace it based on outcome significance; do not infer equivalence or causality.