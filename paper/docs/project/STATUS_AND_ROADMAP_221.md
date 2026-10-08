# Paper 2.2.1 — Status and roadmap

**2026-10-07 — IMPLEMENTED, NOT EXECUTED.** Forked from Paper 2.1 `0e39a875343c03ca3bb5c793f1f9e7c2bcba6173`. Shared initial estimator, synthetic tests, experiment/figure runners, manual Actions artifact workflow, independent LaTeX draft and dated `notes/` were committed. Controlled-data models, boundary stability and Wald validation have **not** been run/verified.

| Gate | Work to complete | Deliverable / acceptance |
|---|---|---|
| D0 | Check inherited branch and source files, update agent/index docs | Present handoff, reproducible frozen parent SHA (DONE) |
| D1 | Reconfirm cohort/outcomes, privacy and 8-level support, check 0|1 and sparse 6|7+ | Document support/rank, predeclared discovery/validation design |
| D2 | Objective/lambda scaling, solver, grouped conditional CV loss and one-SE heuristic | Implemented in reusable code; scientific review and synthetic CI verification pending |
| D3 | Shared ordered-fusion helpers on `main/cmat_analysis`, generated function index and synthetic tests | Shared methods and tests implemented; **main CI `37709359094` PASSED** and generated index `37709359125` PASSED; branch-level controlled-data workflow still unrun |
| D4 | Root runners, manuscript and reproducible export workflow | Committed. `--check`, tests, actual tables and PDF build must be verified in CI |
| D5 | Run controlled-data discovery: lambda paths and selected blocks Z and PASS | **NOT RUN**. 128-partition exhaustive comparison is a later sensitivity, not currently implemented |
| D6 | Cluster-bootstrap stability with reselection; 6+ and instructor sensitivity | Bootstrap and optional pooled 6+ implemented but **NOT RUN**; instructor-level sensitivity remains future |
| D7 | Locked holdout unpenalised OLS/LPM with CR Wald and Holm | Code written; **NOT RUN**. Contrast estimability and support still require controlled verification |
| D8 | English LaTeX draft, literature, limitations, review, final article decision | **Draft written**, results and final discussion intentionally unfinished |

## Stop / no-go conditions

Insufficient within-classroom support for selected cuts; held-out clusters without enough overlap; unstable boundary selection; numerical degeneracy; use of outcome-informed holdout tuning; p-values from penalised coefficients; unverified data mapping or privacy issues. Document failures rather than forcing a 2/3/4-block story.

## Unresolved design decisions

Validation split fraction and exact seed; how to handle outcome standardisation of held-out clusters; CV weighting by cluster; minimum block/cluster support; bootstrap count and compute budget; Holm families (cross-outcome adjustments vs separate outcomes); instructor-level sensitivity; journal route. These are intentionally **not presented as pre-registered choices** until decided before analysis.
## Export and interpretation

Manual Actions workflow: `.github/workflows/paper221-experiments.yml`; choose `smoke` first (no bootstrap), then `standard` (30 cluster resamples), and only after audit `full` (100 resamples plus pooled 6+ sensitivity). Successful runs upload CSV/PDF/PDF-manuscript artifact; do not commit generated PDFs to source control. Keep dated run notes in `notes/` with source SHA, run ID, observed findings and unsupported contrasts. No action run has been launched by this documentation update.
