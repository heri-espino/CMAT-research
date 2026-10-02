# Paper 2.1 — mixture, skew-normal, and administrative-outcome analysis

**Status:** controlled-data results verified; reusable estimators upstreamed to `main`; manuscript interpretation updated to distinguish observed density structure from the proposed academic-management mechanism.

## Tail-resolution rerun: exact 6 versus 7+

The exploratory visit-frequency analysis resolves the former `6+` category into exact `6` and `7+`, while the primary inferential specification remains `0/1/2/3/4/5/6+`. The full EM/GMM and skew-normal diagnostic family was re-estimated from the original observations for the two tail groups; the old pooled `6+` posterior assignments were not partitioned after fitting.

### Numeric complete case

Exact six visits contain 43 numeric complete cases. The two-Gaussian fit improves strongly over one Gaussian, but comparison with a flexible one-component skew-normal does not support a stable two-component interpretation: `Delta BIC = -2.36` favours the skew-normal, the skew-normal-null bootstrap gives `p=0.11`, and repeated cross-validation gives a mean GMM-minus-skew held-out log-density difference of `-0.037`.

The `7+` group contains 93 numeric complete cases. BIC favours the two-Gaussian fit over the skew-normal by `+7.34` and the skew-normal-null bootstrap gives `p=0.02`, but the fitted lower component has weight only `1.08%`, mean `Z=-2.86` and SD fixed at the numerical floor `0.001`. The mean held-out log-density difference favours the GMM (`+0.530`), yet it wins only 38% of fold evaluations and fold variability is very large. The apparent lower component is therefore best treated as an extreme-observation/tail diagnostic rather than evidence of a stable lower-performance population.

### Imputed outcome

For exact six visits (`N=50`), BIC slightly favours the skew-normal (`Delta BIC=-2.17`) and the skew-normal-null bootstrap is non-significant (`p=0.12`), whereas repeated cross-validation favours the GMM on average (`+0.321`) and in 70% of folds. This specification is diagnostically mixed. The fitted imputed lower-component weight is 25.2%.

For `7+` (`N=101`), the evidence is more coherent: `Delta BIC=+4.56`, skew-normal-null bootstrap `p=0.02`, positive mean held-out difference `+0.125`, and a 66% GMM fold-win share. The fitted lower-component weight is 14.3%.

The split-tail rerun therefore adds descriptive resolution but does not reveal a monotone distributional transition at six or seven visits. It reinforces the decision to keep `6+` as the primary inference group while using exact `6` and `7+` as a sensitivity. Outputs 53--68 and figures 08--09 contain the full diagnostics.

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

BIC alone is not treated as the final answer because the skew-normal and GMM are non-nested density specifications. Two additional diagnostics were therefore run for every attendance group: a parametric bootstrap generated under the fitted skew-normal null, using the observed BIC advantage of GMM K=2 as the statistic, and repeated held-out log predictive density.

### 6.3 Direct skew-normal-null bootstrap and cross-validation: numeric complete case

The fast controlled-data validation used 99 bootstrap replicates and repeated five-fold cross-validation with five repeats. The canonical runner uses the same estimand with more intensive settings.

| visits | Delta BIC | bootstrap p | mean held-out log-density difference, GMM minus skew | GMM fold win share | interpretation |
| ---: | ---: | ---: | ---: | ---: | --- |
| 0 | +1,223.3 | 0.01 | +0.139 | 1.00 | GMM supported |
| 1 | +20.7 | 0.01 | +0.033 | 0.80 | GMM supported |
| 2 | +12.8 | 0.01 | +0.048 | 0.80 | GMM supported |
| 3 | -4.5 | 0.12 | -0.013 | 0.28 | skew-normal adequate |
| 4 | -6.1 | 0.22 | -0.084 | 0.44 | skew-normal adequate |
| 5 | -2.7 | 0.22 | +0.110 | 0.44 | inconclusive; small N |
| 6+ | -11.7 | 0.62 | -0.014 | 0.16 | skew-normal adequate |

The five-visit group deserves caution. Its average held-out log-density difference is positive, but the GMM wins only 11 of 25 folds and the fold-to-fold standard deviation is much larger than in the lower-frequency groups. With only 49 numeric complete cases, this is not robust evidence for a stable second component.

The complete-case result therefore divides naturally into three categories: zero, one and two visits show concordant evidence that one skewed distribution is insufficient; three, four and 6+ visits are adequately represented by one strongly left-skewed distribution; and five visits remain unresolved because the sample is small and the diagnostics disagree.

### 6.4 Direct skew-normal-null bootstrap and cross-validation: imputed outcome

| visits | Delta BIC | bootstrap p | mean held-out log-density difference, GMM minus skew | GMM fold win share |
| ---: | ---: | ---: | ---: | ---: |
| 0 | +1,066.4 | 0.01 | +0.100 | 1.00 |
| 1 | +77.3 | 0.01 | +0.082 | 0.96 |
| 2 | +32.1 | 0.01 | +0.088 | 0.84 |
| 3 | +28.1 | 0.01 | +0.136 | 0.96 |
| 4 | +3.4 | 0.01 | +0.045 | 0.72 |
| 5 | +12.4 | 0.01 | +0.349 | 0.80 |
| 6+ | +11.4 | 0.01 | +0.109 | 0.84 |

