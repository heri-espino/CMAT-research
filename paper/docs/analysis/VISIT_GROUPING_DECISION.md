# Paper 2.1 — visit-grouping decision

**Decision date:** 2026-09-20  
**Outcome status when decision made:** no grade means, pass rates, pairwise outcome effects, or outcome p-values were inspected in choosing this grouping.

## Historical support-based grouping and current reporting grid

Paper 2.1 will use:

`1 / 2 / 3 / 4 / 5 / 6+`

for the primary analysis among students with positive CMAT attendance.

The outcome-blind audit originally selected `1 / 2 / 3 / 4 / 5 / 6+` as the better-supported positive-frequency inferential grouping because exact six had weaker adjacent instructor-period overlap. The current manuscript reporting grid is `0 / 1 / 2 / 3 / 4 / 5 / 6 / 7+`, which places the zero-attendance benchmark, the PPA threshold and the upper tail in one frame. The earlier pooled `6+` specification remains a robustness check on tail sparsity; the document should not imply that the `7+` cut was pre-specified before outcomes were examined.

## Why the Paper 2 top-code at 4+ was relaxed

Paper 2 deliberately used `4+` as a conservative presentation. For Paper 2.1, the scientific question is specifically whether outcomes differ among students who attend repeatedly, so the positive-frequency tail was audited without looking at outcomes.

Exact-count support was:

| exact visits | students | instructor-period groups |
| ---: | ---: | ---: |
| 1 | 517 | 152 |
| 2 | 245 | 114 |
| 3 | 170 | 84 |
| 4 | 96 | 69 |
| 5 | 55 | 40 |
| 6 | 50 | 36 |
| 7 | 25 | 23 |
| 8 | 19 | 17 |

Both 5 and 6 retain non-trivial marginal support. However, Paper 2.1 is built around pairwise comparisons, so marginal counts alone are insufficient.

## Pair-overlap frontier

For each candidate specification `1, ..., K, (K+1)+`, the outcome-blind audit calculated how many instructor-period groups contain both members of each pair.

The minimum overlap among adjacent groups was:

| top exact K | grouping tail | minimum adjacent overlap |
| ---: | :--- | ---: |
| 2 | 3+ | 88 |
| 3 | 4+ | 59 |
| 4 | 5+ | 45 |
| 5 | 6+ | 26 |
| 6 | 7+ | 15 |
| 7 | 8+ | 7 |

Moving from `1/2/3/4/5/6+` to `1/2/3/4/5/6/7+` therefore increases nominal resolution but reduces the weakest adjacent comparison from 26 to 15 instructor-period groups. The specific 5-versus-6 exact comparison has only 15 groups containing both frequencies.

By contrast, pooling from 6 upward gives a `6+` group with **151 students, 72 instructor-period groups, and 38 instructors**.

## Decision rule

The objective is not to find a mathematically unique “optimal n”, which does not exist without a loss function. The branch instead uses a **support-preserving resolution rule**:

> retain exact visit frequencies while doing so adds useful resolution without a sharp deterioration in the instructor-period overlap required for the planned pairwise comparisons; pool the upper tail at the first clear deterioration in that overlap frontier.

Under that rule, `1/2/3/4/5/6+` is the primary specification.

## Manuscript-ready rationale

The final paper should explain the cut as a **support-based design choice rather than a result-driven threshold**. A compact Methods version can state that exact visit counts were retained while they remained sufficiently represented across instructor--period groups for the planned pairwise comparisons; separating six visits from the upper tail reduced the weakest adjacent-group overlap from 26 to 15 instructor--period groups, so six or more visits were pooled. This rule was fixed before examining Paper 2.1 grade means, pass rates, or pairwise outcome tests.

The purpose of this wording is to make three points explicit without overexplaining the internal audit:

1. the top-code was not inherited arbitrarily from Paper 2;
2. it was not selected from favourable p-values or effect sizes;
3. the relevant constraint was not only the number of students, but the instructor--period overlap needed for the planned adjusted pairwise comparisons.

Do not describe `6+` as a mathematically unique or universally optimal cut. It is the highest-resolution grouping that preserved reasonable comparison support under this study's design.

## Sensitivity grouping

The more granular:

`1 / 2 / 3 / 4 / 5 / 6 / 7+`

may be reported as an exploratory sensitivity because exact 6 still has 50 students in 36 instructor-period groups and the 7+ tail has 101 students in 57 groups.

It was not originally selected as the support-optimal inferential grouping. Its use in the current manuscript is a reporting decision that must remain explicitly distinguished from the earlier outcome-blind support choice.


### Current manuscript interpretation

The current manuscript uses the full `0 / 1 / 2 / 3 / 4 / 5 / 6 / 7+` grid for its main descriptive and pairwise displays while preserving the original support-based `6+` choice as a robustness specification. Three interpretive regions are distinguished without recoding the exposure:

- `0`: no recorded CMAT use;
- `1--3`: attendance that may be partly influenced by the PPA participation-credit option;
- `4+`: repeated CMAT use beyond the three visits needed for that specific credit option, with `7+` retained as a high-frequency tail.

The manuscript may discuss the descriptive changes from 4 to 5 and from 6 to 7+ because they are visible in the observed profile, but neither adjacent contrast is statistically resolved and neither should be labelled a threshold effect. The strongest within-user multiplicity-adjusted result in the full-group PASS model is 7+ versus one visit. This result does not retroactively make the 7+ cut outcome-blind or causal.

### PPA-threshold diagnostic

The `1 / 2 / 3 / 4 / 5 / 6 / 7+` sensitivity also serves a separate descriptive purpose: the institutional PPA participation threshold occurs at three recorded visits. This creates a substantively interesting boundary between one--two visits and three or more visits, because reaching three visits may reflect both demand for mathematics support and an institutional participation incentive.

For that reason the sensitivity analysis now exports all adjusted pairwise comparisons for standardised grade and pass probability, together with two p-value matrices for each outcome:

- unadjusted pairwise p-values, used only to inspect where local contrasts first become visible;
- Holm-adjusted p-values, used for multiplicity-aware interpretation of the full pairwise family.

The corresponding heatmap dashboards mark the boundary between 2 and 3 visits. They are exploratory diagnostics of where differences appear across visit frequencies; they do not identify a causal effect of the PPA incentive, because students are not randomly assigned to reach three visits and visit frequency remains behaviourally selected.

## Reopening this decision

Do not change the primary cut after inspecting outcome significance. Reopen it only if:

- a data-quality issue changes the visit counts;
- a different inferential design changes the relevant support requirement;
- or the user explicitly requests a different estimand.

This document is the durable record that the primary grouping was chosen before the Paper 2.1 outcome comparisons were run.
