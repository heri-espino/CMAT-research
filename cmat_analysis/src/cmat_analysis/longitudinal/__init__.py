"""Longitudinal service-use timing, regularity, and cross-course transitions.

The namespace describes temporal and repeated-use structure without treating
observed timing patterns as randomized assignment or causal identification.
"""

from .temporal import (
    TemporalPeakConfig,
    daily_service_counts,
    detect_period_peaks,
    monthly_periodicity_diagnostics,
    peak_spacing_summary,
    primary_period_visit_events,
    same_day_ppa_behavior,
    student_temporal_regularity,
    top_daily_dates,
)
from .transitions import longitudinal_any_visit_transition

__all__ = [
    "TemporalPeakConfig",
    "daily_service_counts",
    "detect_period_peaks",
    "longitudinal_any_visit_transition",
    "monthly_periodicity_diagnostics",
    "peak_spacing_summary",
    "primary_period_visit_events",
    "same_day_ppa_behavior",
    "student_temporal_regularity",
    "top_daily_dates",
]
