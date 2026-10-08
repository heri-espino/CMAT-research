# Paper 2.2.1 — AI agent research handoff

You are working on `paper/paper2.2.1-fused-frequency`, not Paper 2.1. This branch forks the Paper 2.1 working tree at `0e39a875343c03ca3bb5c793f1f9e7c2bcba6173`. Its inherited code, figures, manuscripts and aggregate tables describe **Paper 2.1** until explicitly rerun and validated here.

**Current state:** branches and design documents only; no fused-lasso implementation, tuning, cluster-bootstrap stability, independent validation or 2.2.1 results. Do not infer groups from a hypothetical figure, use 2.1 numerical findings as new evidence, or claim a final manuscript exists.

## Mission

Discover outcome-supported adjacent-visit plateaus/regimes via a one-dimensional fused lasso applied to full individual-level OLS/LPM designs with unpenalised instructor-period and degree effects. Assess stability and prediction, and only then perform independent-sample post-selection Wald inference.

## Start here

- `PAPER_BRANCH.md` -> `paper/docs/README.md` -> `paper/docs/project/PROJECT_CONTEXT_221.md`.
- Read `paper/docs/analysis/FUSED_LASSO_PROTOCOL.md` and `VALIDATION_AND_INFERENCE_221.md` before implementing.
- Read the **inherited** `paper/docs/analysis/VISIT_GROUPING_DECISION.md` to preserve the pre-outcome pooled `6+` support decision, and `paper/docs/analysis/OUTCOME_FRAMEWORK.md` for BA/BV/RT treatment.
- Read root `AGENTS.md`, `AI_HANDOFF.md`, `docs/REPO_GOVERNANCE.md`, `cmat_analysis/ARCHITECTURE.md`, `cmat_analysis/FUNCTION_INDEX.md`.
- Check `code/README.md` for names of **proposed** entry points.

## Non-negotiable methodology

1. Preserve first eligible MU attempt, period-wide visit exposure, pass threshold 7.5 and controlled-data definitions inherited from 2.1.
2. Use ordered levels `0,1,2,3,4,5,6,7+`; `7+` is already top-coded. Examine pooled `6+` as a support sensitivity.
3. Penalise *only adjacent visit-level differences*; neither classroom nor degree coefficients should be subjected to this fusion penalty.
4. Distinguish cluster-held-out **within-context association score** from genuinely out-of-cluster prediction: unseen instructor-period FE cannot be predicted from training data. Define the actual CV loss and its target explicitly.
5. Repeat lambda selection inside cluster-bootstrap replicates when estimating boundary stability. Stability frequencies are **not p-values**.
6. Do not use standard errors/p-values calculated naively on penalised coefficients; refit selected blocks without penalty.
7. In-sample OLS refit plus ordinary Wald still has **post-selection bias**. Use cluster-level discovery/validation splitting, or justified selective inference, for inferential claims about selected boundaries. Report support, effective validation clusters, rank/identifiability.
8. For validation contrasts calculate CR variance at `CLASSROOM_ID`; report effect size, SE, CI, raw p, Holm-adjusted p in predeclared families; optional instructor-level clustering sensitivity.
9. PASS is an LPM (risk/probability differences in pp); continuous grade uses within-instructor-period standardised Z (SD). Both are observational, with no causal effect claim.
10. Distinguish outcomes: different optimally selected partitions are possible; no requirement that Z and PASS give the same answer.
11. Do not change original pre-outcome Paper 2.1 grouping retrospectively.
12. Never commit row-level institutional data. Publish only disclosure-safe aggregate tables/figures and provenance.

## Implementation contracts

Proposed **branch runner** `code/run_paper221_fused.py`: `--check`, explicit controlled input handling, outcome/specification switches, deterministic seeds, fail clearly on missing controlled data, emit run manifest. Proposed `code/figures_paper221.py`: regime path, boundary stability, prediction vs complexity, holdout estimates/CI. Do not overwrite Paper 2.1 results.

Reusable solver, nuisance FE residualisation, boundary decoding, grouped CV scoring, bootstrap and inference belong upstream to `main/cmat_analysis`, with unit tests including all-equal/single-boundary/extreme lambda, zero-visit reference, sparse-tail, rank deficiency, and synthetic clusters. Update `cmat_analysis/FUNCTION_INDEX.md` after implementation.

## Next actions / exit conditions

Follow `paper/docs/project/STATUS_AND_ROADMAP_221.md` in order: audit inputs -> lock design/holdout -> reusable implementation -> tests -> controlled-data runs -> robustness/interpretation -> manuscript decision. Keep `paper/docs/results/RESULTS_STATUS_221.md` honest and dated, including failed runs and limitations.

The user retains scientific authority. Do not assume other AI chats see unpublished decisions; commit substantive decisions to these documents.