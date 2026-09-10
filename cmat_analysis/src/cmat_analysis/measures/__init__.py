"""Derived academic measures and outcome construction.

Measures are calculated after cohort construction and before statistical
estimation. In particular, the existing classroom-relative grade outcome and
its adverse-state imputation rules are preserved exactly by this refactor.
"""

from .grades import add_primary_outcomes

__all__ = ["add_primary_outcomes"]
