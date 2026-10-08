# 2026-10-07 — First Paper 2.2.1 run: bootstrap metadata failure

**Observed:** the first institutional run successfully estimated a discovery-sample fused-lasso model and performed the reserved-classroom Wald comparison for Z, but **all 100 bootstrap replicates failed in each of four specifications**. These runs do not establish boundary stability.

**Reproduced traceback:** `pandas.concat` compares `DataFrame.attrs` across bootstrap clusters, and an institutional cohort carries a nested DataFrame-valued metadata entry. Pandas cannot evaluate `obj.attrs == attrs` when its elements are DataFrames, producing `ValueError: The truth value of a DataFrame is ambiguous`.

**Fix:** the reusable `cmat_analysis.statistics.ordered_fusion.resample_cluster_rows` function now clears `part.attrs` on the **copied** cluster slices before concatenation, while preserving row values, column dtypes and the original cohort's metadata. A new synthetic test attaches DataFrame-valued `attrs` and verifies both cluster bootstrap and the complete retuning pipeline. The paper runner now marks all-failed bootstrap runs as incomplete and raises an error instead of silently returning success.

**Preliminary selections before stability verification:** for the eight-category Z outcome, `[0]|[1+]`; for PASS, a single all-fused block under the 1-SE-style penalty-selection heuristic. The validation-only Z contrast (1+ vs 0) was 0.264 SD (95% CI 0.150–0.377). These are **not final** regime-stability findings; PASS's all-fused choice is not a test of equality and contrasts with the more differentiated exploratory BIC rankings.

**Required next run:** pull the updated paper branch; reinstall the editable `cmat_analysis` package if necessary; run `python -m pytest cmat_analysis/tests/test_ordered_fusion.py -q`; rerun first on `--bootstrap 2` with `--include-pooled`, then 100 after confirming successful replicates. Review `results/paper221/run_manifest.json`, all `*_boundary_stability.csv` and `*_holdout_wald.csv`. Update results interpretation and manuscript only after valid reruns.

**Scientific restriction:** the code correction fixes an implementation failure, not observational confounding or evidence of a causal attendance threshold.

**Software verification:** GitHub Actions run [37718672591](https://github.com/heri-espino/CMAT-research/actions/runs/37718672591) on `main` completed successfully with the new metadata-specific test, the full `cmat_analysis` test suite and documentation build. This is not a validation of the empirical boundary-stability results; those require a fresh local run.
