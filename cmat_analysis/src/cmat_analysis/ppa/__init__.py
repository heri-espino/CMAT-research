"""PPA exposure-threshold and MU-to-Calculus progression analyses.

PPA visit thresholds are operational exposure definitions, not randomized
assignment cutoffs. The existing cohort, persistence, and progression formulas
are preserved by this architectural move.
"""

from .progression import (
    PPAProgressionCohorts,
    build_ppa_progression_cohort,
    classify_revalidation_records,
    course_specific_transition,
    form_career_crosswalk,
    later_performance_models,
    major_delta_z_welch,
    major_persistence_joint_test,
    major_persistence_summary,
    persistence_by_mu_group,
    persistence_logistic_models,
    piecewise_threshold_persistence_model,
    ppa_behavior_profiles,
    ppa_persistence_association_tests,
)

__all__ = [
    "PPAProgressionCohorts",
    "build_ppa_progression_cohort",
    "classify_revalidation_records",
    "course_specific_transition",
    "form_career_crosswalk",
    "later_performance_models",
    "major_delta_z_welch",
    "major_persistence_joint_test",
    "major_persistence_summary",
    "persistence_by_mu_group",
    "persistence_logistic_models",
    "piecewise_threshold_persistence_model",
    "ppa_behavior_profiles",
    "ppa_persistence_association_tests",
]
