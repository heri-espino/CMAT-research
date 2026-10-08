# 2026-10-07 — Initial Paper 2.2.1 implementation

**Stage:** code and manuscript draft prepared; shared-library CI succeeded; **Paper 2.2.1 workflow and controlled-data experiments have not been run or reviewed**.

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
- **Shared-library test suite PASSED** on `main` GitHub Actions run `37709359094` (Python 3.14, full `cmat_analysis/tests/` and Sphinx build successful); generated function index workflow `37709359125` also PASSED. This does not test Paper 2.2.1 runner or execute its institutional analysis.
- Execute the **paper-branch manual workflow**; record and resolve any runner or controlled-data failures.
- Confirm canonical cohort and both outcome columns load exactly as expected.
- Audit structural rank and degree categories unseen by inner CV folds; the implementation fails explicitly rather than imputing unsupported degree effects.
- Check sparse support of 6 vs 7+, and how many validation classrooms contain every selected block.
- Verify runtime/compute cost before increasing bootstrap replicates.
- Review paper methodology against external fused-lasso and post-selection inference literature before submission.
- Confirm aggregate privacy thresholds and whether to retain/redact group counts.

## First result interpretation
**Not yet available.** Populate this section in a NEW dated note referencing the actual run and exported files.
## Additional implemented diagnostics

The runner now exports a discovery-sample enumeration of all 128 contiguous partitions (64 for pooled 6+) with SSE, conditional R² and relative BIC. This is a descriptive fit comparison, **not** a confirmatory p-value. Held-out Wald outputs also report each block's sample/cluster support and the number of classrooms containing students from both adjacent blocks. The Paper 2.2.1 Actions execution is still pending.
