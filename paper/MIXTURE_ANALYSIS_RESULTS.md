# Paper 2.1 — mixture, skew-normal, and administrative-outcome analysis

**Status:** controlled-data results verified; reusable estimators upstreamed to `main`; manuscript interpretation updated to distinguish observed density structure from the proposed academic-management mechanism.

## 1. Why this analysis was added

The original Paper 2.1 distribution plots suggested more than one concentration of final performance. This was scientifically important because the primary continuous outcome contains numerical representations of BV, RT, and BA, while the numeric complete-case outcome contains only observed numerical final grades.

The analysis therefore evolved through four questions:

1. Is the zero-versus-positive attendance result still visible when administrative outcomes are removed and only observed numeric failure is analysed?
2. Is a single Gaussian an adequate model for the standardised-grade distribution within each attendance-frequency group?
3. If a Gaussian mixture fits better, is this merely because several symmetric Gaussians are approximating one strongly skewed continuous distribution?
4. In the imputed outcome, is the lower mixture component associated with the observed administrative final states, especially BV?

The final hierarchy answers each question separately rather than treating a visually bimodal ridgeline as proof of two literal student types.

## 2. Analysis population and outcomes

The full Paper 2.1 cohort contains 6,627 first eligible MU attempts:

- 5,393 students with zero recorded same-period CMAT visits;
- 1,234 students with one or more visits.

The frozen zero-inclusive frequency groups are:

`0 / 1 / 2 / 3 / 4 / 5 / 6+`.

Two continuous outcomes are used:

- `Z_GRADE_COMPLETE_CASE`: instructor-period-standardised observed numeric final grade only;
- `Z_GRADE_PRIMARY`: the primary instructor-period-standardised outcome after the canonical adverse-outcome imputation for BV/RT/BA.

The complete-case outcome is the primary density-shape check because it is not mechanically affected by numerical values assigned to administrative outcomes. The imputed outcome is then used to study how administrative-outcome representation changes the distribution.

## 3. Observed numeric failure

Before fitting mixtures, the analysis removes BV, RT, and BA entirely and asks whether an observed numeric final grade is below the 7.5 pass mark.

Model-standardised numeric-failure probabilities for `0/1/2/3/4/5/6+` were approximately:

| visits | adjusted P(numeric grade < 7.5) |
| ---: | ---: |
| 0 | 13.3% |
| 1 | 3.3% |
| 2 | 4.6% |
| 3 | 3.6% |
| 4 | 1.3% |
| 5 | 3.7% |
| 6+ | 3.8% |

The zero-inclusive fixed-effect logistic omnibus strongly rejected equal failure odds, while the user-only omnibus was not significant (`p=0.480`) and no user-only pairwise odds ratio survived Holm adjustment.

This result matters because the broad user/non-user difference is not created solely by assigning numerical values to administrative outcomes.

## 4. Gaussian-mixture analysis

For every zero-inclusive attendance group, the complete-case outcome was fit with Gaussian mixtures for `K=1,2,3`.

The two-component candidate used:

- standard multi-start EM;
- the empirical 25th and 75th percentiles as an additional start;
- `(-1.1, 0.5)` as another additional start, not an imposed component location.

For every `K`, the highest-likelihood converged solution was retained. The diagnostics include:

- log-likelihood;
- AIC;
- BIC;
- ICL;
- posterior entropy;
- mean maximum posterior responsibility;
- component weights, means and standard deviations;
- Ashman's D for the two-component model;
- a parametric-bootstrap likelihood-ratio comparison of `K=1` versus `K=2`.

### 4.1 Parametric-bootstrap result

With 199 bootstrap replicates, the complete-case comparison rejected a single Gaussian in every attendance group:

