# Active branch: method/reconcile-v8-v5

This is a short-lived feature branch created from the current `main`.

## Concrete task

Reconcile the historical v8 longitudinal pipeline with the later methodology corrections while preserving all validated functionality.

## Planned changes

- classroom-level KDE imputation for BV/RT/BA;
- all pairwise `0 / 1 / 2 / 3 / 4+` visit comparisons;
- 4,211-progressor sensitivity while preserving the 6,627-MU estimand;
- population-specific periodicity analyses;
- expanded degree-programme analyses;
- preservation of refined PPA longitudinal/revalidation logic from v8.

## Not part of this branch

- manuscript rewriting;
- literature reorganization;
- privacy-policy changes;
- raw-data migration;
- deletion of historical outputs.

## Merge criteria

- no lost v8 functionality;
- tests pass;
- protocol/changelog/function index/handoff updated;
- canonical outputs regenerate consistently;
- new scientific source fingerprint recorded;
- PR documents any changed numerical results or interpretations.

After merge, this branch should be deleted. The next task starts from the new `main`.
