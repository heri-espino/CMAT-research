# Paper 2.1 — preliminary controlled-data results

**Status:** core performance results verified in the Paper 2.1 controlled recipe; academic-management extension verified from GitHub Actions run `35515296397` at commit `871c0583fc76cd8f22e2bbe8882219acbd5a3467`.  
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

## 4. Academic-result composition and the management margin

The four-state decomposition separates PASS, numeric grades below 7.5, BV/RT, and BA.

### Zero visits versus any attendance

For students with zero visits:

- 72.1% passed;
- 10.8% received a numeric grade below 7.5;
- 15.9% had BV/RT;
- 1.2% had BA.

For students with one or more visits, aggregating the positive-frequency groups:

- 82.4% passed;
- 3.2% received a numeric grade below 7.5;
- 14.3% had BV/RT;
- 0.2% had BA.

Thus users did **not** have more administrative outcomes overall. The important difference is that numeric failure was substantially less common.

### Conditional on non-PASS

Among the 1,504 zero-visit students who did not pass, 923 (61.4%) had an administrative outcome and 581 (38.6%) had a numeric grade below 7.5.

Among the 217 CMAT users who did not pass, 178 (82.0%) had an administrative outcome and 39 (18.0%) had a numeric grade below 7.5.

With instructor-period fixed effects, degree-programme indicators, and clustered standard errors, any attendance versus zero visits was associated with **+13.2 percentage points** in the probability that a non-PASS outcome was administrative rather than numeric (95% CI 6.8 to 19.6 pp; p < 0.001).

### The pattern is specifically concentrated in BV

The exact administrative-token decomposition shows that the broad category BA/BV/RT hides different patterns:

- BV represented 9.8% of all zero-visit outcomes and 12.9% of all positive-attendance outcomes;
- RT represented 6.1% of zero-visit outcomes but only 1.4% among users;
- BA represented 1.2% of zero-visit outcomes and 0.2% among users.

Among non-PASS cases restricted to BV or numeric failure, any attendance was associated with **+16.8 percentage points** in the adjusted probability of BV rather than a numeric failure (95% CI 9.5 to 24.1 pp; p < 0.001).

The analogous adjusted contrast for RT versus numeric failure was essentially null: **+0.5 percentage points** (95% CI -15.1 to 16.2 pp; p = 0.945).

This makes BV, rather than administrative withdrawal in general, the relevant observed component for the academic-engagement/institutional-navigation hypothesis.

### Frequency among users

The management composition did not show a clear adjusted frequency gradient among users:

- administrative versus numeric non-PASS omnibus: p = 0.495;
- BV/RT versus numeric failure omnibus: p = 0.599;
- BV versus numeric failure omnibus: p = 0.523.

No positive-frequency pairwise contrast survived Holm adjustment. As with the performance outcomes, the main empirical separation is currently zero attendance versus any attendance.

## 5. Distributional interpretation

The imputed continuous outcome and the numeric complete-case outcome tell an important joint story.

Under the primary imputed outcome, higher-frequency groups differ more visibly in the lower tail than in the upper tail: the 90th percentile is broadly similar, while the 10th and 25th percentiles are less negative for some higher-frequency groups. This is not consistent with a simple story in which a small number of very high-performing users pull up the mean.

The numeric complete-case profile is substantially flatter, and the complete-case omnibus test across positive frequency groups is non-significant (p = 0.397). The contrast between the imputed and complete-case distributions is consistent with a meaningful part of the lower-tail pattern being linked to the composition of administrative outcomes.

This does not establish that attendance prevents withdrawal or causes students to use BV. It shows that the **type of adverse final outcome** differs systematically with attendance and therefore deserves separate analysis rather than being hidden inside a single non-PASS category.

## 6. Interpretation emerging from the current results

The current evidence supports a four-part descriptive structure:

1. a large adjusted difference between **zero attendance and any attendance** in both continuous final performance and probability of passing;
2. no clear adjusted separation among the positive attendance-frequency groups after multiplicity control;
3. a substantial difference in the **composition of non-PASS outcomes** between zero-attendance students and CMAT users;
4. within that management composition, the most distinctive administrative code is **BV**, whereas RT shows no analogous adjusted contrast.

The academic-management mechanism is therefore worth developing in the Discussion, but it must remain an explanation compatible with the data rather than a measured engagement construct. The records do not show whether students knew the withdrawal rules, received advice, cared more about GPA, or chose BV for a particular reason.

The requested entrance-exam data will be especially useful here because prior preparation may explain part of both help-seeking and adverse-outcome management, although it will not measure engagement or institutional knowledge directly.
