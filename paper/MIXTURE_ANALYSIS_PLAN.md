# Paper 2.1 — observed numeric failure and Gaussian-mixture plan

**Status:** implemented; numerical results must not be interpreted until a controlled-data run completes successfully.

## Scientific motivation

The Paper 2.1 ridgeline suggests that some positive-attendance groups may contain more than one concentration of final performance. The primary continuous outcome includes numerical imputations for BV, RT, and BA, so apparent multimodality in that outcome cannot by itself establish two performance distributions.

The analysis therefore follows an evidence hierarchy that separates observed numeric outcomes from the imputed sensitivity.

## A. Observed numeric failure

Restrict to students who received a numeric final grade.

Define numeric failure as a final numeric grade below 7.5 and numeric pass as a final numeric grade of at least 7.5.

For each attendance group 0 / 1 / 2 / 3 / 4 / 5 / 6+, report the number of numeric final grades, the number and probability of numeric failure, and raw failure odds.

Then fit a logistic model with attendance-frequency indicators, instructor-period fixed effects, degree-programme indicators, and cluster-robust standard errors at instructor-period level. Report pairwise odds ratios with Holm adjustment and repeat the omnibus/pairwise analysis among positive-attendance groups only.

Odds ratios are complementary to probabilities, not intrinsically more interpretable. Manuscript prose should normally report observed probabilities first and use ORs as model-based relative comparisons.

If sparse failures cause separation or unstable intervals, do not force the logit result. Retain the observed probabilities and document the instability.

## B. Primary Gaussian-mixture analysis: numeric complete case

The primary mixture outcome is Z_GRADE_COMPLETE_CASE, which contains only observed numeric final grades.

For each group 0 / 1 / 2 / 3 / 4 / 5 / 6+ independently:

1. fit univariate Gaussian mixtures with K = 1, 2, 3;
2. use multiple default EM starts;
3. for the two-component model, include (-1.1, 0.5) as one additional initialization, not the unique initialization;
4. also include the group's empirical 25th/75th percentiles as an additional two-component start;
5. choose the highest-likelihood converged solution for each K;
6. compare K using BIC and ICL;
7. test K=1 versus K=2 using a parametric-bootstrap likelihood-ratio test;
8. order the two components by their estimated means and label them lower_performance and higher_performance;
9. report component means, SDs, weights, Ashman's D, posterior entropy, and mean maximum responsibility.

The ordinary chi-square likelihood-ratio reference distribution must not be used for the component-count test because mixture-model regularity conditions fail at the boundary.

## C. Posterior component composition

Do not convert responsibilities to hard student labels for the primary interpretation.

For each two-component model, use posterior responsibilities to calculate soft expected composition by observed final state. In the complete-case analysis, the relevant states are numeric pass and numeric non-pass.

The estimated lower-component weight is a distributional parameter, not an observed proportion of a literal student type.

## D. Imputed-outcome sensitivity

Repeat exactly the same GMM procedure using Z_GRADE_PRIMARY, which numerically imputes BV/RT/BA. This analysis is a sensitivity only.

Interpret the comparison as follows:

- bimodality present in complete-case and imputed outcomes: evidence that the structure is not solely created by administrative-outcome imputation;
- bimodality weak or absent complete-case but strong imputed: the apparent second mode is likely driven materially by the representation of administrative outcomes;
- similar component means but changing component weights: differences in group means may reflect changing mixture composition more than a uniform location shift;
- changing component means with stable weights: the pattern is more consistent with within-component location shifts;
- unstable component estimates in small high-frequency groups: treat the tail as inconclusive rather than as evidence that a component disappeared.

## E. What the model cannot establish

Even a well-separated two-component GMM does not identify good students versus students who tried and failed, motivation or effort, a causal effect of CMAT attendance, a transition of a student from one latent type to another, or that six visits eliminate failure.

The safe terminology is lower-performance component and higher-performance component.

Accumulating many visits also requires remaining enrolled long enough to do so, so an apparent disappearance of low outcomes at high frequency is vulnerable to opportunity-time and persistence selection.

## F. Planned outputs

The controlled Paper 2.1 recipe produces:

- 30_numeric_failure_descriptives.csv;
- 31--36 adjusted numeric-failure logit outputs;
- 37--40 complete-case GMM model selection, parameters, bootstrap, and soft composition;
- 41--44 corresponding imputed-outcome sensitivity outputs;
- 45_gmm_component_comparison_complete_vs_imputed.csv.

No row-level responsibilities are written to artifacts.

## Decision rule for manuscript inclusion

Do not add a two-population narrative to the paper merely because a ridgeline appears bimodal.

Promote the mixture analysis into the main manuscript only if the numeric complete-case evidence is coherent across model-selection criteria, component separation, bootstrap evidence, and stability. Otherwise keep it exploratory or omit it.
