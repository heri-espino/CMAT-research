# Paper 2.2.1 — Clustered validation, stability and honest inference

**Do not equate post-lasso OLS with automatically valid post-selection inference.** This protocol separates discovery from confirmatory evidence.

## Why post-hoc Wald needs protection

If the same outcomes determine lambda and the chosen boundaries, and are then used to run standard OLS/LPM CR Wald tests on those chosen contrasts, the p-values ignore selection and may be anti-conservative. Fused coefficients also have L1 shrinkage, making their usual OLS SE inapplicable. Refitting without penalty corrects shrinkage in estimation **conditional on the selected partition**, not selection bias in tests.

## Discovery and validation split

1. Reserve instructor-period **clusters**, not individual students, for validation before any 2.2.1 outcome-informed model selection. E.g. a documented 60/40 or 70/30 partition is a *candidate design*, to be chosen with support audits and seed recorded. Preserve adequate high-frequency representation/overlap in both halves; document failure if impossible.
2. Use discovery clusters for all pre-processing that can learn from outcomes, lambda-grid choice, grouped CV, fusion and final partition selection. Canonical within-classroom outcome definitions may require special handling when computed on test clusters; define estimand and leakage policy beforehand.
3. Freeze discovered boundaries, outcome family and contrasts. The holdout data were not used to select them.
4. Refit **unpenalised** OLS (Z) or LPM (PASS) on validation clusters only, with `CLASSROOM_ID` FE and degree indicators. The validation model estimates its **own** classroom FE, so unseen training FE need not be predicted; validate column rank/positivity/support before inference. Number of validation clusters, not 190 total clusters, drives its asymptotic reliability.
5. Construct `a' beta_hat` and `SE=sqrt(a' V_CR a)`; use the stated normal/Wald reference (and report degrees-of-freedom/small-cluster robustness as appropriate), two-sided CI and p. Apply Holm to a **predeclared validation family** for each outcome. Compare adjacent selected blocks, zero-versus-positive benchmark, and any original 2|3 PPA contrast (distinct question, family must be explicit).
6. Report no inferential conclusion for a boundary unidentifiable in validation; do not quietly join groups or rerun selection on holdout.
7. Holdout testing supports reproducibility of the *association contrast under this design*, not causality, formal within-block equality or external-generalisation guarantees.

## Bootstrap stability

Resample whole `CLASSROOM_ID` clusters with replacement, **redo the entire selection procedure including lambda tuning**, and record seven binary boundary indicators. For each boundary report fraction selected, instability across CV seeds, number of distinct partitions and cluster-support failures. Use e.g. 1,000 replicates if computationally feasible; target is a plan, not a completed run. Optionally obtain out-of-bag stability or instructor-level bootstrap as sensitivity.

A boundary selected in 80% of replicates means a *selection frequency*, not `p=0.20` or a probability the boundary truly exists. Reused data and different cluster compositions limit interpretation. Raw pointwise bootstrap CIs after selecting a partition are not automatically selective CIs.

## Alternatives and comparisons

- **Exhaustive ordered partitions:** all 128 potential contiguous partitions, compared under the same nuisance controls and grouped conditional CV; suitable independent check on fused-lasso path and whether a parsimonious model performs similarly. This is not 128 independent Wald hypothesis tests.
- **Nested CV:** if all data are used to report out-of-sample selection performance, tune lambda only inside inner folds; outer folds estimate predictive performance with no leakage.
- **Repeated honest splitting / multi-splitting:** possible efficiency sensitivity, but aggregating correlated split-wise p-values requires a justified algorithm, not naive averaging.
- **Equivalence tests:** require a predeclared meaningful margin in pp/SD; a nonsignificant Wald test never establishes equivalence or a plateau.
- Cluster robustness to within-instructor correlation across academic periods requires a sensitivity at instructor level, where feasible.
- Do not use global permutation of visits: observational exchangeability does not hold by default.

## Minimal report checklist

Prespecified splits, random seeds and cluster counts; cohort; exactly which losses were scored; lambda grid/rule; selection frequencies with Monte Carlo uncertainty; rank/support; independently validated coefficients and CR SE/CI/p; multiplicity policy; both outcomes; 6+ sensitivity; comparison with Paper 2.1 baseline; all limitations. **None of these outputs exists yet**.