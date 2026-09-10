# cmat_analysis AI handoff

This directory is the shared scientific library. Before writing reusable code, search `FUNCTION_INDEX.md` and inspect the nearest implementation. New cohort logic, outcomes, estimators, tests, models, confidence intervals, imputation rules and reusable plotting functions belong under `src/cmat_analysis/`, with tests and concise docstrings.

The package must remain installable with `python -m pip install -e ./cmat_analysis`; consumers should use normal `cmat_analysis...` imports rather than injecting repository paths into `sys.path`. Paper-specific execution order/specifications belong in the current paper branch's root `code/`; broad exploratory orchestration belongs in `brainstorm/<topic>/code/`.
