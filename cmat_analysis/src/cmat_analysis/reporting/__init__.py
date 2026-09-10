"""Reusable tabular reporting, formatting, and provenance utilities.

Publication-specific report orchestration is retained only as a compatibility
layer during migration and is not part of this package's public API.
"""

from .provenance import write_run_log

__all__ = ["write_run_log"]
