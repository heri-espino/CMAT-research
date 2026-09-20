# Paper 2.1 — preliminary controlled-data results

**Status:** verified from GitHub Actions run `35513628711` at commit `48bdbef5f361db0d9d4008d99f65d77ca79053a5`.  
These are reproducible intermediate results, not frozen manuscript claims. Reverify against the current branch head before submission.

## 1. Benchmark: no recorded attendance versus any attendance

Using the full Paper 2.1 cohort (N = 6,627) with instructor-period fixed effects, degree-programme indicators, and standard errors clustered at the instructor-period level:

- any CMAT attendance versus zero visits was associated with **+0.361 standard deviations** in the continuous standardised-grade outcome (95% CI 0.302 to 0.421; p < 0.001);
- any CMAT attendance versus zero visits was associated with **+15.3 percentage points** in the probability of passing (95% CI 12.4 to 18.1 percentage points; p < 0.001).

These are observational associations, not estimates of student-level improvement or causal CMAT effects.

## 2. Primary frequency groups among users

Frozen primary groups:

`1 / 2 / 3 / 4 / 5 / 6+`

There are 1,234 students with positive same-period CMAT attendance.

Unadjusted descriptive outcomes:

| visits | n | mean Z | pass rate |
| ---: | ---: | ---: | ---: |
| 1 | 517 | 0.219 | 81.0% |
| 2 | 245 | 0.247 | 80.8% |
| 3 | 170 | 0.278 | 81.8% |
| 4 | 96 | 0.267 | 86.5% |
| 5 | 55 | 0.382 | 85.5% |
| 6+ | 151 | 0.401 | 86.8% |

The descriptive pattern is compatible with somewhat higher outcomes at higher frequencies, but the adjusted user-only inference does not establish distinct frequency groups.

### Omnibus tests among users

- continuous standardised grade: p = **0.317**;
- pass probability: p = **0.152**.

Thus the joint null of equal adjusted outcomes across the positive attendance-frequency groups was not rejected for either principal outcome.

### Pairwise comparisons

No pairwise comparison among the six positive attendance-frequency groups survived Holm adjustment for either the continuous standardised grade or pass probability.

For orientation only:

- 1 versus 6+ visits in the continuous outcome had raw p = 0.022 but Holm-adjusted p = 0.328;
- 1 versus 6+ visits in pass probability had raw p = 0.011 but Holm-adjusted p = 0.171.

These examples illustrate why the paper must not select or narrate isolated unadjusted pairwise findings.

## 3. Sensitivity with a more granular tail

Exploratory sensitivity groups:

`1 / 2 / 3 / 4 / 5 / 6 / 7+`

The descriptive 7+ group had mean Z = 0.457 and pass rate = 89.1%, whereas exact 6 visits had mean Z = 0.288 and pass rate = 82.0%. This instability in the sparse upper tail reinforces the outcome-blind decision not to make 7+ the primary specification.

Adjusted omnibus tests remained non-significant:

- continuous standardised grade: p = **0.213**;
- pass probability: p = **0.102**.

No pairwise contrast survived Holm adjustment in this sensitivity.

## 4. What non-PASS means among CMAT users

Across all 1,234 students with at least one recorded visit:

- 1,017 passed (82.4%);
- 39 received a numeric final grade below 7.5 (3.2%);
- 178 had BA/BV/RT (14.4%).

Among the 217 users classified as non-PASS, **178 (82.0%) were BA/BV/RT** and only **39 (18.0%)** had a numeric final grade below 7.5.

By primary attendance group:

| visits | pass | numeric <7.5 | BA/BV/RT |
| ---: | ---: | ---: | ---: |
| 1 | 81.0% | 2.9% | 16.1% |
| 2 | 80.8% | 4.5% | 14.7% |
| 3 | 81.8% | 2.9% | 15.3% |
| 4 | 86.5% | 1.0% | 12.5% |
| 5 | 85.5% | 3.6% | 10.9% |
| 6+ | 86.8% | 3.3% | 9.9% |

This decomposition is substantively useful: among students who attended CMAT but did not pass, administrative withdrawal codes dominate over completed numeric grades below the pass mark.

Do not infer that CMAT attendance prevents withdrawal, that students withdrew because they did not attend, or that students with BA/BV/RT would otherwise have failed. The table describes the composition of observed final outcomes.

## 5. Interpretation emerging from the first run

The current evidence is more consistent with:

1. a large and precisely estimated difference between **zero attendance and any attendance**;
2. descriptively higher outcomes at some higher attendance frequencies;
3. insufficient adjusted evidence to distinguish the positive attendance-frequency groups from one another under the current sample and multiplicity control;
4. an important distinction between **continuous final performance**, **crossing the 7.5 pass threshold**, and **the composition of non-passing outcomes**.

The paper should not yet use the phrase “diminishing returns”, “frequency effect”, or “two types of CMAT users”. The distributional profile provides an additional qualification. Under the primary imputed outcome, the higher-frequency groups differ more visibly in the lower tail than in the upper tail: the 90th percentile is broadly similar across groups, while the 10th and 25th percentiles are less negative for some higher-frequency groups. This does **not** look like a simple story in which a small number of very high-performing users pull up the mean.

However, the numeric complete-case profile is substantially flatter: medians and lower quartiles do not display the same upward pattern, and the complete-case omnibus test across positive frequency groups is non-significant (p = 0.397). The contrast between the imputed and complete-case distributions is consistent with the descriptive frequency pattern being strongly related to the changing prevalence of BA/BV/RT across attendance groups.

This should be stated carefully. The data show that administrative withdrawals are less common in the higher-frequency groups and that including them as adverse outcomes changes the lower tail of the continuous distribution. They do not establish that additional CMAT attendance prevents withdrawal, because withdrawal timing and opportunity to accumulate visits are not randomized.
