# 2026-10-07 — Initial Paper 2.2.1 implementation

**Stage:** code and manuscript draft prepared; **controlled-data experiments have not yet been run or reviewed**.

## From previous research
Paper 2 compared any CMAT attendance against none. Paper 2.1 exposed 0/1/2/3/4/5/6/7+ visits with instructor-period FE, degree controls, OLS Z and LPM PASS, cluster covariance and Holm contrasts. The historically outcome-blind grouping pooled 6+. Non-monotonic and weakly distinguished positive-frequency results motivate searching for robust contiguous regimes; suggested [0]|[1-4]|[5-6]|[7+] is only an illustrative hypothesis.

## Implementation checkpoint
- Shared estimator: `main/cmat_analysis/src/cmat_analysis/statistics/ordered_fusion.py`.
- Synthetic tests: `main/cmat_analysis/tests/test_ordered_fusion.py`.
- Publication runner: `code/run_paper221_fused.py`.
- Figures: `code/figures_paper221.py`.
- Independent English manuscript draft: `paper/paper221/main.tex`.
- Publication output namespace: `results/paper221/`.
- Manual Actions job: `.github/workflows/paper221-experiments.yml`.
- Research log: `notes/` and `paper/docs/results/RESULTS_STATUS_221.md`.

## Hypotheses for testing, NOT RESULTS
Might observe a substantial 0|1 separation; an additional high-frequency split may or may not be reproducible, and it can differ across Z and PASS. Fused lasso is free to return one, two, three, four or more blocks and must not be forced into the illustrative four-block structure.

## Key implementation design decisions
1. Reserve entire classrooms before selection; discovery sample used for lambda tuning and cluster bootstrap.
2. Penalise adjacent group contrasts only; FE and degree are unpenalised.
3. Cross-validated target: within-held-out-classroom residual MSE; no transfer of unseen classroom intercepts.
4. Bootstrap repeats the selection process; boundary selection frequency is not p-value.
5. Independently test adjacent discovered blocks in reserved classrooms using unpenalised OLS/LPM, cluster-robust covariance and Holm.
6. Two separate outcomes and an optional pooled-6+ sensitivity; code exports only aggregate outputs.

## Technical and scientific checks STILL PENDING
- Execute pytest and the branch workflow; test failures must be recorded.
- Confirm canonical cohort and both outcome columns load exactly as expected.
- Audit structural rank and degree categories unseen by inner CV folds; the implementation fails explicitly rather than imputing unsupported degree effects.
- Check sparse support of 6 vs 7+, and how many validation classrooms contain every selected block.
- Verify runtime/compute cost before increasing bootstrap replicates.
- Review paper methodology against external fused-lasso and post-selection inference literature before submission.
- Confirm aggregate privacy thresholds and whether to retain/redact group counts.

## First result interpretation
**Not yet available.** Populate this section in a NEW dated note referencing the actual run and exported files.