| visits | N | LR, K=1 vs K=2 | bootstrap p |
| ---: | ---: | ---: | ---: |
| 0 | 4,467 | 3,356.7 | 0.005 |
| 1 | 433 | 150.2 | 0.005 |
| 2 | 209 | 79.9 | 0.005 |
| 3 | 144 | 41.1 | 0.005 |
| 4 | 84 | 32.3 | 0.005 |
| 5 | 49 | 15.9 | 0.015 |
| 6+ | 136 | 39.6 | 0.005 |

With 199 replicates, `0.005 = 1/(199+1)` is the minimum possible empirical p-value when no simulated statistic exceeds the observed one.

This establishes that one Gaussian is inadequate. It does not yet establish literal latent student classes.

### 4.2 BIC and ICL

For the complete-case outcome:

| visits | BIC preferred K | ICL preferred K |
| ---: | ---: | ---: |
| 0 | 3 | 2 |
| 1 | 2 | 1 |
| 2 | 2 | 1 |
| 3 | 3 | 1 |
| 4 | 3 | 1 |
| 5 | 2 | 2 |
| 6+ | 3 | 1 |

For the imputed primary outcome:

| visits | BIC preferred K | ICL preferred K |
| ---: | ---: | ---: |
| 0 | 3 | 2 |
| 1 | 2 | 3 |
| 2 | 2 | 3 |
| 3 | 2 | 3 |
| 4 | 2 | 3 |
| 5 | 2 | 2 |
| 6+ | 2 | 2 |

BIC therefore consistently finds that a single Gaussian is too restrictive, while ICL is much more conservative in the numeric complete-case analysis because the fitted Gaussian components often overlap substantially.

### 4.3 Two-component complete-case parameters

The estimated lower-component weights for positive attendance groups were:

`15.7%, 13.0%, 44.4%, 25.4%, 4.1%, 14.8%`

for `1,2,3,4,5,6+`, respectively.

The corresponding Ashman's D values were approximately:

`1.43, 1.95, 1.22, 1.64, 5.41, 1.41`.

Five of the six positive-frequency groups therefore had D below 2. The five-visit exception had only 49 complete cases and an estimated lower-component weight of about 4%, so it is not evidence of a stable large second population.

The weights are not monotone in visit frequency, which is one reason the mixtures must not be interpreted as a simple attendance-dose mechanism.

## 5. Why a skew-normal comparison was necessary

Rejecting a single Gaussian does not distinguish between:

- genuinely multi-component density structure; and
- one continuous but strongly asymmetric distribution.

A Gaussian mixture can approximate a skewed density by placing several symmetric Gaussian components along its tail. To test that explanation directly, a one-component skew-normal was fit to exactly the same observations and compared with:

1. one Gaussian;
2. one skew-normal;
3. a two-Gaussian mixture.

The reusable comparison reports log-likelihood, AIC, BIC, fitted skew-normal parameters, and the AIC/BIC-preferred model.

The fitted skew-normal shape parameters were strongly negative, approximately -4 to -7 in most groups. The single-component alternative was therefore allowed substantial left skew; the test was not merely Gaussian versus a nearly Gaussian skew-normal.

## 6. Skew-normal versus two-Gaussian results

Define

`Delta BIC = BIC(skew-normal K=1) - BIC(GMM K=2)`.

Positive values favour the two-Gaussian mixture; negative values favour the one-component skew-normal.

### 6.1 Numeric complete case

| visits | N | skew shape | Delta BIC | BIC preferred |
| ---: | ---: | ---: | ---: | --- |
| 0 | 4,467 | -6.07 | +1,223.3 | GMM K=2 |
| 1 | 433 | -4.11 | +20.7 | GMM K=2 |
| 2 | 209 | -4.20 | +12.8 | GMM K=2 |
| 3 | 144 | -4.08 | -4.5 | skew-normal |
| 4 | 84 | -6.43 | -6.1 | skew-normal |
| 5 | 49 | -4.22 | -2.7 | skew-normal |
| 6+ | 136 | -5.24 | -11.7 | skew-normal |

