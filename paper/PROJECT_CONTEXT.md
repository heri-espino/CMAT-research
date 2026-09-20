# Paper 2 — CMAT attendance and MU performance

**Working title:** *Attendance at a Mathematics Support Centre and Academic Performance in First-Year University Mathematics*

**Operational status:** see `paper/STATUS_AND_ROADMAP.md`.

This directory is the canonical home for Paper 2. Shared scientific implementation remains in `cmat_analysis/`; Paper 2 owns only its publication specification, selected literature, outputs, manuscript, and submission materials.

## Research question

How is CMAT attendance during the same academic period associated with the standardised grade in a student's first eligible attempt at Matemáticas Universitarias (MU), and do standardised grades differ among students who attend once, twice, three times, or four or more times?

## Primary population

First eligible MU attempts in academic periods with observable CMAT registration coverage. The retained shared-study snapshot contains `N=6,627` students. Future-Calculus cohorts are not the Paper 2 estimand and belong primarily to Papers 1 and 5.

## Exposure

CMAT registrations occurring in the same academic period as the focal MU attempt, **irrespective of the subject label attached to an individual visit**. The primary presentation is `0 / 1 / 2 / 3 / 4+` visits so that the analysis does not hide the exact one- and two-visit groups. The historical `1–2` pooling is retained only as a secondary equivalence/parsimony sensitivity, and threshold-oriented PPA contrasts are secondary provenance analyses rather than the Paper 2 estimand.

The global historical `VISITAS` variable from `proyecto_visitas`, which accumulated registrations over the available advisory workbook, is provenance only and must not be substituted for the temporally aligned exposure.

## Primary outcome

Continuous final performance standardised within the existing instructor × academic-period grading group:

`Z = (grade - instructor-period mean) / instructor-period sample SD`.

In the code this grouping is `CLASSROOM_ID = professor × year × academic session`; because the Paper 2 cohort is MU, the course is already fixed by the study population. This grouping is substantive: instructors set and grade their own assessments, so raw grade distributions may differ across teaching contexts. The primary outcome retains adverse non-numeric academic outcomes using the canonical project rule; complete-case and alternative adverse-imputation outcomes are sensitivities.

## Baseline preparation

The available optional DMU diagnostic exam is **not used as a Paper 2 covariate or sensitivity**, because participation is incomplete/selective and does not provide a sufficiently uniform baseline across the analytic cohorts. Do not condition the main analysis on diagnostic participation.

The university entrance-exam results were requested on **2026-09-19** and are currently an external dependency. If received, they may be used as an observed-preparation sensitivity only after auditing missingness, linkage coverage, cohort/scale comparability, score meaning, and temporal ordering. Follow `paper/ENTRANCE_EXAM_PLAN.md`; receiving a score does not convert the study into a causal effect design.

## Current retained interpretation

The strongest reproducible feature is the distinction between zero visits and positive CMAT use. The exact-group controlled-data rerun is the primary reporting basis; manuscript numbers should be taken from the canonical generated exact-group outputs rather than reconstructed from older pooled summaries.

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

## Submission metadata

Current author order:

1. Heriberto Espino-Montelongo — Universidad de las Américas Puebla; ORCID `0009-0009-1230-2931`.
2. Daniela Cortés-Toto — Universidad de las Américas Puebla; email and biography are recorded in `paper/SUBMISSION_METADATA.md`; ORCID is not provided and must not be invented.

Funding: **None declared.**

Protected row-level administrative data are not planned for public release; the manuscript states that privacy and institutional data-governance restrictions prevent public release of the microdata, while code and non-disclosive aggregate or synthetic replication materials may be shared.

The major remaining submission metadata blocker is the exact institutional ethics/data-use authorization statement and identifier.

## Reproducibility

Paper-local runner: `code/run_paper.py`.

Controlled Paper 2 inputs are the pseudonymized academic and CMAT advisory records. The recipe does not use the optional DMU diagnostic file.

Primary publication outputs are generated under `results/tables/` and `results/figures/`. Tables `30`–`34` define the main exact-group analysis; table `37` and table `38` contain current outcome/small-group sensitivities; the current referee-oriented recipe additionally generates tables `39`–`42` and `49`–`50`; tables `80+` retain secondary/provenance analyses. See `paper/STATUS_AND_ROADMAP.md` for which outputs have been scientifically reviewed versus merely implemented.
