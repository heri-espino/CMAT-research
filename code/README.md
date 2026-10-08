# Paper 2.2.1 — root code/ entry-point index

**Documentation-only stage: no Paper 2.2.1 runner implemented.**

Planned:
- `code/run_paper221_fused.py`: publication-specific orchestration: cohort load, eight-level outcome contract, root reproducibility CLI/`--check`, fused-lasso discovery, clustered CV, locked validation, table writes under `results/paper221/`.
- `code/figures_paper221.py`: figures generated **only** from approved aggregate results; no row-level exports.
- Optional `paper/paper_build_221.py` and `paper/notebook_221.ipynb` after tests and results, without overwriting inherited Paper 2.1 build/notebook.

Existing `run_paper21*.py`, `figures_paper21.py` and Paper 2 runners are **inherited sources**. They are not 2.2.1 experiments until consciously reused with provenance.

Architecture: reusable fused-lasso solver, FE absorption, cluster-aware CV and resampling, contrast/covariance and plotting helpers go to `main/cmat_analysis/src/cmat_analysis/`, with tests and `cmat_analysis/FUNCTION_INDEX.md` update, then sync to this paper branch. `code/` contains only thin orchestration. Read `PAPER_BRANCH.md` and `paper/docs/analysis/VALIDATION_AND_INFERENCE_221.md` before coding.

Controlled institutional microdata must never enter Git or generated files. Do not claim `--check` or analysis completed before running it.