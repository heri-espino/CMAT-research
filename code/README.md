# Paper 2.2.2 — root code/ entry-point index

**Documentation-only stage: no Paper 2.2.2 runner or figures exist yet.**

Proposed:
- `code/run_paper222_modality.py`: thin publication orchestration: checked cohort load, explicit numeric-complete-case primary and imputed sensitivity, grade measurement audits, inherited GMM re-runs, new modality assessment with calibration gates, reproducibility CLI/`--check`, disclosure-safe aggregate tables under `results/paper222/`.
- `code/figures_paper222.py`: plots of grade heaping, fitted densities and total modes, smoothing/bandwidth stability and uncertainty; only from approved aggregate or local controlled data, never commit observation data.
- Optional `paper/paper_build_222.py`/dedicated notebook once validated outputs exist.

Inherited `code/run_paper21_mixture.py`, `run_paper21_shape_check.py`, other 2.1 runners/figures and the 2.1 notebook are historical baselines, not new 2.2.2 scripts. Reuse rather than fork shared methods.

Reusable methods (GMM extensions, mode counting, calibrated unimodality testing, bounded/heaped null simulation, cluster-bootstrap uncertainty) belong upstream in `main/cmat_analysis/src/cmat_analysis/`; update tests, public API and `cmat_analysis/FUNCTION_INDEX.md` there, then sync here. Root `code/` is runner/orchestration only. See `PAPER_BRANCH.md`, `paper/docs/analysis/MODALITY_VALIDATION_AND_LIMITATIONS_222.md`.