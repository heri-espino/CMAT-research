# Paper 2.2.1 — root code/ entry-point index

**Implemented source stage: controlled-data run and result validation pending.**

Implemented:
- `code/run_paper221_fused.py`: publication-specific orchestration: cohort load, eight-level outcome contract, root reproducibility CLI/`--check`, fused-lasso discovery, clustered CV, locked validation, table writes under `results/paper221/`.
- `code/figures_paper221.py`: figures generated **only** from approved aggregate results; no row-level exports.
- - `paper/paper221/main.tex` is a separate English manuscript draft with explicitly pending results.
- `notes/` is the dated analysis and interpretation log.
- `.github/workflows/paper221-experiments.yml` provides manual `smoke`, `standard`, `full` execution and artifact export.

Optional dedicated notebook/build wrapper may follow validation, without overwriting inherited Paper 2.1 build/notebook.

Existing `run_paper21*.py`, `figures_paper21.py` and Paper 2 runners are **inherited sources**. They are not 2.2.1 experiments until consciously reused with provenance.

Architecture: reusable fused-lasso solver, FE absorption, cluster-aware CV and resampling, contrast/covariance and plotting helpers go to `main/cmat_analysis/src/cmat_analysis/`, with tests and `cmat_analysis/FUNCTION_INDEX.md` update, then sync to this paper branch. `code/` contains only thin orchestration. Read `PAPER_BRANCH.md` and `paper/docs/analysis/VALIDATION_AND_INFERENCE_221.md` before coding.

Controlled institutional microdata must never enter Git or generated files. The synthetic tests are in `cmat_analysis/tests/test_ordered_fusion.py`; their CI result must be checked separately. No controlled-data outcomes are currently published.