# Paper 2.2.2 — Research context: mixture components versus modes

## From Paper 2 to Paper 2.1

Paper 2 provides an observational comparison between zero and positive CMAT use, and Paper 2.1 profiles multiple attendance frequencies and final outcomes. Paper 2.1's exploratory distributional extension fitted GMMs for observed numeric complete-case grades and imputed adverse-outcome Z scores. Under some specifications, two-component Gaussian mixtures fit much better than single Gaussian or skew-normal alternatives; the pattern is sensitive to outcome definition, especially treatment of BV/RT/BA. The historical details are in `paper/docs/results/MIXTURE_ANALYSIS_RESULTS.md`.

This inspires — but does not answer — a sharper scientific question. A GMM with two components can produce **one peak**; conversely two peaks can be modelled without two true student classes. The grade scale is bounded and rounded, and administrative imputation may introduce an artificial accumulation of low values.

## Separate hypotheses

1. **Fit complexity:** does K=2 approximate the observed density better than a one-component Gaussian?
2. **Unimodal adequacy:** could a single unimodal asymmetric / bounded / discretised outcome model explain the data?
3. **Modal structure:** does the *population density* have two or more separated local maxima, after smoothing resolution and uncertainty?
4. **Latent subpopulations:** is there independent evidence for distinct generating populations rather than flexible density approximation? This fourth claim generally cannot be proven solely from marginal grade histograms.

## Primary estimand and datasets

Primary: shape and mode count of the numeric complete-case, instructor-period-standardised Z distribution **within each supported attendance-frequency group**. Sensitivity: adverse-outcome-imputed `Z_GRADE_PRIMARY`, explicitly recognising that this mixes a numeric support scale with administrative outcome coding. Inspect pooled 6+ versus exact 6/7+ due sparse support. Compare also full-sample distributions where scientifically meaningful but do not conflate cross-group mixtures with within-group mixture components.

Descriptive interpretation is conditional on observed selection into numeric grades and visits; results do not identify causal support effects or naturally occurring student kinds.

## What result would count as progress?

A reproducible report showing whether apparent multiple components correspond to separated modes **after** tie/boundary/cluster-aware sensitivity, numerical regularisation and held-out fit checks — including the possibility of a credible negative result (a single skewed/heaped distribution explains the data). A defensible non-bimodality conclusion would be informative and publishable only if positioned against a meaningful literature gap.

## Literature gaps for next agent

Find and assess literature on mixture testing nonregularity, selection of components (BIC/ICL), modality testing with ties and bounded/rounded outcomes, cluster bootstrap validity, skew-normal and flexible unimodal alternatives, mixture interpretability and higher-education mathematics-support outcome measurement. Do not claim an uncited method is validated for heaped grade scales.