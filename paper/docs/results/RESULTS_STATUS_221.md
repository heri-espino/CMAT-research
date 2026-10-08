# Paper 2.2.1 — Results status (2026-10-07)

**Initial analysis source and independent LaTeX draft are committed, but no Paper 2.2.1 controlled-data results have been generated or verified.** No actual selected regime count, lambda, stability frequency, holdout estimate, Wald p-value, or data-derived figure exists. The manual artifact workflow is configured but has not yet been dispatched. The illustrative partitions in the plan are not estimates.

Publication-safe outputs from the first successful manual run will be stored at `results/paper221/tables/` and `results/paper221/figures/`, with a run manifest recording source commit, tool/library version, controlled-data fingerprint (non-identifying), outcome version, seeds, cluster folds, tune grid, partition, and known failures. Do not transfer `results/paper21/` values and label them 2.2.1.

Update this document with dated results only after a verifiable controlled-data run. Do not publish row-level records or identifiers.
## Verification provenance

The reusable `cmat_analysis` library and synthetic test suite passed main-branch CI run [37709359094](https://github.com/heri-espino/CMAT-research/actions/runs/37709359094), and its generated function index passed [37709359125](https://github.com/heri-espino/CMAT-research/actions/runs/37709359125). These are **software checks**, not controlled-data experiments. The 2.2.1 manual workflow is not yet dispatched; there are no new aggregate empirical tables to interpret.
