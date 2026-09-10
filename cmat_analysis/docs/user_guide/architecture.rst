Architecture and scientific boundaries
======================================

The library separates input handling, cohort construction, derived measures,
statistical estimation, longitudinal/PPA analysis, visualization, and generic
reporting. This separation is methodological: a plotting function should not
silently redefine a cohort, and a cohort builder should not select a
publication-specific estimand.

Canonical namespaces
--------------------

``io`` and ``preprocessing`` prepare inputs; ``cohorts`` constructs analysis
populations; ``measures`` derives outcomes; ``statistics`` estimates summaries
and models; ``longitudinal`` and ``ppa`` represent stable higher-level research
capabilities; ``visualization`` and ``reporting`` consume analytical results.

Compatibility code
------------------

The historical ``analysis`` and ``study`` namespaces remain only where needed
for reproducibility. Import-only shims point to one canonical implementation.
New reusable functions must be added to the canonical namespace that describes
their scientific responsibility.

Scientific invariants
---------------------

Software reorganization must not silently alter passing thresholds, PPA
exposure definitions, classroom definitions, attempt/revalidation handling,
imputation, standardization, inclusion rules, estimands, confidence intervals,
or clustering. Such changes require a separate scientific review.
