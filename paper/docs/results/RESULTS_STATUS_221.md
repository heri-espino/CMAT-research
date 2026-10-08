# Paper 2.2.1 — Empirical results status (2026-10-07 local / 2026-10-08 UTC)

**Computational run completed for the prespecified main pipeline:** 100/100 successful bootstrap replications with 0 failures in each of the four combinations of outcome and upper-tail representation. Run provenance and exact parameters: `results/paper221/run_manifest.json`, source SHA `c9faa397bd0a6c7c8c67025ab94f8314e0996018`, 6,627 students in 190 classroom clusters.

**Standardised-grade Z:** selected blocks `[0]|[1+]`, with 0|1 retained in 100/100 bootstrap replicates; other positive-frequency boundaries in at most 10/100. Reserved-cluster Wald for 1+ minus 0: +0.263616877 SD (CR SE 0.057975195; nominal 95% CI 0.149985494 to 0.377248260; p=0.00000543997). Validation N=1,952, 57 instructor-periods, of which 52 contain both groups.

**PASS:** the conservative one-SE-style tuning rule selected one all-fused block, yet 0|1 appeared in 37/100 bootstrap replicates and the all-fused model ranked 128th of 128 discovery-only relative BIC alternatives. This is tuning-sensitivity evidence, not proof of no association or equality. There is no PASS selected-boundary Wald p-value because no boundary was selected.

**Sensitivity:** pooling high-frequency visits at 6+ did not change the selected partitions, and 0|1 bootstrap rates remained 100% (Z) and 37% (PASS).

**Still open:** numeric complete-case Z, alternative minimum-CV-loss tuning and repeated cluster folds, instructor-level dependence, and genuinely new-cohort replication. The reserved clusters were not used in this new algorithm's tuning, but the full institutional cohort had been explored in earlier Paper 2.1 research; avoid claiming independent external/prospective confirmation.

A prior local run failed all bootstrap replicates due to pandas DataFrame-valued metadata during concat; the bug was fixed, regression-tested (main CI [37718672591](https://github.com/heri-espino/CMAT-research/actions/runs/37718672591)) and superseded by the successful 100-replicate run. Keep its record at `notes/2026-10-07_bootstrap_metadata_fix.md`.

**Research interpretation:** `notes/2026-10-07_fused_lasso_100_bootstrap_results.md`. **Draft manuscript:** `paper/paper221/main.tex` and `paper/paper221/results_221.tex`. **Exported source data:** `results/paper221/tables/`, `results/paper221/figures/`. No row-level microdata may be published; review small-cell disclosure before public distribution.
