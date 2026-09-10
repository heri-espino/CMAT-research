"""Statistical estimation, uncertainty, diagnostics, and selection adjustment.

This namespace contains reusable estimators and inferential diagnostics. It does
not define cohorts or mutate source data. Observational estimators remain
associational unless their original design and assumptions identify otherwise.
"""

from .inference import (
    bunching_metrics,
    continuation_curve,
    dose_group_fixed_effect_model,
    exact_visit_count_regularity_summary,
    group_summary,
    longitudinal_summary,
    primary_fixed_effect_models,
    robust_two_group_tests,
    secondary_pass_model,
    temporal_regularity_performance_models,
    visit_distribution,
)
from .selection import propensity_att_sensitivity
from .group_comparisons import (
    career_performance_analysis,
    career_usage_association,
    career_visit_interaction_model,
    clustered_career_omnibus,
    clustered_omnibus_career_test,
    clustered_omnibus_visit_group_test,
    clustered_visit_group_omnibus,
    exact_visit_index_trend,
    exact_visit_performance_index,
    one_two_pooling_analysis,
    welch_anova_visit_groups,
)

__all__ = [
    "bunching_metrics",
    "career_performance_analysis",
    "career_usage_association",
    "career_visit_interaction_model",
    "clustered_career_omnibus",
    "clustered_omnibus_career_test",
    "clustered_omnibus_visit_group_test",
    "clustered_visit_group_omnibus",
    "continuation_curve",
    "dose_group_fixed_effect_model",
    "exact_visit_count_regularity_summary",
    "exact_visit_index_trend",
    "exact_visit_performance_index",
    "group_summary",
    "longitudinal_summary",
    "one_two_pooling_analysis",
    "primary_fixed_effect_models",
    "propensity_att_sensitivity",
    "robust_two_group_tests",
    "secondary_pass_model",
    "temporal_regularity_performance_models",
    "visit_distribution",
    "welch_anova_visit_groups",
]
