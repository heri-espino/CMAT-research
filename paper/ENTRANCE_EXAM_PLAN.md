# Paper 2 — university entrance-exam integration plan

**Status:** requested from the university on 2026-09-19; data not yet received.

The requested entrance-exam data are intended to provide a genuinely pre-enrolment measure of prior academic or mathematical preparation for a **sensitivity analysis**. They are not intended to turn Paper 2 into a causal study, and they must not replace the existing period-wide CMAT exposure or instructor--period standardisation of MU grades.

## Why this matters

The strongest remaining design limitation is that students who attend CMAT may differ from students who do not attend before or during MU. Degree programme and instructor--period context do not measure prior mathematical attainment directly. A broad pre-enrolment score could test whether attendance-group estimates remain similar after adjustment for observed baseline preparation.

The optional DMU diagnostic exam already in the repository is not an acceptable substitute because participation is incomplete/selective.

## Phase A — intake and governance

When the file arrives, do not immediately merge it into the Paper 2 model. Record first:

- source/authorizing office and delivery date;
- whether the file contains direct identifiers;
- student identifier or join key;
- score fields and definitions;
- total score range;
- whether a quantitative/mathematics subscore exists;
- admission cohort/year and exam-version/form fields;
- missing-value codes;
- whether score interpretation or scaling changed across cohorts.

Raw direct identifiers must not be committed. Follow repository controlled-data and pseudonymisation rules before the data enter a reproducible workflow. If ingestion requires reusable parsing or validation logic, route that capability through the repo-admin/upstream process.

## Phase B — linkage audit before modelling

Produce aggregate diagnostics first:

1. confirm the score precedes MU and CMAT exposure;
2. report how many of the 6,627 Paper 2 students can be linked;
3. inspect coverage by academic/admission cohort;
4. inspect coverage by 0/1/2/3/4+ attendance group;
5. inspect coverage by degree programme;
6. audit score range, centre, spread, extremes, and data-quality problems;
7. determine whether admission cohorts/exam forms use comparable scales;
8. determine whether a quantitative/mathematics component exists and is comparable;
9. audit duplicate/conflicting records and document any deterministic resolution rule.

Do not set an arbitrary missingness threshold in advance. Judge usability from the missingness pattern, cohort comparability, and population retained.

## Phase C — construct the baseline measure

Preferred order:

1. a documented quantitative/mathematics component, if comparable across cohorts;
2. otherwise a documented total entrance score, if comparable;
3. if forms/scales differ, harmonise only when university documentation supports the transformation.

Do not standardise within cohort merely because it is convenient. Keep the documented source score and any transformed analysis variable separately named.

## Phase D — sensitivity model

The current Paper 2 model remains the reference analysis. Preserve:

- the same study-population definition before baseline-data missingness is applied;
- period-wide CMAT visits;
- 0/1/2/3/4+ groups;
- instructor--period standardised MU outcome;
- instructor--period fixed effects;
- degree-programme adjustment;
- the same multiplicity logic.

Add the entrance-exam measure as an observed baseline covariate and compare sample size, retained/excluded composition, attendance-group coefficients, confidence intervals, adjusted p-values, and substantive interpretation.

If baseline scores are missing for a meaningful portion of the original cohort, a complete-case baseline model must remain a sensitivity analysis rather than silently replacing the main sample.

## Phase E — optional diagnostics

Propensity-score methods may be considered only as a diagnostic/sensitivity tool if the observed baseline covariate set becomes rich enough. They do not solve unmeasured confounding and should not be introduced merely because an entrance score becomes available. A regression sensitivity with the pre-enrolment score directly addresses the current referee concern and is easier to interpret.

## Phase F — manuscript decision

After auditing and modelling:

- **broad, comparable coverage:** report the baseline-adjusted sensitivity, with compact main-text treatment and fuller aggregate diagnostics if useful;
- **usable but selective coverage:** retain it as a clearly labelled sensitivity and describe the population loss;
- **poor/non-comparable coverage:** document why the score is not used rather than forcing it into the paper.

In all cases, do not claim that entrance-exam adjustment removes self-selection or establishes a causal tutoring effect.

## Expected reproducible outputs

Do not reserve exact filenames until the incoming schema is known, but the eventual recipe should generate aggregate outputs for linkage/coverage by cohort and attendance group, score distribution, model information, exact-group pairwise estimates with baseline adjustment, and a comparison against the current estimates.

Any manuscript number must come from those canonical outputs rather than a manual calculation.

## Completion criterion

This task is complete only when another agent can reproduce the linkage audit and sensitivity model from controlled inputs, understand any harmonisation, and trace every entrance-exam claim in the manuscript to a generated aggregate output.
