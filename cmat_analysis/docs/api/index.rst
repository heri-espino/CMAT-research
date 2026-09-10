Public API reference
====================

This reference is intentionally restricted to symbols exported by the
reviewed canonical namespace ``__all__`` declarations. Compatibility
namespaces, private implementation modules, historical pipelines, and
non-exported helpers are excluded.

io
--

.. automodule:: cmat_analysis.io

This namespace currently exposes no stable public callables.

preprocessing
-------------

.. automodule:: cmat_analysis.preprocessing

.. autofunction:: cmat_analysis.preprocessing.clean_materias_df
   :no-index-entry:

.. autofunction:: cmat_analysis.preprocessing.get_salones_with_imputations
   :no-index-entry:

cohorts
-------

.. automodule:: cmat_analysis.cohorts

.. autoclass:: cmat_analysis.cohorts.StudyData
   :no-index-entry:

.. autofunction:: cmat_analysis.cohorts.attach_visits
   :no-index-entry:

.. autofunction:: cmat_analysis.cohorts.build_study_cohorts
   :no-index-entry:

.. autofunction:: cmat_analysis.cohorts.first_attempts
   :no-index-entry:

.. autofunction:: cmat_analysis.cohorts.load_and_clean_inputs
   :no-index-entry:

.. autofunction:: cmat_analysis.cohorts.normalize_identifier
   :no-index-entry:

.. autofunction:: cmat_analysis.cohorts.normalize_session
   :no-index-entry:

.. autofunction:: cmat_analysis.cohorts.normalize_text
   :no-index-entry:

.. autofunction:: cmat_analysis.cohorts.period_index
   :no-index-entry:

.. autofunction:: cmat_analysis.cohorts.period_label
   :no-index-entry:

.. autofunction:: cmat_analysis.cohorts.visit_group
   :no-index-entry:

measures
--------

.. automodule:: cmat_analysis.measures

.. autofunction:: cmat_analysis.measures.add_primary_outcomes
   :no-index-entry:

statistics
----------

.. automodule:: cmat_analysis.statistics

.. autofunction:: cmat_analysis.statistics.add_exact_visit_group
   :no-index-entry:

.. autofunction:: cmat_analysis.statistics.games_howell_exact_groups
   :no-index-entry:

.. autofunction:: cmat_analysis.statistics.bunching_metrics
   :no-index-entry:

.. autofunction:: cmat_analysis.statistics.career_performance_analysis
   :no-index-entry:

.. autofunction:: cmat_analysis.statistics.career_usage_association
   :no-index-entry:

.. autofunction:: cmat_analysis.statistics.career_visit_interaction_model
   :no-index-entry:

.. autofunction:: cmat_analysis.statistics.clustered_career_omnibus
   :no-index-entry:

.. autofunction:: cmat_analysis.statistics.clustered_omnibus_career_test
   :no-index-entry:

.. autofunction:: cmat_analysis.statistics.clustered_omnibus_visit_group_test
   :no-index-entry:

.. autofunction:: cmat_analysis.statistics.clustered_visit_group_omnibus
   :no-index-entry:

.. autofunction:: cmat_analysis.statistics.continuation_curve
   :no-index-entry:

.. autofunction:: cmat_analysis.statistics.dose_group_fixed_effect_model
   :no-index-entry:

.. autofunction:: cmat_analysis.statistics.exact_visit_count_regularity_summary
   :no-index-entry:

.. autofunction:: cmat_analysis.statistics.exact_visit_index_trend
   :no-index-entry:

.. autofunction:: cmat_analysis.statistics.exact_visit_performance_index
   :no-index-entry:

.. autofunction:: cmat_analysis.statistics.group_summary
   :no-index-entry:

.. autofunction:: cmat_analysis.statistics.longitudinal_summary
   :no-index-entry:

.. autofunction:: cmat_analysis.statistics.one_two_pooling_analysis
   :no-index-entry:

.. autofunction:: cmat_analysis.statistics.primary_fixed_effect_models
   :no-index-entry:

.. autofunction:: cmat_analysis.statistics.propensity_att_sensitivity
   :no-index-entry:

