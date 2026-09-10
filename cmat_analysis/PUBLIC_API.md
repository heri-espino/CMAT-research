# cmat_analysis public API

This inventory defines the reviewed documentation surface. A symbol is
public here only when it is exported from the canonical namespace
`__all__`. Compatibility namespaces and non-exported helpers are not API.

## `cmat_analysis.io`

No public callables.

## `cmat_analysis.preprocessing`

- `clean_materias_df` — function
- `get_salones_with_imputations` — function

## `cmat_analysis.cohorts`

- `StudyData` — class
- `attach_visits` — function
- `build_study_cohorts` — function
- `first_attempts` — function
- `load_and_clean_inputs` — function
- `normalize_identifier` — function
- `normalize_session` — function
- `normalize_text` — function
- `period_index` — function
- `period_label` — function
- `visit_group` — function

## `cmat_analysis.measures`

- `add_primary_outcomes` — function

## `cmat_analysis.statistics`

- `add_exact_visit_group` — function
- `games_howell_exact_groups` — function
- `bunching_metrics` — function
- `career_performance_analysis` — function
- `career_usage_association` — function
- `career_visit_interaction_model` — function
- `clustered_career_omnibus` — function
- `clustered_omnibus_career_test` — function
- `clustered_omnibus_visit_group_test` — function
- `clustered_visit_group_omnibus` — function
- `continuation_curve` — function
- `dose_group_fixed_effect_model` — function
- `exact_visit_count_regularity_summary` — function
- `exact_visit_index_trend` — function
- `exact_visit_performance_index` — function
- `group_summary` — function
- `longitudinal_summary` — function
- `one_two_pooling_analysis` — function
- `primary_fixed_effect_models` — function
- `propensity_att_sensitivity` — function
- `robust_two_group_tests` — function
- `secondary_pass_model` — function
- `temporal_regularity_performance_models` — function
- `visit_distribution` — function
- `welch_anova_visit_groups` — function

## `cmat_analysis.longitudinal`

- `TemporalPeakConfig` — class
- `daily_service_counts` — function
- `detect_period_peaks` — function
- `longitudinal_any_visit_transition` — function
- `monthly_periodicity_diagnostics` — function
- `peak_spacing_summary` — function
- `primary_period_visit_events` — function
- `same_day_ppa_behavior` — function
- `student_temporal_regularity` — function
- `top_daily_dates` — function

## `cmat_analysis.ppa`

- `PPAProgressionCohorts` — class
- `build_ppa_progression_cohort` — function
- `classify_revalidation_records` — function
- `course_specific_transition` — function
- `form_career_crosswalk` — function
- `later_performance_models` — function
- `major_delta_z_welch` — function
- `major_persistence_joint_test` — function
- `major_persistence_summary` — function
- `persistence_by_mu_group` — function
- `persistence_logistic_models` — function
- `piecewise_threshold_persistence_model` — function
- `ppa_behavior_profiles` — function
- `ppa_persistence_association_tests` — function

## `cmat_analysis.visualization`

- `mpl_apply` — function
- `plotly_apply` — function
- `set_style` — function

## `cmat_analysis.reporting`

- `write_run_log` — function

## `cmat_analysis.privacy`

- `canonical_identifier` — function
- `hmac_pseudonym` — function

Public functions: **66**  
Public classes: **3**
