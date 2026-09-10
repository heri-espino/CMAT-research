"""Compatibility and publication-orchestration namespace.

Reusable scientific components formerly under ``study`` now live in
responsibility-based namespaces. The historical study pipeline remains here so
retained outputs stay reproducible while brainstorm/paper runners migrate.
New reusable scientific functions must not be added to this namespace.
"""

from .pipeline import run_study_pipeline

__all__ = ["run_study_pipeline"]
