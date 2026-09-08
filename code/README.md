# Code

Canonical scientific-analysis code for the CMAT project.

## Role

This folder should contain the single scientific pipeline from which canonical aggregate outputs are generated.

## Current state

The imported code is the historical **v8** research snapshot. It contains the refined longitudinal PPA progression logic, including revalidation handling and MU-to-Calculus analyses.

A later methodology snapshot introduced additional corrections and extensions that are not yet fully reconciled into this v8 tree. Those include:

- classroom-level KDE imputation for adverse non-numeric outcomes;
- all pairwise comparisons among `0 / 1 / 2 / 3 / 4+` visits;
- 4,211-progressor sensitivity analyses;
- periodicity analyses for multiple populations;
- expanded degree-programme summaries/scatterplots.

The short-lived branch `method/reconcile-v8-v5` is reserved for merging those improvements into one canonical pipeline.

## Scientific rules

- Classroom = `instructor × course × academic period` unless a reviewed methodological change explicitly replaces it.
- Student-selected CMAT use is observational; do not use causal language without an identification design that supports it.
- Paper-specific code should not diverge from this canonical pipeline.
- Scientific code changes require tests, methodology/protocol updates, function-index updates, and a new source fingerprint.

## Data boundary

Raw administrative data and row-level linked student records remain outside GitHub. Paths/configuration may refer to controlled local inputs, but those inputs must not be committed.

## Outputs

Historical outputs currently remain under `code/outputs/` for provenance. Once the reconciled pipeline is stable, canonical privacy-reviewed aggregate outputs should be consolidated under `analysis/`.
