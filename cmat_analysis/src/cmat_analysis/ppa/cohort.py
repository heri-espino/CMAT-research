"""Internal dependency bridge for the relocated PPA implementation.

This module is not part of the public API. It preserves the former relative
imports in ``_progression`` so the scientific implementation can remain intact.
"""

from cmat_analysis.cohorts.attempts import attach_visits, normalize_text, visit_group

__all__ = ["attach_visits", "normalize_text", "visit_group"]
