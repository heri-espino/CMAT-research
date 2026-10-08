# Paper 2.2.2 — Distribution shape, modality and mixture adequacy

**Branch:** `paper/paper2.2.2-distributional-heterogeneity`  
**Frozen starting point:** Paper 2.1 `paper/paper2.1-visit-frequency` at `0e39a875343c03ca3bb5c793f1f9e7c2bcba6173`, 2026-10-07.  
**Status:** research-design documentation only; no Paper 2.2.2 experiments, new modality tests or validated claims.

## Scientific question

Do observed final mathematics grades exhibit **more than one mode**, or can their shape be accounted for by one asymmetric, bounded, discrete/heaped distribution? Does a two-Gaussian mixture reflect true **density complexity** rather than simply skewness, imputation artifacts, or sparse tails? Is there robust evidence of distinct **latent subpopulations**? These are three *different questions*; positive evidence for a K=2 GMM does **not** establish bimodality or identifiable student types.

## Scientific origin

Paper 2.1 currently includes one/two/three-component Gaussian mixtures fitted separately by recorded visit groups, using **numeric complete-case instructor-period-standardised Z as the primary mixture outcome** and canonical adverse-outcome-imputed primary Z as a sensitivity. It compares AIC/BIC/ICL, posterior responsibilities/entropy, Ashman's D, parametric-bootstrap K=1 vs K=2 LRT, skew-normal vs GMM2 bootstrap of BIC advantage and repeated held-out log predictive density. Controlled-data historical findings are documented in inherited `paper/docs/results/MIXTURE_ANALYSIS_RESULTS.md`; those are **Paper 2.1 exploratory findings** and do not establish two populations.

The 2.2.2 extension challenges the inferential meaning of this model-selection pattern. Explicitly audit modality, heaping/discreteness, grade boundaries, sparse groups, clustering, and whether administrative imputation produces lower-tail structure that does not exist in numeric observed grades.

## Reading order

1. `PAPER_BRANCH.md` (this file)
2. `paper/AI_HANDOFF.md`
3. `paper/docs/project/PROJECT_CONTEXT_222.md`
4. `paper/docs/analysis/DISTRIBUTIONAL_PROTOCOL.md`
5. `paper/docs/analysis/MODALITY_VALIDATION_AND_LIMITATIONS_222.md`
6. `paper/docs/project/STATUS_AND_ROADMAP_222.md`, `paper/docs/results/RESULTS_STATUS_222.md`
7. Historical Paper 2.1: `paper/docs/analysis/MIXTURE_ANALYSIS_PLAN.md`, `paper/docs/results/MIXTURE_ANALYSIS_RESULTS.md`, `paper/docs/analysis/OUTCOME_FRAMEWORK.md`, `paper/docs/analysis/VISIT_GROUPING_DECISION.md`
8. `code/README.md`, `cmat_analysis/FUNCTION_INDEX.md`, `AGENTS.md`, `AI_HANDOFF.md`

## Repository boundaries

Branch-local scripts planned in root `code/` (e.g. `code/run_paper222_modality.py`, `code/figures_paper222.py`); **none created yet**. Reusable modality/calibration/density/cluster-bootstrap algorithms must be added and tested in `main/cmat_analysis/src/cmat_analysis/` and propagated down; `code/` only orchestrates. Publication-safe aggregates and figures will go to `results/paper222/`, separate from inherited `results/paper21/`. Existing Paper 2.1 `paper/sections/`, notebook and build files are inherited baseline documents, **not** a Paper 2.2.2 manuscript.

No raw data, student IDs, credentials or sensitive cell contents in Git. No causal interpretation of visits, behavioural labels, or natural latent classes without independent evidence. Keep Paper 2.1 immutable as historical parent; never merge whole paper branches back to `main`.

## Publication gate

Only call this a separate paper if the analysis delivers a credible, genuinely new contribution over the established Paper 2.1 density sensitivity and the modality claim survives relevant alternatives, uncertainty and reproducibility checks. Otherwise report it as an exploratory extension with negative or inconclusive findings.