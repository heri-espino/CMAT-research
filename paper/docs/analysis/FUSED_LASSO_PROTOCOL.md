# Paper 2.2.1 — Fused-lasso analysis protocol (proposed; not executed)

## Statistical target and design

Let `K_i` be one of eight ordered categories `0,1,2,3,4,5,6,7+`, `C_i` instructor-period and `D_i` degree. Use the same analytic cohort and outcome construction as Paper 2.1. For each outcome separately, estimate category levels `gamma_k` and nuisance effects `alpha_c, delta_d` by penalised least squares:

```text
minimize (1/2n) * sum_i [Y_i - gamma[K_i] - alpha[C_i] - delta[D_i]]^2
         + lambda * sum_{k=1}^{7} |gamma[k]-gamma[k-1]|
```

Choose an explicit identifiability constraint (reference `gamma_0=0` with intercept, or sum-to-zero), documenting exactly where the intercept sits. Penalise **only** adjacent-frequency contrasts; never penalise instructor-period/degree effects. Because 7+ is a top-code, `6|7+` is a boundary between exact six and an aggregated tail, not consecutive exact numeric doses. If loss is normalised by n, keep lambda scaling consistent across CV/bootstrap reruns.

LPM squared loss is legitimate for estimating adjusted probability differences, but raw fitted probabilities may leave [0,1]; do not clip predictions before contrasts. Continuous Z is in instructor-period SD units. Fit with a numerically stable solver and multiple checks that lambda=0 matches unpenalised FE OLS (to tolerance); sufficiently large lambda gives all visit levels equal. Specify solver convergence, lambda grid, warm starts and deterministic seeds.

## Why fused lasso

For adjacent contrasts `d_k=gamma_k-gamma_{k-1}`, the L1 penalty sets some `d_k=0`, creating exact contiguous blocks. The method uses the ordinal structure, unlike agglomerative clustering of arbitrary categories or selecting groups by pairwise p>0.05. Unlike hard-coded illustrative partitions, block count and position emerge from tuning.

At most seven boundaries exist, hence `2^7=128` possible contiguous partitions. An exhaustive contiguous-partition fit or dynamic-programming benchmark is a valuable *audit/sensitivity* for global fit and solver consistency; fused lasso need not produce every unconstrained partition at any lambda. Do not call fused lasso a formal hierarchical dendrogram, and do not interpret its entire lambda path as nested unless nesting is verified for the implementation/data.

## Selection and comparison

- The zero-inclusive eight-level grid is the discovery basis. Also rerun the historically supported `0/1/2/3/4/5/6+` grid to test sparse-tail sensitivity.
- Freeze the outcome family, bootstrap counts, lambda rule, score and minimum support criteria before inspecting newly generated outputs.
- Fit lambda=0 fully separated, large-lambda all-fused, and intermediate path; compare against explicit `[0]|[1+]`, `[0]|[1-6]|[7+]`, and `[0]|[1-4]|[5-6]|[7+]` as *illustrations/benchmarks*, never forced answers.
- Use **grouped** folds where all rows in one `CLASSROOM_ID` stay together; if there are repeated students or instructors across periods, audit dependence and add instructor-level splitting sensitivity.
- Unseen held-out classroom fixed effects have no trained coefficient. Primary tuning score should target **within-held-out-classroom variation**, e.g. remove the held-out-classroom mean from `(Y-X_visit gamma-X_degree delta)` before squared-error aggregation. This is a conditional within-context loss, not unqualified new-classroom prediction. Report how scoring weights classroom sizes, support, and fold composition; consider alternative scoring that treats nuisance intercepts explicitly.
- Choose lambda by the prespecified best conditional held-out loss and optional one-SE *heuristic* preferring fewer blocks. Dependent repeated folds do not produce independent t-test p-values. Compare single-outcome vs prespecified shared-boundary exploratory objective, but do not silently pool Z and PASS on incompatible scales.
- Audit effective positive-frequency overlap: groups that rarely coexist within classroom are inherently difficult to separate. Report design-rank and weak-identification diagnostics.
- Generate block point estimates after a separate unpenalised refit, not by interpreting shrunken penalised coefficients directly.
- Plot coefficients/uncertainty and boundary stability against visits, avoiding causal `effect of visit` language.

## Planned sensitivities

Different training seeds and partitions; bootstrap by classroom; leave-one-instructor-out or instructor-level clustering; pooled 6+; numeric complete-case Z; alternative within-context scoring; penalisation of 0|1 vs treating the zero boundary as compulsory (only as labeled sensitivity); comparison with exhaustive contiguous partitions and simple benchmark groupings. Clearly explain any degenerate all-fused solution.

## Target tables/figures (not yet generated)

`results/paper221/tables/`: cohort/support audit, path/tuning metrics, partition/selection frequency, held-out score, block coefficients/contrasts, inference, group assignment and provenance. `results/paper221/figures/`: fusion path, selected block strips with uncertainty, boundary stability across seven cuts, tuning vs complexity, holdout Wald forest plot. Output only disclosure-safe aggregates.