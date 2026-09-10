# Paper 2 — CMAT use and classroom-relative MU performance

**Working title:** *Mathematics Support Use and Classroom-Relative Performance in First-Year University Mathematics*

This directory is the canonical home for Paper 2. Shared scientific implementation remains in `cmat_analysis/`; Paper 2 owns only its publication specification, selected literature, outputs, manuscript, and submission materials.

## Research question

How is contemporaneous CMAT use associated with classroom-relative academic performance in a student's first eligible attempt at Matemáticas Universitarias (MU), and is the observed pattern better described as a separation between non-use and positive use or as a monotone dose-response among users?

## Primary population

First eligible MU attempts in academic periods with observable CMAT registration coverage. The retained shared-study snapshot contains `N=6,627` students. Future-Calculus cohorts are not the Paper 2 estimand and belong primarily to Papers 1 and 5.

## Exposure

CMAT registrations occurring in the same academic period as the focal MU attempt. The principal presentation uses `0 / 1–2 / 3 / 4+` visits. Exact 1 versus 2 visits are retained as a pooling diagnostic, and threshold contrasts are secondary historical sensitivities.

The global historical `VISITAS` variable from `proyecto_visitas`, which accumulated registrations over the available advisory workbook, is provenance only and must not be substituted for the temporally aligned exposure.

## Primary outcome

Continuous final performance standardised within classroom:

`Z = (grade - classroom mean) / classroom sample SD`,

where classroom is professor × course × academic period. The primary outcome retains adverse non-numeric academic outcomes using the canonical project rule; complete-case and alternative adverse-imputation outcomes are sensitivities.

## Current retained interpretation

The strongest reproducible feature is the distinction between zero visits and positive CMAT use. In the retained first-MU snapshot, means are approximately `-0.060 / 0.218 / 0.325 / 0.342` for `0 / 1–2 / 3 / 4+`, respectively. Games–Howell comparisons distinguish each positive-use group from zero but do not distinguish the positive-use groups from one another at the 5% level. Classroom fixed-effect group contrasts relative to zero are positive for all three positive-use categories.

This is an observational association. Do not write that CMAT attendance causes improvement or that visit count is a causal dose.

## Historical decomposition

`paper/DECOMPOSITION_FROM_PROYECTO_VISITAS.md` is the binding map for reusing the old `brainstorm/proyecto_visitas` work:

- student support use and student performance → Paper 2;
- professor grade distributions, grading profiles, clustering, and stability → Paper 3;
- general service-load/report artifacts → remain brainstorm/provenance unless later justified.

## Journal strategy

1. *Teaching Mathematics and its Applications* (TEAMAT) — primary target.
2. *International Journal of Mathematical Education in Science and Technology* (IJMEST) — second choice.
3. *International Journal of Research in Undergraduate Mathematics Education* (IJRUME) — ambitious option if the mathematics-education contribution is strengthened.

## Reproducibility

Paper-local runner: `code/run_paper.py`.

Retained aggregate checkpoint: `brainstorm/shared/historical_outputs/study/tables/`.

Before submission, run the controlled-data recipe with `--compare-retained` and reconcile any discrepancy with later methodology-restoration snapshots before changing manuscript numbers.