No bootstrap replicate in the fast validation produced a BIC advantage at least as large as the observed value in any imputed-outcome group, so 0.01 is the minimum possible empirical p-value with 99 replicates. The held-out comparison also favoured the GMM on average in every group and in a majority of folds for every group.

This agreement across penalised in-sample fit, simulation from a strongly skewed one-component null and out-of-sample prediction is the main result of the direct specification check: simple asymmetry is not sufficient to explain the imputed density structure.

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
2. A single Gaussian is inadequate even for the numeric complete-case distribution in every frequency group, but this alone does not distinguish multimodality from ordinary skewness.
3. For zero, one and two visits, BIC, the skew-normal-null bootstrap and held-out prediction agree that the complete-case density requires more than one skewed component.
4. For three, four and 6+ visits, the complete-case diagnostics are compatible with one strongly left-skewed distribution; the five-visit group is inconclusive because N is small and the diagnostics disagree.
5. For the imputed primary outcome, the two-Gaussian mixture is favoured over a single strongly skewed distribution in all seven groups by BIC, the skew-normal-null bootstrap and mean held-out predictive density.
6. The lower imputed component is strongly enriched in BV/RT/BA, with BV accounting for roughly half of its expected mass among CMAT users.
7. The difference between complete-case and imputed results is therefore consistent with administrative-outcome imputation **sharpening a lower component**, while underlying numeric-grade heterogeneity remains especially clear at zero, one and two visits.
8. Neither component weights nor locations follow a monotone visit-frequency sequence, so this analysis does not establish a visit-by-visit dose response or literal latent student classes.

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
| `parametric_bootstrap_skew_normal_vs_gmm` | test whether the observed GMM BIC advantage is unusually large under a fitted skew-normal null |
| `cross_validated_skew_normal_vs_gmm` | compare skew-normal and GMM K=2 by repeated held-out log predictive density |
| `mixture_component_density` | construct weighted density components for distribution/composition figures |

The skew-normal and direct skew-normal-versus-GMM diagnostics were promoted to `main` as part of `cmat-analysis 0.4.3`. Their synthetic tests include:

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
- table 48: imputed Gaussian/skew-normal/GMM specification comparison;
- table 49: complete-case skew-normal-null parametric bootstrap versus GMM K=2;
- table 50: complete-case repeated cross-validated predictive comparison;
- table 51: imputed skew-normal-null parametric bootstrap versus GMM K=2;
- table 52: imputed repeated cross-validated predictive comparison.

### `code/run_paper21_shape_check.py`

A focused controlled-data runner that executes the Gaussian/skew-normal/GMM comparison, the skew-normal-null bootstrap and repeated cross-validation, writing tables 47--52. It exists so the specification question can be checked without rerunning the complete Paper 2.1 analysis.

No row-level responsibilities are uploaded as artifacts.

## 11. Controlled validation provenance

### Full GMM validation

- GitHub Actions run: `35657154301`
- analysis commit: `50876b0e66f4893b4a447018be33f35bba4054e1`
- bootstrap replicates: 199 per group/specification
- artifact: `paper21-analysis-50876b0e66f4893b4a447018be33f35bba4054e1`
- artifact ID: `10666204196`
- verified outputs: tables 01--46 and figures 01--05.

### Current integrated validation

After promoting the reusable shape comparison to `main/cmat_analysis` and making the Paper 2.1 runners downstream consumers, the complete recipe was run again on the current branch code:

- GitHub Actions run: `36685329947`
- branch head: `93b16efb40efd7ed6803ab50568bc5fb075a10b9`
- conclusion: success
- bootstrap replicates: 199 per GMM group/specification
- artifact: `paper21-analysis-93b16efb40efd7ed6803ab50568bc5fb075a10b9`
- artifact ID: `11084615356`
- verified outputs: tables 01--48 and figures 01--05.

This is the canonical validation for the integrated implementation. The earlier full GMM and fast shape-check runs below remain useful provenance because they isolate the two development stages that produced the final workflow.

### Direct skew-normal-null and predictive validation

- GitHub Actions run: `36826363767`
- branch head: `50f6e568aa38f3b9ec99be4b08124c72a1e989b8`
- conclusion: success
- skew-normal-null bootstrap: 99 replicates per group/specification
- predictive diagnostic: repeated 5-fold CV with 5 repeats
- artifact: `paper21-shape-validation-50f6e568aa38f3b9ec99be4b08124c72a1e989b8`
- artifact ID: `11145891079`
- verified outputs: tables 47--52.
- note: this focused workflow is the rapid specification validation; the integrated runner uses more intensive bootstrap/CV settings.

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
