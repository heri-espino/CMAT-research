# Paper 2.2.2 — AI agent handoff

You are working on `paper/paper2.2.2-distributional-heterogeneity`, forked from `paper/paper2.1-visit-frequency` at commit `0e39a875343c03ca3bb5c793f1f9e7c2bcba6173`. **No 2.2.2 methods have run yet.** All historical GMM tables, figures, runner outputs, paper sections and notebooks are inherited Paper 2.1 material, not independently replicated 2.2.2 findings.

## The non-equivalences to preserve

1. Better fit of K=2 Gaussian mixture than K=1 Gaussian **does not** establish bimodality.
2. Two mixture components **do not** establish two real student classes, psychological types or behavioural regimes.
3. Multimodal marginal grade density **does not** identify a causal CMAT mechanism.
4. An imputed outcome can create a lower cluster by coding design; investigate this mechanism before claiming a natural mixture.
5. Numeric grade values are bounded, often discrete/heaped; a continuous Gaussian fit is a misspecified working approximation unless shown otherwise.

## Inputs and outcomes

First eligible MU attempt, recorded period-wide CMAT visits, instructor-period standardisation, degree context, PASS threshold 7.5, BA/BV/RT handling inherited from 2.1. For mixture research **numeric complete-case Z is primary**; imputed primary Z is sensitivity, NOT interchangeable. The sample changes when restricting to numeric grades; explicitly report sample selection and adverse-state composition. Keep historical `0/1/2/3/4/5/6/7+` plus pooled 6+ support sensitivity.

## Existing tests vs new research

Existing in inherited `code/run_paper21_mixture.py` and `cmat_analysis.statistics.mixtures`: GMM K=1/2/3 selection via AIC/BIC/ICL, parametric-bootstrap LRT K1 vs K2, skew-normal vs GMM K2 BIC bootstrap, held-out cross-validated log predictive density, posterior entropy/responsibilities, Ashman D, soft administrative-state composition. These procedures are **not direct proof of multimodality**. Historical default `--gmm-bootstrap=999`, `--shape-bootstrap=199`, `--shape-cv-folds=5`, `--shape-cv-repeats=10` are implementation defaults, not established 2.2.2 experiments.

New 2.2.2 research: explicitly define one vs >=2 density modes, inspect KDE bandwidth/critical bandwidth, investigate dip/critical-bandwidth unimodality tests with **tie-, boundary-, grade-heaping- and cluster-aware null calibration**; compare bounded/discrete one-mode families, skew-normal and flexible single-mode alternatives against mixtures using properly separated training/holdout and shape checking. The exact mode-testing algorithm is **pending feasibility review**. Do not run textbook dip/Silverman p-values on heavily tied/imputed grades and call them valid without calibration.

## Inference and risk constraints

- Predeclare primary numeric-complete-case groups and hypothesis family. Repeated testing across visit groups/outcomes needs multiplicity control; distinguish secondary exploratory checks.
- Standard parametric bootstrap from i.i.d. Gaussian/skew-normal models conditions on those simplifying assumptions; it does not automatically handle intra-classroom dependence. Add cluster resampling for stability and evaluate dependence-adjusted null procedures before p-value claims.
- More bootstrap replications improve Monte Carlo precision but cannot repair a wrong null model.
- Examine upper/lower bounds, ties, rounding, administrative mass points, outliers and sparse tail before modality assertions.
- Student-component assignment is soft; avoid hard labels and claims of two mechanisms. Multiple starts/degeneracy controls must be documented.
- Distinguish bootstrap support for a density feature from population probability that it is true; no causal claims.
- Never invent significance, missing runs or outputs.

## Agent execution pathway

`PAPER_BRANCH.md` -> `paper/docs/README.md` -> context -> analytic protocol -> modality calibration/limitations -> roadmap. Search `cmat_analysis/FUNCTION_INDEX.md`, reusable `statistics/mixtures.py` and existing 2.1 runner before writing functions. Reusable statistics to `main/cmat_analysis` with tests + function index; new runner `code/run_paper222_modality.py` and figures `code/figures_paper222.py` in branch root `code/` (planned, not created); output `results/paper222/`, not `results/paper21/`. Record git SHA, random seeds, input contracts, sample sizes, cluster distribution, heaping, folds, calibration and finite-rep uncertainty.

Update `paper/docs/results/RESULTS_STATUS_222.md` only after verifiable controlled-data execution. The user has final scientific authority.