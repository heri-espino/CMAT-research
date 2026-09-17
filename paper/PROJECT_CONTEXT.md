# Paper 2 — CMAT use and classroom-relative MU performance

**Working title:** *Mathematics Support Use and Classroom-Relative Performance in First-Year University Mathematics*

This directory is the canonical home for Paper 2. Shared scientific implementation remains in `cmat_analysis/`; Paper 2 owns only its publication specification, selected literature, outputs, manuscript, and submission materials.

## Research question

How is contemporaneous CMAT use associated with classroom-relative academic performance in a student's first eligible attempt at Matemáticas Universitarias (MU), and is the observed pattern better described as a separation between non-use and positive use or as a monotone dose-response among users?

## Primary population

First eligible MU attempts in academic periods with observable CMAT registration coverage. The retained shared-study snapshot contains `N=6,627` students. Future-Calculus cohorts are not the Paper 2 estimand and belong primarily to Papers 1 and 5.

## Exposure

CMAT registrations occurring in the same academic period as the focal MU attempt. The **primary presentation is `0 / 1 / 2 / 3 / 4+` visits** so that the analysis does not hide the exact one- and two-visit groups. The historical `1–2` pooling is retained only as a secondary equivalence/parsimony sensitivity, and threshold-oriented PPA contrasts are secondary provenance analyses rather than the Paper 2 estimand.

The global historical `VISITAS` variable from `proyecto_visitas`, which accumulated registrations over the available advisory workbook, is provenance only and must not be substituted for the temporally aligned exposure.

## Primary outcome

Continuous final performance standardised within classroom:

`Z = (grade - classroom mean) / classroom sample SD`,

where classroom is professor × course × academic period. The primary outcome retains adverse non-numeric academic outcomes using the canonical project rule; complete-case and alternative adverse-imputation outcomes are sensitivities.

## Baseline preparation

The available optional DMU diagnostic exam is **not used as a Paper 2 covariate or sensitivity**, because participation is incomplete/selective and does not provide a sufficiently uniform baseline across the analytic cohorts. Do not condition the main analysis on diagnostic participation.

A potentially useful future improvement is to request a genuinely pre-enrolment university entrance-exam score, provided that its coverage and scale are sufficiently comparable across cohorts. If obtained, it may be used as an observed-preparation sensitivity after auditing missingness, cohort coverage, scale comparability, and temporal ordering. It would not convert the study into a causal effect design.

## Current retained interpretation

The strongest reproducible feature is the distinction between zero visits and positive CMAT use. The exact-group controlled-data rerun is now the primary reporting basis; manuscript numbers should be taken from the current `30`–`34` exact-group tables rather than reconstructed from the older pooled `1–2` summary.

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

For TEAMAT, follow `paper/AI_HANDOFF.md`: use the official IMA template, Harvard author–year references, exact visit groups in the main presentation, minimal PPA framing, and a real research-ethics statement before submission.

## Reproducibility

Paper-local runner: `code/run_paper.py`.

Controlled Paper 2 inputs are the pseudonymized academic and CMAT advisory records. The recipe does not use the optional DMU diagnostic file.

Primary publication outputs are generated under `results/tables/` and `results/figures/`; tables `30`–`34` define the exact-group analysis, while the `80+` tables retain secondary/provenance analyses.
