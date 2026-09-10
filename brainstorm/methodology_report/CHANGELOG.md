# Report changelog

## Atomic report architecture — 2026-09-10

- Moved the stable methodology-report entry point from `code/experiments/methodology_report.py` to `brainstorm/methodology_report/code/methodology_report.py`.
- Kept reusable scientific and build functions in root `cmat_analysis/src/cmat_analysis/`; the report-local script is intentionally only a thin importer/launcher.
- Added `cmat_analysis/src/cmat_analysis/reporting/methodology_build.py` as the root-code home for report-build orchestration previously embedded in the central runner.
- Moved disposable methodology working outputs from `code/outputs/methodology_report/` to the report-local ignored `build/` directory.
- Retained reviewed CSV/LaTeX table assets and figures inside the report folder.
- Updated repository documentation to define `code/ → brainstorm/ → papers/` as the primary production hierarchy.

## v2 methodology — 2026-09-07

Historical methodology-state label retained for provenance.

- Rewritten as one continuous technical report; publication split moved to the end.
- Expanded mathematical/statistical explanations for the methods and assumptions.
- Corrected official-career linkage description.
- Corrected KDE-based adverse-outcome imputation method and documented SciPy defaults/fallbacks.
- Added continuation-probability examples for k=0,1,2,3.
- Added exact temporal peak algorithm and ACF/periodogram methodology for two populations.
- Added all 0/1/2/3/4+ pairwise performance comparisons and multiplicity-adjusted FE contrasts.
- Added exact 0-12 dose diagnostics.
- Added omitted-career appendix.
- Added three-population career mean-Z plots and use-vs-Z scatterplots.
- Added N=4,211 future-progressor MU sensitivity with explicit selection/estimand discussion.
- Expanded privacy, anonymization and journal data-sharing discussion.
- Added proposed publication split only after all findings and methodological synthesis.
