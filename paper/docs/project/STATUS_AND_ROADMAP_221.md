# Paper 2.2.1 — Status and roadmap

**2026-10-07 — IMPLEMENTED AND FIRST FULL RUN COMPLETED (100 BOOTSTRAP REPLICATES).** Forked from Paper 2.1 `0e39a875343c03ca3bb5c793f1f9e7c2bcba6173`. Shared initial estimator, synthetic tests, experiment/figure runners, manual Actions artifact workflow, independent LaTeX draft and dated `notes/` were committed. Controlled-data main-run Z/PASS fusion, 100 cluster-bootstrap replicates, pooled-6+ sensitivity and reserved-cluster Wald for the selected Z boundary have been run and recorded; additional sensitivity checks remain pending.

| Gate | Work to complete | Deliverable / acceptance |
|---|---|---|
| D0 | Check inherited branch and source files, update agent/index docs | Present handoff, reproducible frozen parent SHA (DONE) |
| D1 | Reconfirm cohort/outcomes, privacy and 8-level support, check 0|1 and sparse 6|7+ | Document support/rank, predeclared discovery/validation design |
| D2 | Objective/lambda scaling, solver, grouped conditional CV loss and one-SE heuristic | Implemented in reusable code; scientific review and synthetic CI verification pending |
| D3 | Shared ordered-fusion helpers on `main/cmat_analysis`, generated function index and synthetic tests | Shared methods and tests implemented; **main CI `37709359094` PASSED** and generated index `37709359125` PASSED; branch-level controlled-data workflow still unrun |
| D4 | Root runners, manuscript and reproducible export workflow | Committed. `--check`, tests, actual tables and PDF build must be verified in CI |
| D5 | Run controlled-data discovery: lambda paths and selected blocks Z and PASS | **DONE (first full run)**. All 128 contiguous partitions are now enumerated by the runner as a discovery-sample fit sensitivity, without inferential p-values |
| D6 | Cluster-bootstrap stability with reselection; 6+ and instructor sensitivity | **DONE:** 100/100 bootstrap fits per outcome/spec, 0 failures and pooled-6+ rerun; instructor-level sensitivity still pending |
| D7 | Locked holdout unpenalised OLS/LPM with CR Wald and Holm | **DONE for selected Z boundary** (+0.264 SD, CI 0.150--0.377); PASS selected no boundary, so no PASS Wald; additional prospective validation pending |
| D8 | English LaTeX draft, literature, limitations, review, final article decision | **First numerical results incorporated**, but follow-up sensitivities, literature/declarations and submission review pending |

## Stop / no-go conditions

Insufficient within-classroom support for selected cuts; held-out clusters without enough overlap; unstable boundary selection; numerical degeneracy; use of outcome-informed holdout tuning; p-values from penalised coefficients; unverified data mapping or privacy issues. Document failures rather than forcing a 2/3/4-block story.

## Unresolved design decisions

Validation split fraction and exact seed; how to handle outcome standardisation of held-out clusters; CV weighting by cluster; minimum block/cluster support; bootstrap count and compute budget; Holm families (cross-outcome adjustments vs separate outcomes); instructor-level sensitivity; journal route. These are intentionally **not presented as pre-registered choices** until decided before analysis.
## Export and interpretation

Manual Actions workflow: `.github/workflows/paper221-experiments.yml`; choose `smoke` first (no bootstrap), then `standard` (30 cluster resamples), and only after audit `full` (100 resamples plus pooled 6+ sensitivity). Successful runs upload CSV/PDF/PDF-manuscript artifact; do not commit generated PDFs to source control. Keep dated run notes in `notes/` with source SHA, run ID, observed findings and unsupported contrasts. A complete local run was subsequently pushed to GitHub; its exact provenance is in `results/paper221/run_manifest.json` and `notes/2026-10-07_fused_lasso_100_bootstrap_results.md`.
