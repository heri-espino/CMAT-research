# Paper 4 results

This directory contains generated or deliberately **publication-level aggregate outputs** for Paper 4. Reusable scientific calculations live in the shared `cmat_analysis` library; the branch-local scripts under `../code/` are thin recipes that compose those functions and write aggregate outputs only.

The controlled analysis has three reproducible layers: `run_engagement.py` generates the original engagement/adaptation tables `200`–`210`; `run_confirmatory.py` generates the pre-draft design checks `220`–`229`; and `run_confirmatory_extra.py` generates the stabilized programme-interaction, numeric-failure and state-audit tables `230`–`233`. The corresponding CI artifacts also contain `engagement_run_summary.json`, `confirmatory_run_summary.json` and `confirmatory_extra_run_summary.json`.

## Reviewed tables

### Original longitudinal adaptation analysis

- `200_mu_attempt_outcome_summary.csv`: first-pass, second-pass, third-or-later-pass and no-observed-pass groups.
- `203_calc_choice_association_models.csv`: prior MU experience and later Calculus historical instructor-outcome rank.
- `204_calc_choice_performance_difficulty_interaction.csv`: continuous MU performance × classroom-context model for later Calculus instructor context.
- `205_mu_repeat_attempt_summary.csv`: repeated-attempt professor switching, CMAT change, next-attempt pass rate and historical instructor-context shift.
- `207_career_adaptation_summary.csv`: programme differences in MU outcomes, support use and later Calculus context.
- `208_mu_experience_state_summary.csv`: initial exploratory five-state summary; retained for provenance, but the confirmatory within-cohort classification in `232` is canonical for the main analysis.
- `209_calc_choice_by_mu_experience_state.csv`: adjusted later Calculus instructor-context differences across initial MU states.
- `210_post_failure_adaptation_strategy.csv`: descriptive next-attempt outcomes by observed adaptation strategy.

Tables `201`–`202` and `206` remain detailed exploratory reproducibility outputs.

### Confirmatory empirical-design closure

- `220_difficulty_threshold_sensitivity.csv`: five-state summaries across the pre-specified 3×3 performance/difficulty threshold grid.
- `221_difficulty_contrast_stability.csv`: directional stability of CMAT-use contrasts across the nine state definitions.
- `222_continuous_challenge_cmat_model.csv`: continuous, cluster-robust first-MU performance × classroom-context model for same-period CMAT use.
- `223_post_failure_response_models.csv`: adjusted repeated-attempt models for professor-context movement, next CMAT use and increased CMAT use.
- `224_post_failure_context_definition_sensitivity.csv`: repeated-attempt movement using within-period percentile, absolute strictly-prior pass rate and absolute strictly-prior mean grade.
- `225_career_heterogeneity_omnibus.csv`: degree-programme omnibus main-effect tests; its unrestricted 116-df programme×state interaction is retained as a diagnostic rather than the primary interaction inference.
- `226_calc_choice_set_audit.csv`: observed and historically rankable Calculus instructor-set support by period/student.
- `227_calc_choice_set_model_sensitivity.csv`: later-Calculus state associations under stricter rankable-set and historical-coverage requirements.
- `228_administrative_choice_constraint_audit.csv`: audit showing that section, schedule, capacity and room fields are unavailable for reconstructing individual feasible choice sets.
- `229_post_failure_choice_set_audit.csv`: support/coverage of the historical instructor comparison after each failed MU attempt.
- `230_career_experience_interaction_reduced.csv`: canonical reduced-dimensional programme×state interaction sensitivity under pre-specified programme-size pooling thresholds.
- `231_post_failure_numeric_severity_models.csv`: numeric-failure severity models for subsequent professor-context and CMAT responses.
- `232_primary_experience_state_summary.csv`: **canonical primary five-state summary**, with the difficulty threshold recomputed inside the covered analytic cohort.
- `233_state_measurement_audit.csv`: audit of missing classroom-relative performance and classroom-context measures underlying the state definition.

## Confirmatory sample anchors

The controlled rerun contains 6,627 students whose first real MU attempt occurs during CMAT coverage, 4,151 students with a later observed Calculus attempt in CMAT coverage after an MU pass, 3,224 rankable later Calculus instructor contexts and 1,007 covered transitions from a failed/adverse MU attempt to a subsequent MU attempt.

## Interpretation boundary

The historical instructor variable uses academic outcomes from periods strictly before the focal enrolment. Within-period percentiles are defined among instructors observed teaching the course in that academic period, but the data do **not** contain section identifiers, schedules, capacity or rooms that would reconstruct each student's feasible choice set. Therefore these outputs describe subsequent enrolment with historically higher/lower-outcome instructors, not unconstrained preference and not deliberate selection of an “easy” professor.

First-MU experience states use realized classroom-relative performance and realized leave-one-out classroom pass rates. Their association with CMAT use in the same period is contemporaneous and descriptive; later Calculus and next-attempt analyses have temporal ordering but remain observational. CMAT non-use must not be interpreted as disengagement, and descriptive post-failure differences in later pass rates must not be interpreted as treatment effects.

Do not hand-edit numerical tables. Administrative row-level data, student identifiers, instructor identifiers, row-level joined cohorts or private local inputs must never be committed here.
