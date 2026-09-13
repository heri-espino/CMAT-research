# Instructor-linked uptake and prior CMAT familiarity — shared handoff

## Portfolio decision

The instructor-linked uptake analysis is a cross-paper methodological finding, but its publication use belongs primarily to Paper 1. Paper 2 remains focused on contemporaneous CMAT use and classroom-relative MU performance, while Paper 3 remains focused on grading comparability across instructor-course-period contexts.

Paper 1 may study two observational mechanisms associated with later Calculus CMAT use:

1. **Prior CMAT familiarity**: prior MU-period use classified as `0 / 1-2 / exactly 3 / 4+`. Exactly three registrations are retained as the institutionally salient PPA threshold, while `4+` distinguishes behavior beyond that threshold.
2. **Instructor-linked uptake/implementation**: students' current instructor identifies an instructional context in which CMAT use rates may systematically differ. Instructors recommend CMAT as a source of mathematics tutoring, but the administrative data do not directly observe recommendation intensity, so instructor identity or historical uptake must not be labelled as a measured encouragement treatment.

## Shared scientific implementation

Reusable estimators live in `cmat_analysis.ppa`, including:

- `build_ppa_mu_baseline_cohort` for initial MU participation without conditioning on later Calculus progression;
- `professor_visit_group_distribution` and `professor_visit_group_multinomial_increment` for `0 / 1-2 / 3 / 4+` uptake heterogeneity;
- `professor_uptake_increment` for binary uptake heterogeneity;
- `leave_period_out_professor_propensity` for instructor uptake rates estimated from other academic periods;
- `familiarization_professor_persistence_models` for later-use contrasts by prior MU familiarity, including a specification with current Calculus-instructor fixed effects;
- `professor_familiarization_interaction_model` for descriptive interaction between prior familiarity and leave-period-out current-instructor uptake propensity.

Paper branches should import these functions rather than maintain divergent implementations.

## Interpretation boundary

All of these analyses are observational. Instructor identity can affect learning, grading, communication and student composition directly, while prior CMAT use is student-selected; therefore neither instructor identity nor leave-period-out instructor uptake is a valid instrument by itself, and prior use is not a randomized familiarity treatment. The functions quantify instructor-linked implementation and persistence/familiarity patterns rather than causal effects.

The initial instructor-to-MU-uptake analysis should use the MU baseline cohort rather than only MU students who later progress to Calculus, because conditioning on progression can induce selection. The later persistence analysis may use the linked MU-to-Calculus cohort because later CMAT use is its outcome.
