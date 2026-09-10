"""Compatibility shim for :mod:`cmat_analysis.preprocessing.cleaning`.

New code must import cleaning operations from ``cmat_analysis.preprocessing``.
The implementation moved without scientific changes.
"""

from cmat_analysis.preprocessing.cleaning import *  # noqa: F401,F403
