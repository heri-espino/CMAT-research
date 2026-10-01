# Paper 2.1 — preliminary controlled-data results

**Status:** the current integrated controlled recipe was verified successfully in GitHub Actions run `36685329947` at branch head `93b16efb40efd7ed6803ab50568bc5fb075a10b9`. The run completed the outcome, numeric-failure, Gaussian-mixture and skew-normal specification analyses with 199 GMM bootstrap replicates, generated figures 01--05, verified outputs 01--48 and uploaded artifact `paper21-analysis-93b16efb40efd7ed6803ab50568bc5fb075a10b9` (artifact ID `11084615356`).  
These results are reproducible controlled-data outputs; claims that depend on future entrance-exam data or institutional policy verification remain provisional.

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

## 6. Numeric failure among students with numeric final grades

The observed-failure extension removes BV, RT and BA from the endpoint and asks directly whether a completed numeric grade fell below 7.5.

Model-standardised failure probabilities in the zero-inclusive model were:

| visits | adjusted P(numeric grade < 7.5) | 95% CI |
| ---: | ---: | ---: |
| 0 | 13.3% | 13.0%–13.5% |
| 1 | 3.3% | 1.9%–4.8% |
| 2 | 4.6% | 2.0%–7.2% |
| 3 | 3.6% | 0.4%–6.7% |
| 4 | 1.3% | 0.0%–3.7% |
| 5 | 3.7% | 0.0%–8.3% |
| 6+ | 3.8% | 0.6%–6.9% |

The zero-inclusive logit omnibus test strongly rejected equal adjusted log odds ($p=3.41\times10^{-17}$). After Holm adjustment, zero visits differed from 1, 2, 3 and 6+ visits; the sparse 4- and 5-visit contrasts were less precise.

Among users only, adjusted failure probabilities were 2.5%, 4.8%, 5.3%, 2.0%, 6.6% and 4.6% for 1, 2, 3, 4, 5 and 6+ visits. The user-only omnibus test was not significant ($p=0.480$), and no pairwise odds ratio survived Holm adjustment. Thus the broad user/non-user difference persists even when administrative outcomes are excluded, while repeated attendance still does not show a regular numeric-failure gradient.

## 7. Instructor-level clustering sensitivity

The primary models cluster by instructor-period. Re-clustering by instructor preserves the same point estimates but allows dependence across periods taught by the same instructor.

The zero-versus-positive benchmark remained essentially unchanged:

- continuous outcome: +0.361 SD (95% CI 0.305 to 0.417; 53 instructor clusters);
- pass probability: +15.3 percentage points (95% CI 12.8 to 17.8 pp; 53 instructor clusters).

Among users, with 51 instructor clusters:

- continuous-outcome omnibus: **p = 0.0477**;
- pass-probability omnibus: **p = 0.0551**.

No continuous pairwise contrast survived Holm adjustment. One pass-probability contrast did: 6+ visits versus one visit was +12.0 percentage points (95% CI 4.3 to 19.8 pp; Holm-adjusted p = 0.0358). No adjacent pass-frequency contrast survived Holm adjustment.

This sensitivity means the manuscript should not say that the positive-frequency groups are simply identical. A broader low-versus-high separation is plausible under instructor-level clustering, but the evidence still does not support a visit-by-visit staircase.

## 8. Gaussian-mixture sensitivity

The GMM analysis is exploratory and is intended to describe distributional shape, not to discover literal latent student classes.

For the numeric complete-case outcome, the 199-replicate parametric-bootstrap comparison of K=1 versus K=2 rejected the single-Gaussian fit in every group (bootstrap p = 0.005 except the five-visit group, p = 0.015). However, BIC and ICL disagreed substantially:

- among positive-frequency groups, BIC preferred K=2 for 1, 2 and 5 visits and K=3 for 3, 4 and 6+;
- ICL preferred K=1 for 1, 2, 3, 4 and 6+ and K=2 only for 5 visits.

For the two-component complete-case fits, lower-component weights were:

1: 15.7% / 2: 13.0% / 3: 44.4% / 4: 25.4% / 5: 4.1% / 6+: 14.8%.

The imputed-outcome sensitivity produced:

1: 25.2% / 2: 21.4% / 3: 21.2% / 4: 35.7% / 5: 9.1% / 6+: 19.1%.

