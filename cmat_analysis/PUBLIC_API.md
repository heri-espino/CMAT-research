# cmat_analysis public API

This inventory defines the reviewed documentation surface. A symbol is public here only when it is exported from the canonical namespace `__all__`. Compatibility namespaces and non-exported helpers are not API. The Sphinx reference documents the same canonical surface.

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

- `add_academic_outcome_states` — function
- `add_primary_outcomes` — function

## `cmat_analysis.statistics`

- `compare_univariate_shape_models` — function
- `cross_validated_skew_normal_vs_gmm` — function
- `add_exact_visit_group` — function
- `add_topcoded_visit_group` — function
- `distribution_profile` — function
- `fixed_effect_group_comparisons` — function
- `fixed_effect_logistic_group_comparisons` — function
- `fixed_effect_logistic_adjusted_probabilities` — function
- `group_outcome_summary` — function
- `mixture_component_density` — function
- `outcome_state_composition` — function
- `pairwise_effect_matrix` — function
- `visit_frequency_cut_frontier` — function
- `visit_frequency_support_audit` — function
- `visit_group_pair_overlap` — function
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
- `fit_univariate_gaussian_mixture` — function
- `gaussian_mixture_component_summary` — function
- `gaussian_mixture_model_selection` — function
- `gaussian_mixture_responsibilities` — function
- `parametric_bootstrap_gmm_lrt` — function
- `parametric_bootstrap_skew_normal_vs_gmm` — function
- `soft_component_composition` — function
- `skew_normal_fit_summary` — function
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

- `EngagementTrajectoryData` — class
- `PPAProgressionCohorts` — class
- `academic_context_uptake_models` — function
- `build_engagement_trajectory_data` — function
- `build_mu_classroom_outcome_context` — function
- `build_ppa_mu_baseline_cohort` — function
- `build_ppa_progression_cohort` — function
- `calc_choice_association_models` — function
- `classify_revalidation_records` — function
- `clustered_academic_context_uptake_models` — function
- `course_specific_transition` — function
- `experience_profile_summary` — function
- `familiarization_professor_persistence_models` — function
- `form_career_crosswalk` — function
- `instructor_choice_percentiles` — function
- `later_performance_models` — function
- `leave_period_out_professor_academic_context` — function
- `leave_period_out_professor_propensity` — function
- `major_delta_z_welch` — function
- `major_persistence_joint_test` — function
- `major_persistence_summary` — function
- `major_uptake_increment` — function
- `major_visit_group_multinomial_increment` — function
- `major_visit_group_summary` — function
- `persistence_by_mu_group` — function
- `persistence_logistic_models` — function
- `piecewise_threshold_persistence_model` — function
- `ppa_behavior_profiles` — function
- `ppa_persistence_association_tests` — function
- `professor_familiarization_interaction_model` — function
- `professor_period_context_correlations` — function
- `professor_uptake_increment` — function
- `professor_visit_group_distribution` — function
- `professor_visit_group_multinomial_increment` — function
- `repeat_attempt_summary` — function
- `strict_prior_instructor_context` — function

## `cmat_analysis.visualization`

- `mpl_apply` — function
- `plot_stacked_ridgeline` — function
- `plotly_apply` — function
- `set_style` — function

## `cmat_analysis.reporting`

- `save_figure_variants` — function
- `write_run_log` — function

## `cmat_analysis.privacy`

- `canonical_identifier` — function
- `hmac_pseudonym` — function

Public functions: **112**  
Public classes: **4**
