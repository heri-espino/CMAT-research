Mixture models and skew-normal specification checks
=================================================

Purpose
-------

Finite mixtures are useful when a continuous outcome has more structure than a
single symmetric Gaussian can represent. A second Gaussian component can,
however, approximate a genuinely multimodal density, ordinary skewness, heavy
tails, or structure introduced by outcome construction. The reusable API
therefore separates density fitting from substantive interpretation.

Recommended hierarchy
---------------------

For a one-dimensional outcome:

1. fit a one-component Gaussian as the symmetric benchmark;
2. fit a one-component skew-normal to test whether ordinary asymmetry is enough;
3. fit Gaussian mixtures with candidate component counts, normally K=1, 2, 3,
   using multiple EM starts;
4. compare log-likelihood, AIC and BIC on the same observations, and inspect ICL
   and posterior entropy when component separability matters;
5. use :func:`cmat_analysis.statistics.parametric_bootstrap_gmm_lrt` for the
   Gaussian K=1 versus K=2 comparison instead of an ordinary chi-square test;
6. inspect component weights, locations, scales, Ashman's D and posterior
   responsibilities;
7. when both observed and imputed outcomes exist, analyse the observed outcome
   first and treat the imputed version as a sensitivity.

Gaussian-mixture tools
----------------------

:func:`cmat_analysis.statistics.fit_univariate_gaussian_mixture` uses
expectation-maximization with multiple starts. Scientifically motivated means
should be additional starts rather than the unique initialization.

:func:`cmat_analysis.statistics.gaussian_mixture_model_selection` reports
log-likelihood, AIC, BIC, ICL, posterior entropy, mean maximum responsibility,
convergence status and iteration count.

:func:`cmat_analysis.statistics.gaussian_mixture_component_summary` orders a
two-component model by mean and reports weights, means, standard deviations and
Ashman's D. The labels lower_performance and higher_performance are ordering
labels, not identified psychological or causal student types.

Posterior responsibilities
--------------------------

Use :func:`cmat_analysis.statistics.gaussian_mixture_responsibilities` to
retain uncertainty in component membership, and
:func:`cmat_analysis.statistics.soft_component_composition` to aggregate
observed categorical states by posterior probability rather than hard
classification.

A difference in soft composition shows association between a density component
and an observed state; it does not establish that the state caused the
component or that the component is a natural class.

Parametric bootstrap
--------------------

Adding a mixture component violates the regularity conditions behind the usual
chi-square likelihood-ratio reference distribution. The reusable
:func:`cmat_analysis.statistics.parametric_bootstrap_gmm_lrt` fits the null
and alternative, simulates datasets from the fitted one-component null, refits
both models, and returns an empirical p-value.

With B replicates and zero simulated statistics at least as large as the
observed statistic, the minimum reported p-value is 1/(B+1); with 199
replicates it is 0.005.

Skew-normal comparator
----------------------

:func:`cmat_analysis.statistics.skew_normal_fit_summary` fits a single
skew-normal distribution and returns shape, location, scale, log-likelihood,
AIC and BIC.

If the skew-normal matches or beats the two-Gaussian mixture, ordinary asymmetry
can explain the apparent mixture parsimoniously. If the two-Gaussian mixture
remains materially preferred, simple skewness is not sufficient to explain the
density shape. That result is stronger evidence for distributional
heterogeneity than rejecting a single Gaussian alone, but it still does not
prove literal latent populations.

Example
-------

.. code-block:: python

   from cmat_analysis.statistics import (
       gaussian_mixture_component_summary,
       gaussian_mixture_model_selection,
       gaussian_mixture_responsibilities,
       parametric_bootstrap_gmm_lrt,
       skew_normal_fit_summary,
   )

   selection, models = gaussian_mixture_model_selection(
       z,
       component_counts=(1, 2, 3),
       random_state=42,
       n_init=30,
       two_component_mean_starts=((-1.1, 0.5),),
   )
   skew = skew_normal_fit_summary(z)
   components = gaussian_mixture_component_summary(models[2])
   responsibilities = gaussian_mixture_responsibilities(models[2], z)
   bootstrap = parametric_bootstrap_gmm_lrt(
       z,
       n_bootstrap=199,
       random_state=42,
       n_init=20,
       two_component_mean_starts=((-1.1, 0.5),),
   )

Interpretation boundaries
-------------------------

When an imputation rule maps administrative outcomes into the lower tail,
compare mixture structure with a numeric complete-case outcome. Stronger
multi-component preference only after imputation indicates that outcome
construction contributes materially to the apparent mixture. Persistence in
the complete-case outcome shows that imputation is not the sole source of
non-Gaussian structure.

Mixture membership alone must not be used to infer motivation, engagement,
effort, treatment response, or a causal transition between student types.
