# Paper 2.2.1 — Ordered attendance-regime discovery (fused lasso)

**Branch:** `paper/paper2.2.1-fused-frequency`  
**Frozen starting point:** Paper 2.1 `paper/paper2.1-visit-frequency` at `0e39a875343c03ca3bb5c793f1f9e7c2bcba6173`, 2026-10-07.  
**Status:** initial implementation and independent English manuscript draft completed; synthetic CI and controlled-data experiments pending. No Paper 2.2.1 regimes, empirical coefficients, or significance claims have been validated.

## Research question

How many *statistically distinguishable, stable, contiguous attendance regimes* are supported by observational student outcomes when adjusting for instructor-period grading context and degree? The exposure is ordinal: `0,1,2,3,4,5,6,7+`. Fused lasso is a **discovery method**, not an assumption that there are four regimes.

Candidate illustrations `[0]|[1+]`, `[0]|[1-6]|[7+]`, and `[0]|[1-4]|[5-6]|[7+]` are **hypotheses, not empirical findings**. A valid analysis may return a single regime or a different grouping. Do not equate a nonsignificant pairwise contrast with equality.

## Scientific origin

Paper 2 reports an observational zero-versus-positive CMAT attendance association. Paper 2.1 expands to the full frequency profile: OLS for instructor-period-standardised `Z_GRADE_PRIMARY`, an OLS linear-probability model (LPM) for `PASS`, instructor-period fixed effects, degree indicators, cluster-robust inference, omnibus tests and Holm-adjusted pairwise contrasts. Its outcome-blind support audit preferred a pooled `6+` group; its later full `0/1/2/3/4/5/6/7+` figures are exploratory. The question here is whether an explicitly penalised **ordered** model can discover a parsimonious, stable resolution without hand-picking visits from pairwise p-values.

The 3-visit PPA incentive threshold is contextual, not a data-derived or causal changepoint. Participation is self-selected; final outcomes are not pre/post improvement measures.

## Required reading, in order

1. This `PAPER_BRANCH.md`
2. `paper/AI_HANDOFF.md`
3. `paper/docs/project/PROJECT_CONTEXT_221.md`
4. `paper/docs/analysis/FUSED_LASSO_PROTOCOL.md`
5. `paper/docs/analysis/VALIDATION_AND_INFERENCE_221.md`
6. `paper/docs/project/STATUS_AND_ROADMAP_221.md`
7. `paper/docs/results/RESULTS_STATUS_221.md`
8. Parent Paper 2.1 historical contracts: `paper/docs/analysis/VISIT_GROUPING_DECISION.md`, `paper/docs/analysis/OUTCOME_FRAMEWORK.md`, `paper/docs/analysis/ANALYSIS_PLAN.md`, `paper/docs/results/PRELIMINARY_RESULTS.md`
9. `code/README.md`, `cmat_analysis/FUNCTION_INDEX.md`, `AGENTS.md`, `AI_HANDOFF.md`

## Ownership and boundaries

- Publication-specific orchestration **is implemented** in root `code/run_paper221_fused.py` and `code/figures_paper221.py`, pending the first complete branch workflow execution.
- Reusable estimators, proximal solvers, cluster-aware CV, covariance and testing utilities belong to **`main/cmat_analysis/src/cmat_analysis/`**, with tests, API/index/docs updated upstream first and propagated back. Never quietly duplicate the scientific library in a paper runner.
- New aggregate outputs (not yet generated) belong under `results/paper221/` and paper-specific text under `paper/`. Existing `results/paper21/`, `paper/sections/`, and Paper 2.1 runners are **inherited provenance**, not new Paper 2.2.1 results.
- No raw microdata, direct identifiers, keys or credentials in Git or CI artifacts. Treat controlled-data access separately; local `--check` may work without it.
- Keep Paper 2.1 intact. Do not merge entire paper branches into `main`.
- A publication decision is deferred until methods, validation and literature support a substantial standalone contribution.

**Next step:** inspect synthetic CI, then manually run the controlled-data workflow at `.github/workflows/paper221-experiments.yml`, inspect artifact outputs and write a dated `notes/` interpretation record. Code and paper draft are not results.