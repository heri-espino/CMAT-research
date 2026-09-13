# Paper 1 — incentive-linked support use and persistence

**Working title:** *Beyond the Incentive Threshold: Academic Support Use and Persistence After a First-Year Participation Incentive*

Canonical portfolio: `../../docs/PUBLICATION_PORTFOLIO.md`.

This branch is the canonical publication workspace for Paper 1. Reusable cohort definitions and estimators live in `cmat_analysis`; `code/run_paper.py` is a thin paper-specific recipe that imports the shared library and writes only aggregate publication outputs.

## Current empirical framing

Paper 1 studies whether formal mathematics-support use persists across contexts and whether two observational channels are associated with later CMAT uptake:

1. **Prior CMAT familiarity/use history.** MU-period registrations are classified as `0 / 1–2 / exactly 3 / 4+`; exactly three remains institutionally salient because it corresponds to the historical PPA participation threshold, while `4+` distinguishes use beyond that threshold.
2. **Instructor-linked support context.** Instructors routinely recommend CMAT as a tutoring resource, but the administrative data do not observe recommendation intensity. The empirical variable is therefore instructor-linked uptake/implementation, measured either through instructor fixed effects or through the instructor's CMAT-use rate in other academic periods.

Neither channel is randomized. Prior use can reflect stable help-seeking propensity, perceived difficulty, motivation and other student selection, while instructor assignment and instructor-linked uptake can reflect student composition, scheduling, pedagogy and other instructor-associated factors. The analysis estimates persistence and implementation-linked associations, not causal encouragement effects.

## Research questions

The current controlled-data analysis asks:

1. How strongly does the distribution of initial MU-period CMAT use (`0 / 1–2 / 3 / 4+`) vary across instructors after accounting for academic period and degree programme?
2. Does prior MU-period use predict any CMAT use in the subsequent eligible Calculus period after controlling for prior MU performance, degree programme, academic period and the current Calculus instructor?
3. Is later CMAT use also associated with the current instructor's historical uptake context, estimated from the same instructor's students in other academic periods?
4. Do prior familiarity and instructor-linked uptake appear to substitute for or complement one another descriptively?

## Outcomes and exposures

The primary later outcome is any CMAT use during the strict next-regular-term eligible Calculus I period.

The primary familiarity exposure is MU-period visit group: `0 / 1–2 / exactly 3 / 4+`.

For instructor-linked implementation, the primary descriptive measures are instructor fixed effects and a leave-period-out instructor uptake rate. The latter excludes the focal academic period, requires at least 30 students from other periods, and is standardized across the included student sample.

## Core populations

The current controlled rerun uses three related populations:

- **Initial MU uptake baseline:** `N=4,906`, 53 MU instructors. This cohort is constructed before conditioning on later Calculus progression, so the instructor-to-initial-uptake analysis does not select only students who later progress.
- **Primary persistence cohort:** `N=3,241`, 48 Calculus instructors, linking MU to the subsequent eligible next-regular-term Calculus attempt.
- **All-subsequent sensitivity cohort:** `N=3,389`, retaining later eligible Calculus attempts beyond the strict next-regular-term definition.

The historical `N=4,211` broad progressor snapshot remains provenance rather than the canonical current controlled rerun and should not be mixed with the current estimates.

## Controlled-data results added in September 2026

Instructor identity is strongly associated with the complete initial MU visit-group distribution. In the `N=4,906` baseline, adding 53 instructor fixed effects to period and degree-programme controls raises McFadden's pseudo-R² from 0.0617 to 0.1237; the joint multinomial likelihood-ratio test is `LR=426.83`, `df=156`, `p=4.97e-27`. For the simpler outcome of any MU-period use, adding instructor fixed effects raises R² from 0.0649 to 0.1216 (`partial R²=0.0606`, joint `p=4.31e-37`).

The instructor distribution is substantively heterogeneous. Among the 42 MU instructors with at least 30 eligible students, the median share in the zero-use group is 80.4%, while the 10th and 90th percentiles are 65.3% and 89.5%. For exact-three use, the corresponding shares are 0.6%, 2.5% and 6.1%; for `4+`, they are 1.0%, 4.4% and 9.4%.

Current Calculus instructor context is also associated with later CMAT use. In the primary persistence cohort, adding Calculus instructor fixed effects to period and degree-programme controls raises R² from 0.0674 to 0.1211 (`partial R²=0.0575`, joint `p=7.38e-19`).

Prior use remains strongly associated with later use after controlling for the current Calculus instructor. Relative to students with zero MU-period visits, the fully adjusted risk differences are +23.7 percentage points for `1–2`, +32.5 points for exactly `3`, and +47.8 points for `4+`; the joint prior-group test has `p=4.69e-113`. The all-subsequent sensitivity gives similar estimates of +22.9, +31.9 and +46.8 points.

The joint descriptive model uses the current Calculus instructor's leave-period-out uptake propensity and is estimated on 2,447 primary-cohort students across 30 instructors. A one-standard-deviation higher instructor propensity is associated with +3.34 percentage points of later use among students with no prior MU use, compared with +8.85 points after `1–2` MU visits, +9.93 after exactly `3`, and +9.52 after `4+`; the interaction terms are jointly significant (`p=7.68e-6`). The all-subsequent sensitivity shows the same pattern. This is consistent with complementarity between prior familiarity and an instructor-linked support context, but it must not be interpreted as a causal interaction because both components are observational.

## Contribution

The current contribution is broader than a threshold-only persistence comparison: formal help-seeking is strongly patterned by prior exposure and by instructional context, while prior CMAT use continues to predict later use within the same current-instructor context. This supports a behavioral interpretation centered on repeated formal help-seeking and reduced familiarity barriers, while keeping stable student selection and instructor-associated composition visible as competing explanations.

## Interpretation rule

This remains an observational study. The analysis does **not** identify a causal PPA effect, a causal professor recommendation effect, a tutoring treatment effect, motivation, or habit formation. Instructor identity and historical instructor uptake are not valid instruments by themselves.

## Reproducibility boundary

Reusable scientific functions are implemented, tested and documented under `main/cmat_analysis/src/cmat_analysis/ppa/`. Paper 1 imports those functions through `code/run_paper.py`; it does not maintain divergent estimators. Aggregate tables `120`–`132` under `results/tables/` are the reviewed controlled-data outputs for the instructor/familiarity extension. Cross-paper interpretation is documented in `brainstorm/shared/INSTRUCTOR_FAMILIARITY_HANDOFF.md`.
