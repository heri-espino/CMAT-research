# Paper 2.2.1 — Results status (2026-10-07)

**The first local controlled-data run generated preliminary outputs, but is NOT a complete validated Paper 2.2.1 analysis.** The selected blocks and holdout contrasts are available as provisional estimates; every attempted bootstrap replicate failed, so boundary stability remains entirely unassessed. The implementation was corrected after the run and requires a fresh execution before final scientific interpretation.

Publication-safe aggregate outputs from the initial run are stored at `results/paper221/tables/` and `results/paper221/figures/`, with a run manifest recording source commit, tool/library version, controlled-data fingerprint (non-identifying), outcome version, seeds, cluster folds, tune grid, partition, and known failures. Do not transfer `results/paper21/` values and label them 2.2.1.

Do not publish row-level records or identifiers.

## Verification provenance

The reusable `cmat_analysis` library and synthetic test suite passed main-branch CI run [37709359094](https://github.com/heri-espino/CMAT-research/actions/runs/37709359094), and its generated function index passed [37709359125](https://github.com/heri-espino/CMAT-research/actions/runs/37709359125). These are **software checks**, not controlled-data experiments. A first local run has been uploaded to `results/paper221/`, but **all 100 cluster-bootstrap resamples failed in each of four outcome/grouping specifications** due to DataFrame-valued pandas metadata. Its preliminary Z partition `[0]|[1+]` and held-out contrast (+0.264 SD, 95% CI 0.150–0.377) cannot yet be accompanied by bootstrap stability claims; PASS all-fused is a CV-selection result, not equivalence. See `notes/2026-10-07_bootstrap_metadata_fix.md`. A corrected rerun is pending.
