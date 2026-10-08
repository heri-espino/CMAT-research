# Paper 2.2.1 — Status and roadmap

**2026-10-07 — DESIGN ONLY.** Branch created from Paper 2.1 commit `0e39a875343c03ca3bb5c793f1f9e7c2bcba6173`. No new code runner, experiment, split, tuning, chart, inference or paper draft has been completed.

| Gate | Work to complete | Deliverable / acceptance |
|---|---|---|
| D0 | Check inherited branch and source files, update agent/index docs | Present handoff, reproducible frozen parent SHA (DONE) |
| D1 | Reconfirm cohort/outcomes, privacy and 8-level support, check 0|1 and sparse 6|7+ | Document support/rank, predeclared discovery/validation design |
| D2 | Decide objective/lambda scaling, solver, grouped conditional CV loss, convergence and one-SE heuristic | Versioned specification and synthetic design tests |
| D3 | Implement shared ordered-fusion/selection/uncertainty helpers upstream on `main/cmat_analysis`, update API/function index/tests | Tested reusable API, then sync into branch |
| D4 | Add thin root `code/run_paper221_fused.py`, `code/figures_paper221.py`, optional 2.2.1 notebook/build entry | `--check`, seeds, separate outputs, no data leakage |
| D5 | Run controlled-data discovery: lambda paths, block counts for Z and PASS, exhaustive-partition comparison | `results/paper221/` aggregate manifest and tables |
| D6 | Cluster bootstrap stability with nested lambda reselection; 6+ tail and instructor sensitivity | Boundary frequencies and failure counts |
| D7 | Locked holdout unpenalised OLS/LPM with CR Wald and Holm; no holdout-based reselection | Honest estimates, CIs, adjusted p and support diagnostics |
| D8 | Manuscript, literature, limitations, peer review; decide standalone versus Paper 2.1 extension | Approved scientific claims and reproducible manuscript artifacts |

## Stop / no-go conditions

Insufficient within-classroom support for selected cuts; held-out clusters without enough overlap; unstable boundary selection; numerical degeneracy; use of outcome-informed holdout tuning; p-values from penalised coefficients; unverified data mapping or privacy issues. Document failures rather than forcing a 2/3/4-block story.

## Unresolved design decisions

Validation split fraction and exact seed; how to handle outcome standardisation of held-out clusters; CV weighting by cluster; minimum block/cluster support; bootstrap count and compute budget; Holm families (cross-outcome adjustments vs separate outcomes); instructor-level sensitivity; journal route. These are intentionally **not presented as pre-registered choices** until decided before analysis.