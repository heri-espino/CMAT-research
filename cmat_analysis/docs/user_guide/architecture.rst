Architecture and scientific boundaries
======================================

The library separates input handling, cohort construction, derived measures,
statistical estimation, longitudinal/PPA analysis, visualization, and generic
reporting. This separation is methodological: a plotting function should not
silently redefine a cohort, and a cohort builder should not select a
publication-specific estimand.

Canonical namespaces
--------------------

io and preprocessing prepare inputs; cohorts constructs analysis populations;
measures derives outcomes; statistics estimates summaries and models;
longitudinal and ppa represent stable higher-level research capabilities;
visualization and reporting consume analytical results.

Reusable education-research methods belong in these canonical namespaces even
when they originate in a specific paper. Paper-specific orchestration, labels,
tables, figure captions, and manuscript decisions remain downstream.

Compatibility code
------------------

The historical analysis and study namespaces remain only where needed for
reproducibility. New reusable functions must be added to the canonical namespace
that describes their scientific responsibility.

Scientific invariants
---------------------

Software reorganization must not silently alter passing thresholds, exposure
definitions, classroom definitions, attempt/revalidation handling, imputation,
standardization, inclusion rules, estimands, confidence intervals, or
clustering. Such changes require separate scientific review.

Outcome-blind exposure design
-----------------------------

When an attendance-frequency grouping is chosen from observed support, the
support audit must be separable from academic outcomes. Reusable functions may
report student counts, cluster overlap, and tail support, but should not choose a
top-code from grade means or significance tests. The grouping decision belongs
to the study design and should be documented before outcome comparisons.

Downstream paper branches
-------------------------

Long-lived paper branches should consume reviewed functions from cmat_analysis
rather than maintain parallel implementations. A reusable method discovered in a
paper should be upstreamed to main, tested and documented here, and only then
consumed by downstream paper runners.
