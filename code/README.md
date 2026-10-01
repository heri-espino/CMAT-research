# Paper 2.1 code

This directory contains thin publication orchestration for the visit-frequency paper. Reusable cohort definitions, outcome construction, estimators, uncertainty calculations, mixture models and shared plotting primitives belong in `cmat_analysis/` and are imported through its public API.

## Active Paper 2.1 entry points

- `run_paper21.py` — outcome-blind support audit used to freeze the positive-attendance grouping.
- `run_paper21_outcomes.py` — benchmark, frequency, outcome-composition and complete-case analyses.
- `run_paper21_mixture.py` — observed numeric-failure, Gaussian-mixture and skew-normal analyses.
- `run_paper21_shape_check.py` — isolated shape-diagnostic runner retained for targeted validation.
- `figures_paper21.py` — publication-vector figure generation from aggregate Paper 2.1 tables.

The preferred user-facing build interface is `paper/paper_build.py`, which orchestrates tables, figures and manuscript compilation with dependency checking.

## Inherited Paper 2 files

`run_paper.py` and `figures.py` are inherited from the parent Paper 2 branch and are not canonical Paper 2.1 entry points. Paper 2.1 outputs are written only under `results/paper21/`.

## Setup

```bash
python -m pip install -e './cmat_analysis[dev]'
python code/run_paper21.py --check
python code/run_paper21_outcomes.py --check
python code/run_paper21_mixture.py --check
python paper/paper_build.py --check
```

Raw or row-level administrative outputs must not be written to this directory.