.. autofunction:: cmat_analysis.statistics.robust_two_group_tests
   :no-index-entry:

.. autofunction:: cmat_analysis.statistics.secondary_pass_model
   :no-index-entry:

.. autofunction:: cmat_analysis.statistics.temporal_regularity_performance_models
   :no-index-entry:

.. autofunction:: cmat_analysis.statistics.visit_distribution
   :no-index-entry:

.. autofunction:: cmat_analysis.statistics.welch_anova_visit_groups
   :no-index-entry:

longitudinal
------------

.. automodule:: cmat_analysis.longitudinal

.. autoclass:: cmat_analysis.longitudinal.TemporalPeakConfig
   :no-index-entry:

.. autofunction:: cmat_analysis.longitudinal.daily_service_counts
   :no-index-entry:

.. autofunction:: cmat_analysis.longitudinal.detect_period_peaks
   :no-index-entry:

.. autofunction:: cmat_analysis.longitudinal.longitudinal_any_visit_transition
   :no-index-entry:

.. autofunction:: cmat_analysis.longitudinal.monthly_periodicity_diagnostics
   :no-index-entry:

.. autofunction:: cmat_analysis.longitudinal.peak_spacing_summary
   :no-index-entry:

.. autofunction:: cmat_analysis.longitudinal.primary_period_visit_events
   :no-index-entry:

.. autofunction:: cmat_analysis.longitudinal.same_day_ppa_behavior
   :no-index-entry:

.. autofunction:: cmat_analysis.longitudinal.student_temporal_regularity
   :no-index-entry:

.. autofunction:: cmat_analysis.longitudinal.top_daily_dates
   :no-index-entry:

ppa
---

.. automodule:: cmat_analysis.ppa

.. autoclass:: cmat_analysis.ppa.PPAProgressionCohorts
   :no-index-entry:

.. autofunction:: cmat_analysis.ppa.build_ppa_progression_cohort
   :no-index-entry:

.. autofunction:: cmat_analysis.ppa.classify_revalidation_records
   :no-index-entry:

.. autofunction:: cmat_analysis.ppa.course_specific_transition
   :no-index-entry:

.. autofunction:: cmat_analysis.ppa.form_career_crosswalk
   :no-index-entry:

.. autofunction:: cmat_analysis.ppa.later_performance_models
   :no-index-entry:

.. autofunction:: cmat_analysis.ppa.major_delta_z_welch
   :no-index-entry:

.. autofunction:: cmat_analysis.ppa.major_persistence_joint_test
   :no-index-entry:

.. autofunction:: cmat_analysis.ppa.major_persistence_summary
   :no-index-entry:

.. autofunction:: cmat_analysis.ppa.persistence_by_mu_group
   :no-index-entry:

.. autofunction:: cmat_analysis.ppa.persistence_logistic_models
   :no-index-entry:

.. autofunction:: cmat_analysis.ppa.piecewise_threshold_persistence_model
   :no-index-entry:

.. autofunction:: cmat_analysis.ppa.ppa_behavior_profiles
   :no-index-entry:

.. autofunction:: cmat_analysis.ppa.ppa_persistence_association_tests
   :no-index-entry:

visualization
-------------

.. automodule:: cmat_analysis.visualization

.. autofunction:: cmat_analysis.visualization.mpl_apply
   :no-index-entry:

.. autofunction:: cmat_analysis.visualization.plotly_apply
   :no-index-entry:

.. autofunction:: cmat_analysis.visualization.set_style
   :no-index-entry:

reporting
---------

.. automodule:: cmat_analysis.reporting

.. autofunction:: cmat_analysis.reporting.save_figure_variants
   :no-index-entry:

.. autofunction:: cmat_analysis.reporting.write_run_log
   :no-index-entry:

privacy
-------

.. automodule:: cmat_analysis.privacy

.. autofunction:: cmat_analysis.privacy.canonical_identifier
   :no-index-entry:

.. autofunction:: cmat_analysis.privacy.hmac_pseudonym
   :no-index-entry:
