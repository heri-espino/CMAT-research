"""Cohort construction, attempt classification, and visit exposure attachment.

Cohorts are defined from cleaned academic and CMAT visit data while preserving
the study's existing definitions of academic periods, attempts, revalidations,
and visit-count groups. This namespace owns population construction rather than
outcome calculation or statistical estimation.
"""

from .attempts import (
    StudyData,
    attach_visits,
    build_study_cohorts,
    first_attempts,
    load_and_clean_inputs,
    normalize_identifier,
    normalize_session,
    normalize_text,
    period_index,
    period_label,
    visit_group,
)

__all__ = [
    "StudyData",
    "attach_visits",
    "build_study_cohorts",
    "first_attempts",
    "load_and_clean_inputs",
    "normalize_identifier",
    "normalize_session",
    "normalize_text",
    "period_index",
    "period_label",
    "visit_group",
]
