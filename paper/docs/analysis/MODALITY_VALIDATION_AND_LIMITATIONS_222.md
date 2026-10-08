# Paper 2.2.2 — Validating distribution shape and limiting claims

## Why textbook tests can mislead

The numerical grade is neither unbounded nor a perfect continuous iid sample. Scores may be reported on a discrete grid with repeated ties, administrative codes are not numeric scores, and multiple students share instructor-period assessment context. Standard Gaussian-mixture EM and unimodality-test reference distributions often assume observations are independent and continuous. Z-standardisation within classroom does not automatically remove all cluster dependence, nor does imputing administrative outcomes yield a continuously measured latent grade.

An i.i.d. parametric bootstrap from the fitted K1 normal/skew-normal tests that *specific simplified null model*, not all unimodal distributions, and cannot by itself control false positives induced by dependence/rounding.

## Recommended validation sequence

1. **Measurement audit:** quantisation, repeated scores, endpoints, grade discretisation and imputation map; include descriptive plots and group-level counts without student-level disclosure.
2. **Simulation falsification:** construct synthetic one-mode grade generators with plausible rounding, truncation/bounds, class effects and administrative mass; run candidate modality procedures to estimate empirical false-positive behaviour. Use identical pipeline of standardisation and top-coding.
3. **Dependence:** evaluate cluster bootstrap of whole instructor-periods for stability of estimated mode locations/counts and run instructor-level sensitivity where useful. Cluster resampling alone does not create the null distribution of a modality test. Any *hypothesis-test* p-value must arise from a documented calibrated null that matches the tested design or be expressly conditional/illustrative.
4. **Model comparison:** nested/held-out predictive log density, BIC/ICL and flexible one-mode alternatives; report mode count of the **total density** rather than inferring from component count.
5. **Sensitivity:** numeric primary vs administrative imputation; pooled tail vs exact 6/7+; different smoothing bandwidths, latent mixture starts, outlier trimming rules fixed in advance, degree/classroom mixture composition.
6. **Multiplicity and transparency:** prespecify group family before new tests; include bootstrap Monte Carlo error, uncertainty bands, convergence failures and anomalous/sparse groups. Avoid selectively emphasizing the most dramatic group.

## Claims ladder

- **Allowed:** 'Two-component Gaussian mixture improves BIC relative to one Gaussian under the specified sample/model.'
- **Conditionally allowed:** 'The observed score distribution shows two peaks stable to bandwidth and resampling' when plots and uncertainty support it; clarify density resolution and sample.
- **Strongest, not justified by fits alone:** 'There are two natural kinds of students', 'CMAT attendance moves students between latent academic classes', 'two causal regimes', 'all groups are bimodal'.

An inconclusive result due to sparse data is a legitimate finding; do not change outcome coding or threshold to obtain significance.

## Method-specific readiness tests for an AI agent

Create simulation fixtures for one normal, one skew-normal, rounded/truncated unimodal, two separated Gaussian components, two heavily overlapping components with **one** total-density mode, an outlier-induced tiny mixture component, administrative-imputation spikes, and correlated instructor-period clusters. Verify that algorithms can distinguish *component number* from *total-density modal count* and behave honestly under ties and small samples. Require numerical consistency and a documented calibration before any inferential modality plot carries stars or p-values.