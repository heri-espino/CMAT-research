"""Redesigned CMAT longitudinal study.

This package is intentionally separate from the legacy report pipeline so the
original analysis remains reproducible while the publication-oriented design
can evolve independently.
"""

from .pipeline import run_study_pipeline

__all__ = ["run_study_pipeline"]