Thus the complete-case outcome contains two distinct patterns. For zero, one and two visits, even a strongly skewed one-component distribution does not absorb the multi-component signal. For three or more visits, BIC generally prefers the one-component skew-normal, although AIC is less decisive for the three- and five-visit groups.

### 6.2 Imputed primary outcome

| visits | N | skew shape | Delta BIC | BIC preferred |
| ---: | ---: | ---: | ---: | --- |
| 0 | 5,393 | -7.28 | +1,066.4 | GMM K=2 |
| 1 | 517 | -6.62 | +77.3 | GMM K=2 |
| 2 | 245 | -6.12 | +32.1 | GMM K=2 |
| 3 | 170 | -7.24 | +28.1 | GMM K=2 |
| 4 | 96 | -6.89 | +3.4 | GMM K=2 |
| 5 | 55 | -3.87 | +12.4 | GMM K=2 |
| 6+ | 151 | -5.47 | +11.4 | GMM K=2 |

For the imputed outcome, the two-Gaussian mixture has lower BIC in all seven frequency groups, and AIC also selects it in all seven groups.

This is the main result of the skew-normal specification check: simple asymmetry is not sufficient to explain the imputed density structure.

## 7. Component composition and administrative outcomes

The imputed two-component GMM was not converted into hard student labels. Instead, posterior responsibilities were summed within the observed final states PASS, numeric non-pass, BV, RT and BA.

Aggregating the positive-attendance groups, the expected component sizes sum to the 1,234 users:

- lower component: 286.9 expected students;
- higher component: 947.1 expected students.

Their soft state composition was:

| state | lower component | higher component |
| --- | ---: | ---: |
| PASS | 34.4% | 97.0% |
| numeric <7.5 | 10.1% | 1.1% |
| BV | 49.5% | 1.8% |
| RT | 5.3% | 0.2% |
| BA | 0.7% | approximately 0% |
| any administrative outcome | **55.5%** | **2.0%** |

The lower component of the imputed outcome is therefore strongly enriched in administrative outcomes, especially BV. This connects the density-shape analysis directly with the separate academic-management result in which BV, rather than RT, was the administrative code that distinguished users from non-users conditional on an adverse outcome.

This association does **not** prove that the lower component is a behavioral student type or that CMAT caused BV. It shows that the numerical representation of administrative outcomes is a major contributor to the lower-density mass in the imputed continuous outcome.

## 8. Integrated interpretation

The combined evidence supports the following interpretation.

1. The broad zero-versus-positive attendance difference persists in observed numeric failure, so the benchmark is not an artefact of adverse-outcome imputation.
2. A single Gaussian is inadequate even for the numeric complete-case distribution in every frequency group.
3. Some complete-case non-Gaussianity, especially in groups with three or more visits, can be represented parsimoniously by one strongly left-skewed distribution.
4. For zero, one and two visits, the complete-case two-Gaussian mixture remains preferred over a single skew-normal by BIC, so imputation is not the sole source of complex distributional structure.
5. For the imputed primary outcome, a two-Gaussian mixture is preferred over a single strongly skewed distribution in all seven groups.
6. The lower imputed component is strongly enriched in BV/RT/BA, with BV accounting for roughly half of its expected mass among CMAT users.
7. The difference between complete-case and imputed results is therefore consistent with administrative-outcome imputation **reinforcing or creating a clearer lower component**, while underlying numeric-grade heterogeneity remains in at least part of the sample.
8. Neither component weights nor locations follow a monotone visit-frequency sequence, so this analysis does not establish a visit-by-visit dose response.

The behavioral mechanism remains a hypothesis: students who seek CMAT support may also differ in academic monitoring, advice seeking, or use of institutional withdrawal procedures. The records do not measure that mechanism directly.

## 9. Reusable functions

The reusable implementation belongs in `main/cmat_analysis`, not in Paper 2.1 runners.

