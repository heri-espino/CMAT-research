# Paper 2.2.2 — Status and roadmap

**2026-10-07 — DESIGN ONLY.** New branch forked from Paper 2.1 at `0e39a875343c03ca3bb5c793f1f9e7c2bcba6173`; no new Paper 2.2.2 analysis, runner or manuscript has been completed.

| Gate | Required work | Acceptance |
|---|---|---|
| D0 | Archive intent, separate branch-specific handoff/index from inherited 2.1 | Current documents (DONE) |
| D1 | Audit continuous-grade support: ties, bounds, rounding, administrative imputation, cluster dependence | Reproducible, disclosure-safe measurement summary |
| D2 | Reproduce Paper 2.1 K1/2/3, LRT bootstrap, skew-normal comparison and predictive CV under new output namespace | Verified baseline and input/seed manifest, no invented gains |
| D3 | Study feasibility/calibration of dip/critical-bandwidth or alternative direct modality tests on tied/clustered grades | Tested method decision; no naive p-values |
| D4 | Implement reusable density/mode finding, support-aware calibration and simulation utilities on `main/cmat_analysis`; index/tests | Validated upstream library synced here |
| D5 | Add thin root `code/run_paper222_modality.py` and `code/figures_paper222.py` | Check mode and reproducible aggregate outputs |
| D6 | Run controlled numeric-complete-case primary + imputed sensitivity, multiple bandwidths/starts, pooled tail, cluster robustness | Traceable tables, figures, support/failure diagnostics |
| D7 | Compare alternative one-mode models, held-out log score, mode stability and multiplicity-adjusted valid tests (if possible) | Transparent results incl. null or inconclusive findings |
| D8 | Synthesize scientific claims, literature and decision on separate paper vs Paper 2.1 supplement | Approved manuscript or clear non-paper conclusion |

## Stop/no-go

No inference from K=2 to 2 modes; no latent class claims; no uncalibrated mode-test p-values with ties/heaping or clusters; no administrative imputation presented as observed grades; no results copied from 2.1 with new labels; no raw microdata. If calibration is not feasible, limit conclusions to descriptive robustness and conditional model fit.

## Pending decisions (not preregistered)

Primary modality family and multiplicity; feasible null generators for grading/rounding and cluster dependence; degree/instructor contextual adjustment beyond prior within-context Z; sample-size threshold; bootstrap simulations/compute budget; publication positioning and literature route.