Five of the six positive-frequency complete-case fits had Ashman's D below 2, indicating substantial component overlap; the exception was the sparse five-visit group (n = 49), where the lower component contained only about 4% of the group. The three-visit group was especially sensitive to imputation, with its estimated lower-component weight changing from 44.4% to 21.2%.

The correct interpretation is therefore that the grade distributions depart from a single Gaussian, but neither component weights nor model-selection criteria support a stable, monotone two-class attendance-response structure. The mixture figures belong in the paper as distributional diagnostics, not as a latent-class result.

## 9. Interpretation emerging from the current results

The current evidence supports a six-part descriptive structure:

1. a large adjusted difference between **zero attendance and any attendance** in both continuous final performance and probability of passing;
2. a similarly large zero-versus-positive separation in **completed numeric failure**, showing that the benchmark is not created solely by administrative-outcome imputation;
3. no multiplicity-supported **adjacent** visit-frequency contrasts among users, although instructor-level clustering leaves open a broader low-versus-high separation and yields one non-adjacent 1-versus-6+ pass contrast;
4. a substantial difference in the **composition of non-PASS outcomes** between zero-attendance students and CMAT users;
5. within that management composition, the most distinctive administrative code is **BV**, whereas RT shows no analogous adjusted contrast;
6. non-Gaussian grade distributions in which the imputed outcome remains better represented by a two-Gaussian mixture than by a single strongly skewed distribution across every frequency group, while the numeric complete-case outcome is more mixed; this links the clearer imputed lower component to administrative-outcome representation without implying a monotone dose response or literal student types.

The academic-management mechanism is therefore worth developing in the Discussion, but it must remain an explanation compatible with the data rather than a measured engagement construct. The records do not show whether students knew the withdrawal rules, received advice, cared more about GPA, or chose BV for a particular reason.

The requested entrance-exam data will be especially useful here because prior preparation may explain part of both help-seeking and adverse-outcome management, although it will not measure engagement or institutional knowledge directly.


## 10. Skew-normal specification check

A follow-up specification check asked whether the Gaussian-mixture result could be explained by a single strongly asymmetric distribution. For each `0/1/2/3/4/5/6+` group, the same observations were fit with one Gaussian, one skew-normal, and a two-Gaussian mixture. The fitted skew-normal shape parameters were strongly negative, so the one-component alternative was allowed substantial left skew.

Using `Delta BIC = BIC(skew-normal) - BIC(GMM K=2)`, the numeric complete-case values were:

| visits | Delta BIC | BIC preferred |
| ---: | ---: | --- |
| 0 | +1223.3 | GMM K=2 |
| 1 | +20.7 | GMM K=2 |
| 2 | +12.8 | GMM K=2 |
| 3 | -4.5 | skew-normal |
| 4 | -6.1 | skew-normal |
| 5 | -2.7 | skew-normal |
| 6+ | -11.7 | skew-normal |

For the imputed primary outcome, the two-Gaussian mixture was preferred in all seven groups:

| visits | Delta BIC |
| ---: | ---: |
| 0 | +1066.4 |
| 1 | +77.3 |
| 2 | +32.1 |
| 3 | +28.1 |
| 4 | +3.4 |
| 5 | +12.4 |
| 6+ | +11.4 |

Thus simple skewness is not sufficient to explain the imputed density structure. In the numeric complete-case outcome, by contrast, a single skew-normal is sufficient by BIC for several higher-frequency groups, while 0, 1 and 2 visits still prefer the two-Gaussian representation.

The posterior-responsibility composition adds an important substantive link. Aggregating positive-attendance students, the imputed lower component contained approximately **55.5% administrative outcomes** (49.5% BV, 5.3% RT, 0.7% BA), 34.4% PASS and 10.1% numeric non-PASS. The higher component contained approximately **2.0% administrative outcomes** (1.8% BV and 0.2% RT), 97.0% PASS and 1.1% numeric non-PASS.

This strongly connects the lower imputed density component with the observed academic-management states, especially BV. It does not establish that the component is a behavioral student type or that CMAT caused withdrawal. The complete analysis, exact model-selection tables, function map and controlled-run provenance are documented in `paper/docs/results/MIXTURE_ANALYSIS_RESULTS.md`.