| function | role |
| --- | --- |
| `fit_univariate_gaussian_mixture` | fit a univariate Gaussian mixture with multiple EM starts |
| `gaussian_mixture_model_selection` | compare K values with likelihood, AIC, BIC, ICL, entropy and posterior classification diagnostics |
| `gaussian_mixture_component_summary` | order components by mean and report weights, means, SDs and Ashman's D |
| `gaussian_mixture_responsibilities` | return posterior membership probabilities |
| `soft_component_composition` | aggregate observed states by posterior responsibility without hard classification |
| `parametric_bootstrap_gmm_lrt` | empirical K=1 versus K=2 likelihood-ratio reference under the fitted Gaussian null |
| `skew_normal_fit_summary` | fit one skew-normal and report parameters, log-likelihood, AIC and BIC |
| `compare_univariate_shape_models` | compare Gaussian K=1, skew-normal K=1 and Gaussian-mixture K=2 on the same observations |
| `mixture_component_density` | construct weighted density components for distribution/composition figures |

The skew-normal function and the generic three-way shape comparator were promoted to `main` as part of `cmat-analysis 0.4.2`. Their synthetic tests include:

- a unimodal skew-normal sample, where allowing skewness improves over a single Gaussian;
- a clearly bimodal sample, where the two-Gaussian mixture remains preferred.

Paper-specific code retains only the grouping, outcome selection, fixed starts used as additional candidates, output filenames and publication orchestration.

## 10. Paper-specific runners and outputs

### `code/run_paper21_mixture.py`

Produces:

- tables 30--36: observed numeric-failure descriptives and fixed-effect logit results;
- tables 37--40: complete-case GMM selection, parameters, bootstrap and soft composition;
- tables 41--44: imputed-outcome GMM sensitivity;
- table 45: complete-case versus imputed component comparison;
- table 46: complete-case density source for the ridgeline;
- table 47: complete-case Gaussian/skew-normal/GMM specification comparison;
- table 48: imputed Gaussian/skew-normal/GMM specification comparison.

### `code/run_paper21_shape_check.py`

A fast controlled-data runner that executes only the Gaussian/skew-normal/GMM comparison and writes tables 47 and 48. It exists so the specification question can be checked without rerunning the 199-replicate bootstrap.

No row-level responsibilities are uploaded as artifacts.

## 11. Controlled validation provenance

### Full GMM validation

- GitHub Actions run: `35657154301`
- analysis commit: `50876b0e66f4893b4a447018be33f35bba4054e1`
- bootstrap replicates: 199 per group/specification
- artifact: `paper21-analysis-50876b0e66f4893b4a447018be33f35bba4054e1`
- artifact ID: `10666204196`
- verified outputs: tables 01--46 and figures 01--05.

### Skew-normal specification validation

- implementation commit: `5a03ab0074142613ab258c4104c354bcee51cfa9`
- fast-run commit: `dc12a547acd726a6d8289115641813c0e5723c5a`
- GitHub Actions run: `36678572075`
- conclusion: success
- artifact: `paper21-skewnormal-shape-dc12a547acd726a6d8289115641813c0e5723c5a`
- artifact ID: `11079944669`
- verified outputs: tables 47 and 48.

## 12. Interpretation guardrails

Do not write that the mixture has discovered "good students" and "bad students", or that the lower component is literally "students who will withdraw".

Do not infer that CMAT attendance causes a student to move between components.

Do not infer from the component composition that CMAT users are definitively more committed to university or more knowledgeable about withdrawal rules.

Preferred wording is that the imputed outcome contains a lower distributional component strongly enriched in administrative outcomes, especially BV, and that the contrast with the numeric complete-case specification indicates that administrative-outcome representation materially contributes to the observed bimodality.

The engagement/institutional-navigation explanation remains a mechanism compatible with the observed evidence and should remain in the Discussion rather than be presented as a directly measured result.
