# Paper 2.1 — analysis plan

This file is the pre-outcome analysis contract for the visit-frequency study. The purpose is to prevent the upper attendance cut and the inferential story from being chosen after inspecting favourable p-values.

## Stage 0 — reproduce the benchmark

Reproduce the simple Paper 2 contrast between:

- 0 recorded visits;
- 1 or more recorded visits.

Do this for both principal outcomes:

1. PASS/non-PASS;
2. continuous standardised grade with the canonical adverse-outcome imputation.

This is a benchmark and literature bridge, not the central Paper 2.1 result.

## Stage 1 — outcome-blind support audit

Before looking at group means, pass rates, pairwise effects, or p-values, compute for every exact positive visit count k:

- number of students;
- number of instructor-period groups containing k;
- number of instructor-period groups in which k can be compared with at least one other positive-frequency group;
- distribution of students across instructor-period groups;
- share of all positive-attendance students;
- cumulative tail size at >= k.

The grouping rule should **maximize retained frequency resolution subject to pre-declared support requirements**, rather than selecting the cut where statistical significance happens to disappear.

Candidate starting point from marginal counts: `1 / 2 / 3 / 4 / 5 / 6 / 7+`.

The support audit may move the top-code lower if the 5- or 6-visit groups are concentrated in too few instructor-period groups, or higher only if the exact upper categories remain adequately supported.

Record the final rule and its rationale before running the pairwise outcome analysis.

## Stage 2 — descriptive outcome profiles

For each retained attendance-frequency group report:

### Binary outcome
- N;
- pass rate;
- 95% CI.

### Continuous outcome
- N;
- mean standardised grade;
- SD;
- 95% CI.

Display the two outcome profiles separately. Do not treat one as validation of the other; they answer related but distinct questions.

## Stage 3 — omnibus inference among CMAT users

Restrict the main frequency-shape analysis to students with >=1 visit.

### Continuous standardised grade

Primary model:

- attendance-frequency indicators;
- instructor-period fixed effects;
- degree-programme indicators;
- cluster-robust standard errors at instructor-period level.

Test the joint null that all positive attendance-frequency coefficients are equal.

Welch ANOVA may be reported as an unadjusted descriptive/secondary check, not as the primary inferential result.

### PASS/non-PASS

Primary estimand: adjusted **risk differences in probability of passing**, expressed in percentage points.

Use a model preserving the same instructor-period and degree-programme adjustment structure and cluster-robust inference. A linear-probability fixed-effect model is the preferred starting point because pairwise contrasts are directly interpretable as percentage-point differences.

A logistic fixed-effect or other binary-response model may be added only as a sensitivity if it is estimable and materially informative; it should not replace the directly interpretable risk-difference analysis merely for methodological appearance.

## Stage 4 — pairwise contrasts

For every retained positive attendance group pair, estimate:

### Continuous outcome
- adjusted mean difference in Z;
- 95% CI;
- raw p-value;
- Holm-adjusted p-value.

### Binary outcome
- adjusted pass-probability difference in percentage points;
- 95% CI;
- raw p-value;
- Holm-adjusted p-value.

Multiplicity adjustment should be applied within a clearly defined family of positive-group pairwise contrasts for each outcome. The 0-versus-positive benchmark belongs to a separate benchmark family unless a later preregistered rationale combines them.

Also report adjacent contrasts explicitly:

- 1 vs 2;
- 2 vs 3;
- 3 vs 4;
- etc.

Adjacent contrasts are scientifically important because they address whether successive attendance frequencies are distinguishable.

## Stage 5 — equivalence analysis

A non-significant difference is **not evidence of equality**.

If practical-equivalence margins can be justified before inspecting the pairwise results, run equivalence tests for selected contrasts, especially adjacent groups.

Candidate scales for discussion, not yet final decisions:

- continuous Z: a small standardised difference bound such as +/-0.15 or +/-0.20 SD;
- PASS probability: a small absolute risk-difference bound such as +/-5 percentage points.

The final margins must be justified and frozen before the equivalence results are calculated. If no defensible margin can be justified, omit formal equivalence claims and use “inconclusive” rather than “equivalent”.

Classify each pair only when justified as:

- evidence of a difference;
- evidence of practical equivalence;
- inconclusive.

## Stage 6 — heatmaps

Produce two primary pairwise heatmaps among CMAT users.

### Panel A — continuous performance
Cell colour = adjusted difference in standardised grade.

### Panel B — academic success
Cell colour = adjusted difference in pass probability, in percentage points.

Each cell should display the effect estimate. Statistical/equivalence status may be represented by a compact symbol or border, but **colour must encode effect magnitude/direction rather than p-value**.

A supplementary heatmap may include the zero-visit group to visually recover the known benchmark separation, but the main heatmap should emphasize variation among users.

## Stage 7 — shape diagnostics

As a secondary exploratory description, fit attendance frequency more continuously among users, for example with a restricted spline or another low-complexity smooth.

Purpose: assess whether the pairwise pattern resembles a plateau, gradual increase, saturation, decline, or irregular curve.

Do not use the spline to choose the categorical cut retrospectively. The support-based grouping must already have been fixed.

## Stage 8 — outcome-construction and exposure-opportunity robustness

The two principal outcome families are themselves a robustness structure:

- PASS requires no numerical imputation for BA/BV/RT;
- continuous Z uses the canonical imputation and contains more outcome information.

However, PASS does **not** solve exposure-opportunity bias. A student who withdraws early has less time to accumulate visits, so high visit counts mechanically require more opportunity to remain enrolled long enough to attend. A positive frequency--PASS pattern could therefore partly reflect persistence in the course rather than a benefit of additional CMAT attendance.

Retain the numeric-only complete-case continuous outcome as an additional sensitivity because it removes BA/BV/RT and the imputation assumption, while recognizing that it conditions on observed numeric course completion and therefore does not fully identify a causal frequency effect.

When interpreting frequency patterns, explicitly separate:
- robustness to numerical imputation;
- robustness to excluding administrative withdrawals;
- unresolved same-period timing and opportunity-to-accumulate-visits concerns.

## Stage 9 — clustering sensitivity

Because instructors recur across periods, compare instructor-period clustering with clustering by instructor for the main pairwise models. Do not change the estimand or the instructor-period grade standardisation.

## Stage 10 — entrance-exam sensitivity when available

If the requested university entrance-exam score becomes available and passes the Paper 2 intake/comparability audit, repeat the principal adjusted frequency analysis with the baseline score included.

The entrance score is an observed-preparation sensitivity; it does not turn visit frequency into a causal treatment dose.

## Outputs to preserve

At minimum generate aggregate, reproducible files for:

- exact-count support audit;
- chosen grouping specification and decision record;
- descriptive summaries for both outcomes;
- user-only omnibus tests;
- all pairwise contrasts for both outcomes;
- adjacent contrasts;
- equivalence results if used;
- instructor-level clustering sensitivity;
- heatmap source matrices;
- optional smooth/spline diagnostics;
- entrance-exam sensitivity when available.

No manuscript number should be calculated manually outside the canonical recipe.
