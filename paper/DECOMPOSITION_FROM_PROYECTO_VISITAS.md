# Paper 2 decomposition from `proyecto_visitas`

This document records how the historical `proyecto_visitas` work is decomposed into the current publication portfolio. The historical source is preserved on branch `brainstorm/proyecto-visitas` under `brainstorm/proyecto_visitas/`; Paper 2 does not copy that subtree or treat its original analysis choices as canonical.

## Scientific boundary

Paper 2 asks how contemporaneous CMAT use is associated with classroom-relative academic performance in a student's first eligible attempt at Matemáticas Universitarias (MU). Paper 3 owns the distinct question of grading heterogeneity across instructors/classrooms, including professor-specific grade distributions, clustering of grading profiles, temporal stability of those profiles, and implications for grade comparability.

The decomposition is therefore conceptual rather than a file split:

| Historical `proyecto_visitas` material | Destination | Rule |
|---|---|---|
| Student use of CMAT, visit-count distributions, users versus non-users | Paper 2 | Retain as motivation and descriptive precedent, but recompute with course-period-aligned exposure. |
| Association between CMAT use/intensity and student grades | Paper 2 | Re-estimate on first-attempt MU with the canonical classroom-relative outcome. |
| Robustness to non-numeric/adverse grade outcomes | Paper 2 | Use the current `cmat_analysis.measures` outcome definitions and retained sensitivities. |
| Professor grade distributions and pass-rate profiles | Paper 3 | Do not use as a Paper 2 result except to motivate within-classroom standardisation. |
| Professor/instructor clusters and relationships among grading features | Paper 3 | Entirely outside Paper 2's empirical contribution. |
| Stability of instructor grading regimes across terms | Paper 3 | Entirely outside Paper 2's empirical contribution. |
| Service-load descriptions, most-frequent visitors, historical dashboard/report assets | `brainstorm/` only | Keep as provenance unless a later publication question requires them. |

## Historical exposure is not the Paper 2 exposure

The old report defined `VISITAS` as a student's total advisory registrations across the full advisory workbook and merged that total back onto each cleaned academic observation. That construction was useful for the original exploratory report but does not establish that a visit occurred during the course/term whose grade is being analysed.

Paper 2 therefore uses the current canonical temporal reconstruction:

- population: first eligible MU attempt;
- coverage: only academic periods with CMAT advisory-record coverage;
- exposure: CMAT registrations during the same academic period as that MU attempt;
- primary grouping: `0`, `1–2`, `3`, `4+` visits, with exact `1` versus `2` diagnostics retained to justify pooling;
- primary outcome: final performance standardised within classroom, where classroom is professor × course × academic period.

Consequently, old global counts such as 10,413 cleaned students, 26,140 student-classroom observations, or the old 28.1% any-visit rate are historical descriptive quantities and must not be reported as Paper 2 sample statistics. The retained current Paper 2 snapshot has 6,627 first-MU students with advisory coverage, of whom 18.6% have at least one same-period CMAT registration.

## Empirical story retained for Paper 2

The historical work suggested that students who used CMAT tended to have different academic outcomes from non-users. The current analysis sharpens that observation rather than claiming a causal tutoring effect. In the retained first-MU snapshot, classroom-relative mean performance is approximately -0.060 for zero visits, 0.218 for 1–2 visits, 0.325 for exactly 3 visits, and 0.342 for 4+ visits. Multiplicity-aware Games–Howell comparisons separate each positive-use group from zero visits, whereas contrasts among positive-use groups do not reach the same threshold of evidence. Classroom fixed-effect dose-group models likewise estimate positive contrasts for each positive-use category relative to zero.

The publication claim should therefore distinguish two empirical questions:

1. **use versus non-use:** a substantial positive association between observed formal help-seeking and classroom-relative performance;
2. **dose among users:** no robust evidence in the retained snapshot for a simple monotone ordering across positive-use groups.

Neither pattern identifies a causal effect because baseline mathematics proficiency, motivation, perceived difficulty, study effort, and other determinants of both help-seeking and performance are not fully observed.

## Retained evidence and provenance

Paper 2's current numerical draft is traced to `brainstorm/shared/historical_outputs/study/tables/`, especially:

- `01_cohort_flow.csv`;
- `02_visit_distribution_mu_vs_calculus.csv`;
- `10_primary_outcome_by_visit_group.csv`;
- `11_primary_robust_gt3_vs_le3.csv`;
- `12_primary_fixed_effect_models.csv`;
- `13_primary_dose_group_model.csv`;
- `14_continuous_outcome_sensitivity.csv`;
- `80_justify_pooling_exact_1_vs_2.csv`;
- `81_visit_groups_welch_anova.csv`;
- `82_visit_groups_welch_summary.csv`;
- `83_visit_groups_games_howell.csv`.

These retained tables are a reproducibility checkpoint, not a substitute for rerunning the paper from controlled institutional inputs before submission.

## Snapshot reconciliation item

A later methodology-restoration workspace contains some exact-dose summaries that are not numerically identical to the retained shared-study tables above. Paper 2 must not mix the two snapshots. The current draft uses `brainstorm/shared/historical_outputs/study/` consistently; before submission, the branch runner should be executed on the controlled inputs and any discrepancy between retained snapshots should be reconciled explicitly rather than silently selecting preferred numbers.

## What Paper 2 deliberately does not claim

Paper 2 does not claim that students "improve because they go to CMAT," because there is no randomized assignment and the current outcome is not a pre/post change score. Its defensible question is whether contemporaneous formal mathematics-support use is associated with higher performance relative to peers evaluated in the same classroom context, while quantifying how much of the observed pattern is concentrated in the distinction between non-use and positive use.
